"""Command-line interface for test healing system."""
import argparse
import json
from pathlib import Path
from typing import Optional

from .analyzer import TestFailureAnalyzer
from .auto_fixer import TestAutoFixer
from .models import SeverityLevel


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for healing CLI.
    
    Returns:
        ArgumentParser configured for healing commands.
    """
    parser = argparse.ArgumentParser(
        description="Test Healing System - Analyze and fix failing tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze recent failures
  python -m utils.healing.cli analyze
  
  # Get critical issues only
  python -m utils.healing.cli suggest --severity critical
  
  # Auto-fix with backup
  python -m utils.healing.cli fix
  
  # Preview changes without applying
  python -m utils.healing.cli fix --dry-run
  
  # Generate detailed report
  python -m utils.healing.cli report --format html
  
  # Rollback all healing changes
  python -m utils.healing.cli rollback
  
  # View healing logs
  python -m utils.healing.cli log --last 10
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze test failures")
    analyze_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    analyze_parser.add_argument(
        "--allure-dir",
        type=Path,
        help="Path to allure-results directory"
    )
    
    # Suggest command
    suggest_parser = subparsers.add_parser("suggest", help="Get healing suggestions")
    suggest_parser.add_argument(
        "-s", "--severity",
        choices=["critical", "medium", "low"],
        help="Filter by severity level"
    )
    suggest_parser.add_argument(
        "-t", "--type",
        choices=["auto_fix", "manual_review"],
        help="Filter by fix type"
    )
    suggest_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    
    # Fix command
    fix_parser = subparsers.add_parser("fix", help="Apply auto-fixes")
    fix_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying"
    )
    fix_parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't backup files before modifying"
    )
    fix_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate healing report")
    report_parser.add_argument(
        "-f", "--format",
        choices=["text", "json", "html"],
        default="text",
        help="Report output format"
    )
    report_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path"
    )
    report_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    
    # Rollback command
    rollback_parser = subparsers.add_parser("rollback", help="Rollback healing changes")
    rollback_parser.add_argument(
        "-s", "--session",
        help="Specific session ID to rollback"
    )
    rollback_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    
    # Log command
    log_parser = subparsers.add_parser("log", help="View healing logs")
    log_parser.add_argument(
        "--last",
        type=int,
        default=5,
        help="Show last N sessions"
    )
    log_parser.add_argument(
        "-w", "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root directory"
    )
    
    return parser


def command_analyze(workspace: Path) -> None:
    """Execute analyze command.
    
    Args:
        workspace: Workspace root directory.
    """
    print("🔍 Analyzing test failures...")
    print()
    
    analyzer = TestFailureAnalyzer(workspace)
    failures = analyzer.scan_allure_results()
    
    if not failures:
        print("✅ No failures found!")
        return
    
    print(f"Found {len(failures)} failures:\n")
    
    for failure in failures:
        print(f"❌ {failure}")
        print(f"   File: {failure.file_path}:{failure.line_number}")
        print(f"   Type: {failure.error_type.value}")
        print(f"   Message: {failure.error_message[:100]}...")
        print()
    
    # Generate report
    report = analyzer.analyze_failures()
    print(report.summary)


def command_suggest(workspace: Path, severity: Optional[str] = None, type_filter: Optional[str] = None) -> None:
    """Execute suggest command.
    
    Args:
        workspace: Workspace root directory.
        severity: Optional severity filter.
        type_filter: Optional type filter.
    """
    print("💡 Getting healing suggestions...\n")
    
    analyzer = TestFailureAnalyzer(workspace)
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    suggestions = report.suggestions
    
    # Filter by severity if specified
    if severity:
        severity_level = SeverityLevel(severity)
        suggestions = [s for s in suggestions if s.severity == severity_level]
    
    # Filter by type if specified
    if type_filter:
        suggestions = [s for s in suggestions if s.fix_type.value == type_filter]
    
    if not suggestions:
        print("✅ No suggestions found!")
        return
    
    print(f"Found {len(suggestions)} suggestions:\n")
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion.title}")
        print(f"   Severity: {suggestion.severity.value.upper()}")
        print(f"   Type: {suggestion.fix_type.value}")
        print(f"   Affected tests: {len(suggestion.affected_tests)}")
        print(f"   Description: {suggestion.description}")
        print(f"   Risk: {suggestion.risk_level}")
        print()


def command_fix(workspace: Path, dry_run: bool = False, no_backup: bool = False) -> None:
    """Execute fix command.
    
    Args:
        workspace: Workspace root directory.
        dry_run: If True, preview changes without applying.
        no_backup: If True, don't backup files.
    """
    print("🔧 Applying auto-fixes...\n")
    
    analyzer = TestFailureAnalyzer(workspace)
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    fixer = TestAutoFixer(workspace, backup=not no_backup)
    
    if dry_run:
        print("📋 DRY-RUN MODE - No changes will be applied\n")
    
    session = fixer.apply_fixes(report, dry_run=dry_run)
    
    print(session.summary())
    
    # Save log
    if not dry_run:
        log_file = fixer.save_session_log()
        print(f"\n📝 Session log saved to: {log_file}")


def command_report(workspace: Path, format_type: str = "text", output: Optional[Path] = None) -> None:
    """Execute report command.
    
    Args:
        workspace: Workspace root directory.
        format_type: Report format (text, json, html).
        output: Output file path.
    """
    print(f"📊 Generating {format_type} report...\n")
    
    analyzer = TestFailureAnalyzer(workspace)
    analyzer.scan_allure_results()
    report = analyzer.analyze_failures()
    
    if format_type == "text":
        content = report.summary
        print(content)
    
    elif format_type == "json":
        content = json.dumps({
            "total_failures": report.total_failures,
            "auto_fixable": report.auto_fixable,
            "requires_review": report.requires_review,
            "failures": [
                {
                    "test": f.test_name,
                    "type": f.error_type.value,
                    "severity": f.severity.value,
                    "message": f.error_message
                }
                for f in report.failures
            ],
            "suggestions": [
                {
                    "title": s.title,
                    "type": s.fix_type.value,
                    "severity": s.severity.value,
                    "affected_tests": len(s.affected_tests)
                }
                for s in report.suggestions
            ]
        }, indent=2)
        print(content)
    
    elif format_type == "html":
        content = f"""
