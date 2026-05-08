"""Environment diagnostics and troubleshooting utilities."""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiagnosticResult:
    """Result of a diagnostic check."""
    category: str
    check: str
    passed: bool
    message: str
    suggestion: Optional[str] = None
    severity: str = "info"  # info, warning, error


@dataclass
class EnvironmentReport:
    """Environment diagnostic report."""
    timestamp: str
    python_info: Dict
    venv_info: Dict
    dependencies: Dict
    issues: List[DiagnosticResult]
    suggestions: List[str]
    
    @property
    def summary(self) -> str:
        """Get summary of report."""
        error_count = sum(1 for i in self.issues if i.severity == "error")
        warning_count = sum(1 for i in self.issues if i.severity == "warning")
        
        return f"""
╔════════════════════════════════════════╗
║      ENVIRONMENT DIAGNOSTIC REPORT      ║
╚════════════════════════════════════════╝

📅 Timestamp: {self.timestamp}

✓ Python: {self.python_info.get('version', 'unknown')}
✓ Location: {self.python_info.get('executable', 'unknown')}
✓ venv: {'✅ Active' if self.venv_info.get('active') else '❌ Inactive'}

📊 ISSUES FOUND:
   • Errors: {error_count}
   • Warnings: {warning_count}
   • Info: {len([i for i in self.issues if i.severity == 'info'])}

💡 SUGGESTIONS:
{chr(10).join(f'   {i+1}. {s}' for i, s in enumerate(self.suggestions[:5]))}

📋 Run @troubleshooting Fix for automatic repair
        """


