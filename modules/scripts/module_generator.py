#!/usr/bin/env python3
"""
Enhanced Visual Module Generator for Power BI PBIP Templates

Generates visual modules from YAML configuration supporting both Sales and Healthcare dashboard patterns.
Includes healthcare-specific visuals and domain-specific validation rules.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import argparse
import os

class ModuleGenerator:
    """Generates Power BI visual modules from configuration with domain-specific support"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.output_dir = Path("generated_modules")
        self.domain = self.config.get('project', {}).get('domain', 'generic')
        self.templates_dir = Path(__file__).parent.parent  # modules/ directory
        
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
            
    def generate_all(self):
        """Generate all modules defined in configuration"""
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"🏗️  Generating {self.domain} modules from {self.config_path}")
        print(f"📁 Output directory: {self.output_dir}")
        
        # Generate KPI strip
        if 'kpis' in self.config:
            self._generate_kpi_strip()
            
        # Generate individual visuals
        if 'visuals' in self.config:
            self._generate_visuals()
            
        # Generate slicers
        if 'slicers' in self.config:
            self._generate_slicers()
            
        # Generate interaction rules
        if 'interactions' in self.config:
            self._generate_interaction_rules()
            
        # Generate healthcare-specific templates if domain is healthcare
        if self.domain == 'healthcare':
            self._generate_healthcare_templates()
            
    def _generate_healthcare_templates(self):
        """Generate healthcare-specific visual templates"""
        print(f"🏥 Generating healthcare-specific templates...")
        
        # Generate matrix heatmap for day/hour analysis
        if any(v.get('type') == 'matrix_heatmap' for v in self.config.get('visuals', [])):
            self._generate_from_template('matrix_heatmap')
            
        # Generate SLA alert cards
        if any(v.get('type') == 'gauge_chart' for v in self.config.get('visuals', [])):
            self._generate_from_template('gauge_chart')
            
        # Generate data model validation report
        self._generate_healthcare_validation_report()
        
    def _generate_from_template(self, template_type: str):
        """Generate visual from template file"""
        template_mappings = {
            'matrix_heatmap': 'charts/_template_matrix-heatmap.json',
            'gauge_chart': 'charts/_template_gauge-chart.json',
            'sla_alert_card': 'kpi/_template_sla-alert-card.json'
        }
        
        if template_type not in template_mappings:
            print(f"⚠️  Unknown template type: {template_type}")
            return
            
        template_path = self.templates_dir / template_mappings[template_type]
        if not template_path.exists():
            print(f"⚠️  Template not found: {template_path}")
            return
            
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
                
            # Find matching visuals in config
            matching_visuals = [v for v in self.config.get('visuals', []) if v.get('type') == template_type]
            
            for visual in matching_visuals:
                # Apply configuration to template
                generated_visual = self._apply_config_to_template(template, visual)
                
                # Save generated visual
                output_path = self.output_dir / f"{visual['name']}_healthcare_{template_type}.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(generated_visual, f, indent=2, ensure_ascii=False)
                print(f"🏥 Generated healthcare visual: {output_path}")
                
        except Exception as e:
            print(f"❌ Error generating {template_type}: {e}")
            
    def _apply_config_to_template(self, template: Dict[str, Any], visual_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply visual configuration to template"""
        import copy
        result = copy.deepcopy(template)
        
        # Apply config mappings if they exist
        if 'config_mapping' in template:
            mappings = template['config_mapping']
            template_content = result['template']
            
            # Simple string replacement for now (could be enhanced with Jinja2)
            template_str = json.dumps(template_content)
            
            for key, config_path in mappings.items():
                if '.' in config_path:
                    # Handle nested paths like "visuals[?].position.x"
                    value = self._get_nested_value(visual_config, config_path.split('.'))
                else:
                    value = visual_config.get(config_path)
                    
                if value is not None:
                    template_str = template_str.replace(f"{{{key}}}", str(value))
                    
            result['template'] = json.loads(template_str)
            
        # Add configuration metadata
        result['config_applied'] = {
            'source_config': str(self.config_path),
            'visual_name': visual_config.get('name'),
            'domain': self.domain
        }
        
        return result
        
    def _get_nested_value(self, data: Dict[str, Any], path: List[str]) -> Any:
        """Get nested value from dictionary using path"""
        current = data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
        
    def _generate_healthcare_validation_report(self):
        """Generate healthcare-specific validation report"""
        validation_report = {
            "generated_from": str(self.config_path),
            "domain": "healthcare",
            "validation_type": "data_model_healthcare",
            "timestamp": "generated_at_runtime",
            "rules": []
        }
        
        # Add validation rules from config
        if 'validation_rules' in self.config:
            validation_report['rules'] = self.config['validation_rules']
            
        # Add healthcare-specific checks
        healthcare_checks = [
            {
                "rule_type": "datetime_modeling",
                "description": "Verify DateTime fields are properly split and modeled",
                "check": "Ensure DateTime columns are split into separate Date and Time columns",
                "severity": "error",
                "healthcare_reason": "Healthcare analytics require precise time-based analysis for patient flow"
            },
            {
                "rule_type": "calendar_table",
                "description": "Verify calendar table exists for time intelligence",
                "check": "Confirm calendar table is present and properly related to fact tables",
                "severity": "error", 
                "healthcare_reason": "Required for patient admission trending and capacity planning"
            },
            {
                "rule_type": "patient_count_validation",
                "description": "Ensure patient counts use DISTINCTCOUNT",
                "check": "All patient counting measures must use DISTINCTCOUNT aggregation",
                "severity": "error",
                "healthcare_reason": "Prevents double-counting patients across multiple records"
            },
            {
                "rule_type": "sla_threshold_parameterization",
                "description": "Verify SLA thresholds are parameterized",
                "check": "SLA thresholds should not be hard-coded in DAX measures",
                "severity": "warning",
                "healthcare_reason": "SLA targets may vary by department or change over time"
            },
            {
                "rule_type": "hipaa_compliance",
                "description": "Verify patient privacy protections",
                "check": "Patient Details dashboard requires RLS and audit logging",
                "severity": "critical",
                "healthcare_reason": "HIPAA requires protection of patient identifiable information"
            }
        ]
        
        validation_report['rules'].extend(healthcare_checks)
        
        # Save validation report
        output_path = self.output_dir / "healthcare_validation_report.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(validation_report, f, indent=2, ensure_ascii=False)
        print(f"🏥 Generated healthcare validation report: {output_path}")
        
    def _generate_kpi_strip(self):
        """Generate KPI strip module with domain-specific validation"""
        kpis = self.config['kpis']
        branding = self.config.get('branding', {})
        
        kpi_module = {
            "generated_from": str(self.config_path),
            "module_type": "kpi_strip",
            "domain": self.domain,
            "cards": [],
            "validation_rules": []
        }
        
        for kpi in kpis:
            # Extract validation rules
            validation = kpi.get('validation', {})
            
            card = {
                "field": kpi['field'],
                "display_name": kpi['display_name'],
                "aggregation": kpi['aggregation'],
                "format": kpi.get('format', '#,0'),
                "display_units": kpi.get('display_units', 'auto'),
                "description": kpi.get('description', ''),
                "primary_color": branding.get('primary_color', '#0078D4')
            }
            
            # Add healthcare-specific validation rules
            if validation:
                if 'aggregation_must_be' in validation:
                    kpi_module['validation_rules'].append({
                        "field": kpi['field'],
                        "rule": validation['aggregation_must_be'],
                        "reason": validation.get('reason')
                    })
                    
            kpi_module['cards'].append(card)
            
        # Save KPI module
        output_path = self.output_dir / f"kpi_strip_{self.domain}_generated.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(kpi_module, f, indent=2, ensure_ascii=False)
        print(f"📊 Generated {self.domain} KPI strip: {output_path}")
        
    def _generate_visuals(self):
        """Generate individual visual modules with domain-specific features"""
        visuals = self.config['visuals']
        branding = self.config.get('branding', {})
        
        for visual in visuals:
            visual_module = {
                "generated_from": str(self.config_path),
                "module_type": visual['type'],
                "domain": self.domain,
                "name": visual['name'],
                "title": visual['title'],
                "position": visual.get('position', {}),
                "data_config": self._extract_data_config(visual),
                "style": {
                    "primary_color": branding.get('primary_color', '#0078D4'),
                    "secondary_color": branding.get('secondary_color', '#FFFFFF'),
                    "accent_color": branding.get('accent_color', '#28A745'),
                    "alert_color": branding.get('alert_color', '#DC3545')
                },
                "features": visual.get('features', {}),
                "insights": visual.get('insights', [])
            }
            
            # Add healthcare-specific features
            if self.domain == 'healthcare' and visual['type'] in ['matrix_heatmap', 'gauge_chart']:
                visual_module['healthcare_specific'] = {
                    "clinical_value": "Supports evidence-based decision making",
                    "compliance_notes": "Aligns with Joint Commission and CMS standards"
                }
            
            # Save visual module
            output_path = self.output_dir / f"{visual['name']}_{self.domain}_generated.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(visual_module, f, indent=2, ensure_ascii=False)
            print(f"📈 Generated {self.domain} visual: {output_path}")
            
    def _generate_slicers(self):
        """Generate slicer modules with domain-specific configurations"""
        slicers = self.config['slicers']
        
        for slicer in slicers:
            slicer_module = {
                "generated_from": str(self.config_path),
                "module_type": "slicer", 
                "domain": self.domain,
                "name": slicer['name'],
                "field": slicer['field'],
                "title": slicer.get('title', slicer['field']),
                "style": slicer.get('style', 'dropdown'),
                "multi_select": slicer.get('multi_select', True),
                "select_all": slicer.get('select_all', True),
                "position": slicer.get('position', {}),
                "default_selection": slicer.get('default_selection', 'all'),
                "dashboard_visibility": slicer.get('dashboard_visibility', [])
            }
            
            # Save slicer module
            output_path = self.output_dir / f"{slicer['name']}_{self.domain}_generated.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(slicer_module, f, indent=2, ensure_ascii=False)
            print(f"🎛️  Generated {self.domain} slicer: {output_path}")
            
    def _generate_interaction_rules(self):
        """Generate interaction rules module with domain-specific behavior"""
        interactions = self.config['interactions']
        
        interaction_module = {
            "generated_from": str(self.config_path),
            "module_type": "interaction_rules",
            "domain": self.domain,
            "default_behavior": interactions.get('default_behavior', 'filter'),
            "rules": interactions.get('rules', []),
            "application_notes": [
                "Apply these rules after creating all visuals",
                "Use 'Edit Interactions' in Power BI Desktop",
                "Test each interaction by clicking visuals",
                "Validate that no highlighting behavior remains"
            ]
        }
        
        # Add domain-specific interaction notes
        if self.domain == 'healthcare':
            interaction_module['healthcare_notes'] = [
                "Time-based interactions are critical for patient flow analysis",
                "Ensure KPI cards do not filter other visuals to maintain clarity",
                "Patient demographic filters should highlight correlations"
            ]
        
        # Save interaction module
        output_path = self.output_dir / f"interaction_rules_{self.domain}_generated.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(interaction_module, f, indent=2, ensure_ascii=False)
        print(f"🔄 Generated {self.domain} interaction rules: {output_path}")
        
    def _extract_data_config(self, visual: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data configuration from visual definition"""
        data_config = {}
        
        # Common data bindings
        data_fields = [
            'x_axis', 'y_axis', 'location_field', 'color_field', 
            'category_field', 'value_field', 'rows_field', 'columns_field'
        ]
        
        for field in data_fields:
            if field in visual:
                data_config[field] = visual[field]
                
        # Aggregation settings
        for agg_field in ['color_aggregation', 'value_aggregation', 'x_axis_aggregation', 'y_axis_aggregation']:
            if agg_field in visual:
                data_config[agg_field] = visual[agg_field]
                
        # Tooltips
        if 'tooltips' in visual:
            data_config['tooltips'] = visual['tooltips']
            
        return data_config
        
    def validate_generated_modules(self):
        """Validate generated modules against domain-specific configuration rules"""
        validation_issues = []
        
        # Check KPI strip validation rules
        kpi_file = self.output_dir / f"kpi_strip_{self.domain}_generated.json"
        if kpi_file.exists():
            with open(kpi_file, 'r', encoding='utf-8') as f:
                kpi_data = json.load(f)
                
            for rule in kpi_data.get('validation_rules', []):
                # Simulate validation logic
                field = rule['field']
                required_agg = rule['rule']
                
                # Find corresponding card
                for card in kpi_data['cards']:
                    if card['field'] == field:
                        if card['aggregation'] != required_agg:
                            validation_issues.append(
                                f"❌ {self.domain.title()} KPI '{field}': Expected {required_agg}, got {card['aggregation']}"
                            )
                        else:
                            print(f"✅ {self.domain.title()} KPI '{field}': Correctly using {required_agg} aggregation")
        
        # Healthcare-specific validation
        if self.domain == 'healthcare':
            validation_issues.extend(self._validate_healthcare_rules())
                            
        if validation_issues:
            print(f"\n🚨 {self.domain.upper()} VALIDATION ISSUES FOUND:")
            for issue in validation_issues:
                print(f"  {issue}")
        else:
            print(f"\n✅ All generated {self.domain} modules passed validation")
            
        return len(validation_issues) == 0
        
    def _validate_healthcare_rules(self) -> List[str]:
        """Validate healthcare-specific rules"""
        issues = []
        
        # Check for DateTime field usage
        date_config = self.config.get('date', {})
        if 'datetime_field' in date_config and not date_config.get('validation', {}).get('no_datetime_joins'):
            issues.append("⚠️  Healthcare: DateTime field detected - should be split into Date and Time")
            
        # Check for calendar table requirement
        if not date_config.get('calendar_table') == 'required':
            issues.append("❌ Healthcare: Calendar table is required for time intelligence")
            
        # Check patient count aggregations
        for kpi in self.config.get('kpis', []):
            if 'patient' in kpi.get('field', '').lower() and kpi.get('aggregation') != 'DISTINCTCOUNT':
                issues.append(f"❌ Healthcare: Patient count '{kpi['field']}' must use DISTINCTCOUNT")
                
        return issues
            
def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description="Generate Power BI visual modules from configuration")
    parser.add_argument("config", help="Path to YAML configuration file")
    parser.add_argument("--output", "-o", help="Output directory for generated modules")
    parser.add_argument("--validate", action="store_true", help="Validate generated modules")
    
    args = parser.parse_args()
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return 1
        
    try:
        generator = ModuleGenerator(config_path)
        
        if args.output:
            generator.output_dir = Path(args.output)
            
        generator.generate_all()
        
        if args.validate:
            if not generator.validate_generated_modules():
                return 1
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
