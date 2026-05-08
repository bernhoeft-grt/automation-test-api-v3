"""Test Healing & Auto-Repair System.

This package provides automated diagnosis and repair of failing tests.

Quick Start:
    from utils.healing.analyzer import TestFailureAnalyzer
    from utils.healing.auto_fixer import TestAutoFixer
    
    # Analyze
    analyzer = TestFailureAnalyzer()
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    # Fix
    fixer = TestAutoFixer()
    session = fixer.apply_fixes(report)

CLI Usage:
    python -m utils.healing.cli analyze
    python -m utils.healing.cli suggest --severity critical
    python -m utils.healing.cli fix
    python -m utils.healing.cli rollback
"""

from .analyzer import TestFailureAnalyzer
from .auto_fixer import TestAutoFixer
from .models import (
    TestFailure,
    HealingSuggestion,
    HealingReport,
    HealingFixResult,
    HealingSession,
    FailureType,
    SeverityLevel,
    FixType,
)

__all__ = [
    # Main classes
    "TestFailureAnalyzer",
    "TestAutoFixer",
    # Models
    "TestFailure",
    "HealingSuggestion",
    "HealingReport",
    "HealingFixResult",
    "HealingSession",
    # Enums
    "FailureType",
    "SeverityLevel",
    "FixType",
]

__version__ = "1.0.0"