class EnvironmentDiagnostics:
    """Diagnose and repair environment issues."""

    def __init__(self):
        self.issues: List[DiagnosticResult] = []
        self.fixes_applied: List[str] = []

    def diagnose_full(self) -> EnvironmentReport:
        """Run comprehensive diagnostics."""
        self.issues = []
        
        python_info = self._check_python()
        venv_info = self._check_venv()
        dependencies = self._check_dependencies()
        
        # Additional checks
        self._check_env_variables()
        self._check_paths()
        self._check_git()

        suggestions = self._generate_suggestions()

        return EnvironmentReport(
            timestamp=datetime.now().isoformat(),
            python_info=python_info,
            venv_info=venv_info,
            dependencies=dependencies,
            issues=self.issues,
            suggestions=suggestions,
        )

    def _check_python(self) -> Dict:
        """Check Python configuration."""
        try:
            version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            executable = sys.executable
            
            self.issues.append(DiagnosticResult(
                category="Python",
                check="Python Found",
                passed=True,
                message=f"Python {version} at {executable}"
            ))
            
            return {
                "version": version,
                "executable": executable,
                "architecture": "64bit" if sys.maxsize > 2**32 else "32bit",
            }
        except Exception as e:
            self.issues.append(DiagnosticResult(
                category="Python",
                check="Python Found",
                passed=False,
                message=str(e),
                severity="error"
            ))
            return {}

    def _check_venv(self) -> Dict:
        """Check virtual environment."""
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        
        venv_path = os.environ.get('VIRTUAL_ENV', '')
        
        if in_venv:
            self.issues.append(DiagnosticResult(
                category="Virtual Environment",
                check="venv Active",
                passed=True,
                message=f"Virtual environment active: {venv_path}"
            ))
        else:
            self.issues.append(DiagnosticResult(
                category="Virtual Environment",
                check="venv Active",
                passed=False,
                message="Virtual environment not activated",
                suggestion="Run: source venv/bin/activate",
                severity="error"
            ))
        
        return {
            "active": in_venv,
            "path": venv_path,
        }

    def _check_dependencies(self) -> Dict:
        """Check installed dependencies."""
        required = {
            'pytest': 'Testing framework',
            'requests': 'HTTP library',
            'pydantic': 'Data validation',
            'allure': 'Test reporting',
            'dotenv': 'Environment config',
        }
        
        installed = {}
        missing = []
        
        for package, description in required.items():
            try:
                mod = __import__(package)
                version = getattr(mod, '__version__', 'unknown')
                installed[package] = version
                
                self.issues.append(DiagnosticResult(
                    category="Dependencies",
                    check=f"{package}",
                    passed=True,
                    message=f"{package} {version} installed"
                ))
            except ImportError:
                missing.append(package)
                
                self.issues.append(DiagnosticResult(
                    category="Dependencies",
                    check=f"{package}",
                    passed=False,
                    message=f"{package} not installed",
                    suggestion=f"Run: pip install {package}",
                    severity="error"
                ))
        
        return {
            "installed": installed,
            "missing": missing,
            "total_installed": len(installed),
            "total_required": len(required),
        }

    def _check_env_variables(self):
        """Check environment variables."""
        required_vars = {
            'SWAGGER_URL': 'API Swagger specification',
            'BASE_URL': 'API base URL',
        }
        
        for var, description in required_vars.items():
            if os.getenv(var):
                self.issues.append(DiagnosticResult(
                    category="Configuration",
                    check=f"ENV: {var}",
                    passed=True,
                    message=f"{var} is set"
                ))
            else:
                self.issues.append(DiagnosticResult(
                    category="Configuration",
                    check=f"ENV: {var}",
                    passed=False,
                    message=f"{var} not set",
                    suggestion=f"Add to .env: {var}=...",
                    severity="warning"
                ))

    def _check_paths(self):
        """Check Python paths."""
        # Just verify PYTHONPATH if set
        pythonpath = os.getenv('PYTHONPATH', '')
        if pythonpath:
            self.issues.append(DiagnosticResult(
                category="Paths",
                check="PYTHONPATH",
                passed=True,
                message=f"PYTHONPATH: {pythonpath}"
            ))

    def _check_git(self):
        """Check git configuration."""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                self.issues.append(DiagnosticResult(
                    category="System Tools",
                    check="git",
                    passed=True,
                    message=result.stdout.strip()
                ))
        except:
            self.issues.append(DiagnosticResult(
                category="System Tools",
                check="git",
                passed=False,
                message="git not found",
                severity="warning"
            ))

    def _generate_suggestions(self) -> List[str]:
        """Generate fix suggestions."""
        suggestions = []
        
        for issue in self.issues:
            if not issue.passed and issue.suggestion:
                if issue.suggestion not in suggestions:
                    suggestions.append(issue.suggestion)
        
        if not suggestions:
            return ["✅ No issues found! Environment is healthy."]
        
        return suggestions

    def get_python_executable(self) -> str:
        """Get path to python executable."""
        return sys.executable

    def get_pip_executable(self) -> str:
        """Get path to pip executable."""
        return f"{self.get_python_executable()} -m pip"

    def print_report(self, report: EnvironmentReport):
        """Pretty print diagnostic report."""
        print(report.summary)
        
        print("\n📋 DETAILED ISSUES:")
        for issue in report.issues:
            icon = "✅" if issue.passed else "❌"
            print(f"{icon} [{issue.category}] {issue.check}: {issue.message}")
            if issue.suggestion:
                print(f"   💡 Suggestion: {issue.suggestion}")

    def apply_fixes(self, fix_types: Optional[List[str]] = None) -> bool:
        """Apply fixes to environment."""
        if fix_types is None:
            fix_types = ['install_missing', 'use_binary_wheels']
        
        print("🔧 Applying fixes...\n")
        
        for fix_type in fix_types:
            if fix_type == 'install_missing':
                self._fix_install_missing()
            elif fix_type == 'use_binary_wheels':
                self._fix_use_binary_wheels()
            elif fix_type == 'rebuild_venv':
                self._fix_rebuild_venv()
        
        return True

    def _fix_install_missing(self):
        """Install missing packages."""
        print("📦 Installing missing packages...")
        subprocess.run([
            self.get_python_executable(), '-m', 'pip', 'install',
            'pytest', 'requests', 'pydantic', 'python-dotenv'
        ])
        self.fixes_applied.append('install_missing')

    def _fix_use_binary_wheels(self):
        """Use binary wheels (no compilation)."""
        print("⚙️ Installing with prebuilt wheels (no compilation)...\n")
        
        packages = [
            'pytest', 'requests', 'pydantic', 'pydantic-core',
            'allure-pytest', 'python-dotenv', 'greenlet'
        ]
        
        cmd = [
            self.get_python_executable(), '-m', 'pip', 'install',
            '--only-binary', ':all:', '--upgrade', 'pip', 'setuptools', 'wheel'
        ]
        
        print(f"Running: {' '.join(cmd)}\n")
        subprocess.run(cmd)
        
        for package in packages:
            cmd = [
                self.get_python_executable(), '-m', 'pip', 'install',
                '--only-binary', ':all:', package
            ]
            subprocess.run(cmd, capture_output=True)
        
        self.fixes_applied.append('use_binary_wheels')

    def _fix_rebuild_venv(self):
        """Rebuild virtual environment."""
        print("🔨 Rebuilding virtual environment...")
        print("⚠️ This will remove and recreate venv\n")
        
        venv_path = Path('venv')
        if venv_path.exists():
            import shutil
            print(f"Removing {venv_path}...")
            shutil.rmtree(venv_path)
        
        print("Creating new venv...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        
        print("Installing requirements...")
        subprocess.run([
            str(venv_path / 'bin' / 'pip'), 'install',
            '--upgrade', 'pip'
        ])
        subprocess.run([
            str(venv_path / 'bin' / 'pip'), 'install',
            '-r', 'requirements.txt'
        ])
        
        self.fixes_applied.append('rebuild_venv')


def quick_diagnose():
    """Run quick diagnostic."""
    diag = EnvironmentDiagnostics()
    report = diag.diagnose_full()
    diag.print_report(report)
    return report


def auto_fix():
    """Automatically fix environment."""
    print("🔧 Auto-fixing environment...\n")
    
    diag = EnvironmentDiagnostics()
    report = diag.diagnose_full()
    
    print(report.summary)
    
    if any(i.severity == 'error' for i in report.issues):
        print("\n⚠️ Found issues. Applying fixes...\n")
        diag.apply_fixes(['install_missing', 'use_binary_wheels'])
        
        # Re-diagnose
        print("\n\n✅ Validating fixes...\n")
        report2 = diag.diagnose_full()
        diag.print_report(report2)
    else:
        print("\n✅ Environment is healthy!")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'fix':
        auto_fix()
    else:
        quick_diagnose()
