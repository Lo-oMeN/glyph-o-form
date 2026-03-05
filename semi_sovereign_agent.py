#!/usr/bin/env python3
"""
Semi-Sovereign Agent - Autonomous Testing & Deployment Pipeline
Operates independently: test → report → deploy (staging) → alert
"""

import asyncio
import subprocess
import json
import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

class SemiSovereignAgent:
    """
    Autonomous agent that:
    1. Monitors repository for changes
    2. Runs comprehensive test suite
    3. Generates reports
    4. Deploys to staging (if tests pass)
    5. Alerts on failures
    6. Suggests fixes
    """
    
    def __init__(self, config_path="/root/.openclaw/workspace/.agent_config.json"):
        self.config = self._load_config(config_path)
        self.workspace = "/root/.openclaw/workspace"
        self.app_dir = f"{self.workspace}/app"
        self.report_dir = f"{self.app_dir}/reports"
        self.staging_dir = f"{self.workspace}/staging"
        
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.staging_dir, exist_ok=True)
        
        self.test_history = []
        self.last_commit = None
    
    def _load_config(self, path):
        """Load or create agent configuration"""
        default_config = {
            "autonomous_mode": True,
            "test_on_change": True,
            "auto_deploy_staging": False,  # Requires DE approval
            "alert_on_failure": True,
            "performance_budget": {
                "max_load_time_ms": 2000,
                "max_bundle_size_kb": 500,
                "min_accessibility_score": 0.9
            },
            "notification_channels": ["telegram"],
            "test_schedule": {
                "full_suite": "every_hour",
                "smoke_tests": "every_commit"
            }
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        
        with open(path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    async def run(self):
        """Main autonomous loop"""
        print("🤖 Semi-Sovereign Agent Starting...")
        print(f"📁 Workspace: {self.workspace}")
        print(f"🔄 Autonomous Mode: {self.config['autonomous_mode']}")
        
        while self.config['autonomous_mode']:
            try:
                await self._check_for_changes()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                await self._alert_error(f"Agent error: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 min on error
    
    async def _check_for_changes(self):
        """Check git for new commits"""
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%H"],
            cwd=self.workspace,
            capture_output=True,
            text=True
        )
        
        current_commit = result.stdout.strip()
        
        if current_commit != self.last_commit:
            print(f"📝 New commit detected: {current_commit[:8]}")
            self.last_commit = current_commit
            await self._on_code_change()
    
    async def _on_code_change(self):
        """Handle code change event"""
        print("\n🔍 Running test suite...")
        
        # Run smoke tests
        smoke_results = await self._run_smoke_tests()
        
        if not smoke_results['passed']:
            await self._handle_test_failure(smoke_results)
            return
        
        # Run full test suite
        full_results = await self._run_full_test_suite()
        
        # Generate report
        report = self._generate_report(full_results)
        
        # Save report
        report_path = self._save_report(report)
        
        # Send summary
        await self._send_report_summary(report)
        
        # Auto-deploy to staging (if enabled and tests pass)
        if self.config['auto_deploy_staging'] and full_results['passed']:
            await self._deploy_to_staging()
        elif full_results['passed']:
            await self._suggest_deployment(report)
    
    async def _run_smoke_tests(self):
        """Quick smoke tests (30 seconds)"""
        tests = []
        
        # Test 1: HTML validity
        tests.append(self._test_html_validity())
        
        # Test 2: JavaScript syntax
        tests.append(self._test_js_syntax())
        
        # Test 3: CSS validity
        tests.append(self._test_css_validity())
        
        # Test 4: Server starts
        tests.append(await self._test_server_startup())
        
        all_passed = all(t['passed'] for t in tests)
        
        return {
            'type': 'smoke',
            'passed': all_passed,
            'tests': tests,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _run_full_test_suite(self):
        """Comprehensive test suite (2-3 minutes)"""
        results = {
            'type': 'full',
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }
        
        # Static analysis
        results['tests']['html'] = self._test_html_validity()
        results['tests']['css'] = self._test_css_validity()
        results['tests']['javascript'] = self._test_js_syntax()
        
        # Functional tests
        results['tests']['responsive'] = self._test_responsive_design()
        results['tests']['accessibility'] = self._test_accessibility()
        results['tests']['performance'] = await self._test_performance()
        
        # Security tests
        results['tests']['security'] = self._test_security()
        
        # Calculate score
        scores = [
            1 if t['passed'] else 0 
            for t in results['tests'].values()
        ]
        results['score'] = sum(scores) / len(scores)
        results['passed'] = results['score'] >= 0.8
        
        return results
    
    def _test_html_validity(self):
        """Validate HTML files"""
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        if not html_files:
            return {'passed': False, 'error': 'No HTML files found'}
        
        results = []
        for html_file in html_files:
            with open(html_file, 'r') as f:
                content = f.read()
            
            checks = {
                'doctype': content.strip().startswith('<!DOCTYPE html>'),
                'html_tag': '<html' in content.lower(),
                'head_body': '<head>' in content and '<body>' in content
            }
            
            results.append({
                'file': html_file.name,
                'passed': all(checks.values()),
                'checks': checks
            })
        
        all_passed = all(r['passed'] for r in results)
        
        return {
            'passed': all_passed,
            'files_tested': len(results),
            'details': results
        }
    
    def _test_js_syntax(self):
        """Check JavaScript syntax"""
        js_files = list(Path(self.app_dir).glob('*.js'))
        
        if not js_files:
            return {'passed': True, 'note': 'No JS files to test'}
        
        results = []
        for js_file in js_files:
            try:
                result = subprocess.run(
                    ['node', '--check', str(js_file)],
                    capture_output=True,
                    timeout=5
                )
                results.append({
                    'file': js_file.name,
                    'passed': result.returncode == 0,
                    'error': result.stderr.decode() if result.returncode != 0 else None
                })
            except Exception as e:
                results.append({
                    'file': js_file.name,
                    'passed': False,
                    'error': str(e)
                })
        
        all_passed = all(r['passed'] for r in results)
        
        return {
            'passed': all_passed,
            'files_tested': len(results),
            'details': results
        }
    
    def _test_css_validity(self):
        """Check CSS validity"""
        css_files = list(Path(self.app_dir).glob('*.css'))
        
        # Also check inline styles in HTML
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        issues = []
        
        for html_file in html_files:
            with open(html_file, 'r') as f:
                content = f.read()
            
            # Check for basic CSS issues
            if content.count('{') != content.count('}'):
                issues.append(f"{html_file.name}: Mismatched braces")
        
        return {
            'passed': len(issues) == 0,
            'css_files': len(css_files),
            'issues': issues
        }
    
    async def _test_server_startup(self):
        """Test if server starts successfully"""
        try:
            proc = await asyncio.create_subprocess_exec(
                'python3', '-m', 'http.server', '9999',
                '--directory', self.app_dir,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            
            await asyncio.sleep(2)
            
            # Test if port is open
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:9999/'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            proc.terminate()
            
            status_code = result.stdout.strip()
            
            return {
                'passed': status_code == '200',
                'status_code': status_code
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_responsive_design(self):
        """Check for responsive design patterns"""
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        scores = []
        for html_file in html_files:
            with open(html_file, 'r') as f:
                content = f.read().lower()
            
            checks = {
                'viewport': 'viewport' in content,
                'media_queries': '@media' in content,
                'flex_or_grid': 'flex' in content or 'grid' in content,
                'percent_units': '%' in content
            }
            
            score = sum(checks.values()) / len(checks)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'passed': avg_score >= 0.6,
            'score': avg_score,
            'average': f"{avg_score:.1%}"
        }
    
    def _test_accessibility(self):
        """Basic accessibility checks"""
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        scores = []
        for html_file in html_files:
            with open(html_file, 'r') as f:
                content = f.read().lower()
            
            checks = {
                'alt_text': 'alt="' in content or "alt='" in content,
                'lang_attr': 'lang=' in content,
                'semantic_html': any(tag in content for tag in ['<main', '<header', '<nav'])
            }
            
            score = sum(checks.values()) / len(checks)
            scores.append(score)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'passed': avg_score >= 0.6,
            'score': avg_score,
            'average': f"{avg_score:.1%}"
        }
    
    async def _test_performance(self):
        """Performance budget tests"""
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        total_size = 0
        for html_file in html_files:
            total_size += html_file.stat().st_size
        
        size_kb = total_size / 1024
        budget = self.config['performance_budget']['max_bundle_size_kb']
        
        return {
            'passed': size_kb <= budget,
            'size_kb': round(size_kb, 2),
            'budget_kb': budget,
            'utilization': f"{size_kb/budget:.1%}"
        }
    
    def _test_security(self):
        """Basic security checks"""
        html_files = list(Path(self.app_dir).glob('*.html'))
        
        issues = []
        for html_file in html_files:
            with open(html_file, 'r') as f:
                content = f.read()
            
            # Check for inline event handlers (XSS risk)
            if 'onclick=' in content.lower() or 'onerror=' in content.lower():
                issues.append(f"{html_file.name}: Inline event handlers detected")
            
            # Check for http links (mixed content)
            if 'http://' in content and 'https://' not in content:
                issues.append(f"{html_file.name}: Insecure HTTP links")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'files_checked': len(html_files)
        }
    
    def _generate_report(self, results):
        """Generate comprehensive test report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'commit': self.last_commit,
            'summary': {
                'passed': results['passed'],
                'score': f"{results['score']:.1%}",
                'duration': 'auto'
            },
            'tests': results['tests'],
            'recommendations': self._generate_recommendations(results)
        }
    
    def _generate_recommendations(self, results):
        """Generate actionable recommendations"""
        recommendations = []
        
        for test_name, test_result in results['tests'].items():
            if not test_result.get('passed'):
                if test_name == 'accessibility':
                    recommendations.append("🔧 Add alt text to images and semantic HTML tags")
                elif test_name == 'responsive':
                    recommendations.append("🔧 Add viewport meta tag and media queries")
                elif test_name == 'security':
                    for issue in test_result.get('issues', []):
                        recommendations.append(f"🔒 {issue}")
                elif test_name == 'javascript':
                    recommendations.append("🔧 Fix JavaScript syntax errors before deployment")
        
        return recommendations
    
    def _save_report(self, report):
        """Save report to disk"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"{self.report_dir}/report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    async def _send_report_summary(self, report):
        """Send report summary to Telegram"""
        summary = report['summary']
        
        status = "✅ PASS" if summary['passed'] else "❌ FAIL"
        score = summary['score']
        
        message = f"""🧪 Test Report: {status}

Score: {score}
Commit: {self.last_commit[:8] if self.last_commit else 'N/A'}
Time: {datetime.now().strftime('%H:%M:%S')}

Tests:
"""
        for test_name, test_result in report['tests'].items():
            icon = "✅" if test_result.get('passed') else "❌"
            message += f"{icon} {test_name.title()}\n"
        
        if report.get('recommendations'):
            message += "\n📝 Recommendations:\n"
            for rec in report['recommendations'][:3]:
                message += f"{rec}\n"
        
        # Write to notification file (for external pickup)
        notif_file = f"{self.report_dir}/latest_notification.txt"
        with open(notif_file, 'w') as f:
            f.write(message)
        
        print(message)
        return message
    
    async def _handle_test_failure(self, results):
        """Handle test failure"""
        print("❌ Smoke tests failed - stopping pipeline")
        
        # Generate failure report
        report = self._generate_report(results)
        report_path = self._save_report(report)
        
        # Send alert
        await self._alert_error(f"Tests failed. Report: {report_path}")
        
        # Suggest fixes
        await self._suggest_fixes(report)
    
    async def _suggest_fixes(self, report):
        """Generate fix suggestions"""
        suggestions = []
        
        for test_name, test_result in report['tests'].items():
            if not test_result.get('passed'):
                if 'details' in test_result:
                    for detail in test_result['details']:
                        if not detail.get('passed'):
                            suggestions.append({
                                'file': detail.get('file', 'unknown'),
                                'issue': detail.get('error', 'unknown error'),
                                'suggestion': self._get_fix_suggestion(test_name, detail)
                            })
        
        # Save suggestions
        fix_file = f"{self.report_dir}/fix_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fix_file, 'w') as f:
            json.dump(suggestions, f, indent=2)
        
        print(f"💡 Fix suggestions saved to: {fix_file}")
    
    def _get_fix_suggestion(self, test_type, detail):
        """Get specific fix suggestion based on error"""
        error = str(detail.get('error', '')).lower()
        
        if 'syntax' in error:
            return "Check for missing semicolons, braces, or quotes"
        elif 'brace' in error or 'bracket' in error:
            return "Ensure all opening braces have matching closing braces"
        elif 'alt' in error:
            return "Add alt attributes to all <img> tags"
        else:
            return f"Review {detail.get('file', 'file')} for errors"
    
    async def _deploy_to_staging(self):
        """Deploy to staging environment"""
        print("🚀 Deploying to staging...")
        
        # Copy files to staging
        subprocess.run(['cp', '-r', f'{self.app_dir}/*', self.staging_dir])
        
        # Start staging server
        # (Implementation depends on staging setup)
        
        print(f"✅ Deployed to: {self.staging_dir}")
        await self._alert_success("Deployed to staging successfully")
    
    async def _suggest_deployment(self, report):
        """Suggest deployment to DE"""
        message = f"""📦 Deployment Ready

All tests passed ({report['summary']['score']}).
Ready to deploy to staging.

Run: python3 semi_sovereign_agent.py --deploy
"""
        print(message)
    
    async def _alert_error(self, message):
        """Send error alert"""
        alert = f"🚨 ALERT: {message}"
        print(alert)
        # Could also send to Telegram, email, etc.
    
    async def _alert_success(self, message):
        """Send success alert"""
        alert = f"✅ {message}"
        print(alert)

# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Semi-Sovereign Testing Agent')
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    parser.add_argument('--deploy', action='store_true', help='Deploy to staging')
    parser.add_argument('--report', action='store_true', help='Generate latest report')
    
    args = parser.parse_args()
    
    agent = SemiSovereignAgent()
    
    if args.deploy:
        asyncio.run(agent._deploy_to_staging())
    elif args.report:
        # Generate manual report
        results = asyncio.run(agent._run_full_test_suite())
        report = agent._generate_report(results)
        print(json.dumps(report, indent=2))
    elif args.run_once:
        results = asyncio.run(agent._run_full_test_suite())
        report = agent._generate_report(results)
        print(agent._send_report_summary(report))
    else:
        # Run continuous monitoring
        asyncio.run(agent.run())
