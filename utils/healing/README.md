# Test Healing & Auto-Repair System

## Overview

The **Test Healing** system automatically diagnoses failing tests, analyzes root causes, and applies intelligent fixes to get your test suite back to green. It's designed to work seamlessly with the Allure reporting system and pytest.

## Features

- 🔍 **Failure Detection**: Automatically scans Allure results and pytest output
- 🔎 **Root Cause Analysis**: Categorizes failures and identifies underlying issues
- 💡 **Smart Suggestions**: Provides ranked fixes from critical to low priority
- 🔧 **Auto-Fix**: Applies safe, automatic corrections
- 📊 **Detailed Reports**: HTML/JSON/Text reports with before/after comparisons
- 💾 **Safe Operations**: Automatic backups before any modifications
- ⏮️ **Rollback**: Undo all healing changes in one command

## Quick Start

### 1. Analyze Recent Failures

```bash
python -m utils.healing.cli analyze
```

Output shows all failures found:
```
Found 12 failures:

❌ test_area_create - AssertionError: 201 != 400
   File: tests/area/test_create.py:15
   Type: assertion_error
   Message: Expected status 201, got 400...
```

### 2. Get Suggestions

```bash
python -m utils.healing.cli suggest --severity critical
```

List all recommended fixes, sorted by severity.

### 3. Preview Fixes (Dry-Run)

```bash
python -m utils.healing.cli fix --dry-run
```

See what would be fixed without making changes.

### 4. Apply Auto-Fixes

```bash
python -m utils.healing.cli fix
```

Apply automatic fixes with backup.

### 5. Generate Report

```bash
python -m utils.healing.cli report --format html --output healing-report.html
```

## Python API

### Basic Usage

```python
from utils.healing.analyzer import TestFailureAnalyzer
from utils.healing.auto_fixer import TestAutoFixer

# Analyze
analyzer = TestFailureAnalyzer()
failures = analyzer.scan_allure_results()
report = analyzer.analyze_failures()

print(report.summary)

# Auto-fix
fixer = TestAutoFixer(backup=True)
session = fixer.apply_fixes(report, dry_run=False)

print(session.summary())
```

### Advanced Analysis

```python
from utils.healing.models import SeverityLevel

# Get critical failures only
critical_failures = [
    f for f in report.failures
    if f.severity == SeverityLevel.CRITICAL
]

# Get specific failure details
failure = analyzer.get_failure("test_area_create")
print(f"Type: {failure.error_type}")
print(f"Message: {failure.error_message}")
print(f"Traceback: {failure.traceback}")

# Get suggestions for specific severity
critical_suggestions = analyzer.get_suggestions(SeverityLevel.CRITICAL)
for suggestion in critical_suggestions:
    print(f"{suggestion.title}: {suggestion.description}")
```

### Custom Fixing

```python
from utils.healing.auto_fixer import TestAutoFixer

fixer = TestAutoFixer()

# Apply specific suggestion
for suggestion in report.suggestions:
    if suggestion.fix_type == FixType.AUTO_FIX:
        result = fixer.apply_fix(suggestion, dry_run=False)
        print(f"Applied: {result}")

# Rollback if needed
fixer.rollback_all()
```

## Failure Categories

### 1. Assertion Failures
**When**: Expected != Actual
```
AssertionError: assert 201 == 400
```
**Fixes**: Update assertions, add missing fields, adjust expected values

### 2. Schema Mismatches
**When**: Pydantic validation errors
```
ValidationError: Field 'user_id' required
```
**Fixes**: Add missing fields to schema, make optional, update types

### 3. Fixture Issues
**When**: Setup/teardown failures
```
Fixture 'api_client' failed during setup
```
**Fixes**: Regenerate fixtures, fix conftest.py, update data

### 4. API Changes
**When**: Endpoint deprecated or changed
```
404 Not Found
```
**Fixes**: Update endpoint URLs, adjust request/response format

### 5. Authentication Failures
**When**: Token expired or invalid
```
401 Unauthorized
```
**Fixes**: Refresh tokens, update credentials

### 6. Timeout Issues
**When**: Tests exceed max duration
```
Timeout: test took >30 seconds
```
**Fixes**: Increase timeout, optimize tests, mock slow calls

## Configuration

### `.env` Settings

```bash
# Enable healing system
HEALING_ENABLED=true

# Auto-apply fixes automatically
HEALING_AUTO_FIX=true

# Backup files before modifying
HEALING_BACKUP_ORIGINALS=true

# Increase timeout by multiplier
HEALING_TIMEOUT_MULTIPLIER=1.5

# Auto-update Pydantic schemas
HEALING_SCHEMA_AUTO_UPDATE=true

# Report format
HEALING_REPORT_FORMAT=html
```

### `pytest.ini` Configuration

```ini
[pytest]
# Base timeout for all tests
timeout = 30

# Markers for healing
markers =
    healing: Mark test for healing analysis
    flaky: Known flaky test
    critical: Critical path test
```

## Safety Features

### Automatic Backups

All files modified are automatically backed up:
```
.backups/
├── 2026-04-19-143022/
│   └── tests/
│       └── area/
│           └── page.py
└── 2026-04-19-143500/
    └── pytest.ini
```

