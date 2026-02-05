#!/usr/bin/env python3
"""
Validation Tools for Power BI PBIP Module System
This script provides comprehensive validation for visual modules, performance testing, and accessibility checks.

Usage:
    python validation_tools.py validate-module --file modules/kpi/revenue-card.json
    python validation_tools.py validate-performance --file modules/charts/trend-line.json
    python validation_tools.py validate-accessibility --file modules/layouts/executive-layout.json
    python validation_tools.py validate-all --directory modules/

Author: _[Team/Individual]_
Version: 1.0
Created: _[Date]_
"""

import json
import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validation_tools.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModuleValidator:
    """Class for validating Power BI visual modules."""
    
    def __init__(self):
        """Initialize the Module Validator."""
        self.validation_results = []
        self.error_count = 0
        self.warning_count = 0
        
        # Define validation schemas
        self.required_fields = {
            'module': {
                'name': str,
                'type': str,
                'category': str,
                'description': str,
                'version': str,
                'author': str,
                'created': str,
                'config': dict
            }
        }
        
        # Define valid categories and types
        self.valid_categories = ['kpi', 'charts', 'filters', 'layouts']
        self.valid_types = {
            'kpi': ['card', 'gauge', 'kpi'],
            'charts': ['lineChart', 'columnChart', 'barChart', 'areaChart', 'pieChart', 'donutChart', 'scatterChart', 'map'],
            'filters': ['slicer', 'dropdown', 'list', 'tiles'],
            'layouts': ['layout', 'template']
        }
        
        # Color contrast requirements (WCAG AA)
        self.min_contrast_ratio = 4.5
        self.min_contrast_ratio_large = 3.0
        
        # Performance thresholds
        self.performance_limits = {
            'max_file_size_kb': 100,
            'max_config_depth': 10,
            'max_projections': 20
        }
    
    def validate_module_structure(self, module_data: Dict[str, Any], file_path: str) -> List[Dict[str, str]]:
        """
        Validate the basic structure of a module.
        
        Args:
            module_data (Dict): The module data to validate
            file_path (str): Path to the module file
            
        Returns:
            List[Dict]: List of validation issues
        """
        issues = []
        
        # Check top-level structure
        if 'module' not in module_data:
            issues.append({
                'type': 'error',
                'category': 'structure',
                'message': 'Missing required top-level "module" key',
                'file': file_path
            })
            return issues
        
        module = module_data['module']
        
        # Check required fields
        for field, field_type in self.required_fields['module'].items():
            if field not in module:
                issues.append({
                    'type': 'error',
                    'category': 'structure',
                    'message': f'Missing required field: {field}',
                    'file': file_path
                })
            elif not isinstance(module[field], field_type):
                issues.append({
                    'type': 'error',
                    'category': 'structure',
                    'message': f'Field "{field}" should be of type {field_type.__name__}',
                    'file': file_path
                })
        
        # Validate category and type
        if 'category' in module:
            category = module['category']
            if category not in self.valid_categories:
                issues.append({
                    'type': 'error',
                    'category': 'validation',
                    'message': f'Invalid category: {category}. Must be one of {self.valid_categories}',
                    'file': file_path
                })
            elif 'type' in module:
                module_type = module['type']
                if category in self.valid_types and module_type not in self.valid_types[category]:
                    issues.append({
                        'type': 'warning',
                        'category': 'validation',
                        'message': f'Unexpected type "{module_type}" for category "{category}"',
                        'file': file_path
                    })
        
        # Validate version format
        if 'version' in module:
            version_pattern = r'^\d+\.\d+(\.\d+)?$'
            if not re.match(version_pattern, module['version']):
                issues.append({
                    'type': 'warning',
                    'category': 'validation',
                    'message': 'Version should follow semantic versioning (e.g., 1.0, 1.0.0)',
                    'file': file_path
                })
        
        # Validate date format
        if 'created' in module:
            try:
                datetime.strptime(module['created'], '%Y-%m-%d')
            except ValueError:
                issues.append({
                    'type': 'warning',
                    'category': 'validation',
                    'message': 'Created date should be in YYYY-MM-DD format',
                    'file': file_path
                })
        
        return issues
    
    def validate_config_structure(self, module_data: Dict[str, Any], file_path: str) -> List[Dict[str, str]]:
        """
        Validate the configuration structure of a module.
        
        Args:
            module_data (Dict): The module data to validate
            file_path (str): Path to the module file
            
        Returns:
            List[Dict]: List of validation issues
        """
        issues = []
        
        if 'module' not in module_data or 'config' not in module_data['module']:
            return issues
        
        config = module_data['module']['config']
        
        # Check for required config fields based on module type
        module_type = module_data['module'].get('type', '')
        
        if module_type in ['card', 'gauge', 'kpi']:
            # KPI modules should have specific structure
            if 'visualType' not in config:
                issues.append({
                    'type': 'error',
                    'category': 'config',
                    'message': 'KPI modules must have visualType in config',
                    'file': file_path
                })
            
            if 'activeProjections' not in config:
                issues.append({
                    'type': 'warning',
                    'category': 'config',
                    'message': 'KPI modules should have activeProjections for data binding',
                    'file': file_path
                })
        
        elif module_type in ['lineChart', 'columnChart', 'barChart', 'areaChart']:
            # Chart modules should have axes and data projections
            if 'activeProjections' not in config:
                issues.append({
                    'type': 'error',
                    'category': 'config',
                    'message': 'Chart modules must have activeProjections for data binding',
                    'file': file_path
                })
            else:
                projections = config['activeProjections']
                if module_type in ['lineChart', 'columnChart', 'barChart', 'areaChart']:
                    if 'Category' not in projections and 'X' not in projections:
                        issues.append({
                            'type': 'warning',
                            'category': 'config',
                            'message': 'Chart modules typically need Category or X axis data',
                            'file': file_path
                        })
                    if 'Y' not in projections and 'Values' not in projections:
                        issues.append({
                            'type': 'warning',
                            'category': 'config',
                            'message': 'Chart modules typically need Y axis or Values data',
                            'file': file_path
                        })
        
        elif module_type == 'slicer':
            # Slicer modules should have Values projection
            if 'activeProjections' not in config:
                issues.append({
                    'type': 'error',
                    'category': 'config',
                    'message': 'Slicer modules must have activeProjections for filtering',
                    'file': file_path
                })
            elif 'Values' not in config['activeProjections']:
                issues.append({
                    'type': 'warning',
                    'category': 'config',
                    'message': 'Slicer modules typically need Values for filter data',
                    'file': file_path
                })
        
        # Check positioning information
        if 'positioning' not in config:
            issues.append({
                'type': 'warning',
                'category': 'config',
                'message': 'Module should include positioning information (width, height)',
                'file': file_path
            })
        else:
            positioning = config['positioning']
            required_pos_fields = ['width', 'height']
            for field in required_pos_fields:
                if field not in positioning:
                    issues.append({
                        'type': 'warning',
                        'category': 'config',
                        'message': f'Positioning should include {field}',
                        'file': file_path
                    })
        
        return issues
    
    def validate_accessibility(self, module_data: Dict[str, Any], file_path: str) -> List[Dict[str, str]]:
        """
        Validate accessibility compliance of a module.
        
        Args:
            module_data (Dict): The module data to validate
            file_path (str): Path to the module file
            
        Returns:
            List[Dict]: List of accessibility issues
        """
        issues = []
        
        if 'module' not in module_data:
            return issues
        
        module = module_data['module']
        
        # Check for accessibility section
        if 'accessibility' not in module:
            issues.append({
                'type': 'warning',
                'category': 'accessibility',
                'message': 'Module should include accessibility information',
                'file': file_path
            })
        else:
            accessibility = module['accessibility']
            
            # Check for required accessibility fields
            recommended_fields = ['aria_labels', 'color_blind_safe', 'keyboard_navigation']
            for field in recommended_fields:
                if field not in accessibility or not accessibility[field]:
                    issues.append({
                        'type': 'warning',
                        'category': 'accessibility',
                        'message': f'Accessibility should include {field}',
                        'file': file_path
                    })
        
        # Check color contrast in config
        config = module.get('config', {})
        branding = module.get('organizational_branding', {})
        
        # Extract colors and check contrast
        colors = []
        self._extract_colors(config, colors)
        self._extract_colors(branding, colors)
        
        if colors:
            contrast_issues = self._validate_color_contrast(colors)
            for issue in contrast_issues:
                issues.append({
                    'type': 'warning',
                    'category': 'accessibility',
                    'message': issue,
                    'file': file_path
                })
        
        return issues
    
    def validate_performance(self, module_data: Dict[str, Any], file_path: str) -> List[Dict[str, str]]:
        """
        Validate performance characteristics of a module.
        
        Args:
            module_data (Dict): The module data to validate
            file_path (str): Path to the module file
            
        Returns:
            List[Dict]: List of performance issues
        """
        issues = []
        
        # Check file size
        try:
            file_size_kb = os.path.getsize(file_path) / 1024
            if file_size_kb > self.performance_limits['max_file_size_kb']:
                issues.append({
                    'type': 'warning',
                    'category': 'performance',
                    'message': f'Module file size ({file_size_kb:.1f}KB) exceeds recommended limit ({self.performance_limits["max_file_size_kb"]}KB)',
                    'file': file_path
                })
        except OSError:
            pass
        
        # Check config complexity
        if 'module' in module_data and 'config' in module_data['module']:
            config = module_data['module']['config']
            depth = self._get_dict_depth(config)
            if depth > self.performance_limits['max_config_depth']:
                issues.append({
                    'type': 'warning',
                    'category': 'performance',
                    'message': f'Configuration depth ({depth}) may impact performance',
                    'file': file_path
                })
            
            # Check number of data projections
            if 'activeProjections' in config:
                total_projections = 0
                for key, value in config['activeProjections'].items():
                    if isinstance(value, list):
                        total_projections += len(value)
                    else:
                        total_projections += 1
                
                if total_projections > self.performance_limits['max_projections']:
                    issues.append({
                        'type': 'warning',
                        'category': 'performance',
                        'message': f'High number of data projections ({total_projections}) may impact performance',
                        'file': file_path
                    })
        
        return issues
    
    def validate_naming_convention(self, file_path: str) -> List[Dict[str, str]]:
        """
        Validate file naming conventions.
        
        Args:
            file_path (str): Path to the module file
            
        Returns:
            List[Dict]: List of naming convention issues
        """
        issues = []
        
        filename = os.path.basename(file_path)
        
        # Check file extension
        if not filename.endswith('.json'):
            issues.append({
                'type': 'error',
                'category': 'naming',
                'message': 'Module files should have .json extension',
                'file': file_path
            })
        
        # Check naming pattern (should be lowercase with hyphens)
        name_without_ext = filename.replace('.json', '')
        if not re.match(r'^[a-z0-9-_]+$', name_without_ext):
            issues.append({
                'type': 'warning',
                'category': 'naming',
                'message': 'Module filenames should use lowercase letters, numbers, hyphens, and underscores only',
                'file': file_path
            })
        
        # Check if filename contains template indicator
        if name_without_ext.startswith('_template'):
            issues.append({
                'type': 'info',
                'category': 'naming',
                'message': 'This appears to be a template file',
                'file': file_path
            })
        
        return issues
    
    def validate_module_file(self, file_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive validation of a module file.
        
        Args:
            file_path (str): Path to the module file
            
        Returns:
            Dict: Validation results
        """
        results = {
            'file': file_path,
            'valid': True,
            'issues': [],
            'summary': {
                'errors': 0,
                'warnings': 0,
                'info': 0
            }
        }
        
        try:
            # Load and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
        
        except json.JSONDecodeError as e:
            results['valid'] = False
            results['issues'].append({
                'type': 'error',
                'category': 'json',
                'message': f'Invalid JSON: {str(e)}',
                'file': file_path
            })
            return results
        
        except FileNotFoundError:
            results['valid'] = False
            results['issues'].append({
                'type': 'error',
                'category': 'file',
                'message': 'File not found',
                'file': file_path
            })
            return results
        
        # Perform all validations
        validation_functions = [
            self.validate_module_structure,
            self.validate_config_structure,
            self.validate_accessibility,
            self.validate_performance,
            self.validate_naming_convention
        ]
        
        for validation_func in validation_functions:
            try:
                if validation_func == self.validate_naming_convention:
                    issues = validation_func(file_path)
                else:
                    issues = validation_func(module_data, file_path)
                results['issues'].extend(issues)
            except Exception as e:
                logger.error(f"Error in validation function {validation_func.__name__}: {str(e)}")
        
        # Calculate summary
        for issue in results['issues']:
            issue_type = issue['type']
            results['summary'][issue_type] = results['summary'].get(issue_type, 0) + 1
            if issue_type == 'error':
                results['valid'] = False
        
        return results
    
    def validate_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Validate all modules in a directory.
        
        Args:
            directory_path (str): Path to the directory containing modules
            
        Returns:
            Dict: Overall validation results
        """
        results = {
            'directory': directory_path,
            'files_validated': 0,
            'files_passed': 0,
            'files_failed': 0,
            'total_issues': 0,
            'file_results': []
        }
        
        # Walk through directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.json') and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    
                    file_result = self.validate_module_file(file_path)
                    results['file_results'].append(file_result)
                    results['files_validated'] += 1
                    results['total_issues'] += len(file_result['issues'])
                    
                    if file_result['valid']:
                        results['files_passed'] += 1
                    else:
                        results['files_failed'] += 1
        
        return results
    
    def _extract_colors(self, obj: Any, colors: List[str]):
        """Extract color values from a nested object."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and (key.lower().find('color') != -1 or value.startswith('#')):
                    if value.startswith('#') and len(value) in [4, 7]:
                        colors.append(value)
                elif isinstance(value, (dict, list)):
                    self._extract_colors(value, colors)
        elif isinstance(obj, list):
            for item in obj:
                self._extract_colors(item, colors)
    
    def _validate_color_contrast(self, colors: List[str]) -> List[str]:
        """Validate color contrast ratios."""
        issues = []
        
        # Simple contrast validation (would need more sophisticated implementation for production)
        for color in colors:
            if color.lower() in ['#ffffff', '#fff']:
                issues.append(f"White background may have contrast issues with light text colors")
            elif color.lower() in ['#000000', '#000']:
                issues.append(f"Black background may have contrast issues with dark text colors")
        
        return issues
    
    def _get_dict_depth(self, d: Dict, depth: int = 0) -> int:
        """Calculate the maximum depth of a nested dictionary."""
        if not isinstance(d, dict) or not d:
            return depth
        
        return max(self._get_dict_depth(v, depth + 1) if isinstance(v, dict) else depth + 1 
                  for v in d.values())
    
    def generate_report(self, validation_results: Dict[str, Any], output_file: str = None) -> str:
        """
        Generate a comprehensive validation report.
        
        Args:
            validation_results (Dict): Results from validation
            output_file (str): Optional output file path
            
        Returns:
            str: Report content
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'directory' in validation_results:
            # Directory validation report
            report_lines = [
                "# Module Validation Report",
                f"Generated: {timestamp}",
                f"Directory: {validation_results['directory']}",
                "",
                "## Summary",
                f"- Files Validated: {validation_results['files_validated']}",
                f"- Files Passed: {validation_results['files_passed']}",
                f"- Files Failed: {validation_results['files_failed']}",
                f"- Total Issues: {validation_results['total_issues']}",
                ""
            ]
            
            if validation_results['file_results']:
                report_lines.extend([
                    "## File Details",
                    ""
                ])
                
                for file_result in validation_results['file_results']:
                    status = "✅ PASS" if file_result['valid'] else "❌ FAIL"
                    report_lines.append(f"### {os.path.basename(file_result['file'])} {status}")
                    
                    if file_result['issues']:
                        for issue in file_result['issues']:
                            icon = "🔴" if issue['type'] == 'error' else "🟡" if issue['type'] == 'warning' else "ℹ️"
                            report_lines.append(f"- {icon} [{issue['category']}] {issue['message']}")
                        report_lines.append("")
        
        else:
            # Single file validation report
            report_lines = [
                "# Module Validation Report",
                f"Generated: {timestamp}",
                f"File: {validation_results['file']}",
                "",
                "## Summary",
                f"- Valid: {'Yes' if validation_results['valid'] else 'No'}",
                f"- Errors: {validation_results['summary']['errors']}",
                f"- Warnings: {validation_results['summary']['warnings']}",
                f"- Info: {validation_results['summary']['info']}",
                ""
            ]
            
            if validation_results['issues']:
                report_lines.extend([
                    "## Issues",
                    ""
                ])
                
                for issue in validation_results['issues']:
                    icon = "🔴" if issue['type'] == 'error' else "🟡" if issue['type'] == 'warning' else "ℹ️"
                    report_lines.append(f"- {icon} **{issue['category'].title()}**: {issue['message']}")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                logger.info(f"Validation report saved to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving report: {str(e)}")
        
        return report_content

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(description='Validation Tools for Power BI PBIP Module System')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate module command
    module_parser = subparsers.add_parser('validate-module', help='Validate a single module file')
    module_parser.add_argument('--file', required=True, help='Module file to validate')
    module_parser.add_argument('--report', help='Output file for validation report')
    
    # Validate performance command
    perf_parser = subparsers.add_parser('validate-performance', help='Validate module performance')
    perf_parser.add_argument('--file', required=True, help='Module file to validate')
    
    # Validate accessibility command
    access_parser = subparsers.add_parser('validate-accessibility', help='Validate module accessibility')
    access_parser.add_argument('--file', required=True, help='Module file to validate')
    
    # Validate all command
    all_parser = subparsers.add_parser('validate-all', help='Validate all modules in directory')
    all_parser.add_argument('--directory', required=True, help='Directory containing modules')
    all_parser.add_argument('--report', help='Output file for validation report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize validator
    validator = ModuleValidator()
    
    # Execute command
    if args.command == 'validate-module':
        results = validator.validate_module_file(args.file)
        
        if args.report:
            validator.generate_report(results, args.report)
        else:
            print(validator.generate_report(results))
        
        sys.exit(0 if results['valid'] else 1)
    
    elif args.command == 'validate-performance':
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
            
            issues = validator.validate_performance(module_data, args.file)
            
            if issues:
                print(f"Performance issues found in {args.file}:")
                for issue in issues:
                    print(f"- {issue['message']}")
                sys.exit(1)
            else:
                print(f"No performance issues found in {args.file}")
                sys.exit(0)
                
        except Exception as e:
            logger.error(f"Error validating performance: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'validate-accessibility':
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
            
            issues = validator.validate_accessibility(module_data, args.file)
            
            if issues:
                print(f"Accessibility issues found in {args.file}:")
                for issue in issues:
                    print(f"- {issue['message']}")
                sys.exit(1)
            else:
                print(f"No accessibility issues found in {args.file}")
                sys.exit(0)
                
        except Exception as e:
            logger.error(f"Error validating accessibility: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'validate-all':
        results = validator.validate_directory(args.directory)
        
        if args.report:
            validator.generate_report(results, args.report)
        else:
            print(validator.generate_report(results))
        
        print(f"\nValidation Summary:")
        print(f"Files Validated: {results['files_validated']}")
        print(f"Files Passed: {results['files_passed']}")
        print(f"Files Failed: {results['files_failed']}")
        
        sys.exit(0 if results['files_failed'] == 0 else 1)

if __name__ == '__main__':
    main()