<html>
<head>
    <title>Test Healing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 10px; border-radius: 5px; }}
        .failure {{ margin: 10px 0; padding: 10px; border-left: 3px solid red; }}
        .suggestion {{ margin: 10px 0; padding: 10px; border-left: 3px solid blue; }}
    </style>
</head>
<body>
    <h1>Test Healing Report</h1>
    <div class="summary">
        <p>Total Failures: {report.total_failures}</p>
        <p>Auto-fixable: {report.auto_fixable}</p>
        <p>Requires Review: {report.requires_review}</p>
    </div>
    
    <h2>Failures</h2>
    {''.join(f'<div class="failure">{f.test_name}: {f.error_message}</div>' for f in report.failures)}
    
    <h2>Suggestions</h2>
    {''.join(f'<div class="suggestion">{s.title} ({s.fix_type.value})</div>' for s in report.suggestions)}
</body>
</html>
"""
        print(content)
    
    # Save to file if specified
    if output:
        output.write_text(content)
        print(f"\n✅ Report saved to: {output}")


def command_rollback(workspace: Path, session_id: Optional[str] = None) -> None:
    """Execute rollback command.
    
    Args:
        workspace: Workspace root directory.
        session_id: Optional specific session to rollback.
    """
    print("⏮️  Rolling back healing changes...\n")
    
    if session_id:
        print(f"Rolling back session: {session_id}")
    
    fixer = TestAutoFixer(workspace)
    success = fixer.rollback_all()
    
    if success:
        print("✅ Rollback completed successfully!")
    else:
        print("❌ Rollback failed!")


def command_log(workspace: Path, last_n: int = 5) -> None:
    """Execute log command.
    
    Args:
        workspace: Workspace root directory.
        last_n: Number of recent sessions to show.
    """
    print(f"📝 Recent healing sessions (last {last_n}):\n")
    
    log_dir = workspace / ".healing-logs"
    
    if not log_dir.exists():
        print("No healing logs found!")
        return
    
    log_files = sorted(log_dir.glob("healing-*.json"), reverse=True)[:last_n]
    
    for log_file in log_files:
        with open(log_file) as f:
            session = json.load(f)
        
        print(f"Session: {session['session_id']}")
        print(f"  Time: {session['started_at']}")
        print(f"  Fixes: {session['successful']}/{session['total_fixes']} successful")
        print(f"  Success Rate: {session['success_rate']:.1f}%")
        print()


def main():
    """Main entrypoint for healing CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Dispatch to command handler
    if args.command == "analyze":
        command_analyze(args.workspace)
    
    elif args.command == "suggest":
        command_suggest(args.workspace, args.severity, args.type)
    
    elif args.command == "fix":
        command_fix(args.workspace, args.dry_run, args.no_backup)
    
    elif args.command == "report":
        command_report(args.workspace, args.format, args.output)
    
    elif args.command == "rollback":
        command_rollback(args.workspace, args.session)
    
    elif args.command == "log":
        command_log(args.workspace, args.last)


if __name__ == "__main__":
    main()
