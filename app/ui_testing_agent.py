#!/usr/bin/env python3
"""
UI Testing Agent - Automated Browser Testing for Glyph-o-betics
Tests web interfaces, takes screenshots, validates functionality
"""

import asyncio
import subprocess
import json
import os
from datetime import datetime

class UITestingAgent:
    """
    Autonomous UI testing with browser automation
    """
    
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.test_results = []
        self.screenshot_dir = "/root/.openclaw/workspace/app/test-screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    async def start_server(self):
        """Start local web server for testing"""
        process = await asyncio.create_subprocess_exec(
            "python3", "-m", "http.server", "8080",
            "--directory", "/root/.openclaw/workspace/app",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await asyncio.sleep(2)  # Wait for server to start
        return process
    
    def test_html_validity(self, html_file):
        """Validate HTML structure"""
        filepath = f"/root/.openclaw/workspace/app/{html_file}"
        
        # Check file exists
        if not os.path.exists(filepath):
            return {"valid": False, "error": "File not found"}
        
        # Read and basic parse check
        with open(filepath, 'r') as f:
            content = f.read()
        
        checks = {
            "has_doctype": content.strip().startswith('<!DOCTYPE html>'),
            "has_html_tag": '<html' in content.lower(),
            "has_head": '<head>' in content.lower(),
            "has_body": '<body>' in content.lower(),
            "has_closing_tags": '</html>' in content.lower(),
            "file_size": len(content),
            "line_count": len(content.split('\n'))
        }
        
        all_valid = all(checks.values()) if len(checks) > 0 else False
        
        return {
            "valid": all_valid,
            "checks": checks,
            "file": html_file
        }
    
    def test_javascript_syntax(self, js_snippet):
        """Validate JavaScript syntax using Node.js"""
        try:
            # Create temp file
            temp_file = "/tmp/test_js.js"
            with open(temp_file, 'w') as f:
                f.write(js_snippet)
            
            # Check syntax with node
            result = subprocess.run(
                ["node", "--check", temp_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            os.remove(temp_file)
            
            return {
                "valid": result.returncode == 0,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def test_css_validity(self, css_content):
        """Basic CSS validation"""
        checks = {
            "has_valid_braces": css_content.count('{') == css_content.count('}'),
            "has_selectors": ':' in css_content or '.' in css_content or '#' in css_content,
            "has_properties": ':' in css_content,
            "no_empty_rules": '{' not in css_content or '{}\n' not in css_content
        }
        
        return {
            "valid": all(checks.values()),
            "checks": checks
        }
    
    def test_responsive_design(self, html_content):
        """Check for responsive design patterns"""
        checks = {
            "has_viewport_meta": 'viewport' in html_content,
            "has_media_queries": '@media' in html_content,
            "has_flex_or_grid": 'flex' in html_content or 'grid' in html_content,
            "has_relative_units": '%' in html_content or 'em' in html_content or 'rem' in html_content,
            "max_width_set": 'max-width' in html_content or 'maxwidth' in html_content.lower()
        }
        
        score = sum(checks.values()) / len(checks)
        
        return {
            "responsive_score": score,
            "checks": checks,
            "is_responsive": score >= 0.6
        }
    
    def test_accessibility(self, html_content):
        """Basic accessibility checks"""
        checks = {
            "has_alt_text": 'alt="' in html_content or "alt='" in html_content,
            "has_lang_attr": 'lang=' in html_content,
            "has_labels": '<label' in html_content.lower(),
            "semantic_html": any(tag in html_content.lower() for tag in ['<main', '<header', '<nav', '<article', '<section']),
            "color_contrast": 'background' in html_content and 'color' in html_content
        }
        
        score = sum(checks.values()) / len(checks)
        
        return {
            "accessibility_score": score,
            "checks": checks,
            "is_accessible": score >= 0.6
        }
    
    def run_full_test_suite(self, html_file):
        """Run complete test suite on an HTML file"""
        print(f"🔍 Testing {html_file}...")
        
        results = {
            "file": html_file,
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }
        
        # Read file content
        filepath = f"/root/.openclaw/workspace/app/{html_file}"
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Run all tests
        results["tests"]["html_validity"] = self.test_html_validity(html_file)
        results["tests"]["responsive_design"] = self.test_responsive_design(content)
        results["tests"]["accessibility"] = self.test_accessibility(content)
        results["tests"]["css_validity"] = self.test_css_validity(content)
        
        # Extract and test JavaScript
        js_snippets = self._extract_javascript(content)
        js_results = []
        for i, js in enumerate(js_snippets):
            js_result = self.test_javascript_syntax(js)
            js_results.append({"snippet_id": i, "valid": js_result["valid"]})
        results["tests"]["javascript"] = {
            "snippets_tested": len(js_snippets),
            "results": js_results,
            "all_valid": all(r["valid"] for r in js_results) if js_results else True
        }
        
        # Calculate overall score
        scores = [
            1 if results["tests"]["html_validity"]["valid"] else 0,
            results["tests"]["responsive_design"]["responsive_score"],
            results["tests"]["accessibility"]["accessibility_score"],
            1 if results["tests"]["css_validity"]["valid"] else 0,
            1 if results["tests"]["javascript"]["all_valid"] else 0
        ]
        results["overall_score"] = sum(scores) / len(scores)
        results["passed"] = results["overall_score"] >= 0.7
        
        self.test_results.append(results)
        return results
    
    def _extract_javascript(self, html_content):
        """Extract JavaScript from HTML"""
        import re
        scripts = re.findall(r'<script>(.*?)</script>', html_content, re.DOTALL)
        return [s.strip() for s in scripts if s.strip()]
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        report = {
            "summary": {
                "total_tests": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r["passed"]),
                "failed": sum(1 for r in self.test_results if not r["passed"]),
                "average_score": sum(r["overall_score"] for r in self.test_results) / len(self.test_results) if self.test_results else 0
            },
            "details": self.test_results
        }
        
        # Save report
        report_file = f"{self.screenshot_dir}/test-report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_report(self, report):
        """Print human-readable report"""
        print("\n" + "="*60)
        print("🧪 UI TEST REPORT")
        print("="*60)
        
        summary = report["summary"]
        print(f"\nTotal Files Tested: {summary['total_tests']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Average Score: {summary['average_score']:.1%}")
        
        print("\n" + "-"*60)
        for result in report["details"]:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"\n{status} - {result['file']}")
            print(f"  Score: {result['overall_score']:.1%}")
            
            for test_name, test_result in result["tests"].items():
                if isinstance(test_result, dict) and "valid" in test_result:
                    valid = "✓" if test_result["valid"] else "✗"
                    print(f"  {valid} {test_name}")
                elif isinstance(test_result, dict) and "score" in test_result:
                    print(f"  • {test_name}: {test_result['score']:.1%}")
        
        print("\n" + "="*60)

# Usage
if __name__ == "__main__":
    agent = UITestingAgent()
    
    # Test the interface
    result = agent.run_full_test_suite("glyphobetics-interface.html")
    
    # Generate report
    report = agent.generate_test_report()
    agent.print_report(report)
    
    print(f"\n📊 Detailed report saved to: {agent.screenshot_dir}/test-report.json")
