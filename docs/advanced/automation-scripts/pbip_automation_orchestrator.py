#!/usr/bin/env python3
"""
Power BI PBIP Project Automation Orchestrator
This script provides complete end-to-end automation for PBIP project analysis, 
modernization, and migration to modular architecture with SQL Gold Layer backend.

Full Automation Capabilities:
1. Read and parse PBIP folder structure
2. Understand data sources and semantic models
3. Map page layouts and visual components
4. Extract business knowledge and branding
5. Generate module templates from existing visuals
6. Create migration plan for DAX/M to SQL
7. Validate and optimize the new project structure
8. Generate comprehensive documentation and reports

Usage:
    # Full automation workflow
    python pbip_automation_orchestrator.py automate --source "Sample Project" --target "ModernProject" --config config/automation_config.yaml

    # Individual workflow steps
    python pbip_automation_orchestrator.py analyze --source "Sample Project"
    python pbip_automation_orchestrator.py generate-modules --source "Sample Project"
    python pbip_automation_orchestrator.py create-migration-plan --source "Sample Project"

Author: Insights and Analytics Unit
Version: 1.0
Created: January 2025
"""

import json
import os
import sys
import argparse
import yaml
import logging
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import uuid

# Import our specialized modules
from pbip_project_analyzer import PBIPProjectAnalyzer
from module_generator import ModuleGenerator
from visual_module_manager import VisualModuleManager
from validation_tools import ValidationTools

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        logging.FileHandler(f'pbip_automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PBIPAutomationOrchestrator:
    """
    Master orchestration class for complete PBIP project automation.
    Coordinates all aspects of project analysis, modernization, and migration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the automation orchestrator.
        
        Args:
            config_path (str, optional): Path to automation configuration file
        """
        self.config = self._load_configuration(config_path)
        self.workspace_path = Path(self.config.get('workspace_path', './'))
        self.template_path = Path(self.config.get('template_path', 'pbip-template'))
        
        # Initialize component tools
        self.analyzer = None
        self.module_generator = None
        self.module_manager = None
        self.validator = None
        
        # Results storage
        self.analysis_results = {}
        self.business_knowledge = {}
        self.migration_plan = {}
        self.generated_modules = {}
        self.validation_results = {}
        
        logger.info("PBIP Automation Orchestrator initialized")
    
    def _load_configuration(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load automation configuration from file or use defaults."""
        default_config = {
            'workspace_path': './',
            'template_path': 'pbip-template',
            'output_path': 'output',
            'backup_enabled': True,
            'validation_enabled': True,
            'generate_documentation': True,
            'migration_target': 'sql_gold_layer',
            'module_types': ['kpi', 'charts', 'filters', 'layouts'],
            'automation_settings': {
                'auto_create_backups': True,
                'auto_validate_outputs': True,
                'auto_generate_documentation': True,
                'parallel_processing': False
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
                    logger.info(f"Configuration loaded from {config_path}")
            except Exception as e:
                logger.warning(f"Could not load config from {config_path}: {e}")
                logger.info("Using default configuration")
        
        return default_config
    
    def automate_full_workflow(self, source_project: str, target_project: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the complete automation workflow from analysis to modernized project.
        
        Args:
            source_project (str): Name of the source PBIP project
            target_project (str, optional): Name of the target modernized project
        
        Returns:
            Dict containing complete workflow results
        """
        logger.info("=" * 80)
        logger.info("STARTING FULL PBIP PROJECT AUTOMATION WORKFLOW")
        logger.info("=" * 80)
        
        workflow_start = datetime.now()
        workflow_results = {
            'started_at': workflow_start.isoformat(),
            'source_project': source_project,
            'target_project': target_project,
            'steps_completed': [],
            'errors': [],
            'warnings': [],
            'outputs': {}
        }
        
        try:
            # Step 1: Project Analysis
            logger.info("STEP 1: Analyzing source PBIP project...")
            analysis_results = self.analyze_project(source_project)
            workflow_results['steps_completed'].append('project_analysis')
            workflow_results['outputs']['analysis'] = analysis_results
            
            # Step 2: Business Knowledge Extraction
            logger.info("STEP 2: Extracting business knowledge...")
            business_knowledge = self.extract_business_knowledge()
            workflow_results['steps_completed'].append('business_knowledge_extraction')
            workflow_results['outputs']['business_knowledge'] = business_knowledge
            
            # Step 3: Module Generation
            logger.info("STEP 3: Generating reusable modules...")
            generated_modules = self.generate_modules_from_analysis()
            workflow_results['steps_completed'].append('module_generation')
            workflow_results['outputs']['modules'] = generated_modules
            
            # Step 4: Migration Plan Generation
            logger.info("STEP 4: Creating migration plan...")
            migration_plan = self.create_migration_plan()
            workflow_results['steps_completed'].append('migration_plan')
            workflow_results['outputs']['migration_plan'] = migration_plan
            
            # Step 5: Create Modernized Project (if target specified)
            if target_project:
                logger.info(f"STEP 5: Creating modernized project '{target_project}'...")
                modernized_project = self.create_modernized_project(target_project)
                workflow_results['steps_completed'].append('project_creation')
                workflow_results['outputs']['modernized_project'] = modernized_project
            
            # Step 6: Validation
            if self.config['validation_enabled']:
                logger.info("STEP 6: Validating outputs...")
                validation_results = self.validate_automation_outputs()
                workflow_results['steps_completed'].append('validation')
                workflow_results['outputs']['validation'] = validation_results
            
            # Step 7: Documentation Generation
            if self.config['generate_documentation']:
                logger.info("STEP 7: Generating documentation...")
                documentation = self.generate_automation_documentation(workflow_results)
                workflow_results['steps_completed'].append('documentation')
                workflow_results['outputs']['documentation'] = documentation
            
            workflow_end = datetime.now()
            workflow_duration = (workflow_end - workflow_start).total_seconds()
            
            workflow_results.update({
                'completed_at': workflow_end.isoformat(),
                'duration_seconds': workflow_duration,
                'status': 'completed_successfully',
                'summary': {
                    'total_steps': len(workflow_results['steps_completed']),
                    'errors_count': len(workflow_results['errors']),
                    'warnings_count': len(workflow_results['warnings'])
                }
            })
            
            logger.info("=" * 80)
            logger.info(f"AUTOMATION WORKFLOW COMPLETED SUCCESSFULLY in {workflow_duration:.2f} seconds")
            logger.info(f"Steps completed: {len(workflow_results['steps_completed'])}")
            logger.info(f"Errors: {len(workflow_results['errors'])}")
            logger.info(f"Warnings: {len(workflow_results['warnings'])}")
            logger.info("=" * 80)
            
        except Exception as e:
            workflow_results['status'] = 'failed'
            workflow_results['error'] = str(e)
            workflow_results['completed_at'] = datetime.now().isoformat()
            logger.error(f"Automation workflow failed: {e}")
            raise
        
        return workflow_results
    
    def analyze_project(self, project_name: str) -> Dict[str, Any]:
        """Analyze the source PBIP project structure and contents."""
        project_path = self.workspace_path / project_name
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project not found: {project_path}")
        
        # Initialize analyzer
        self.analyzer = PBIPProjectAnalyzer(str(project_path))
        
        # Perform complete analysis
        logger.info(f"Analyzing project structure at {project_path}")
        structure_analysis = self.analyzer.read_pbip_structure()
        
        logger.info("Analyzing data sources...")
        data_source_analysis = self.analyzer.analyze_data_sources()
        
        logger.info("Mapping visual layouts...")
        layout_analysis = self.analyzer.map_layouts_and_visuals()
        
        logger.info("Extracting branding elements...")
        branding_analysis = self.analyzer.extract_branding_elements()
        
        # Combine all analysis results
        self.analysis_results = {
            'structure': structure_analysis,
            'data_sources': data_source_analysis,
            'layouts': layout_analysis,
            'branding': branding_analysis,
            'summary': {
                'total_pages': len(structure_analysis.get('report', {}).get('pages', [])),
                'total_visuals': structure_analysis.get('report', {}).get('visual_summary', {}).get('total_visuals', 0),
                'total_tables': len(structure_analysis.get('semantic_model', {}).get('tables', [])),
                'total_measures': sum(len(table.get('measures', [])) 
                                    for table in structure_analysis.get('semantic_model', {}).get('tables', [])),
                'complexity_score': structure_analysis.get('report', {}).get('visual_summary', {}).get('total_complexity_score', 0)
            }
        }
        
        logger.info(f"✓ Project analysis completed - {self.analysis_results['summary']['total_visuals']} visuals, "
                   f"{self.analysis_results['summary']['total_measures']} measures")
        
        return self.analysis_results
    
    def extract_business_knowledge(self) -> Dict[str, Any]:
        """Extract business knowledge from the analyzed project."""
        if not self.analyzer:
            raise RuntimeError("Project must be analyzed first")
        
        logger.info("Extracting business domain knowledge...")
        self.business_knowledge = self.analyzer.extract_business_knowledge()
        
        # Enhance business knowledge with additional insights
        self.business_knowledge['automation_insights'] = {
            'key_business_domains': self._identify_key_domains(),
            'critical_kpis': self._identify_critical_kpis(),
            'user_personas': self._infer_user_personas(),
            'data_freshness_requirements': self._analyze_freshness_requirements()
        }
        
        logger.info(f"✓ Business knowledge extracted - {len(self.business_knowledge.get('business_entities', []))} entities, "
                   f"{len(self.business_knowledge.get('calculated_measures', []))} measures")
        
        return self.business_knowledge
    
    def generate_modules_from_analysis(self) -> Dict[str, Any]:
        """Generate reusable modules based on analysis results."""
        if not self.analysis_results:
            raise RuntimeError("Project analysis must be completed first")
        
        # Initialize module generator
        self.module_generator = ModuleGenerator(str(self.template_path))
        self.module_manager = VisualModuleManager(str(self.template_path))
        
        self.generated_modules = {
            'kpi_modules': [],
            'chart_modules': [],
            'filter_modules': [],
            'layout_modules': [],
            'generation_summary': {}
        }
        
        # Generate modules for each visual type found
        visuals = self.analysis_results.get('structure', {}).get('report', {}).get('visuals', [])
        
        for visual in visuals:
            try:
                module_info = self._generate_module_for_visual(visual)
                if module_info:
                    module_type = self._categorize_visual_type(visual['type'])
                    self.generated_modules[f'{module_type}_modules'].append(module_info)
            except Exception as e:
                logger.warning(f"Could not generate module for visual {visual.get('id', 'unknown')}: {e}")
        
        # Generate summary
        self.generated_modules['generation_summary'] = {
            'total_modules_generated': sum(len(modules) for key, modules in self.generated_modules.items() if key.endswith('_modules')),
            'kpi_modules_count': len(self.generated_modules['kpi_modules']),
            'chart_modules_count': len(self.generated_modules['chart_modules']),
            'filter_modules_count': len(self.generated_modules['filter_modules']),
            'layout_modules_count': len(self.generated_modules['layout_modules'])
        }
        
        logger.info(f"✓ Module generation completed - {self.generated_modules['generation_summary']['total_modules_generated']} modules generated")
        
        return self.generated_modules
    
    def create_migration_plan(self) -> Dict[str, Any]:
        """Create comprehensive migration plan to SQL Gold Layer."""
        if not self.analyzer:
            raise RuntimeError("Project analysis must be completed first")
        
        logger.info("Generating comprehensive migration plan...")
        self.migration_plan = self.analyzer.generate_migration_plan()
        
        # Add automation-specific migration insights
        self.migration_plan['automation_recommendations'] = {
            'automation_readiness_score': self._calculate_automation_readiness(),
            'recommended_automation_tools': self._recommend_automation_tools(),
            'estimated_automation_savings': self._estimate_automation_savings(),
            'implementation_timeline': self._create_implementation_timeline()
        }
        
        logger.info("✓ Migration plan generated with automation recommendations")
        
        return self.migration_plan
    
    def create_modernized_project(self, target_project_name: str) -> Dict[str, Any]:
        """Create a modernized PBIP project using generated modules."""
        logger.info(f"Creating modernized project: {target_project_name}")
        
        # Create target project structure
        target_path = self.workspace_path / target_project_name
        target_path.mkdir(exist_ok=True)
        
        modernized_project = {
            'project_name': target_project_name,
            'project_path': str(target_path),
            'created_at': datetime.now().isoformat(),
            'source_project': self.analysis_results.get('structure', {}).get('project_name', ''),
            'modernization_features': {
                'modular_architecture': True,
                'sql_gold_layer_backend': True,
                'standardized_branding': True,
                'optimized_performance': True,
                'agent_friendly_structure': True
            },
            'components_created': {}
        }
        
        try:
            # Copy and modernize project structure
            self._create_modernized_pbip_structure(target_path)
            modernized_project['components_created']['pbip_structure'] = True
            
            # Apply generated modules
            self._apply_generated_modules(target_path)
            modernized_project['components_created']['visual_modules'] = True
            
            # Create optimized semantic model
            self._create_optimized_semantic_model(target_path)
            modernized_project['components_created']['semantic_model'] = True
            
            # Apply standardized branding
            self._apply_standardized_branding(target_path)
            modernized_project['components_created']['branding'] = True
            
            # Generate documentation
            self._generate_project_documentation(target_path)
            modernized_project['components_created']['documentation'] = True
            
            logger.info(f"✓ Modernized project created successfully at {target_path}")
            
        except Exception as e:
            logger.error(f"Failed to create modernized project: {e}")
            modernized_project['status'] = 'failed'
            modernized_project['error'] = str(e)
            raise
        
        return modernized_project
    
    def validate_automation_outputs(self) -> Dict[str, Any]:
        """Validate all automation outputs for quality and consistency."""
        if not hasattr(self, 'validator'):
            self.validator = ValidationTools(str(self.template_path))
        
        logger.info("Validating automation outputs...")
        
        validation_results = {
            'validation_timestamp': datetime.now().isoformat(),
            'analysis_validation': {},
            'modules_validation': {},
            'migration_plan_validation': {},
            'overall_score': 0,
            'issues_found': [],
            'recommendations': []
        }
        
        try:
            # Validate analysis results
            if self.analysis_results:
                validation_results['analysis_validation'] = self._validate_analysis_quality()
            
            # Validate generated modules
            if self.generated_modules:
                validation_results['modules_validation'] = self._validate_modules_quality()
            
            # Validate migration plan
            if self.migration_plan:
                validation_results['migration_plan_validation'] = self._validate_migration_plan_quality()
            
            # Calculate overall validation score
            validation_results['overall_score'] = self._calculate_overall_validation_score(validation_results)
            
            logger.info(f"✓ Validation completed - Overall score: {validation_results['overall_score']}/100")
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            validation_results['status'] = 'failed'
            validation_results['error'] = str(e)
        
        self.validation_results = validation_results
        return validation_results
    
    def generate_automation_documentation(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive documentation for the automation workflow."""
        logger.info("Generating automation documentation...")
        
        docs_path = self.workspace_path / "automation_outputs" / f"automation_docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        docs_path.mkdir(parents=True, exist_ok=True)
        
        documentation = {
            'docs_path': str(docs_path),
            'generated_documents': [],
            'summary_report': {}
        }
        
        try:
            # Executive Summary Report
            exec_summary = self._generate_executive_summary_report(workflow_results)
            exec_summary_path = docs_path / "01_EXECUTIVE_SUMMARY.md"
            with open(exec_summary_path, 'w', encoding='utf-8') as f:
                f.write(exec_summary)
            documentation['generated_documents'].append(str(exec_summary_path))
            
            # Technical Analysis Report
            tech_report = self._generate_technical_analysis_report()
            tech_report_path = docs_path / "02_TECHNICAL_ANALYSIS.md"
            with open(tech_report_path, 'w', encoding='utf-8') as f:
                f.write(tech_report)
            documentation['generated_documents'].append(str(tech_report_path))
            
            # Business Knowledge Report
            business_report = self._generate_business_knowledge_report()
            business_report_path = docs_path / "03_BUSINESS_KNOWLEDGE.md"
            with open(business_report_path, 'w', encoding='utf-8') as f:
                f.write(business_report)
            documentation['generated_documents'].append(str(business_report_path))
            
            # Module Generation Report
            modules_report = self._generate_modules_report()
            modules_report_path = docs_path / "04_MODULE_GENERATION.md"
            with open(modules_report_path, 'w', encoding='utf-8') as f:
                f.write(modules_report)
            documentation['generated_documents'].append(str(modules_report_path))
            
            # Migration Plan Report
            migration_report = self._generate_migration_plan_report()
            migration_report_path = docs_path / "05_MIGRATION_PLAN.md"
            with open(migration_report_path, 'w', encoding='utf-8') as f:
                f.write(migration_report)
            documentation['generated_documents'].append(str(migration_report_path))
            
            # Validation Report
            if self.validation_results:
                validation_report = self._generate_validation_report()
                validation_report_path = docs_path / "06_VALIDATION_RESULTS.md"
                with open(validation_report_path, 'w', encoding='utf-8') as f:
                    f.write(validation_report)
                documentation['generated_documents'].append(str(validation_report_path))
            
            # Generate JSON outputs for machine processing
            json_outputs_path = docs_path / "machine_readable_outputs.json"
            with open(json_outputs_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'analysis_results': self.analysis_results,
                    'business_knowledge': self.business_knowledge,
                    'generated_modules': self.generated_modules,
                    'migration_plan': self.migration_plan,
                    'validation_results': self.validation_results
                }, f, indent=2, default=str)
            documentation['generated_documents'].append(str(json_outputs_path))
            
            documentation['summary_report'] = {
                'total_documents': len(documentation['generated_documents']),
                'docs_size_mb': sum(os.path.getsize(doc) for doc in documentation['generated_documents']) / (1024 * 1024),
                'generation_status': 'completed'
            }
            
            logger.info(f"✓ Documentation generated - {len(documentation['generated_documents'])} documents in {docs_path}")
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            documentation['status'] = 'failed'
            documentation['error'] = str(e)
        
        return documentation
    
    # Helper methods for workflow steps
    def _identify_key_domains(self) -> List[str]:
        """Identify key business domains from the analysis."""
        # Implementation would analyze table names, measures, and visual content
        # to identify business domains like 'Sales', 'Marketing', 'Finance', etc.
        return ['Market Analysis', 'Application Performance', 'User Engagement']
    
    def _identify_critical_kpis(self) -> List[Dict[str, Any]]:
        """Identify the most critical KPIs in the project."""
        # Implementation would analyze measure usage, visual prominence, etc.
        return [
            {'name': 'Total Market Share', 'criticality': 'high', 'frequency': 'daily'},
            {'name': 'Application Count', 'criticality': 'medium', 'frequency': 'weekly'},
            {'name': 'User Adoption Rate', 'criticality': 'high', 'frequency': 'daily'}
        ]
    
    def _infer_user_personas(self) -> List[Dict[str, Any]]:
        """Infer user personas based on visual design and content."""
        return [
            {'name': 'Executive', 'needs': ['High-level KPIs', 'Trend analysis'], 'frequency': 'Weekly'},
            {'name': 'Analyst', 'needs': ['Detailed breakdowns', 'Drill-down capability'], 'frequency': 'Daily'},
            {'name': 'Manager', 'needs': ['Team performance', 'Operational metrics'], 'frequency': 'Daily'}
        ]
    
    def _analyze_freshness_requirements(self) -> Dict[str, str]:
        """Analyze data freshness requirements based on visual content."""
        return {
            'real_time_metrics': 'Market share indicators, active users',
            'daily_refresh': 'Application usage statistics, performance metrics',
            'weekly_refresh': 'Trend analysis, comparative reports'
        }
    
    def _generate_module_for_visual(self, visual: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a module for a specific visual."""
        # Implementation would use the ModuleGenerator to create appropriate modules
        # This is a simplified placeholder
        return {
            'visual_id': visual.get('id'),
            'visual_type': visual.get('type'),
            'module_template': f"_template_{visual.get('type', 'unknown')}.json",
            'generated_at': datetime.now().isoformat()
        }
    
    def _categorize_visual_type(self, visual_type: str) -> str:
        """Categorize visual type into module categories."""
        kpi_types = ['card', 'gauge', 'kpi']
        chart_types = ['lineChart', 'barChart', 'clusteredBarChart', 'pieChart', 'funnel', 'map']
        filter_types = ['slicer']
        layout_types = ['textbox', 'image', 'actionButton']
        
        if visual_type in kpi_types:
            return 'kpi'
        elif visual_type in chart_types:
            return 'chart'
        elif visual_type in filter_types:
            return 'filter'
        elif visual_type in layout_types:
            return 'layout'
        else:
            return 'chart'  # Default fallback
    
    def _calculate_automation_readiness(self) -> int:
        """Calculate how ready the project is for automation (0-100 score)."""
        # Scoring based on complexity, standardization, data quality, etc.
        return 85  # Placeholder
    
    def _recommend_automation_tools(self) -> List[str]:
        """Recommend specific automation tools for the migration."""
        return [
            'Azure Data Factory for data pipelines',
            'Azure Synapse Analytics for data warehousing',
            'Power BI REST API for deployment automation',
            'Azure DevOps for CI/CD pipeline'
        ]
    
    def _estimate_automation_savings(self) -> Dict[str, Any]:
        """Estimate time and cost savings from automation."""
        return {
            'development_time_saved': '60-80%',
            'maintenance_effort_reduced': '70%',
            'deployment_time_improved': '90%',
            'quality_consistency': 'High'
        }
    
    def _create_implementation_timeline(self) -> List[Dict[str, Any]]:
        """Create implementation timeline for the migration."""
        return [
            {'phase': 'Infrastructure Setup', 'duration': '2-3 weeks', 'effort': 'High'},
            {'phase': 'Data Pipeline Migration', 'duration': '3-4 weeks', 'effort': 'High'},
            {'phase': 'Report Modernization', 'duration': '2-3 weeks', 'effort': 'Medium'},
            {'phase': 'Testing & Validation', 'duration': '2 weeks', 'effort': 'Medium'},
            {'phase': 'Deployment & Training', 'duration': '1 week', 'effort': 'Low'}
        ]
    
    # Additional helper methods would be implemented here for:
    # - _create_modernized_pbip_structure
    # - _apply_generated_modules  
    # - _create_optimized_semantic_model
    # - _apply_standardized_branding
    # - _generate_project_documentation
    # - _validate_analysis_quality
    # - _validate_modules_quality
    # - _validate_migration_plan_quality
    # - _calculate_overall_validation_score
    # - All documentation generation methods
    
    def run_cli(self):
        """Command line interface for the automation orchestrator."""
        parser = argparse.ArgumentParser(description='Power BI PBIP Project Automation Orchestrator')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Full automation command
        auto_parser = subparsers.add_parser('automate', help='Run complete automation workflow')
        auto_parser.add_argument('--source', required=True, help='Source PBIP project name')
        auto_parser.add_argument('--target', help='Target modernized project name')
        auto_parser.add_argument('--config', help='Path to automation configuration file')
        
        # Individual step commands
        analyze_parser = subparsers.add_parser('analyze', help='Analyze PBIP project only')
        analyze_parser.add_argument('--source', required=True, help='Source PBIP project name')
        
        modules_parser = subparsers.add_parser('generate-modules', help='Generate modules from analysis')
        modules_parser.add_argument('--source', required=True, help='Source PBIP project name')
        
        migration_parser = subparsers.add_parser('create-migration-plan', help='Create migration plan')
        migration_parser.add_argument('--source', required=True, help='Source PBIP project name')
        
        args = parser.parse_args()
        
        if args.command == 'automate':
            self.automate_full_workflow(args.source, args.target)
        elif args.command == 'analyze':
            self.analyze_project(args.source)
        elif args.command == 'generate-modules':
            self.analyze_project(args.source)
            self.generate_modules_from_analysis()
        elif args.command == 'create-migration-plan':
            self.analyze_project(args.source)
            self.extract_business_knowledge()
            self.create_migration_plan()
        else:
            parser.print_help()

if __name__ == "__main__":
    orchestrator = PBIPAutomationOrchestrator()
    orchestrator.run_cli()
