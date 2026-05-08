"""Example usage of the Test Healing system."""

from pathlib import Path
from utils.healing.analyzer import TestFailureAnalyzer
from utils.healing.auto_fixer import TestAutoFixer
from utils.healing.models import SeverityLevel, FixType


def example_analyze_failures():
    """Example: Analyze test failures."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Analyze Test Failures")
    print("="*60)
    
    analyzer = TestFailureAnalyzer()
    
    # Scan Allure results
    failures = analyzer.scan_allure_results()
    
    if not failures:
        print("\n✅ No failures found!")
        return
    
    print(f"\n🔍 Found {len(failures)} test failures:\n")
    for i, failure in enumerate(failures[:5], 1):
        print(f"{i}. {failure}")
        print(f"   File: {failure.file_path}:{failure.line_number}")
        print(f"   Type: {failure.error_type.value}")
        print(f"   Message: {failure.error_message[:80]}...")
        print()


def example_get_suggestions():
    """Example: Get healing suggestions."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Get Healing Suggestions")
    print("="*60)
    
    analyzer = TestFailureAnalyzer()
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    # Get critical suggestions only
    critical_suggestions = analyzer.get_suggestions(SeverityLevel.CRITICAL)
    
    print(f"\n💡 Critical suggestions ({len(critical_suggestions)}):\n")
    for i, suggestion in enumerate(critical_suggestions[:3], 1):
        print(f"{i}. {suggestion.title}")
        print(f"   Description: {suggestion.description}")
        print(f"   Type: {suggestion.fix_type.value}")
        print(f"   Affected tests: {len(suggestion.affected_tests)}")
        print(f"   File to modify: {suggestion.file_to_modify}")
        print()


def example_auto_fix():
    """Example: Apply automatic fixes."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Apply Auto-Fixes (DRY-RUN)")
    print("="*60)
    
    analyzer = TestFailureAnalyzer()
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    if not report.suggestions:
        print("\n✅ No suggestions to fix!")
        return
    
    fixer = TestAutoFixer()
    
    print(f"\n🔧 Would apply {len(report.suggestions)} fixes (dry-run mode):\n")
    
    # Show what would be fixed
    auto_fixable = [s for s in report.suggestions if s.fix_type == FixType.AUTO_FIX]
    
    for i, suggestion in enumerate(auto_fixable[:5], 1):
        print(f"{i}. {suggestion.title}")
        print(f"   File: {suggestion.file_to_modify}")
        print(f"   Risk: {suggestion.risk_level}")
        print(f"   Effort: {suggestion.estimated_effort}")
        print()
    
    # Dry-run the fixes
    session = fixer.apply_fixes(report, dry_run=True)
    print(f"\n📊 Dry-run summary:")
    print(f"   Would modify: {len(session.files_backed_up)} files")
    print(f"   Would apply: {session.total_fixes_applied} fixes")


def example_detailed_report():
    """Example: Generate detailed healing report."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generate Detailed Report")
    print("="*60)
    
    analyzer = TestFailureAnalyzer()
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    print(report.summary)
    
    print("\n📋 Top 3 Failures:")
    for i, failure in enumerate(report.failures[:3], 1):
        print(f"\n{i}. {failure.test_name}")
        print(f"   Severity: {failure.severity.value}")
        print(f"   Type: {failure.error_type.value}")
        print(f"   Message: {failure.error_message}")
    
    print("\n💡 Top 3 Suggestions:")
    for i, suggestion in enumerate(report.suggestions[:3], 1):
        print(f"\n{i}. {suggestion.title}")
        print(f"   Fix Type: {suggestion.fix_type.value}")
        print(f"   Affected: {len(suggestion.affected_tests)} tests")
        print(f"   Risk Level: {suggestion.risk_level}")


def example_analyze_specific_failure():
    """Example: Analyze a specific test failure."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Analyze Specific Failure")
    print("="*60)
    
    analyzer = TestFailureAnalyzer()
    analyzer.scan_allure_results()
    
    if not analyzer.failures:
        print("\n✅ No failures to analyze!")
        return
    
    # Get first failure
    failure = analyzer.failures[0]
    
    print(f"\n🔎 Analyzing: {failure.test_name}\n")
    print(f"File: {failure.file_path}:{failure.line_number}")
    print(f"Severity: {failure.severity.value}")
    print(f"Type: {failure.error_type.value}")
    print(f"Message: {failure.error_message}")
    print(f"\nTraceback (first 500 chars):")
    print(failure.traceback[:500])


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  TEST HEALING SYSTEM - EXAMPLES".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        example_analyze_failures()
    except Exception as e:
        print(f"⚠️  Example 1 skipped: {e}")
    
    try:
        example_get_suggestions()
    except Exception as e:
        print(f"⚠️  Example 2 skipped: {e}")
    
    try:
        example_auto_fix()
    except Exception as e:
        print(f"⚠️  Example 3 skipped: {e}")
    
    try:
        example_detailed_report()
    except Exception as e:
        print(f"⚠️  Example 4 skipped: {e}")
    
    try:
        example_analyze_specific_failure()
    except Exception as e:
        print(f"⚠️  Example 5 skipped: {e}")
    
    print("\n" + "="*60)
    print("✅ Examples complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: python utils/healing/examples.py")
    print("2. Use CLI: python -m utils.healing.cli analyze")
    print("3. Use Agent: @healing Analyze test failures")
    print("\nFor more info: utils/healing/README.md")
    print()


if __name__ == "__main__":
    main()