### Dry-Run Mode

Preview all changes before applying:
```bash
python -m utils.healing.cli fix --dry-run
```

### Rollback Command

Undo all healing changes:
```bash
python -m utils.healing.cli rollback
```

### Session Audit Trail

All fixes logged to `.healing-logs/`:
```json
{
  "session_id": "a1b2c3d4",
  "started_at": "2026-04-19T14:30:22",
  "total_fixes": 8,
  "successful": 8,
  "failed": 0,
  "success_rate": 100.0,
  "results": [...]
}
```

View recent sessions:
```bash
python -m utils.healing.cli log --last 10
```

## CLI Commands

### analyze
Scan and analyze all test failures.
```bash
python -m utils.healing.cli analyze
```

### suggest
Get healing suggestions for failures.
```bash
python -m utils.healing.cli suggest
python -m utils.healing.cli suggest --severity critical
python -m utils.healing.cli suggest --type auto_fix
```

### fix
Apply automatic fixes.
```bash
python -m utils.healing.cli fix              # Apply fixes
python -m utils.healing.cli fix --dry-run    # Preview
python -m utils.healing.cli fix --no-backup  # No backup
```

### report
Generate detailed healing reports.
```bash
python -m utils.healing.cli report                      # Text
python -m utils.healing.cli report -f json -o out.json  # JSON
python -m utils.healing.cli report -f html -o out.html  # HTML
```

### rollback
Undo healing changes.
```bash
python -m utils.healing.cli rollback
python -m utils.healing.cli rollback -s a1b2c3d4  # Specific session
```

### log
View healing session history.
```bash
python -m utils.healing.cli log
python -m utils.healing.cli log --last 20
```

## Report Example

### Text Report
```
╔════════════════════════════════════════════════════╗
║         TEST HEALING REPORT - 2026-04-19           ║
╚════════════════════════════════════════════════════╝

📊 SUMMARY
  Total Failures: 12
  Auto-fixable: 8 (67%)
  Requires Review: 4 (33%)

🔴 CRITICAL (4)
🟡 MEDIUM (5)
🟢 LOW (3)

✅ AUTO-FIX RESULTS
  Applied: 8 fixes
  Files Modified: 12
  Success Rate: 100%
```

### JSON Report
```json
{
  "total_failures": 12,
  "auto_fixable": 8,
  "requires_review": 4,
  "failures": [
    {
      "test": "test_area_create",
      "type": "assertion_error",
      "severity": "medium",
      "message": "Expected status 201, got 400"
    }
  ],
  "suggestions": [...]
}
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Analyze failing tests
  run: python -m utils.healing.cli analyze

- name: Apply auto-fixes
  run: python -m utils.healing.cli fix

- name: Re-run tests
  run: pytest tests/ -v
```

### GitLab CI Example
```yaml
healing:
  stage: test
  script:
    - python -m utils.healing.cli analyze
    - python -m utils.healing.cli fix
    - pytest tests/ -v --alluredir=allure-results
```

## Troubleshooting

### Healing didn't fix all issues
- Some issues require manual review (⚠️ flagged)
- Check severity levels, critical fixes first
- Review detailed logs: `python -m utils.healing.cli log`

### Too many changes made
- Inspect changes: `python -m utils.healing.cli rollback`
- Try dry-run next time: `--dry-run`
- Check backup: `.backups/`

### Authentication token issues
- Ensure `.env` has valid credentials
- Manual fixture review might be needed
- Check API token expiration policy

## Advanced Usage

### Custom Failure Detection

```python
from utils.healing.analyzer import TestFailureAnalyzer

class CustomAnalyzer(TestFailureAnalyzer):
    def _detect_failure_type(self, message, traceback):
        # Add custom detection logic
        if "my_custom_error" in message:
            return FailureType.CUSTOM
        return super()._detect_failure_type(message, traceback)

analyzer = CustomAnalyzer()
```

### Custom Auto-Fix

```python
from utils.healing.auto_fixer import TestAutoFixer

class CustomFixer(TestAutoFixer):
    def apply_fix(self, suggestion, dry_run=False):
        # Add custom fix logic
        if suggestion.title == "Custom Fix":
            return self._apply_custom_fix(suggestion, dry_run)
        return super().apply_fix(suggestion, dry_run)

fixer = CustomFixer()
```

## Architecture

```
Test Results (pytest, Allure)
           ↓
   TestFailureAnalyzer
   ├─ scan_allure_results()
   ├─ analyze_failures()
   └─ get_suggestions()
           ↓
    HealingReport
   (failures + suggestions)
           ↓
    TestAutoFixer
   ├─ apply_fixes()
   ├─ apply_fix()
   ├─ backup_file()
   └─ rollback_all()
           ↓
    HealingSession
   (results + audit trail)
```

## Contributing

To add new failure types or auto-fixes:

1. Add to `models.py` enums if needed
2. Implement detection in `analyzer.py`
3. Implement fix in `auto_fixer.py`
4. Add CLI example
5. Update documentation

## License

Part of the Automation Test CWeb API project.
