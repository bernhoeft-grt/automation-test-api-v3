"""Healing utility models and data structures."""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SeverityLevel(str, Enum):
    """Severity levels for test failures."""
    CRITICAL = "critical"
    MEDIUM = "medium"
    LOW = "low"


class FailureType(str, Enum):
    """Types of test failures."""
    ASSERTION_ERROR = "assertion_error"
    SCHEMA_MISMATCH = "schema_mismatch"
    FIXTURE_ERROR = "fixture_error"
    API_CHANGE = "api_change"
    AUTH_FAILURE = "auth_failure"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class FixType(str, Enum):
    """Types of fixes available."""
    AUTO_FIX = "auto_fix"
    MANUAL_REVIEW = "manual_review"
    REQUIRES_INVESTIGATION = "requires_investigation"


@dataclass
class TestFailure:
    """Represents a single test failure."""
    test_name: str
    file_path: str
    line_number: int
    error_type: FailureType
    error_message: str
    traceback: str
    severity: SeverityLevel
    affected_tests: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.test_name}: {self.error_message}"


@dataclass
class HealingSuggestion:
    """Represents a suggested fix for a test failure."""
    title: str
    description: str
    failure_type: FailureType
    severity: SeverityLevel
    fix_type: FixType
    affected_tests: List[str]
    file_to_modify: str
    modification_details: Dict[str, Any]
    alternative_solutions: List[str] = field(default_factory=list)
    risk_level: str = "low"  # low, medium, high
    estimated_effort: str = "low"  # low, medium, high
    
    def __str__(self) -> str:
        return f"[{self.fix_type.value}] {self.title} ({self.severity.value})"


@dataclass
class HealingReport:
    """Complete healing analysis report."""
    generated_at: datetime
    total_failures: int
    auto_fixable: int
    requires_review: int
    failures_by_severity: Dict[SeverityLevel, int]
    failures: List[TestFailure]
    suggestions: List[HealingSuggestion]
    
    @property
    def pass_rate_before(self) -> float:
        """Calculate pass rate if all failures existed."""
        total = self.total_failures
        if total == 0:
            return 100.0
        return ((total - self.total_failures) / total) * 100
    
    @property
    def summary(self) -> str:
        """Generate summary text."""
        return f"""
╔════════════════════════════════════════════════════╗
║         TEST HEALING REPORT - {self.generated_at.strftime('%Y-%m-%d')}           ║
╚════════════════════════════════════════════════════╝

📊 SUMMARY
  Total Failures: {self.total_failures}
  Auto-fixable: {self.auto_fixable} ({self._percentage(self.auto_fixable)}%)
  Requires Review: {self.requires_review} ({self._percentage(self.requires_review)}%)

🔴 CRITICAL: {self.failures_by_severity.get(SeverityLevel.CRITICAL, 0)}
🟡 MEDIUM: {self.failures_by_severity.get(SeverityLevel.MEDIUM, 0)}
🟢 LOW: {self.failures_by_severity.get(SeverityLevel.LOW, 0)}

📋 RECOMMENDATIONS
  Total fixes suggested: {len(self.suggestions)}
  Auto-fixes available: {sum(1 for s in self.suggestions if s.fix_type == FixType.AUTO_FIX)}
  Need review: {sum(1 for s in self.suggestions if s.fix_type == FixType.MANUAL_REVIEW)}
"""
    
    @staticmethod
    def _percentage(value: int, total: int = 0) -> float:
        # Will be calculated properly when called
        return 0


@dataclass
class HealingFixResult:
    """Result of applying a fix."""
    suggestion: HealingSuggestion
    success: bool
    error: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    tests_affected: int = 0
    modified_at: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"{status}: {self.suggestion.title}"


@dataclass
class HealingSession:
    """Complete healing session with all operations."""
    session_id: str
    started_at: datetime
    total_fixes_applied: int = 0
    fixes_successful: int = 0
    fixes_failed: int = 0
    files_backed_up: List[str] = field(default_factory=list)
    fix_results: List[HealingFixResult] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Calculate fix success rate."""
        total = self.fixes_successful + self.fixes_failed
        if total == 0:
            return 0.0
        return (self.fixes_successful / total) * 100
    
    def summary(self) -> str:
        """Generate session summary."""
        return f"""
📈 HEALING SESSION SUMMARY
  Session ID: {self.session_id}
  Started: {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}
  
  Total Fixes Applied: {self.total_fixes_applied}
  ✅ Successful: {self.fixes_successful}
  ❌ Failed: {self.fixes_failed}
  Success Rate: {self.success_rate:.1f}%
  
  Files Backed Up: {len(self.files_backed_up)}
  
  {self._detailed_results()}
"""
    
    def _detailed_results(self) -> str:
        """Generate detailed results."""
        if not self.fix_results:
            return ""
        
        lines = ["  Details:"]
        for result in self.fix_results:
            status = "✅" if result.success else "❌"
            lines.append(f"    {status} {result.suggestion.title}")
            if result.files_modified:
                lines.append(f"       Files: {', '.join(result.files_modified)}")
        
        return "\n".join(lines)
