#!/usr/bin/env python3
"""
Validation script to check if code follows the Copilot Guidelines.
This script demonstrates the practical application of the guidelines.
"""

import ast
import os
import sys
from typing import List, Dict, Any


class GuidelinesValidator:
    """Validates code against the established Copilot Guidelines."""
    
    def __init__(self):
        self.issues: List[str] = []
    
    def validate_python_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a Python file against guidelines."""
        results = {
            "file": file_path,
            "passed": True,
            "issues": [],
            "educational_compliance": True
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Check for educational compliance keywords
            educational_indicators = [
                'educational', 'simulation', 'disclaimer', 'virtual', 
                'learning', 'compliance', 'educational_only'
            ]
            
            has_educational_context = any(
                indicator in content.lower() 
                for indicator in educational_indicators
            )
            
            if not has_educational_context and 'educational' in file_path.lower():
                results["issues"].append("Missing educational context indicators")
                results["educational_compliance"] = False
            
            # Check for prohibited real trading keywords
            prohibited_keywords = [
                'real_money', 'live_trading', 'actual_api', 'production_trading',
                'withdrawal', 'deposit', 'payment'
            ]
            
            for keyword in prohibited_keywords:
                if keyword in content.lower():
                    results["issues"].append(f"Prohibited keyword found: {keyword}")
                    results["educational_compliance"] = False
                    results["passed"] = False
            
            # Check for proper error handling patterns
            has_try_except = 'try:' in content and 'except' in content
            if len(content) > 500 and not has_try_except:  # Only for substantial files
                results["issues"].append("Consider adding error handling (try/except blocks)")
            
            # Check for docstrings in classes and functions
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        results["issues"].append(
                            f"Missing docstring for {node.__class__.__name__.lower()}: {node.name}"
                        )
            
        except Exception as e:
            results["issues"].append(f"Error parsing file: {e}")
            results["passed"] = False
        
        if results["issues"]:
            results["passed"] = False
        
        return results
    
    def validate_repository(self, src_path: str = "src") -> Dict[str, Any]:
        """Validate the entire repository against guidelines."""
        results = {
            "total_files": 0,
            "passed_files": 0,
            "educational_compliant": 0,
            "files": []
        }
        
        for root, dirs, files in os.walk(src_path):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_results = self.validate_python_file(file_path)
                    
                    results["files"].append(file_results)
                    results["total_files"] += 1
                    
                    if file_results["passed"]:
                        results["passed_files"] += 1
                    
                    if file_results["educational_compliance"]:
                        results["educational_compliant"] += 1
        
        return results


def main():
    """Run guidelines validation on the repository."""
    print("🔍 Validating repository against Copilot Guidelines")
    print("=" * 50)
    
    validator = GuidelinesValidator()
    results = validator.validate_repository()
    
    # Print summary
    print(f"📊 Validation Summary:")
    print(f"   Total Python files: {results['total_files']}")
    print(f"   Files passing guidelines: {results['passed_files']}")
    print(f"   Educational compliance: {results['educational_compliant']}")
    
    if results["total_files"] > 0:
        pass_rate = (results["passed_files"] / results["total_files"]) * 100
        compliance_rate = (results["educational_compliant"] / results["total_files"]) * 100
        
        print(f"   Pass rate: {pass_rate:.1f}%")
        print(f"   Educational compliance rate: {compliance_rate:.1f}%")
    
    print("\n📋 Detailed Results:")
    for file_result in results["files"]:
        status = "✅" if file_result["passed"] else "❌"
        compliance = "🎓" if file_result["educational_compliance"] else "⚠️"
        
        print(f"   {status} {compliance} {file_result['file']}")
        
        for issue in file_result["issues"]:
            print(f"      • {issue}")
    
    print("\n" + "=" * 50)
    print("💡 Guidelines validation complete!")
    print("   Review the Copilot Guidelines in copilot-guidelines.md for details.")
    
    return 0 if results["passed_files"] == results["total_files"] else 1


if __name__ == "__main__":
    sys.exit(main())