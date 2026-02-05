#!/usr/bin/env python3
"""
Module Generator for Power BI PBIP Projects
This script generates visual modules from templates and configuration files.

Usage:
    python module_generator.py generate-kpi --config config/kpi_config.yaml --output modules/kpi/
    python module_generator.py generate-charts --config config/charts_config.yaml --output modules/charts/
    python module_generator.py generate-all --config config/full_config.yaml

Author: _[Team/Individual]_
Version: 1.0
Created: _[Date]_
"""

import json
import os
import sys
import argparse
import yaml
import logging
from datetime import datetime
from typing import Dict, List, Any
from string import Template
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('module_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModuleGenerator:
    """Class for generating Power BI visual modules from templates."""
    
    def __init__(self, project_path: str = "./"):
        """
        Initialize the Module Generator.
        
        Args:
            project_path (str): Path to the Power BI PBIP project root
        """
        self.project_path = project_path
        self.modules_path = os.path.join(project_path, "modules")
        self.templates_path = self.modules_path  # Templates are in the modules directory
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.modules_path,
            os.path.join(self.modules_path, "kpi"),
            os.path.join(self.modules_path, "charts"),
            os.path.join(self.modules_path, "filters"),
            os.path.join(self.modules_path, "layouts"),
            os.path.join(self.modules_path, "scripts")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def load_template(self, template_type: str, template_name: str) -> Dict[str, Any]:
        """
        Load a template file.
        
        Args:
            template_type (str): Type of template (kpi, charts, filters, layouts)
            template_name (str): Name of the template file
            
        Returns:
            Dict: Template data
        """
        template_path = os.path.join(self.templates_path, template_type, template_name)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Template file not found: {template_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in template file: {str(e)}")
            return {}
    
    def substitute_template_variables(self, template_data: Dict[str, Any], variables: Dict[str, str]) -> Dict[str, Any]:
        """
        Substitute template variables with actual values.
        
        Args:
            template_data (Dict): Template data with placeholders
            variables (Dict): Variable substitutions
            
        Returns:
            Dict: Template data with substituted values
        """
        # Convert template data to string for substitution
        template_str = json.dumps(template_data, indent=2)
        
        # Create Template object and substitute
        template = Template(template_str)
        
        try:
            substituted_str = template.substitute(variables)
            return json.loads(substituted_str)
        except KeyError as e:
            logger.error(f"Missing template variable: {str(e)}")
            return template_data
        except json.JSONDecodeError as e:
            logger.error(f"Error after template substitution: {str(e)}")
            return template_data
    
    def generate_kpi_modules(self, config: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate KPI modules from configuration.
        
        Args:
            config (Dict): KPI configuration
            variables (Dict): Global variables for substitution
            output_dir (str): Output directory for modules
            
        Returns:
            List[str]: List of generated module file paths
        """
        generated_files = []
        
        # Load template
        template_data = self.load_template("kpi", "_template_metric-card.json")
        if not template_data:
            logger.error("Failed to load KPI template")
            return generated_files
        
        # Extract organization and global config
        organization = config.get("organization", {})
        measures = config.get("measures", [])
        
        for measure in measures:
            # Create variables for this specific KPI
            variables = {
                # Module metadata
                "_Module Display Name_": f"{measure['name']} Card",
                "_Business purpose and usage description_": f"KPI card for {measure['name']} with organizational branding",
                "_Creator or team name_": config.get("author", "Module Generator"),
                "_ISO date format: YYYY-MM-DD_": datetime.now().strftime("%Y-%m-%d"),
                
                # Data binding
                "_Required table 1_": measure.get("data_table", "BaseTable"),
                "_Required table 2_": measure.get("secondary_table", ""),
                "_Required measure 1_": measure["name"],
                "_Source table name_": measure.get("data_table", "BaseTable"),
                "_Measure name_": measure["name"],
                
                # Formatting
                "_Format: #,0|0.0%|$#,0|etc_": measure.get("format", "#,0"),
                
                # Branding
                "_Organization primary color hex_": organization.get("primary_color", "#004B87"),
                "_Text color for readability_": organization.get("text_color", "#333333"),
                "_Organization font family_": organization.get("font_family", "Segoe UI"),
                
                # Positioning
                "_Default width in pixels_": str(measure.get("width", 200)),
                "_Default height in pixels_": str(measure.get("height", 120)),
                
                # Responsive behavior
                "_Desktop width_": str(measure.get("width", 200)),
                "_Desktop height_": str(measure.get("height", 120)),
                "_Tablet width_": str(int(measure.get("width", 200) * 0.9)),
                "_Tablet height_": str(int(measure.get("height", 120) * 0.9)),
                "_Mobile width_": str(int(measure.get("width", 200) * 0.8)),
                "_Mobile height_": str(int(measure.get("height", 120) * 0.8)),
                
                # Additional metadata
                "_Organization secondary color hex_": organization.get("secondary_color", "#FFC627"),
                "_Standard font family_": organization.get("font_family", "Segoe UI"),
                "_Logo positioning guidelines_": organization.get("logo_placement", "Top-left corner"),
                "_Screen reader descriptions_": f"KPI card showing {measure['name']}",
                "_Color blind accessibility notes_": "Uses high contrast colors for accessibility",
                "_Keyboard interaction support_": "Supports keyboard navigation and focus",
                "_Recommended placement in report_": f"Featured in KPI section for {measure.get('audience', 'general')} audience",
                "_Cross-filtering and drill-through behavior_": "Supports cross-filtering with time and category filters",
                "_Mobile-specific adaptations_": "Scales down font size and adjusts layout for mobile",
                "_Performance considerations and load time impact_": "Lightweight visual with minimal performance impact",
                "_Available color scheme options_": "Primary, secondary, high contrast, and department-specific variants",
                "_Different size configurations_": "Compact, standard, and expanded sizing options",
                "_Alternative data binding options_": "Can be bound to different measures of same data type"
            }
            
            # Substitute variables
            module_data = self.substitute_template_variables(template_data, variables)
            
            # Generate output filename
            safe_name = measure["name"].lower().replace(" ", "-").replace("%", "percent")
            output_filename = f"{safe_name}-card.json"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the module
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(module_data, f, indent=2, ensure_ascii=False)
                generated_files.append(output_path)
                logger.info(f"Generated KPI module: {output_path}")
                
            except Exception as e:
                logger.error(f"Error saving KPI module {output_path}: {str(e)}")
        
        return generated_files
    
    def generate_chart_modules(self, config: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate chart modules from configuration.
        
        Args:
            config (Dict): Chart configuration
            output_dir (str): Output directory for modules
            
        Returns:
            List[str]: List of generated module file paths
        """
        generated_files = []
        
        # Load template
        template_data = self.load_template("charts", "_template_trend-line-chart.json")
        if not template_data:
            logger.error("Failed to load chart template")
            return generated_files
        
        # Extract organization and chart configs
        organization = config.get("organization", {})
        chart_types = config.get("chart_types", [])
        
        for chart in chart_types:
            # Create variables for this specific chart
            variables = {
                # Module metadata
                "_Chart Display Name_": f"{chart['purpose'].replace('_', ' ').title()} {chart['type'].title()} Chart",
                "_lineChart|barChart|columnChart|areaChart|scatterChart_": chart["type"],
                "_Chart purpose and analysis type_": f"{chart['purpose']} analysis using {chart['type']} visualization",
                "_Creator or team name_": config.get("author", "Module Generator"),
                "_ISO date format: YYYY-MM-DD_": datetime.now().strftime("%Y-%m-%d"),
                
                # Data binding
                "_Required table 1_": chart.get("dimensions", ["BaseTable"])[0] if chart.get("dimensions") else "BaseTable",
                "_Required table 2_": chart.get("dimensions", ["", ""])[1] if len(chart.get("dimensions", [])) > 1 else "",
                "_Required measure 1_": chart.get("measures", ["Measure"])[0] if chart.get("measures") else "Measure",
                "_Required measure 2_": chart.get("measures", ["", ""])[1] if len(chart.get("measures", [])) > 1 else "",
                "_Source table name_": chart.get("dimensions", ["BaseTable"])[0] if chart.get("dimensions") else "BaseTable",
                "_Category field name_": chart.get("dimensions", ["Category"])[0] if chart.get("dimensions") else "Category",
                "_Measure name_": chart.get("measures", ["Measure"])[0] if chart.get("measures") else "Measure",
                
                # Visual type
                "_lineChart|columnChart|etc_": chart["type"],
                
                # Branding
                "_Organization font family_": organization.get("font_family", "Segoe UI"),
                "_Organization primary color hex_": organization.get("primary_color", "#004B87"),
                "_Color 1 hex_": organization.get("primary_color", "#004B87"),
                "_Color 2 hex_": organization.get("secondary_color", "#FFC627"),
                "_Color 3 hex_": organization.get("accent_color", "#28A745"),
                "_Color 4 hex_": organization.get("neutral_color", "#6C757D"),
                
                # Positioning
                "_Default width in pixels_": str(chart.get("width", 400)),
                "_Default height in pixels_": str(chart.get("height", 300)),
                
                # Responsive behavior
                "_Desktop width_": str(chart.get("width", 400)),
                "_Desktop height_": str(chart.get("height", 300)),
                "_Tablet width_": str(int(chart.get("width", 400) * 0.9)),
                "_Tablet height_": str(int(chart.get("height", 300) * 0.9)),
                "_Mobile width_": str(int(chart.get("width", 400) * 0.8)),
                "_Mobile height_": str(int(chart.get("height", 300) * 0.8)),
                
                # Additional metadata
                "_Standard font family_": organization.get("font_family", "Segoe UI"),
                "_Modern|Classic|Corporate_": organization.get("chart_style", "Modern"),
                "_Pattern differentiation in addition to color_": "Uses patterns for color-blind accessibility",
                "_High contrast color scheme_": "High contrast mode available",
                "_Chart description for screen readers_": f"{chart['type']} chart showing {chart['purpose']} analysis",
                "_Trend|Comparison|Distribution|Relationship_": chart.get("analysis_type", chart["purpose"]),
                "_When to use this chart type_": f"Best for {chart['purpose']} analysis and data exploration",
                "_Minimum/maximum data points_": chart.get("data_requirements", "Minimum 2 data points, maximum 1000 for performance"),
                "_Drill-through and cross-filtering_": chart.get("interactions", {}).get("drill_through", "Enabled"),
                "_Line|Area|Stepped line options_": "Multiple visualization styles available",
                "_Sum|Average|Count|etc_": "Supports multiple aggregation methods",
                "_YoY|MoM|QoQ options_": "Time intelligence calculations available"
            }
            
            # Substitute variables
            module_data = self.substitute_template_variables(template_data, variables)
            
            # Generate output filename
            safe_purpose = chart['purpose'].lower().replace('_', '-')
            output_filename = f"{safe_purpose}-{chart['type']}.json"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the module
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(module_data, f, indent=2, ensure_ascii=False)
                generated_files.append(output_path)
                logger.info(f"Generated chart module: {output_path}")
                
            except Exception as e:
                logger.error(f"Error saving chart module {output_path}: {str(e)}")
        
        return generated_files
    
    def generate_filter_modules(self, config: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate filter modules from configuration.
        
        Args:
            config (Dict): Filter configuration
            output_dir (str): Output directory for modules
            
        Returns:
            List[str]: List of generated module file paths
        """
        generated_files = []
        
        # Load template
        template_data = self.load_template("filters", "_template_dimension-slicer.json")
        if not template_data:
            logger.error("Failed to load filter template")
            return generated_files
        
        # Extract organization and filter configs
        organization = config.get("organization", {})
        filter_dimensions = config.get("filter_dimensions", [])
        
        for filter_dim in filter_dimensions:
            # Create variables for this specific filter
            variables = {
                # Module metadata
                "_Filter Display Name_": f"{filter_dim['dimension']} Filter",
                "_Filter purpose and behavior description_": f"Filter for {filter_dim['dimension']} dimension with {filter_dim.get('type', 'dropdown')} interface",
                "_Creator or team name_": config.get("author", "Module Generator"),
                "_ISO date format: YYYY-MM-DD_": datetime.now().strftime("%Y-%m-%d"),
                
                # Data binding
                "_Required table 1_": filter_dim.get("source_table", "BaseTable"),
                "_Source table name_": filter_dim.get("source_table", "BaseTable"),
                "_Filter field name_": filter_dim["dimension"],
                
                # Selection behavior
                "_true|false for select all option_": str(filter_dim.get("multi_select", True)).lower(),
                "_true|false for single vs multi-select_": str(not filter_dim.get("multi_select", True)).lower(),
                
                # Branding
                "_Organization primary color hex_": organization.get("primary_color", "#004B87"),
                "_Header text color hex_": organization.get("text_color", "#333333"),
                "_Header background color hex_": organization.get("secondary_color", "#F8F9FA"),
                "_Item text color hex_": organization.get("text_color", "#333333"),
                "_Item background color hex_": "#FFFFFF",
                "_Organization font family_": organization.get("font_family", "Segoe UI"),
                
                # Positioning
                "_Default width in pixels_": str(filter_dim.get("width", 200)),
                "_Default height in pixels_": str(filter_dim.get("height", 150)),
                
                # Responsive behavior
                "_Desktop width_": str(filter_dim.get("width", 200)),
                "_Desktop height_": str(filter_dim.get("height", 150)),
                "_Tablet width_": str(int(filter_dim.get("width", 200) * 0.9)),
                "_Tablet height_": str(int(filter_dim.get("height", 150) * 0.9)),
                "_Mobile width_": str(int(filter_dim.get("width", 200) * 0.8)),
                "_Mobile height_": str(int(filter_dim.get("height", 150) * 0.8)),
                "_Vertical|Horizontal_": "Vertical",
                
                # Additional metadata
                "_Organization secondary color hex_": organization.get("secondary_color", "#FFC627"),
                "_Standard font family_": organization.get("font_family", "Segoe UI"),
                "_Dropdown|List|Tiles|Cards_": filter_dim.get("type", "dropdown"),
                "_Filter description for screen readers_": f"Filter for {filter_dim['dimension']} dimension",
                "_Tab order and keyboard shortcuts_": "Supports keyboard navigation with Tab and Enter keys",
                "_Visual focus indicators_": "Clear focus indicators for keyboard navigation",
                "_How filter affects other visuals_": "Cross-filters all related visuals on the page",
                "_Default selected values_": filter_dim.get("default_selection", "All items"),
                "_Impact on report performance_": "Minimal performance impact for standard datasets",
                "_When and how to use this filter_": f"Use to filter data by {filter_dim['dimension']}",
                "_Single|Multi|Search enabled_": "Multi" if filter_dim.get("multi_select", True) else "Single",
                "_List|Dropdown|Tiles|Cards_": filter_dim.get("type", "dropdown"),
                "_Alphabetical|Custom|Data driven_": "Alphabetical",
                "_Hierarchical|Flat|Categorized_": "Flat"
            }
            
            # Substitute variables
            module_data = self.substitute_template_variables(template_data, variables)
            
            # Generate output filename
            safe_name = filter_dim["dimension"].lower().replace(" ", "-")
            output_filename = f"{safe_name}-slicer.json"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the module
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(module_data, f, indent=2, ensure_ascii=False)
                generated_files.append(output_path)
                logger.info(f"Generated filter module: {output_path}")
                
            except Exception as e:
                logger.error(f"Error saving filter module {output_path}: {str(e)}")
        
        return generated_files
    
    def generate_layout_modules(self, config: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate layout modules from configuration.
        
        Args:
            config (Dict): Layout configuration
            output_dir (str): Output directory for modules
            
        Returns:
            List[str]: List of generated module file paths
        """
        generated_files = []
        
        # Load template
        template_data = self.load_template("layouts", "_template_executive-dashboard-layout.json")
        if not template_data:
            logger.error("Failed to load layout template")
            return generated_files
        
        # Extract organization and layout configs
        organization = config.get("organization", {})
        layout_types = config.get("layout_types", {})
        
        for layout_name, layout_config in layout_types.items():
            # Create variables for this specific layout
            variables = {
                # Module metadata
                "_Layout Display Name_": f"{layout_name.title()} Dashboard Layout",
                "_Layout purpose and target audience_": f"Layout optimized for {layout_name} users with {layout_config.get('focus', 'general')} focus",
                "_Creator or team name_": config.get("author", "Module Generator"),
                "_ISO date format: YYYY-MM-DD_": datetime.now().strftime("%Y-%m-%d"),
                
                # Layout structure
                "_Header height in pixels_": str(config.get("page_structure", {}).get("header_height", 80)),
                "_Header background color hex_": organization.get("primary_color", "#004B87"),
                "_Logo width_": "60",
                "_Logo height_": "40",
                "_Title font size_": "18",
                "_Organization font family_": organization.get("font_family", "Segoe UI"),
                "_Title text color hex_": "#FFFFFF",
                "_Button|Tab|Dropdown_": "Tab",
                
                "_Filter bar height in pixels_": str(config.get("page_structure", {}).get("filter_bar_height", 60)),
                "_Filter bar background color hex_": "#F8F9FA",
                "_Horizontal|Vertical_": "Horizontal",
                "_Number of filter positions_": str(config.get("page_structure", {}).get("filter_slots", 4)),
                
                "_Number of columns_": str(config.get("page_structure", {}).get("content_area_grid", "4x3").split("x")[0]),
                "_Number of rows_": str(config.get("page_structure", {}).get("content_area_grid", "4x3").split("x")[1]),
                "_Horizontal gap in pixels_": "10",
                "_Vertical gap in pixels_": "10",
                "_Margin around content area_": "20",
                
                "_Footer height in pixels_": "40",
                "_Footer background color hex_": organization.get("secondary_color", "#F8F9FA"),
                "_Date/time display format_": "MMM DD, YYYY HH:mm",
                "_Source info font size_": "10",
                "_Contact information_": organization.get("contact", "Data Team"),
                
                # Visual zones
                "_KPI row height_": "120",
                "_Main chart height_": "300",
                "_Secondary chart height_": "300",
                "_Table height_": "200",
                
                # Branding
                "_Organization primary color hex_": organization.get("primary_color", "#004B87"),
                "_Organization secondary color hex_": organization.get("secondary_color", "#FFC627"),
                "_Organization accent color hex_": organization.get("accent_color", "#28A745"),
                "_Page background color hex_": "#FFFFFF",
                "_Primary text color hex_": organization.get("text_color", "#333333"),
                "_Header font family_": organization.get("font_family", "Segoe UI"),
                "_Body font family_": organization.get("font_family", "Segoe UI"),
                "_Main title size_": "24",
                "_Section title size_": "18",
                "_Subsection title size_": "14",
                "_Standard margin value_": "15",
                "_Standard padding value_": "10",
                "_Gap between elements_": "10",
                
                # Responsive behavior
                "_Desktop canvas width_": "1366",
                "_Desktop canvas height_": "768",
                "_Desktop grid configuration_": "4 columns, flexible rows",
                "_Tablet canvas width_": "1024",
                "_Tablet canvas height_": "768",
                "_Tablet grid configuration_": "3 columns, flexible rows",
                "_Mobile canvas width_": "375",
                "_Mobile canvas height_": "667",
                
                # Additional metadata
                "_Tab order and focus flow_": "Header > Filters > Main content > Footer",
                "_WCAG compliance notes_": "Meets WCAG 2.1 AA standards for color contrast",
                "_Screen reader navigation structure_": "Semantic HTML structure with proper headings",
                "_Available keyboard shortcuts_": "F for filters, R for refresh, H for home",
                "_Executive|Operational|Analytical_": layout_name.title(),
                "_Low|Medium|High_": layout_config.get("visual_density", "Medium"),
                "_Simple|Moderate|Advanced_": layout_config.get("interaction_complexity", "Moderate"),
                "_Real-time|Daily|Weekly|Monthly_": "Daily",
                "_Load time and interaction performance_": f"Optimized for {layout_config.get('visual_density', 'medium')} density layouts",
                "_Light|Dark|High contrast_": "Light",
                "_Compact|Standard|Expanded_": "Standard",
                "_Department-specific customizations_": "Color scheme and logo variants available",
                "_Mobile-specific layout options_": "Single column with collapsible sections"
            }
            
            # Substitute variables
            module_data = self.substitute_template_variables(template_data, variables)
            
            # Generate output filename
            output_filename = f"{layout_name}-dashboard-layout.json"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the module
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(module_data, f, indent=2, ensure_ascii=False)
                generated_files.append(output_path)
                logger.info(f"Generated layout module: {output_path}")
                
            except Exception as e:
                logger.error(f"Error saving layout module {output_path}: {str(e)}")
        
        return generated_files
    
    def generate_all_modules(self, config_file: str) -> Dict[str, List[str]]:
        """
        Generate all modules from a comprehensive configuration file.
        
        Args:
            config_file (str): Path to the configuration file
            
        Returns:
            Dict[str, List[str]]: Generated files by category
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading configuration file: {str(e)}")
            return {}
        
        results = {}
        
        # Generate KPI modules
        if 'kpi' in config or 'measures' in config:
            kpi_config = config.get('kpi', config)
            kpi_output = os.path.join(self.modules_path, "kpi")
            results['kpi'] = self.generate_kpi_modules(kpi_config, kpi_output)
        
        # Generate chart modules
        if 'charts' in config or 'chart_types' in config:
            chart_config = config.get('charts', config)
            chart_output = os.path.join(self.modules_path, "charts")
            results['charts'] = self.generate_chart_modules(chart_config, chart_output)
        
        # Generate filter modules
        if 'filters' in config or 'filter_dimensions' in config:
            filter_config = config.get('filters', config)
            filter_output = os.path.join(self.modules_path, "filters")
            results['filters'] = self.generate_filter_modules(filter_config, filter_output)
        
        # Generate layout modules
        if 'layouts' in config or 'layout_types' in config:
            layout_config = config.get('layouts', config)
            layout_output = os.path.join(self.modules_path, "layouts")
            results['layouts'] = self.generate_layout_modules(layout_config, layout_output)
        
        return results

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(description='Module Generator for Power BI PBIP Projects')
    parser.add_argument('--project-path', default='./', help='Path to the PBIP project root')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate KPI command
    kpi_parser = subparsers.add_parser('generate-kpi', help='Generate KPI modules')
    kpi_parser.add_argument('--config', required=True, help='Configuration file for KPI modules')
    kpi_parser.add_argument('--output', required=True, help='Output directory for KPI modules')
    
    # Generate charts command
    charts_parser = subparsers.add_parser('generate-charts', help='Generate chart modules')
    charts_parser.add_argument('--config', required=True, help='Configuration file for chart modules')
    charts_parser.add_argument('--output', required=True, help='Output directory for chart modules')
    
    # Generate filters command
    filters_parser = subparsers.add_parser('generate-filters', help='Generate filter modules')
    filters_parser.add_argument('--config', required=True, help='Configuration file for filter modules')
    filters_parser.add_argument('--output', required=True, help='Output directory for filter modules')
    
    # Generate layouts command
    layouts_parser = subparsers.add_parser('generate-layouts', help='Generate layout modules')
    layouts_parser.add_argument('--config', required=True, help='Configuration file for layout modules')
    layouts_parser.add_argument('--output', required=True, help='Output directory for layout modules')
    
    # Generate all command
    all_parser = subparsers.add_parser('generate-all', help='Generate all modules from comprehensive config')
    all_parser.add_argument('--config', required=True, help='Comprehensive configuration file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize generator
    generator = ModuleGenerator(args.project_path)
    
    # Execute command
    if args.command == 'generate-kpi':
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            generated = generator.generate_kpi_modules(config, args.output)
            print(f"Generated {len(generated)} KPI modules")
            for file in generated:
                print(f"  - {file}")
                
        except Exception as e:
            logger.error(f"Error generating KPI modules: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'generate-charts':
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            generated = generator.generate_chart_modules(config, args.output)
            print(f"Generated {len(generated)} chart modules")
            for file in generated:
                print(f"  - {file}")
                
        except Exception as e:
            logger.error(f"Error generating chart modules: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'generate-filters':
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            generated = generator.generate_filter_modules(config, args.output)
            print(f"Generated {len(generated)} filter modules")
            for file in generated:
                print(f"  - {file}")
                
        except Exception as e:
            logger.error(f"Error generating filter modules: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'generate-layouts':
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            generated = generator.generate_layout_modules(config, args.output)
            print(f"Generated {len(generated)} layout modules")
            for file in generated:
                print(f"  - {file}")
                
        except Exception as e:
            logger.error(f"Error generating layout modules: {str(e)}")
            sys.exit(1)
    
    elif args.command == 'generate-all':
        results = generator.generate_all_modules(args.config)
        
        total_generated = 0
        for category, files in results.items():
            total_generated += len(files)
            print(f"Generated {len(files)} {category} modules:")
            for file in files:
                print(f"  - {file}")
        
        print(f"\nTotal modules generated: {total_generated}")

if __name__ == '__main__':
    main()
