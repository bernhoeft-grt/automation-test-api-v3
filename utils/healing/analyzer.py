"""Test failure analyzer for healing system."""
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

from .models import (
    TestFailure, HealingSuggestion, HealingReport, FailureType,
    SeverityLevel, FixType
)


class TestFailureAnalyzer:
    """Analyzes test failures and generates healing suggestions."""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize analyzer.
        
        Args:
            workspace_root: Root of the test workspace. Defaults to current directory.
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.allure_results_dir = self.workspace_root / "allure-results"
        self.reports_dir = self.workspace_root / "reports"
        self.tests_dir = self.workspace_root / "tests"
        
        self.failures: List[TestFailure] = []
        self.suggestions: List[HealingSuggestion] = []
    
    def scan_allure_results(self) -> List[TestFailure]:
        """Scan Allure results directory for failures.
        
        Returns:
            List of test failures found.
        """
        failures = []
        
        if not self.allure_results_dir.exists():
            return failures
        
        for result_file in self.allure_results_dir.glob("*-result.json"):
            try:
                with open(result_file) as f:
                    result = json.load(f)
                
                # Include both failed and broken statuses (broken = setup/connection errors)
                if result.get("status") in ("failed", "broken"):
                    failure = self._parse_allure_failure(result)
                    if failure:
                        failures.append(failure)
            except Exception as e:
                print(f"Error parsing {result_file}: {e}")
        
        self.failures = failures
        return failures
    
    def _parse_allure_failure(self, result: Dict[str, Any]) -> Optional[TestFailure]:
        """Parse Allure result into TestFailure.
        
        Args:
            result: Parsed Allure JSON result.
            
        Returns:
            TestFailure object or None if not a valid failure.
        """
        status_details = result.get("statusDetails", {})
        
        # Extract test name
        test_name = result.get("name", "unknown_test")
        
        # Extract error message
        error_message = status_details.get("message", "Unknown error")
        
        # Get traceback
        traceback = status_details.get("trace", "")
        
        # Detect failure type
        failure_type = self._detect_failure_type(error_message, traceback)
        
        # Determine severity
        severity = self._determine_severity(failure_type, error_message)
        
        # Extract file path and line number
        file_path, line_number = self._extract_location(traceback)
        
        return TestFailure(
            test_name=test_name,
            file_path=file_path or "tests/unknown.py",
            line_number=line_number or 0,
            error_type=failure_type,
            error_message=error_message,
            traceback=traceback,
            severity=severity,
        )
    
    def _detect_failure_type(self, message: str, traceback: str) -> FailureType:
        """Detect the type of failure from message and traceback.
        
        Args:
            message: Error message.
            traceback: Full traceback text.
            
        Returns:
            FailureType enum value.
        """
        lower_msg = message.lower()
        lower_trace = traceback.lower()
        
        # Check for connection/broken test issues
        if "connection" in lower_msg or "connection" in lower_trace or "unable to locate the service" in lower_trace:
            return FailureType.API_CHANGE
        
        if "timeout" in lower_msg or "timeout" in lower_trace:
            return FailureType.TIMEOUT
        
        # Check for specific patterns
        if "assertionerror" in lower_trace or "assert " in lower_trace:
            return FailureType.ASSERTION_ERROR
        
        if "validationerror" in lower_trace or "pydantic" in lower_trace:
            return FailureType.SCHEMA_MISMATCH
        
        if "fixture" in lower_trace or "conftest" in lower_trace:
            return FailureType.FIXTURE_ERROR
        
        if "404" in message or "endpoint" in lower_msg or "not found" in lower_msg:
            return FailureType.API_CHANGE
        
        if "401" in message or "unauthorized" in lower_msg or "token" in lower_msg:
            return FailureType.AUTH_FAILURE
        
        return FailureType.UNKNOWN
    
    def _determine_severity(self, failure_type: FailureType, message: str) -> SeverityLevel:
        """Determine severity of failure.
        
        Args:
            failure_type: Type of failure.
            message: Error message.
            
        Returns:
            SeverityLevel enum value.
        """
        # Critical failures
        if failure_type in (
            FailureType.API_CHANGE, FailureType.AUTH_FAILURE,
            FailureType.SCHEMA_MISMATCH, FailureType.FIXTURE_ERROR
        ):
            return SeverityLevel.CRITICAL
        
        if failure_type == FailureType.TIMEOUT:
            return SeverityLevel.MEDIUM
        
        # Assertion errors with specific patterns
        if failure_type == FailureType.ASSERTION_ERROR:
            if "required" in message.lower() or "mandatory" in message.lower():
                return SeverityLevel.CRITICAL
            return SeverityLevel.MEDIUM
        
        return SeverityLevel.LOW
    
    def _extract_location(self, traceback: str) -> tuple[str, int]:
        """Extract file path and line number from traceback.
        
        Args:
            traceback: Error traceback text.
            
        Returns:
            Tuple of (file_path, line_number).
        """
        # Pattern: File "path/to/file.py", line 123
        match = re.search(r'File "([^"]+)", line (\d+)', traceback)
        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))
            
            # Make path relative to workspace
            try:
                file_path = str(Path(file_path).relative_to(self.workspace_root))
            except (ValueError, TypeError):
                pass
            
            return file_path, line_number
        
        return "", 0
    
    def analyze_failures(self) -> HealingReport:
        """Analyze collected failures and generate suggestions.
        
        Returns:
            HealingReport with analysis and suggestions.
        """
        self.suggestions = []
        
        # Group failures by type
        by_type = defaultdict(list)
        for failure in self.failures:
            by_type[failure.error_type].append(failure)
        
        # Generate suggestions for each type
        for failure_type, failures in by_type.items():
            suggestions = self._generate_suggestions(failure_type, failures)
            self.suggestions.extend(suggestions)
        
        # Count by severity
        failures_by_severity = defaultdict(int)
        for failure in self.failures:
            failures_by_severity[failure.severity] += 1
        
        # Count auto-fixable vs needs review
        auto_fixable = sum(
            1 for s in self.suggestions
            if s.fix_type == FixType.AUTO_FIX
        )
        requires_review = sum(
            1 for s in self.suggestions
            if s.fix_type == FixType.MANUAL_REVIEW
        )
        
        return HealingReport(
            generated_at=datetime.now(),
            total_failures=len(self.failures),
            auto_fixable=auto_fixable,
            requires_review=requires_review,
            failures_by_severity=dict(failures_by_severity),
            failures=self.failures,
            suggestions=self.suggestions,
        )
    
    def _generate_suggestions(
        self,
        failure_type: FailureType,
        failures: List[TestFailure]
    ) -> List[HealingSuggestion]:
        """Generate suggestions for a type of failure.
        
        Args:
            failure_type: Type of failure.
            failures: List of failures of this type.
            
        Returns:
            List of healing suggestions.
        """
        suggestions = []
        
        if failure_type == FailureType.ASSERTION_ERROR:
            suggestions.extend(self._suggest_assertion_fixes(failures))
        elif failure_type == FailureType.SCHEMA_MISMATCH:
            suggestions.extend(self._suggest_schema_fixes(failures))
        elif failure_type == FailureType.FIXTURE_ERROR:
            suggestions.extend(self._suggest_fixture_fixes(failures))
        elif failure_type == FailureType.API_CHANGE:
            suggestions.extend(self._suggest_api_change_fixes(failures))
        elif failure_type == FailureType.AUTH_FAILURE:
            suggestions.extend(self._suggest_auth_fixes(failures))
        elif failure_type == FailureType.TIMEOUT:
            suggestions.extend(self._suggest_timeout_fixes(failures))
        
        return suggestions
    
    def _suggest_assertion_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for assertion errors."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Review and update assertion values",
            description="One or more assertions failed due to unexpected values",
            failure_type=FailureType.ASSERTION_ERROR,
            severity=SeverityLevel.MEDIUM,
            fix_type=FixType.MANUAL_REVIEW,
            affected_tests=affected_tests,
            file_to_modify="tests/[endpoint]/test_*.py",
            modification_details={
                "action": "Review and update assertion values",
                "pattern": "assert X == Y",
                "next_step": "Check API specifications for correct values"
            },
            alternative_solutions=[
                "Use less strict assertions (e.g., 'in' instead of '==')",
                "Extract value and update based on expected behavior",
                "Add dynamic value extraction from response"
            ],
            risk_level="medium",
            estimated_effort="medium"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_schema_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for schema mismatch errors."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Update Pydantic schema models",
            description="Response schema doesn't match Pydantic model - missing or extra fields",
            failure_type=FailureType.SCHEMA_MISMATCH,
            severity=SeverityLevel.CRITICAL,
            fix_type=FixType.AUTO_FIX,
            affected_tests=affected_tests,
            file_to_modify="tests/[endpoint]/page.py",
            modification_details={
                "action": "Add missing fields or mark as optional",
                "pattern": "class Schema(BaseModel):",
                "auto_fix": "Add Optional[] for missing fields"
            },
            alternative_solutions=[
                "Use Config.extra = 'allow' to permit extra fields",
                "Regenerate schema from API documentation",
                "Update API client to match current schema"
            ],
            risk_level="low",
            estimated_effort="low"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_fixture_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for fixture errors."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Fix test fixtures in conftest.py",
            description="Test fixture setup failed - check fixture dependencies and data",
            failure_type=FailureType.FIXTURE_ERROR,
            severity=SeverityLevel.CRITICAL,
            fix_type=FixType.MANUAL_REVIEW,
            affected_tests=affected_tests,
            file_to_modify="tests/[endpoint]/conftest.py",
            modification_details={
                "action": "Review fixture setup and dependencies",
                "pattern": "@pytest.fixture",
                "next_step": "Check fixture returns valid data"
            },
            alternative_solutions=[
                "Regenerate fixtures from API schema",
                "Add fixture dependencies",
                "Update fixture return types"
            ],
            risk_level="high",
            estimated_effort="medium"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_api_change_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for API changes."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Update API endpoints due to deprecation/change",
            description="API endpoints have changed - may be deprecated, moved, or restructured",
            failure_type=FailureType.API_CHANGE,
            severity=SeverityLevel.CRITICAL,
            fix_type=FixType.MANUAL_REVIEW,
            affected_tests=affected_tests,
            file_to_modify="tests/[endpoint]/test_*.py",
            modification_details={
                "action": "Update endpoint URLs",
                "pattern": "api_client.get('/api/endpoint')",
                "next_step": "Check API documentation for new endpoints"
            },
            alternative_solutions=[
                "Update to new API version",
                "Migrate to replacement endpoint",
                "Check API changelog for deprecation notice"
            ],
            risk_level="high",
            estimated_effort="high"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_auth_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for authentication failures."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Refresh authentication tokens",
            description="Authentication failed - tokens may be expired or invalid",
            failure_type=FailureType.AUTH_FAILURE,
            severity=SeverityLevel.CRITICAL,
            fix_type=FixType.AUTO_FIX,
            affected_tests=affected_tests,
            file_to_modify="tests/conftest.py",
            modification_details={
                "action": "Add token refresh in auth fixture",
                "pattern": "@pytest.fixture\ndef api_client():",
                "auto_fix": "Call client.refresh_token()"
            },
            alternative_solutions=[
                "Update credentials in .env",
                "Regenerate auth tokens",
                "Check token expiration policy"
            ],
            risk_level="low",
            estimated_effort="low"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_timeout_fixes(self, failures: List[TestFailure]) -> List[HealingSuggestion]:
        """Generate suggestions for timeout issues."""
        suggestions = []
        
        affected_tests = [f.test_name for f in failures]
        
        suggestion = HealingSuggestion(
            title="Increase test timeout thresholds",
            description="Tests are timing out - API responses or test setup may be slow",
            failure_type=FailureType.TIMEOUT,
            severity=SeverityLevel.MEDIUM,
            fix_type=FixType.AUTO_FIX,
            affected_tests=affected_tests,
            file_to_modify="pytest.ini",
            modification_details={
                "action": "Increase timeout value",
                "current": "30",
                "suggested": "45",
                "auto_fix": "Multiply by 1.5x"
            },
            alternative_solutions=[
                "Optimize test payload",
                "Mock slow external services",
                "Add performance debugging"
            ],
            risk_level="low",
            estimated_effort="low"
        )
        suggestions.append(suggestion)
        
        return suggestions
    
    def get_failure(self, test_name: str) -> Optional[TestFailure]:
        """Get a specific failure by test name.
        
        Args:
            test_name: Name of the test.
            
        Returns:
            TestFailure object or None.
        """
        for failure in self.failures:
            if failure.test_name == test_name:
                return failure
        return None
    
    def get_suggestions(self, severity: Optional[SeverityLevel] = None) -> List[HealingSuggestion]:
        """Get suggestions, optionally filtered by severity.
        
        Args:
            severity: Optional severity level to filter by.
            
        Returns:
            List of healing suggestions.
        """
        if severity is None:
            return self.suggestions
        
        return [s for s in self.suggestions if s.severity == severity]
