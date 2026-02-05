#!/usr/bin/env python3
"""
Enhanced Power BI PBIP Validation Tools

Validates common mistakes found in Power BI report definitions for both Sales and Healthcare domains:
- Incorrect aggregations (Avg vs Sum for price/margin fields, DISTINCTCOUNT for patient counts)
- Missing percentage formatting
- Missing display units
- Interaction behavior issues
- Healthcare-specific validation (DateTime modeling, SLA thresholds, HIPAA compliance)

Supports both Adidas sales dashboard and Hospital ER dashboard patterns.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Sales domain field patterns
AVG_REQUIRED_PATTERNS = [
    r".*price.*per.*unit.*",
    r".*operating.*margin.*",
    r".*profit.*margin.*", 
    r".*avg.*price.*",
    r".*average.*price.*",
    r".*unit.*price.*",
    r".*margin.*"
]

PERCENT_REQUIRED_PATTERNS = [
    r".*margin.*",
    r".*percentage.*",
    r".*rate.*",
    r".*ratio.*",
    r".*compliance.*"  # Added for healthcare
]

CURRENCY_PATTERNS = [
    r".*sales.*",
    r".*revenue.*",
    r".*profit.*",
    r".*cost.*",
    r".*price.*"
]

# Healthcare domain field patterns
PATIENT_COUNT_PATTERNS = [
    r".*patient.*id.*",
    r".*patient.*count.*",
    r".*number.*patients.*",
    r".*patient.*visits.*"
]

TIME_FIELD_PATTERNS = [
    r".*wait.*time.*",
    r".*admission.*time.*",
    r".*service.*time.*",
    r".*response.*time.*"
]

DATETIME_PATTERNS = [
    r".*datetime.*",
    r".*timestamp.*",
    r".*admission.*date.*time.*"
]

SLA_THRESHOLD_PATTERNS = [
    r".*sla.*",
    r".*30.*min.*",
    r".*seen.*within.*"
]

@dataclass
class ValidationIssue:
    """Represents a validation issue found in the PBIP project"""
    file_path: Path
    issue_type: str
    field_name: str
    current_value: str
    expected_value: str
    severity: str  # error, warning, info
    description: str

class PBIPValidator:
    """Validates Power BI PBIP project files for common mistakes"""
    
    def __init__(self):
        self.issues: List[ValidationIssue] = []
        
    def validate_project(self, project_root: Path, domain: str = "generic") -> List[ValidationIssue]:
        """Validate Power BI project with domain-specific rules"""
        self.issues = []
        self.domain = domain
        
        print(f"🔍 Validating {domain} Power BI project: {project_root}")
        
        # Find and validate reports
        report_paths = list(project_root.rglob("*.Report"))
        for report_path in report_paths:
            self._validate_report_definition(report_path)
            
        # Find and validate semantic model
        model_paths = list(project_root.rglob("*.SemanticModel"))
        for model_path in model_paths:
            self._validate_semantic_model(model_path)
            
        # Domain-specific validation
        if domain == "healthcare":
            self._validate_healthcare_requirements(project_root)
        elif domain == "sales":
            self._validate_sales_requirements(project_root)
            
        return self.issues
        
    def _validate_report_definition(self, report_path: Path):
        """Validate report definition files"""
        definition_path = report_path / "definition"
        if not definition_path.exists():
            return
            
        # Validate report.json
        report_json = definition_path / "report.json"
        if report_json.exists():
            self._validate_json_file(report_json, "report")
            
        # Validate all JSON files in subdirectories
        for json_file in definition_path.rglob("*.json"):
            if json_file.name != "report.json":
                self._validate_json_file(json_file, "visual")
                
    def _validate_semantic_model(self, model_path: Path):
        """Validate semantic model TMDL files"""
        definition_path = model_path / "definition"
        if not definition_path.exists():
            return
            
        # Validate measures
        measures_path = definition_path / "measures"
        if measures_path.exists():
            for tmdl_file in measures_path.rglob("*.tmdl"):
                self._validate_tmdl_file(tmdl_file)
                
    def _validate_json_file(self, json_path: Path, file_type: str):
        """Validate a JSON file for common issues"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self._scan_for_aggregation_issues(data, json_path)
            self._scan_for_formatting_issues(data, json_path)
            self._scan_for_interaction_issues(data, json_path)
            
        except Exception as e:
            self.issues.append(ValidationIssue(
                file_path=json_path,
                issue_type="parsing_error",
                field_name="",
                current_value="",
                expected_value="",
                severity="error",
                description=f"Failed to parse JSON: {str(e)}"
            ))
            
    def _validate_tmdl_file(self, tmdl_path: Path):
        """Validate TMDL files for measure definitions"""
        try:
            content = tmdl_path.read_text(encoding='utf-8')
            self._scan_tmdl_content(content, tmdl_path)
        except Exception as e:
            self.issues.append(ValidationIssue(
                file_path=tmdl_path,
                issue_type="parsing_error", 
                field_name="",
                current_value="",
                expected_value="",
                severity="error",
                description=f"Failed to parse TMDL: {str(e)}"
            ))
            
    def _scan_for_aggregation_issues(self, obj: Any, file_path: Path, parent_key: str = ""):
        """Scan for incorrect aggregation settings"""
        if isinstance(obj, dict):
            # Look for field definitions
            field_name = obj.get("displayName") or obj.get("name") or obj.get("queryName") or parent_key
            aggregation = obj.get("aggregation") or obj.get("aggregate")
            
            if field_name and aggregation:
                field_name_lower = str(field_name).lower()
                
                # Check if field should use AVERAGE aggregation
                for pattern in AVG_REQUIRED_PATTERNS:
                    if re.match(pattern, field_name_lower, re.IGNORECASE):
                        if str(aggregation).lower() in ["sum", "total", "count"]:
                            self.issues.append(ValidationIssue(
                                file_path=file_path,
                                issue_type="aggregation_error",
                                field_name=field_name,
                                current_value=str(aggregation),
                                expected_value="Average",
                                severity="error",
                                description=f"Field '{field_name}' should use AVERAGE aggregation, not {aggregation}. Unit prices and margins should be averaged across transactions."
                            ))
                            
            # Recurse into nested objects
            for key, value in obj.items():
                self._scan_for_aggregation_issues(value, file_path, key)
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._scan_for_aggregation_issues(item, file_path, f"{parent_key}[{i}]")
                
    def _scan_for_formatting_issues(self, obj: Any, file_path: Path, parent_key: str = ""):
        """Scan for incorrect formatting settings"""
        if isinstance(obj, dict):
            field_name = obj.get("displayName") or obj.get("name") or obj.get("queryName") or parent_key
            format_string = obj.get("formatString") or obj.get("format")
            
            if field_name and format_string:
                field_name_lower = str(field_name).lower()
                format_str = str(format_string)
                
                # Check percentage formatting
                for pattern in PERCENT_REQUIRED_PATTERNS:
                    if re.match(pattern, field_name_lower, re.IGNORECASE):
                        if "%" not in format_str:
                            self.issues.append(ValidationIssue(
                                file_path=file_path,
                                issue_type="format_error",
                                field_name=field_name,
                                current_value=format_str,
                                expected_value="Percentage format (e.g., '0%')",
                                severity="error",
                                description=f"Field '{field_name}' should use percentage formatting. Current format: '{format_str}'"
                            ))
                            
                # Check currency formatting
                for pattern in CURRENCY_PATTERNS:
                    if re.match(pattern, field_name_lower, re.IGNORECASE):
                        if "$" not in format_str and "currency" not in format_str.lower():
                            self.issues.append(ValidationIssue(
                                file_path=file_path,
                                issue_type="format_warning",
                                field_name=field_name,
                                current_value=format_str,
                                expected_value="Currency format (e.g., '$#,0')",
                                severity="warning",
                                description=f"Field '{field_name}' might need currency formatting. Current format: '{format_str}'"
                            ))
                            
            # Check for display units
            display_units = obj.get("displayUnits") or obj.get("units")
            if field_name and not display_units:
                field_name_lower = str(field_name).lower()
                if any(re.match(pattern, field_name_lower, re.IGNORECASE) for pattern in CURRENCY_PATTERNS):
                    if "sales" in field_name_lower or "revenue" in field_name_lower:
                        self.issues.append(ValidationIssue(
                            file_path=file_path,
                            issue_type="display_units_warning",
                            field_name=field_name,
                            current_value="None",
                            expected_value="Millions or Thousands",
                            severity="warning",
                            description=f"Large currency field '{field_name}' should consider display units (Millions/Thousands)"
                        ))
                        
            # Recurse into nested objects
            for key, value in obj.items():
                self._scan_for_formatting_issues(value, file_path, key)
                
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._scan_for_formatting_issues(item, file_path, f"{parent_key}[{i}]")
                
    def _scan_for_interaction_issues(self, obj: Any, file_path: Path):
        """Scan for interaction behavior issues"""
        if isinstance(obj, dict):
            # Look for interaction settings
            interactions = obj.get("interactions") or obj.get("crossFilteringBehavior")
            
            if interactions:
                if isinstance(interactions, str) and interactions.lower() == "highlight":
                    self.issues.append(ValidationIssue(
                        file_path=file_path,
                        issue_type="interaction_warning",
                        field_name="",
                        current_value="highlight",
                        expected_value="filter",
                        severity="warning",
                        description="Consider using 'filter' instead of 'highlight' for better drill-down analysis"
                    ))
                    
            # Recurse into nested objects
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    self._scan_for_interaction_issues(value, file_path)
                    
        elif isinstance(obj, list):
            for item in obj:
                self._scan_for_interaction_issues(item, file_path)
                
    def _scan_tmdl_content(self, content: str, file_path: Path):
        """Scan TMDL content for measure definition issues"""
        lines = content.split('\n')
        current_measure = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Track current measure
            if line.startswith('measure '):
                current_measure = line.replace('measure ', '').replace(' =', '').strip()
                
            # Check for aggregation functions
            if current_measure and ('SUM(' in line or 'AVERAGE(' in line):
                measure_name_lower = current_measure.lower()
                
                # Check if measure should use AVERAGE
                for pattern in AVG_REQUIRED_PATTERNS:
                    if re.match(pattern, measure_name_lower, re.IGNORECASE):
                        if 'SUM(' in line:
                            self.issues.append(ValidationIssue(
                                file_path=file_path,
                                issue_type="dax_aggregation_error",
                                field_name=current_measure,
                                current_value="SUM()",
                                expected_value="AVERAGE()",
                                severity="error",
                                description=f"Measure '{current_measure}' uses SUM() but should use AVERAGE() for unit prices/margins"
                            ))
                            
    def generate_report(self) -> str:
        """Generate a validation report"""
        if not self.issues:
            return "✅ VALIDATION PASSED - No issues found!"
            
        report = ["🔍 POWER BI PBIP VALIDATION REPORT", "=" * 50, ""]
        
        # Group by severity
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        info = [i for i in self.issues if i.severity == "info"]
        
        # Summary
        report.append(f"Total Issues Found: {len(self.issues)}")
        report.append(f"  Errors: {len(errors)}")
        report.append(f"  Warnings: {len(warnings)}")
        report.append(f"  Info: {len(info)}")
        report.append("")
        
        # Detailed issues
        for severity, issues in [("ERRORS", errors), ("WARNINGS", warnings), ("INFO", info)]:
            if issues:
                report.append(f"{severity}:")
                report.append("-" * len(severity))
                for issue in issues:
                    report.append(f"📁 {issue.file_path.name}")
                    report.append(f"   Field: {issue.field_name}")
                    report.append(f"   Issue: {issue.description}")
                    if issue.current_value:
                        report.append(f"   Current: {issue.current_value}")
                    if issue.expected_value:
                        report.append(f"   Expected: {issue.expected_value}")
                    report.append("")
                    
        return "\n".join(report)


    def _validate_healthcare_requirements(self, project_root: Path):
        """Validate healthcare-specific requirements"""
        print("🏥 Running healthcare-specific validation...")
        
        # Check for calendar table requirement
        self._check_calendar_table(project_root)
        
        # Check for DateTime modeling issues
        self._check_datetime_modeling(project_root)
        
        # Check patient count aggregations
        self._check_patient_count_aggregations(project_root)
        
        # Check SLA threshold parameterization
        self._check_sla_parameterization(project_root)
        
        # Check HIPAA compliance notes
        self._check_hipaa_compliance(project_root)
        
    def _validate_sales_requirements(self, project_root: Path):
        """Validate sales-specific requirements"""
        print("💼 Running sales-specific validation...")
        
        # Existing sales validation logic
        pass
        
    def _check_calendar_table(self, project_root: Path):
        """Check if calendar table exists and is properly modeled"""
        model_paths = list(project_root.rglob("*.SemanticModel"))
        for model_path in model_paths:
            model_tmdl = model_path / "definition" / "model.tmdl"
            if model_tmdl.exists():
                with open(model_tmdl, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    
                if 'calendar' not in content and 'date' not in content:
                    self.issues.append(ValidationIssue(
                        file_path=model_tmdl,
                        issue_type="healthcare_calendar_table",
                        severity="error",
                        description="Healthcare analytics require a calendar table for time intelligence",
                        suggestion="Create a calendar table and establish relationships to fact tables"
                    ))
                    
    def _check_datetime_modeling(self, project_root: Path):
        """Check for improper DateTime field usage in relationships"""
        model_paths = list(project_root.rglob("*.SemanticModel"))
        for model_path in model_paths:
            relationships_path = model_path / "definition" / "relationships"
            if relationships_path.exists():
                for rel_file in relationships_path.rglob("*.tmdl"):
                    with open(rel_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                    for pattern in DATETIME_PATTERNS:
                        if re.search(pattern, content):
                            self.issues.append(ValidationIssue(
                                file_path=rel_file,
                                issue_type="healthcare_datetime_modeling",
                                severity="error",
                                description=f"DateTime field detected in relationship - should be split into Date and Time",
                                suggestion="Split DateTime columns into separate Date and Time fields for proper modeling"
                            ))
                            
    def _check_patient_count_aggregations(self, project_root: Path):
        """Check that patient counts use DISTINCTCOUNT aggregation"""
        model_paths = list(project_root.rglob("*.SemanticModel"))
        for model_path in model_paths:
            measures_path = model_path / "definition" / "measures"
            if measures_path.exists():
                for measure_file in measures_path.rglob("*.tmdl"):
                    with open(measure_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for patient count measures
                    for pattern in PATIENT_COUNT_PATTERNS:
                        if re.search(pattern, content.lower()):
                            if 'DISTINCTCOUNT' not in content and 'COUNT' in content:
                                self.issues.append(ValidationIssue(
                                    file_path=measure_file,
                                    issue_type="healthcare_patient_count",
                                    severity="error",
                                    description="Patient count measures must use DISTINCTCOUNT to avoid double-counting",
                                    suggestion="Replace COUNT/COUNTROWS with DISTINCTCOUNT for patient ID fields"
                                ))
                                
    def _check_sla_parameterization(self, project_root: Path):
        """Check that SLA thresholds are parameterized, not hard-coded"""
        model_paths = list(project_root.rglob("*.SemanticModel"))
        for model_path in model_paths:
            measures_path = model_path / "definition" / "measures"
            if measures_path.exists():
                for measure_file in measures_path.rglob("*.tmdl"):
                    with open(measure_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for hard-coded SLA values
                    hardcoded_patterns = [r'<= 30', r'>= 30', r'= 30', r'< 30', r'> 30']
                    for pattern in hardcoded_patterns:
                        if re.search(pattern, content) and any(re.search(sla_pattern, content.lower()) for sla_pattern in SLA_THRESHOLD_PATTERNS):
                            self.issues.append(ValidationIssue(
                                file_path=measure_file,
                                issue_type="healthcare_sla_parameterization",
                                severity="warning",
                                description="SLA thresholds should be parameterized, not hard-coded",
                                suggestion="Create parameters for SLA thresholds to allow flexibility across departments"
                            ))
                            
    def _check_hipaa_compliance(self, project_root: Path):
        """Check for HIPAA compliance notes in patient details dashboards"""
        report_paths = list(project_root.rglob("*.Report"))
        for report_path in report_paths:
            definition_path = report_path / "definition"
            if definition_path.exists():
                for json_file in definition_path.rglob("*.json"):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                    if 'patient' in content and 'details' in content:
                        # Check if compliance notes exist
                        if 'hipaa' not in content and 'privacy' not in content and 'rls' not in content:
                            self.issues.append(ValidationIssue(
                                file_path=json_file,
                                issue_type="healthcare_hipaa_compliance",
                                severity="critical",
                                description="Patient Details dashboard requires HIPAA compliance documentation",
                                suggestion="Add RLS implementation and audit logging documentation for patient data access"
                            ))

def main():
    """Command-line interface for validation"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Power BI PBIP project files")
    parser.add_argument("project_path", help="Path to PBIP project root directory")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--severity", choices=["error", "warning", "info"], default="warning", help="Minimum severity level")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path).resolve()
    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        sys.exit(1)
        
    # Run validation
    validator = PBIPValidator()
    issues = validator.validate_project(project_path)
    
    # Filter by severity
    severity_order = {"info": 0, "warning": 1, "error": 2}
    min_severity = severity_order[args.severity]
    filtered_issues = [i for i in issues if severity_order[i.severity] >= min_severity]
    
    # Output results
    if args.format == "json":
        import json
        output = {
            "project_path": str(project_path),
            "total_issues": len(filtered_issues),
            "issues": [
                {
                    "file": str(i.file_path),
                    "type": i.issue_type,
                    "field": i.field_name,
                    "severity": i.severity,
                    "description": i.description,
                    "current": i.current_value,
                    "expected": i.expected_value
                }
                for i in filtered_issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        validator.issues = filtered_issues
        print(validator.generate_report())
        
    # Exit with error code if errors found
    error_count = len([i for i in filtered_issues if i.severity == "error"])
    sys.exit(error_count)


if __name__ == "__main__":
    main()
