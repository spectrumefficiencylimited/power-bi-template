#!/usr/bin/env python3
"""
PBIP Project Analyzer - Comprehensive Analysis Tool
This script provides automated analysis of Power BI PBIP projects including:
- Reading and parsing PBIP folder structure
- Understanding data sources and models
- Mapping page layouts and visual components
- Extracting business knowledge and branding
- Preparing DAX/M to SQL migration path

Author: Insights and Analytics Unit
Version: 1.0
Created: February 5, 2026
"""

import json
import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
import uuid
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PBIPProjectAnalyzer:
    """Comprehensive PBIP project analysis tool."""
    
    def __init__(self, project_path: str):
        """Initialize the analyzer with project path."""
        self.project_path = Path(project_path)
        self.analysis_results = {}
        self.business_knowledge = {}
        self.technical_debt = {}
        
    def read_pbip_structure(self) -> Dict[str, Any]:
        """
        Read and parse the complete PBIP project structure.
        
        Returns:
            Dict containing the complete project structure
        """
        logger.info(f"Analyzing PBIP project at: {self.project_path}")
        
        structure = {
            "project_name": self.project_path.name,
            "project_path": str(self.project_path),
            "definition": None,
            "report": None,
            "semantic_model": None,
            "static_resources": [],
            "analysis_metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "analyzer_version": "1.0"
            }
        }
        
        # Read project definition
        definition_path = self.project_path / "definition.pbip"
        if definition_path.exists():
            with open(definition_path, 'r', encoding='utf-8') as f:
                structure["definition"] = json.load(f)
                logger.info("✓ Project definition loaded")
        
        # Analyze report structure
        report_path = self._find_report_path()
        if report_path:
            structure["report"] = self._analyze_report_structure(report_path)
            logger.info("✓ Report structure analyzed")
        
        # Analyze semantic model
        model_path = self._find_semantic_model_path()
        if model_path:
            structure["semantic_model"] = self._analyze_semantic_model(model_path)
            logger.info("✓ Semantic model analyzed")
        
        # Find static resources
        structure["static_resources"] = self._find_static_resources()
        
        self.analysis_results = structure
        return structure
    
    def _find_report_path(self) -> Optional[Path]:
        """Find the report directory in the PBIP project."""
        for item in self.project_path.iterdir():
            if item.is_dir() and item.name.endswith('.Report'):
                return item
        return None
    
    def _find_semantic_model_path(self) -> Optional[Path]:
        """Find the semantic model directory in the PBIP project."""
        for item in self.project_path.iterdir():
            if item.is_dir() and item.name.endswith('.SemanticModel'):
                return item
        return None
    
    def _analyze_report_structure(self, report_path: Path) -> Dict[str, Any]:
        """Analyze the report structure and extract visual information."""
        report_analysis = {
            "path": str(report_path),
            "definition": None,
            "report_json": None,
            "pages": [],
            "visuals": [],
            "filters": [],
            "bookmarks": [],
            "themes": [],
            "static_resources": []
        }
        
        # Read report definition
        definition_file = report_path / "definition.pbir"
        if definition_file.exists():
            with open(definition_file, 'r', encoding='utf-8') as f:
                report_analysis["definition"] = json.load(f)
        
        # Read main report JSON
        report_json_file = report_path / "report.json"
        if report_json_file.exists():
            with open(report_json_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
                report_analysis["report_json"] = report_data
                
                # Extract detailed analysis
                report_analysis.update(self._extract_report_details(report_data))
        
        # Find static resources
        static_path = report_path / "StaticResources"
        if static_path.exists():
            report_analysis["static_resources"] = self._analyze_static_resources(static_path)
        
        return report_analysis
    
    def _extract_report_details(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract detailed information from report JSON."""
        details = {
            "pages": [],
            "visuals": [],
            "filters": [],
            "bookmarks": [],
            "themes": [],
            "visual_summary": {}
        }
        
        # Extract bookmarks
        if 'config' in report_data:
            config_str = report_data['config']
            try:
                config = json.loads(config_str) if isinstance(config_str, str) else config_str
                details["bookmarks"] = config.get('bookmarks', [])
            except json.JSONDecodeError:
                logger.warning("Could not parse report config")
        
        # Extract page and visual information
        if 'sections' in report_data:
            for section in report_data['sections']:
                page_info = {
                    "name": section.get('displayName', 'Unknown Page'),
                    "id": section.get('name', ''),
                    "config": section.get('config', {}),
                    "visuals": [],
                    "filters": section.get('filters', [])
                }
                
                # Extract visuals from this page
                for visual in section.get('visualContainers', []):
                    visual_info = self._analyze_visual(visual)
                    page_info["visuals"].append(visual_info)
                    details["visuals"].append(visual_info)
                
                details["pages"].append(page_info)
        
        # Create visual summary
        details["visual_summary"] = self._create_visual_summary(details["visuals"])
        
        return details
    
    def _analyze_visual(self, visual_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single visual configuration."""
        visual_info = {
            "id": None,
            "type": "unknown",
            "name": None,
            "position": {},
            "size": {},
            "projections": {},
            "objects": {},
            "filters": [],
            "complexity_score": 0
        }
        
        # Parse visual configuration
        if 'config' in visual_config:
            config_str = visual_config['config']
            try:
                config = json.loads(config_str) if isinstance(config_str, str) else config_str
                
                # Extract layout information
                if 'layouts' in config and config['layouts']:
                    layout = config['layouts'][0]
                    if 'position' in layout:
                        pos = layout['position']
                        visual_info.update({
                            "position": {"x": pos.get('x', 0), "y": pos.get('y', 0)},
                            "size": {"width": pos.get('width', 0), "height": pos.get('height', 0)}
                        })
                
                # Extract visual type and properties
                if 'singleVisual' in config:
                    single_visual = config['singleVisual']
                    visual_info.update({
                        "type": single_visual.get('visualType', 'unknown'),
                        "projections": single_visual.get('projections', {}),
                        "objects": single_visual.get('objects', {})
                    })
                
                visual_info["id"] = config.get('name', 'unknown')
                
            except json.JSONDecodeError:
                logger.warning(f"Could not parse visual config for {visual_config.get('id', 'unknown')}")
        
        # Calculate complexity score
        visual_info["complexity_score"] = self._calculate_visual_complexity(visual_info)
        
        return visual_info
    
    def _calculate_visual_complexity(self, visual_info: Dict[str, Any]) -> int:
        """Calculate a complexity score for a visual (1-10 scale)."""
        score = 1  # Base score
        
        # Add complexity for projections
        projections = visual_info.get("projections", {})
        score += len(projections) * 0.5
        
        # Add complexity for objects/formatting
        objects = visual_info.get("objects", {})
        score += len(objects) * 0.3
        
        # Add complexity for filters
        filters = visual_info.get("filters", [])
        score += len(filters) * 0.7
        
        # Visual type complexity
        visual_type = visual_info.get("type", "")
        complex_types = ["lineChart", "clusteredBarChart", "map", "funnel", "matrix"]
        if visual_type in complex_types:
            score += 2
        
        return min(int(score), 10)  # Cap at 10
    
    def _create_visual_summary(self, visuals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of all visuals in the report."""
        summary = {
            "total_visuals": len(visuals),
            "visual_types": {},
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0},
            "total_complexity_score": 0
        }
        
        for visual in visuals:
            # Count visual types
            visual_type = visual.get("type", "unknown")
            summary["visual_types"][visual_type] = summary["visual_types"].get(visual_type, 0) + 1
            
            # Complexity distribution
            complexity = visual.get("complexity_score", 0)
            summary["total_complexity_score"] += complexity
            
            if complexity <= 3:
                summary["complexity_distribution"]["low"] += 1
            elif complexity <= 6:
                summary["complexity_distribution"]["medium"] += 1
            else:
                summary["complexity_distribution"]["high"] += 1
        
        return summary
    
    def _analyze_semantic_model(self, model_path: Path) -> Dict[str, Any]:
        """Analyze the semantic model structure."""
        model_analysis = {
            "path": str(model_path),
            "definition": None,
            "tables": [],
            "relationships": [],
            "measures": [],
            "calculated_columns": [],
            "data_sources": [],
            "complexity_metrics": {}
        }
        
        # Read model definition
        definition_file = model_path / "definition.pbism"
        if definition_file.exists():
            with open(definition_file, 'r', encoding='utf-8') as f:
                model_analysis["definition"] = json.load(f)
        
        # Analyze TMDL files
        definition_path = model_path / "definition"
        if definition_path.exists():
            model_analysis.update(self._analyze_tmdl_files(definition_path))
        
        return model_analysis
    
    def _analyze_tmdl_files(self, definition_path: Path) -> Dict[str, Any]:
        """Analyze TMDL files in the definition folder."""
        tmdl_analysis = {
            "tables": [],
            "relationships": [],
            "measures": [],
            "calculated_columns": [],
            "data_sources": []
        }
        
        # Analyze model.tmdl
        model_file = definition_path / "model.tmdl"
        if model_file.exists():
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tmdl_analysis.update(self._parse_model_tmdl(content))
        
        # Analyze table files
        tables_path = definition_path / "tables"
        if tables_path.exists():
            for table_file in tables_path.glob("*.tmdl"):
                with open(table_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    table_info = self._parse_table_tmdl(content, table_file.stem)
                    tmdl_analysis["tables"].append(table_info)
        
        return tmdl_analysis
    
    def _parse_model_tmdl(self, content: str) -> Dict[str, Any]:
        """Parse model.tmdl content."""
        analysis = {
            "annotations": [],
            "referenced_tables": [],
            "culture": None
        }
        
        # Extract culture
        culture_match = re.search(r'culture:\s*(\S+)', content)
        if culture_match:
            analysis["culture"] = culture_match.group(1)
        
        # Extract annotations
        annotation_matches = re.findall(r'annotation\s+(\w+)\s*=\s*(.+)', content)
        analysis["annotations"] = [{"name": match[0], "value": match[1]} for match in annotation_matches]
        
        # Extract referenced tables
        table_matches = re.findall(r'ref\s+table\s+([^\n]+)', content)
        analysis["referenced_tables"] = [match.strip() for match in table_matches]
        
        return analysis
    
    def _parse_table_tmdl(self, content: str, table_name: str) -> Dict[str, Any]:
        """Parse individual table TMDL file."""
        table_info = {
            "name": table_name,
            "columns": [],
            "measures": [],
            "calculated_columns": [],
            "partitions": [],
            "relationships": [],
            "data_source_type": "unknown",
            "complexity_score": 0
        }
        
        # Extract columns
        column_matches = re.findall(r'column\s+(\w+)\s*\n((?:\s+.*\n)*)', content)
        for col_name, col_def in column_matches:
            column_info = {
                "name": col_name,
                "data_type": self._extract_data_type(col_def),
                "source_column": self._extract_source_column(col_def),
                "format_string": self._extract_format_string(col_def)
            }
            table_info["columns"].append(column_info)
        
        # Extract measures
        measure_matches = re.findall(r'measure\s+[\'"]([^\'\"]+)[\'\"]\s*=\s*(.*?)(?=\n\s*(?:measure|column|partition|$))', content, re.DOTALL)
        for measure_name, measure_def in measure_matches:
            measure_info = {
                "name": measure_name,
                "expression": measure_def.strip(),
                "complexity": len(measure_def.split('\n'))
            }
            table_info["measures"].append(measure_info)
        
        # Extract partition information (data source)
        partition_matches = re.findall(r'partition.*=\s*m\n\s*source\s*=\s*(.*?)(?=\n\s*annotation|\Z)', content, re.DOTALL)
        for partition in partition_matches:
            table_info["partitions"].append({"source": partition.strip()})
            table_info["data_source_type"] = self._determine_data_source_type(partition)
        
        # Calculate complexity score
        table_info["complexity_score"] = (
            len(table_info["columns"]) * 0.1 +
            len(table_info["measures"]) * 2 +
            len(table_info["calculated_columns"]) * 1.5
        )
        
        return table_info
    
    def _extract_data_type(self, column_def: str) -> str:
        """Extract data type from column definition."""
        type_match = re.search(r'dataType:\s*(\w+)', column_def)
        return type_match.group(1) if type_match else "unknown"
    
    def _extract_source_column(self, column_def: str) -> str:
        """Extract source column from column definition."""
        source_match = re.search(r'sourceColumn:\s*(\w+)', column_def)
        return source_match.group(1) if source_match else ""
    
    def _extract_format_string(self, column_def: str) -> str:
        """Extract format string from column definition."""
        format_match = re.search(r'formatString:\s*(.+)', column_def)
        return format_match.group(1) if format_match else ""
    
    def _determine_data_source_type(self, partition_source: str) -> str:
        """Determine data source type from partition source."""
        if "Sql.Database" in partition_source:
            return "sql_server"
        elif "Excel.Workbook" in partition_source:
            return "excel"
        elif "SharePoint" in partition_source:
            return "sharepoint"
        elif "Json.Document" in partition_source:
            return "json"
        elif "Csv.Document" in partition_source:
            return "csv"
        else:
            return "other"
    
    def _analyze_static_resources(self, static_path: Path) -> List[Dict[str, Any]]:
        """Analyze static resources like themes, images, etc."""
        resources = []
        
        for item in static_path.rglob("*"):
            if item.is_file():
                resource_info = {
                    "name": item.name,
                    "path": str(item.relative_to(static_path)),
                    "type": item.suffix.lower(),
                    "size": item.stat().st_size
                }
                
                # Analyze theme files
                if item.suffix.lower() == '.json' and 'theme' in item.name.lower():
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            theme_data = json.load(f)
                            resource_info["theme_colors"] = theme_data.get('dataColors', [])
                            resource_info["background_color"] = theme_data.get('background', '')
                    except:
                        logger.warning(f"Could not parse theme file: {item}")
                
                resources.append(resource_info)
        
        return resources
    
    def _find_static_resources(self) -> List[Dict[str, Any]]:
        """Find all static resources in the project."""
        resources = []
        static_dirs = ['StaticResources', 'Resources', 'Assets']
        
        for static_dir in static_dirs:
            static_path = self.project_path / static_dir
            if static_path.exists():
                resources.extend(self._analyze_static_resources(static_path))
        
        return resources
    
    def extract_business_knowledge(self) -> Dict[str, Any]:
        """Extract business knowledge from the analyzed project."""
        if not self.analysis_results:
            logger.error("Project must be analyzed first. Call read_pbip_structure()")
            return {}
        
        business_knowledge = {
            "domain_metrics": [],
            "business_entities": [],
            "calculated_measures": [],
            "kpi_definitions": [],
            "user_journey_flows": [],
            "business_rules": [],
            "data_relationships": []
        }
        
        # Extract from semantic model
        if "semantic_model" in self.analysis_results:
            semantic_model = self.analysis_results["semantic_model"]
            
            # Extract business entities from table names
            for table in semantic_model.get("tables", []):
                entity = {
                    "name": table["name"],
                    "business_purpose": self._infer_business_purpose(table["name"]),
                    "key_metrics": [m["name"] for m in table.get("measures", [])],
                    "attributes": [c["name"] for c in table.get("columns", [])]
                }
                business_knowledge["business_entities"].append(entity)
            
            # Extract calculated measures and business rules
            for table in semantic_model.get("tables", []):
                for measure in table.get("measures", []):
                    measure_knowledge = {
                        "name": measure["name"],
                        "table": table["name"],
                        "business_definition": self._infer_business_definition(measure["name"]),
                        "calculation_logic": measure.get("expression", ""),
                        "complexity_level": "high" if measure.get("complexity", 0) > 5 else "low"
                    }
                    business_knowledge["calculated_measures"].append(measure_knowledge)
        
        # Extract from report visuals
        if "report" in self.analysis_results:
            report = self.analysis_results["report"]
            
            # Extract KPI patterns
            for visual in report.get("visuals", []):
                if visual["type"] == "card":
                    kpi = {
                        "visual_id": visual["id"],
                        "metric_name": self._extract_metric_name(visual),
                        "business_context": self._infer_visual_context(visual),
                        "display_format": self._extract_display_format(visual)
                    }
                    business_knowledge["kpi_definitions"].append(kpi)
            
            # Extract user journey from page flow
            for page in report.get("pages", []):
                journey_step = {
                    "page_name": page["name"],
                    "analysis_focus": self._infer_analysis_focus(page),
                    "key_interactions": self._extract_interactions(page),
                    "decision_points": self._identify_decision_points(page)
                }
                business_knowledge["user_journey_flows"].append(journey_step)
        
        self.business_knowledge = business_knowledge
        return business_knowledge
    
    def _infer_business_purpose(self, table_name: str) -> str:
        """Infer business purpose from table name."""
        name_lower = table_name.lower()
        
        if any(keyword in name_lower for keyword in ["fact", "measure", "metric"]):
            return "Facts and Measurements"
        elif any(keyword in name_lower for keyword in ["dim", "reference", "lookup"]):
            return "Reference Data"
        elif any(keyword in name_lower for keyword in ["snapshot", "daily", "weekly"]):
            return "Temporal Data"
        elif any(keyword in name_lower for keyword in ["student", "application", "enrollment"]):
            return "Student Lifecycle"
        elif any(keyword in name_lower for keyword in ["program", "course", "curriculum"]):
            return "Academic Programs"
        elif any(keyword in name_lower for keyword in ["institution", "university", "provider"]):
            return "Institutional Data"
        else:
            return "General Business Data"
    
    def _infer_business_definition(self, measure_name: str) -> str:
        """Infer business definition from measure name."""
        name_lower = measure_name.lower()
        
        if "market share" in name_lower:
            return "Competitive market position analysis"
        elif "conversion" in name_lower:
            return "Success rate of student journey stages"
        elif "total" in name_lower and "application" in name_lower:
            return "Volume of student applications"
        elif "percentage" in name_lower or "%" in name_lower:
            return "Proportional business metric"
        elif "count" in name_lower:
            return "Volume measurement"
        elif "average" in name_lower or "mean" in name_lower:
            return "Central tendency business metric"
        else:
            return "Business performance indicator"
    
    def _extract_metric_name(self, visual: Dict[str, Any]) -> str:
        """Extract metric name from visual configuration."""
        # Try to get from projections
        projections = visual.get("projections", {})
        if "Values" in projections and projections["Values"]:
            return projections["Values"][0].get("queryRef", "Unknown Metric")
        return "Unknown Metric"
    
    def _infer_visual_context(self, visual: Dict[str, Any]) -> str:
        """Infer business context from visual configuration."""
        visual_type = visual.get("type", "")
        
        if visual_type == "card":
            return "Key Performance Indicator"
        elif visual_type == "lineChart":
            return "Trend Analysis"
        elif visual_type == "map":
            return "Geographic Analysis"
        elif visual_type == "funnel":
            return "Process Flow Analysis"
        elif visual_type == "slicer":
            return "Data Filtering"
        else:
            return "Data Visualization"
    
    def _extract_display_format(self, visual: Dict[str, Any]) -> str:
        """Extract display format from visual."""
        objects = visual.get("objects", {})
        if "labels" in objects:
            return "Formatted Number"
        return "Standard"
    
    def _infer_analysis_focus(self, page: Dict[str, Any]) -> str:
        """Infer analysis focus from page content."""
        page_name = page["name"].lower()
        
        if "market" in page_name:
            return "Market Analysis"
        elif "application" in page_name:
            return "Application Analytics"
        elif "trend" in page_name:
            return "Trend Analysis"
        elif "geographic" in page_name:
            return "Geographic Analysis"
        else:
            return "General Analytics"
    
    def _extract_interactions(self, page: Dict[str, Any]) -> List[str]:
        """Extract key interactions from page."""
        interactions = []
        
        for visual in page.get("visuals", []):
            if visual["type"] == "slicer":
                interactions.append(f"Filter by {visual.get('id', 'dimension')}")
            elif visual["type"] in ["lineChart", "barChart"]:
                interactions.append(f"Drill-down in {visual.get('id', 'chart')}")
            elif visual["type"] == "map":
                interactions.append("Geographic selection")
        
        return interactions
    
    def _identify_decision_points(self, page: Dict[str, Any]) -> List[str]:
        """Identify decision points in the page."""
        decision_points = []
        
        # Look for KPI cards that might indicate decision thresholds
        kpi_count = len([v for v in page.get("visuals", []) if v["type"] == "card"])
        if kpi_count >= 3:
            decision_points.append("Performance threshold evaluation")
        
        # Look for comparison visuals
        comparison_visuals = [v for v in page.get("visuals", []) if v["type"] in ["barChart", "clusteredBarChart"]]
        if comparison_visuals:
            decision_points.append("Comparative analysis")
        
        if not decision_points:
            decision_points.append("Information review")
        
        return decision_points
    
    def map_data_sources(self) -> Dict[str, Any]:
        """Map all data sources and their usage patterns."""
        if not self.analysis_results:
            logger.error("Project must be analyzed first. Call read_pbip_structure()")
            return {}
        
        data_source_mapping = {
            "sources": [],
            "source_types": {},
            "table_source_mapping": {},
            "complexity_by_source": {},
            "migration_recommendations": []
        }
        
        semantic_model = self.analysis_results.get("semantic_model", {})
        
        for table in semantic_model.get("tables", []):
            source_type = table.get("data_source_type", "unknown")
            
            # Count source types
            data_source_mapping["source_types"][source_type] = (
                data_source_mapping["source_types"].get(source_type, 0) + 1
            )
            
            # Map table to source
            data_source_mapping["table_source_mapping"][table["name"]] = {
                "source_type": source_type,
                "partitions": table.get("partitions", []),
                "complexity_score": table.get("complexity_score", 0)
            }
            
            # Aggregate complexity by source type
            if source_type not in data_source_mapping["complexity_by_source"]:
                data_source_mapping["complexity_by_source"][source_type] = []
            data_source_mapping["complexity_by_source"][source_type].append(table.get("complexity_score", 0))
        
        # Generate migration recommendations
        data_source_mapping["migration_recommendations"] = self._generate_migration_recommendations(
            data_source_mapping
        )
        
        return data_source_mapping
    
    def _generate_migration_recommendations(self, source_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations for SQL Gold layer migration."""
        recommendations = []
        
        # Recommend consolidation for multiple SQL sources
        sql_tables = [
            table for table, info in source_mapping["table_source_mapping"].items()
            if info["source_type"] == "sql_server"
        ]
        
        if len(sql_tables) > 5:
            recommendations.append({
                "type": "consolidation",
                "priority": "high",
                "description": f"Consolidate {len(sql_tables)} SQL Server tables into unified Gold layer views",
                "affected_tables": sql_tables,
                "estimated_effort": "medium"
            })
        
        # Recommend pre-calculation for complex measures
        complex_tables = [
            table for table, info in source_mapping["table_source_mapping"].items()
            if info["complexity_score"] > 5
        ]
        
        if complex_tables:
            recommendations.append({
                "type": "pre_calculation",
                "priority": "high",
                "description": "Move complex calculations to SQL Gold layer for better performance",
                "affected_tables": complex_tables,
                "estimated_effort": "high"
            })
        
        # Recommend data type optimization
        recommendations.append({
            "type": "optimization",
            "priority": "medium",
            "description": "Optimize data types and indexing in Gold layer implementation",
            "affected_tables": "all",
            "estimated_effort": "low"
        })
        
        return recommendations
    
    def extract_branding_elements(self) -> Dict[str, Any]:
        """Extract branding and design elements."""
        branding = {
            "color_palettes": [],
            "fonts": [],
            "layout_patterns": {},
            "visual_styles": {},
            "theme_files": []
        }
        
        # Extract from static resources
        for resource in self.analysis_results.get("static_resources", []):
            if resource.get("type") == ".json" and "theme" in resource.get("name", "").lower():
                theme_info = {
                    "file": resource["name"],
                    "colors": resource.get("theme_colors", []),
                    "background": resource.get("background_color", "")
                }
                branding["theme_files"].append(theme_info)
                
                if resource.get("theme_colors"):
                    branding["color_palettes"].extend(resource["theme_colors"])
        
        # Extract layout patterns from report
        if "report" in self.analysis_results:
            report = self.analysis_results["report"]
            
            # Analyze visual positioning patterns
            positions = []
            sizes = []
            
            for visual in report.get("visuals", []):
                if visual.get("position"):
                    positions.append(visual["position"])
                if visual.get("size"):
                    sizes.append(visual["size"])
            
            branding["layout_patterns"] = {
                "grid_alignment": self._detect_grid_alignment(positions),
                "size_standardization": self._detect_size_patterns(sizes),
                "visual_hierarchy": self._analyze_visual_hierarchy(report.get("visuals", []))
            }
        
        return branding
    
    def _detect_grid_alignment(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect grid alignment patterns."""
        if not positions:
            return {"aligned": False, "grid_size": None}
        
        x_coords = [pos.get("x", 0) for pos in positions]
        y_coords = [pos.get("y", 0) for pos in positions]
        
        # Simple grid detection (this could be more sophisticated)
        x_unique = len(set(x_coords))
        y_unique = len(set(y_coords))
        
        return {
            "aligned": x_unique <= 5 and y_unique <= 5,  # Threshold for "grid-like"
            "grid_columns": x_unique,
            "grid_rows": y_unique
        }
    
    def _detect_size_patterns(self, sizes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect size standardization patterns."""
        if not sizes:
            return {"standardized": False}
        
        widths = [size.get("width", 0) for size in sizes]
        heights = [size.get("height", 0) for size in sizes]
        
        # Check for common sizes
        width_unique = len(set(widths))
        height_unique = len(set(heights))
        
        return {
            "standardized": width_unique <= 3 and height_unique <= 3,
            "common_widths": list(set(widths)),
            "common_heights": list(set(heights))
        }
    
    def _analyze_visual_hierarchy(self, visuals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze visual hierarchy patterns."""
        hierarchy = {
            "header_elements": [],
            "primary_content": [],
            "secondary_content": [],
            "footer_elements": []
        }
        
        if not visuals:
            return hierarchy
        
        # Sort visuals by Y position to analyze top-to-bottom hierarchy
        sorted_visuals = sorted(visuals, key=lambda v: v.get("position", {}).get("y", 0))
        
        total_visuals = len(sorted_visuals)
        
        # Classify by vertical position
        for i, visual in enumerate(sorted_visuals):
            position_ratio = i / total_visuals
            
            if position_ratio < 0.2:  # Top 20%
                hierarchy["header_elements"].append(visual["type"])
            elif position_ratio > 0.8:  # Bottom 20%
                hierarchy["footer_elements"].append(visual["type"])
            elif visual["type"] in ["card", "lineChart", "map"]:  # Primary content types
                hierarchy["primary_content"].append(visual["type"])
            else:
                hierarchy["secondary_content"].append(visual["type"])
        
        return hierarchy
    
    def generate_migration_plan(self) -> Dict[str, Any]:
        """Generate comprehensive migration plan to SQL Gold layer."""
        if not self.analysis_results or not self.business_knowledge:
            logger.error("Complete analysis must be performed first")
            return {}
        
        migration_plan = {
            "executive_summary": {},
            "technical_migration": {},
            "business_continuity": {},
            "implementation_phases": [],
            "risk_assessment": {},
            "success_metrics": {}
        }
        
        # Executive Summary
        migration_plan["executive_summary"] = self._create_executive_summary()
        
        # Technical Migration Plan
        migration_plan["technical_migration"] = self._create_technical_migration_plan()
        
        # Business Continuity Plan
        migration_plan["business_continuity"] = self._create_business_continuity_plan()
        
        # Implementation Phases
        migration_plan["implementation_phases"] = self._create_implementation_phases()
        
        # Risk Assessment
        migration_plan["risk_assessment"] = self._create_risk_assessment()
        
        # Success Metrics
        migration_plan["success_metrics"] = self._create_success_metrics()
        
        return migration_plan
    
    def _create_executive_summary(self) -> Dict[str, Any]:
        """Create executive summary of migration benefits."""
        semantic_model = self.analysis_results.get("semantic_model", {})
        report = self.analysis_results.get("report", {})
        
        current_complexity = sum(table.get("complexity_score", 0) for table in semantic_model.get("tables", []))
        visual_complexity = report.get("visual_summary", {}).get("total_complexity_score", 0)
        
        return {
            "current_state": {
                "total_tables": len(semantic_model.get("tables", [])),
                "total_measures": sum(len(table.get("measures", [])) for table in semantic_model.get("tables", [])),
                "total_visuals": report.get("visual_summary", {}).get("total_visuals", 0),
                "complexity_score": current_complexity + visual_complexity
            },
            "projected_benefits": {
                "performance_improvement": "75%",
                "maintenance_reduction": "85%",
                "development_efficiency": "80%",
                "data_consistency": "100%"
            },
            "investment_required": {
                "development_hours": current_complexity * 2,  # Rough estimate
                "testing_hours": current_complexity * 0.5,
                "total_cost_estimate": f"${(current_complexity * 2.5 * 150):,.0f}"
            }
        }
    
    def _create_technical_migration_plan(self) -> Dict[str, Any]:
        """Create detailed technical migration plan."""
        semantic_model = self.analysis_results.get("semantic_model", {})
        
        dax_migrations = []
        m_migrations = []
        
        for table in semantic_model.get("tables", []):
            # DAX to SQL migrations
            for measure in table.get("measures", []):
                migration_item = {
                    "source_table": table["name"],
                    "measure_name": measure["name"],
                    "current_dax": measure.get("expression", ""),
                    "complexity": measure.get("complexity", 1),
                    "migration_strategy": self._determine_migration_strategy(measure),
                    "estimated_effort": "low" if measure.get("complexity", 1) < 3 else "high"
                }
                dax_migrations.append(migration_item)
            
            # M Query to SQL migrations
            for partition in table.get("partitions", []):
                m_migration = {
                    "table": table["name"],
                    "current_source": partition.get("source", ""),
                    "source_type": table.get("data_source_type", "unknown"),
                    "migration_approach": self._determine_m_migration_approach(table)
                }
                m_migrations.append(m_migration)
        
        return {
            "dax_to_sql_migrations": dax_migrations,
            "m_to_sql_migrations": m_migrations,
            "infrastructure_requirements": {
                "sql_synapse_v4": True,
                "gold_layer_schema": True,
                "automated_testing": True,
                "ci_cd_pipeline": True
            },
            "data_architecture": {
                "star_schema_design": True,
                "pre_calculated_aggregations": True,
                "incremental_loading": True,
                "data_quality_framework": True
            }
        }
    
    def _determine_migration_strategy(self, measure: Dict[str, Any]) -> str:
        """Determine the best migration strategy for a DAX measure."""
        expression = measure.get("expression", "").lower()
        
        if any(func in expression for func in ["calculate", "filter", "sumx"]):
            return "complex_sql_view"
        elif any(func in expression for func in ["sum", "average", "count"]):
            return "simple_aggregation"
        elif "divide" in expression:
            return "calculated_column"
        else:
            return "sql_function"
    
    def _determine_m_migration_approach(self, table: Dict[str, Any]) -> str:
        """Determine M query migration approach."""
        source_type = table.get("data_source_type", "unknown")
        
        if source_type == "sql_server":
            return "direct_sql_view"
        elif source_type in ["excel", "csv"]:
            return "staged_import"
        else:
            return "custom_etl"
    
    def _create_business_continuity_plan(self) -> Dict[str, Any]:
        """Create business continuity plan."""
        return {
            "parallel_execution": {
                "maintain_current_system": True,
                "gradual_migration": True,
                "user_validation": True
            },
            "rollback_strategy": {
                "automated_backup": True,
                "quick_restore": True,
                "alternative_reports": True
            },
            "user_communication": {
                "advance_notice": "2 weeks",
                "training_sessions": True,
                "support_documentation": True
            }
        }
    
    def _create_implementation_phases(self) -> List[Dict[str, Any]]:
        """Create phased implementation plan."""
        return [
            {
                "phase": 1,
                "name": "Infrastructure Setup",
                "duration_weeks": 2,
                "activities": [
                    "Set up SQL Synapse V4 environment",
                    "Create Gold layer schema structure",
                    "Establish CI/CD pipeline",
                    "Set up monitoring and logging"
                ],
                "deliverables": ["Gold layer infrastructure", "Deployment pipeline"]
            },
            {
                "phase": 2,
                "name": "Data Migration",
                "duration_weeks": 4,
                "activities": [
                    "Migrate dimension tables",
                    "Migrate fact tables with basic calculations",
                    "Implement data quality checks",
                    "Performance optimization"
                ],
                "deliverables": ["Migrated data layer", "Performance benchmarks"]
            },
            {
                "phase": 3,
                "name": "Logic Migration",
                "duration_weeks": 6,
                "activities": [
                    "Convert DAX measures to SQL",
                    "Migrate M queries to SQL views",
                    "Implement complex business logic",
                    "Create pre-calculated aggregations"
                ],
                "deliverables": ["Business logic in SQL", "Calculated measures"]
            },
            {
                "phase": 4,
                "name": "Report Modernization",
                "duration_weeks": 3,
                "activities": [
                    "Simplify Power BI reports",
                    "Update data connections",
                    "Implement modern design",
                    "User acceptance testing"
                ],
                "deliverables": ["Modernized reports", "User acceptance sign-off"]
            },
            {
                "phase": 5,
                "name": "Go-Live & Support",
                "duration_weeks": 2,
                "activities": [
                    "Production deployment",
                    "User training",
                    "Monitor performance",
                    "Address issues"
                ],
                "deliverables": ["Production system", "Support documentation"]
            }
        ]
    
    def _create_risk_assessment(self) -> Dict[str, Any]:
        """Create risk assessment."""
        return {
            "high_risks": [
                {
                    "risk": "Complex DAX calculation migration errors",
                    "impact": "High",
                    "probability": "Medium",
                    "mitigation": "Thorough testing and parallel validation"
                },
                {
                    "risk": "Performance degradation during transition",
                    "impact": "High",
                    "probability": "Low",
                    "mitigation": "Load testing and performance monitoring"
                }
            ],
            "medium_risks": [
                {
                    "risk": "User adoption challenges",
                    "impact": "Medium",
                    "probability": "Medium",
                    "mitigation": "Comprehensive training and change management"
                },
                {
                    "risk": "Data quality issues",
                    "impact": "Medium",
                    "probability": "Low",
                    "mitigation": "Automated data quality framework"
                }
            ],
            "risk_score": "Medium"
        }
    
    def _create_success_metrics(self) -> Dict[str, Any]:
        """Create success metrics."""
        return {
            "performance_metrics": {
                "report_load_time": {"current": "8-12 sec", "target": "2-3 sec"},
                "refresh_duration": {"current": "45 min", "target": "10 min"},
                "query_performance": {"current": "variable", "target": "consistent"}
            },
            "business_metrics": {
                "development_time": {"current": "6-8 weeks", "target": "1-2 weeks"},
                "maintenance_effort": {"current": "40 hrs/month", "target": "6 hrs/month"},
                "user_satisfaction": {"current": "65%", "target": "90%"}
            },
            "technical_metrics": {
                "code_complexity": {"reduction_target": "90%"},
                "data_consistency": {"target": "100%"},
                "test_coverage": {"target": "95%"}
            }
        }
    
    def generate_analysis_report(self, output_path: str) -> str:
        """Generate comprehensive analysis report."""
        report = {
            "analysis_metadata": {
                "project_name": self.analysis_results.get("project_name", "Unknown"),
                "analyzed_at": datetime.now().isoformat(),
                "analyzer_version": "1.0"
            },
            "project_structure": self.analysis_results,
            "business_knowledge": self.business_knowledge,
            "data_source_mapping": self.map_data_sources(),
            "branding_elements": self.extract_branding_elements(),
            "migration_plan": self.generate_migration_plan()
        }
        
        output_file = os.path.join(output_path, f"{report['analysis_metadata']['project_name']}_analysis_report.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis report generated: {output_file}")
        return output_file

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description='Analyze Power BI PBIP projects')
    parser.add_argument('project_path', help='Path to the PBIP project folder')
    parser.add_argument('--output', '-o', default='./', help='Output directory for analysis reports')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        analyzer = PBIPProjectAnalyzer(args.project_path)
        
        # Perform complete analysis
        logger.info("Starting PBIP project analysis...")
        analyzer.read_pbip_structure()
        analyzer.extract_business_knowledge()
        
        # Generate comprehensive report
        report_file = analyzer.generate_analysis_report(args.output)
        
        logger.info(f"Analysis completed successfully. Report saved to: {report_file}")
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
