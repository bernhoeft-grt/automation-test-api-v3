"""Automatic test fixer for healing system."""
import shutil
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

from .models import (
    HealingReport, HealingSuggestion, HealingFixResult,
    HealingSession, FixType
)


class TestAutoFixer:
    """Automatically applies fixes to failing tests."""
    
    def __init__(self, workspace_root: Optional[Path] = None, backup: bool = True):
        """Initialize auto-fixer.
        
        Args:
            workspace_root: Root of the test workspace.
            backup: Whether to backup files before modifying.
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.backup = backup
        self.backup_dir = self.workspace_root / ".backups" / datetime.now().strftime("%Y-%m-%d-%H%M%S")
        self.session = HealingSession(
            session_id=str(uuid4())[:8],
            started_at=datetime.now()
        )
    
    def apply_fixes(self, report: HealingReport, dry_run: bool = False) -> HealingSession:
        """Apply all suggested fixes from a healing report.
        
        Args:
            report: HealingReport with suggestions.
            dry_run: If True, don't actually modify files.
            
        Returns:
            HealingSession with results.
        """
        auto_fixable = [
            s for s in report.suggestions
            if s.fix_type == FixType.AUTO_FIX
        ]
        
        for suggestion in auto_fixable:
            result = self.apply_fix(suggestion, dry_run=dry_run)
            self.session.fix_results.append(result)
            
            if result.success:
                self.session.fixes_successful += 1
            else:
                self.session.fixes_failed += 1
            
            self.session.total_fixes_applied += 1
        
        return self.session
    
    def apply_fix(self, suggestion: HealingSuggestion, dry_run: bool = False) -> HealingFixResult:
        """Apply a single fix.
        
        Args:
            suggestion: HealingSuggestion to apply.
            dry_run: If True, don't actually modify files.
            
        Returns:
            HealingFixResult with outcome.
        """
        try:
            if suggestion.title == "Update Pydantic schema models":
                return self._fix_schema_mismatch(suggestion, dry_run)
            elif suggestion.title == "Refresh authentication tokens":
                return self._fix_auth_failure(suggestion, dry_run)
            elif suggestion.title == "Increase test timeout thresholds":
                return self._fix_timeout(suggestion, dry_run)
            else:
                # Unknown fix type - needs manual review
                return HealingFixResult(
                    suggestion=suggestion,
                    success=False,
                    error="Fix type not implemented for auto-fix"
                )
        except Exception as e:
            return HealingFixResult(
                suggestion=suggestion,
                success=False,
                error=str(e)
            )
    
    def _fix_schema_mismatch(self, suggestion: HealingSuggestion, dry_run: bool) -> HealingFixResult:
        """Fix schema mismatch by updating Pydantic models.
        
        Args:
            suggestion: HealingSuggestion for schema fix.
            dry_run: If True, don't actually modify files.
            
        Returns:
            HealingFixResult with outcome.
        """
        result = HealingFixResult(suggestion=suggestion, success=False)
        
        # Find page.py files in test directories
        page_files = list(self.workspace_root.glob("tests/*/page.py"))
        
        if not page_files:
            result.error = "No page.py files found to update"
            return result
        
        for page_file in page_files:
            if self.backup and not dry_run:
                self._backup_file(page_file)
            
            # Read current content
            content = page_file.read_text()
            
            # Simple Schema fix: add Optional to fields
            # This is a basic implementation - more sophisticated parsing would be needed
            updated_content = self._add_optional_fields(content)
            
            if updated_content != content and not dry_run:
                page_file.write_text(updated_content)
                result.files_modified.append(str(page_file))
        
        if result.files_modified:
            result.success = True
            result.tests_affected = len(suggestion.affected_tests)
        
        return result
    
    def _add_optional_fields(self, content: str) -> str:
        """Add Optional type hints to fields that might be missing.
        
        Args:
            content: Python file content with Pydantic model.
            
        Returns:
            Updated content.
        """
        lines = content.split('\n')
        updated_lines = []
        
        in_model = False
        for line in lines:
            # Detect start of model class
            if line.strip().startswith('class ') and '(BaseModel)' in line:
                in_model = True
            
            # Detect field definitions
            if in_model and ': ' in line and not line.strip().startswith('#'):
                # Check if field is not already Optional
                if 'Optional[' not in line and '= None' not in line and not line.strip().startswith('"""'):
                    # Extract field name and type
                    if '    ' in line and ':' in line:  # Indented field definition
                        # Simple heuristic: make string and dict fields optional
                        if 'str' in line or 'dict' in line or 'Dict' in line or 'List' in line:
                            if '=' not in line:  # Only if no default value
                                # Make it optional with default None
                                line = line.rstrip() + ' = None'
            
            updated_lines.append(line)
        
        return '\n'.join(updated_lines)
    
    def _fix_auth_failure(self, suggestion: HealingSuggestion, dry_run: bool) -> HealingFixResult:
        """Fix authentication failures by refreshing tokens.
        
        Args:
            suggestion: HealingSuggestion for auth fix.
            dry_run: If True, don't actually modify files.
            
        Returns:
            HealingFixResult with outcome.
        """
        result = HealingFixResult(suggestion=suggestion, success=False)
        
        # Find conftest.py files
        conftest_files = [
            self.workspace_root / "tests" / "conftest.py",
            *self.workspace_root.glob("tests/*/conftest.py")
        ]
        
        conftest_files = [f for f in conftest_files if f.exists()]
        
        if not conftest_files:
            result.error = "No conftest.py files found"
            return result
        
        for conftest_file in conftest_files:
            if self.backup and not dry_run:
                self._backup_file(conftest_file)
            
            content = conftest_file.read_text()
            
            # Add token refresh to api_client fixture
            if 'def api_client()' in content and 'refresh_token' not in content:
                updated_content = self._add_token_refresh(content)
                
                if updated_content != content and not dry_run:
                    conftest_file.write_text(updated_content)
                    result.files_modified.append(str(conftest_file))
                    result.success = True
        
        if result.success:
            result.tests_affected = len(suggestion.affected_tests)
        else:
            result.error = "Could not apply token refresh - fixture structure unexpected"
        
        return result
    
    def _add_token_refresh(self, content: str) -> str:
        """Add token refresh to API client fixture.
        
        Args:
            content: Current conftest.py content.
            
        Returns:
            Updated content with token refresh.
        """
        lines = content.split('\n')
        updated_lines = []
        
        for i, line in enumerate(lines):
            updated_lines.append(line)
            
            # Look for api_client fixture return statement
            if 'return ' in line and 'api_client' in '\n'.join(lines[max(0, i-10):i]):
                # Insert token refresh before return
                indent = len(line) - len(line.lstrip())
                refresh_line = ' ' * indent + 'client.refresh_token()  # Auto-healed: refresh auth token'
                
                # Insert after client creation, before return
                if 'return client' in line:
                    return_indent = len(line) - len(line.lstrip())
                    # Look back for client assignment
                    for j in range(i-1, max(0, i-5), -1):
                        if 'client = ' in lines[j]:
                            # Insert refresh after assignment
                            assign_indent = len(lines[j]) - len(lines[j].lstrip())
                            updated_lines.insert(len(updated_lines)-1, 
                                              ' ' * assign_indent + 'client.refresh_token()  # Auto-healed')
                            break
        
        return '\n'.join(updated_lines)
    
    def _fix_timeout(self, suggestion: HealingSuggestion, dry_run: bool) -> HealingFixResult:
        """Fix timeout issues by increasing timeout threshold.
        
        Args:
            suggestion: HealingSuggestion for timeout fix.
            dry_run: If True, don't actually modify files.
            
        Returns:
            HealingFixResult with outcome.
        """
        result = HealingFixResult(suggestion=suggestion, success=False)
        
        # Find pytest.ini
        pytest_ini = self.workspace_root / "pytest.ini"
        
        if not pytest_ini.exists():
            result.error = "pytest.ini not found"
            return result
        
        if self.backup and not dry_run:
            self._backup_file(pytest_ini)
        
        content = pytest_ini.read_text()
        
        # Update timeout value
        if 'timeout = ' in content:
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if line.startswith('timeout = '):
                    try:
                        current_timeout = int(line.split('=')[1].strip())
                        new_timeout = int(current_timeout * 1.5)
                        line = f'timeout = {new_timeout}  # Auto-healed: increased from {current_timeout}'
                    except (ValueError, IndexError):
                        pass
                
                updated_lines.append(line)
            
            updated_content = '\n'.join(updated_lines)
            
            if updated_content != content and not dry_run:
                pytest_ini.write_text(updated_content)
                result.files_modified.append(str(pytest_ini))
                result.success = True
                result.tests_affected = len(suggestion.affected_tests)
        
        if not result.success:
            result.error = "Could not find or update timeout setting"
        
        return result
    
    def _backup_file(self, file_path: Path) -> Path:
        """Backup a file before modifying it.
        
        Args:
            file_path: File to backup.
            
        Returns:
            Path to backup location.
        """
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Preserve directory structure in backup
        relative_path = file_path.relative_to(self.workspace_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_path)
        self.session.files_backed_up.append(str(file_path))
        
        return backup_path
    
    def rollback_all(self) -> bool:
        """Rollback all healing changes in this session.
        
        Returns:
            True if rollback was successful.
        """
        if not self.backup_dir.exists():
            print(f"Backup directory not found: {self.backup_dir}")
            return False
        
        try:
            # Restore all backed-up files
            for backup_file in self.backup_dir.rglob("*"):
                if backup_file.is_file():
                    # Calculate original path
                    relative_path = backup_file.relative_to(self.backup_dir)
                    original_file = self.workspace_root / relative_path
                    
                    # Restore
                    original_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, original_file)
                    print(f"Restored: {original_file}")
            
            # Remove backup directory
            shutil.rmtree(self.backup_dir)
            print(f"Rollback complete. Removed backup: {self.backup_dir}")
            return True
        
        except Exception as e:
            print(f"Rollback failed: {e}")
            return False
    
    def save_session_log(self) -> Path:
        """Save healing session log.
        
        Returns:
            Path to log file.
        """
        log_dir = self.workspace_root / ".healing-logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"healing-{self.session.session_id}.json"
        
        session_data = {
            "session_id": self.session.session_id,
            "started_at": self.session.started_at.isoformat(),
            "total_fixes": self.session.total_fixes_applied,
            "successful": self.session.fixes_successful,
            "failed": self.session.fixes_failed,
            "success_rate": self.session.success_rate,
            "files_backed_up": self.session.files_backed_up,
            "results": [
                {
                    "suggestion": result.suggestion.title,
                    "success": result.success,
                    "error": result.error,
                    "files": result.files_modified,
                    "affected_tests": result.tests_affected
                }
                for result in self.session.fix_results
            ]
        }
        
        with open(log_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return log_file
