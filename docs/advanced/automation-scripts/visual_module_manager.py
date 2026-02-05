#!/usr/bin/env python3
"""
Visual Module Manager for Power BI PBIP Projects
This script provides automated tools for managing visual modules in Power BI PBIP projects.

Usage:
    python visual_module_manager.py extract --source report.json --output modules/
    python visual_module_manager.py replace --target report.json --module modules/kpi/revenue-card.json
    python visual_module_manager.py backup --project-path ./
    python visual_module_manager.py validate --module modules/charts/trend-line.json

Author: _[Team/Individual]_
Version: 1.0
Created: _[Date]_
"""

import json
import os
import sys
import argparse
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('visual_module_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VisualModuleManager:
    """Main class for managing Power BI visual modules."""
    
    def __init__(self, project_path: str = "./"):
        """
        Initialize the Visual Module Manager.
        
        Args:
            project_path (str): Path to the Power BI PBIP project root
        """
        self.project_path = project_path
        self.modules_path = os.path.join(project_path, "modules")
        self.backups_path = os.path.join(project_path, "backups")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.modules_path,
            self.backups_path,
            os.path.join(self.modules_path, "kpi"),
            os.path.join(self.modules_path, "charts"),
            os.path.join(self.modules_path, "filters"),
            os.path.join(self.modules_path, "layouts"),
            os.path.join(self.modules_path, "scripts")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def extract_visual_as_module(self, report_file: str, visual_id: str, output_path: str, module_metadata: Dict[str, Any]) -> bool:
        """
        Extract a visual from a Power BI report and save as a module.
        
        Args:
            report_file (str): Path to the Power BI report JSON file
            visual_id (str): ID of the visual to extract
            output_path (str): Path where to save the extracted module
            module_metadata (Dict): Metadata for the module
            
        Returns:
            bool: True if extraction successful, False otherwise
        """
        try:
            # Load the report JSON
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # Find the visual in the report
            visual_config = None
            for section in report_data.get('sections', []):
                for visual in section.get('visualContainers', []):
                    if visual.get('config', {}).get('name') == visual_id:
                        visual_config = visual
                        break
                if visual_config:
                    break
            
            if not visual_config:
                logger.error(f"Visual with ID '{visual_id}' not found in report")
                return False
            
            # Create module structure
            module = {
                "module": {
                    "name": module_metadata.get("name", f"Extracted Visual {visual_id}"),
                    "type": self._determine_visual_type(visual_config),
                    "category": module_metadata.get("category", "extracted"),
                    "description": module_metadata.get("description", "Extracted from existing report"),
                    "version": "1.0",
                    "author": module_metadata.get("author", "Visual Module Manager"),
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "dependencies": module_metadata.get("dependencies", []),
                    "measures_required": module_metadata.get("measures_required", []),
                    "config": visual_config.get("config", {}),
                    "organizational_branding": module_metadata.get("organizational_branding", {}),
                    "responsive_behavior": module_metadata.get("responsive_behavior", {}),
                    "accessibility": module_metadata.get("accessibility", {}),
                    "usage_notes": module_metadata.get("usage_notes", {}),
                    "customization_options": module_metadata.get("customization_options", {})
                }
            }
            
            # Save the module
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(module, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully extracted visual '{visual_id}' as module: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error extracting visual as module: {str(e)}")
            return False
    
    def replace_visual_with_module(self, report_file: str, visual_id: str, module_file: str) -> bool:
        """
        Replace a visual in a Power BI report with a module.
        
        Args:
            report_file (str): Path to the Power BI report JSON file
            visual_id (str): ID of the visual to replace
            module_file (str): Path to the module file
            
        Returns:
            bool: True if replacement successful, False otherwise
        """
        try:
            # Create backup first
            backup_path = self.create_backup(report_file)
            if not backup_path:
                logger.error("Failed to create backup, aborting replacement")
                return False
            
            # Load the report JSON
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # Load the module
            with open(module_file, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
            
            # Find and replace the visual
            visual_replaced = False
            for section in report_data.get('sections', []):
                for i, visual in enumerate(section.get('visualContainers', [])):
                    if visual.get('config', {}).get('name') == visual_id:
                        # Preserve the visual ID and position
                        original_config = visual.get('config', {})
                        module_config = module_data.get('module', {}).get('config', {})
                        
                        # Merge configurations
                        new_config = {**module_config}
                        new_config['name'] = original_config.get('name', visual_id)
                        
                        # Preserve positioning if it exists
                        if 'layouts' in original_config:
                            new_config['layouts'] = original_config['layouts']
                        
                        visual['config'] = new_config
                        visual_replaced = True
                        break
                if visual_replaced:
                    break
            
            if not visual_replaced:
                logger.error(f"Visual with ID '{visual_id}' not found in report")
                return False
            
            # Save the updated report
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully replaced visual '{visual_id}' with module: {module_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error replacing visual with module: {str(e)}")
            return False
    
    def add_visual_from_module(self, report_file: str, module_file: str, section_index: int = 0, position: Dict[str, int] = None) -> str:
        """
        Add a new visual to a Power BI report from a module.
        
        Args:
            report_file (str): Path to the Power BI report JSON file
            module_file (str): Path to the module file
            section_index (int): Index of the section to add the visual to
            position (Dict): Position configuration for the visual
            
        Returns:
            str: The ID of the newly added visual, or None if failed
        """
        try:
            # Create backup first
            backup_path = self.create_backup(report_file)
            if not backup_path:
                logger.error("Failed to create backup, aborting visual addition")
                return None
            
            # Load the report JSON
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            # Load the module
            with open(module_file, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
            
            # Generate unique visual ID
            visual_id = f"visual_{uuid.uuid4().hex[:8]}"
            
            # Create visual container from module
            module_config = module_data.get('module', {}).get('config', {})
            visual_container = {
                "config": {
                    **module_config,
                    "name": visual_id
                }
            }
            
            # Add position if specified
            if position:
                if 'layouts' not in visual_container['config']:
                    visual_container['config']['layouts'] = [{}]
                visual_container['config']['layouts'][0].update(position)
            
            # Add to the specified section
            if len(report_data.get('sections', [])) > section_index:
                if 'visualContainers' not in report_data['sections'][section_index]:
                    report_data['sections'][section_index]['visualContainers'] = []
                report_data['sections'][section_index]['visualContainers'].append(visual_container)
            else:
                logger.error(f"Section index {section_index} does not exist in report")
                return None
            
            # Save the updated report
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully added visual '{visual_id}' from module: {module_file}")
            return visual_id
            
        except Exception as e:
            logger.error(f"Error adding visual from module: {str(e)}")
            return None
    
    def create_backup(self, file_path: str) -> str:
        """
        Create a backup of a file with timestamp.
        
        Args:
            file_path (str): Path to the file to backup
            
        Returns:
            str: Path to the backup file, or None if failed
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            backup_filename = f"{timestamp}_{filename}"
            backup_path = os.path.join(self.backups_path, backup_filename)
            
            shutil.copy2(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return None
    
    def validate_module(self, module_file: str) -> bool:
        """
        Validate a module file structure and content.
        
        Args:
            module_file (str): Path to the module file to validate
            
        Returns:
            bool: True if module is valid, False otherwise
        """
        try:
            with open(module_file, 'r', encoding='utf-8') as f:
                module_data = json.load(f)
            
            # Check required top-level structure
            if 'module' not in module_data:
                logger.error("Module file missing 'module' top-level key")
                return False
            
            module = module_data['module']
            
            # Check required fields
            required_fields = ['name', 'type', 'category', 'version', 'config']
            for field in required_fields:
                if field not in module:
                    logger.error(f"Module missing required field: {field}")
                    return False
            
            # Validate config structure
            config = module.get('config', {})
            if 'visualType' not in config:
                logger.error("Module config missing 'visualType'")
                return False
            
            # Additional validation rules can be added here
            logger.info(f"Module validation successful: {module_file}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in module file: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error validating module: {str(e)}")
            return False
    
    def list_modules(self, category: str = None) -> List[Dict[str, Any]]:
        """
        List available modules, optionally filtered by category.
        
        Args:
            category (str): Optional category filter (kpi, charts, filters, layouts)
            
        Returns:
            List[Dict]: List of module information
        """
        modules = []
        
        try:
            categories = [category] if category else ['kpi', 'charts', 'filters', 'layouts']
            
            for cat in categories:
                cat_path = os.path.join(self.modules_path, cat)
                if not os.path.exists(cat_path):
                    continue
                
                for filename in os.listdir(cat_path):
                    if filename.endswith('.json') and not filename.startswith('_template'):
                        module_path = os.path.join(cat_path, filename)
                        try:
                            with open(module_path, 'r', encoding='utf-8') as f:
                                module_data = json.load(f)
                            
                            module_info = {
                                'file_path': module_path,
                                'category': cat,
                                'filename': filename,
                                **module_data.get('module', {})
                            }
                            modules.append(module_info)
                            
                        except Exception as e:
                            logger.warning(f"Error reading module {module_path}: {str(e)}")
            
            return modules
            
        except Exception as e:
            logger.error(f"Error listing modules: {str(e)}")
            return []
    
    def _determine_visual_type(self, visual_config: Dict[str, Any]) -> str:
        """
        Determine the visual type from the configuration.
        
        Args:
            visual_config (Dict): Visual configuration
            
        Returns:
            str: Visual type string
        """
        config = visual_config.get('config', {})
        visual_type = config.get('visualType', 'unknown')
        return visual_type
    
    def restore_from_backup(self, backup_file: str, target_file: str) -> bool:
        """
        Restore a file from backup.
        
        Args:
            backup_file (str): Path to the backup file
            target_file (str): Path to restore the file to
            
        Returns:
            bool: True if restore successful, False otherwise
        """
        try:
            shutil.copy2(backup_file, target_file)
            logger.info(f"Successfully restored {target_file} from {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from backup: {str(e)}")
            return False

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(description='Visual Module Manager for Power BI PBIP Projects')
    parser.add_argument('--project-path', default='./', help='Path to the PBIP project root')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract a visual as a module')
    extract_parser.add_argument('--source', required=True, help='Source report JSON file')
    extract_parser.add_argument('--visual-id', required=True, help='ID of the visual to extract')
    extract_parser.add_argument('--output', required=True, help='Output module file path')
    extract_parser.add_argument('--name', help='Module name')
    extract_parser.add_argument('--category', help='Module category')
    extract_parser.add_argument('--description', help='Module description')
    
    # Replace command
    replace_parser = subparsers.add_parser('replace', help='Replace a visual with a module')
    replace_parser.add_argument('--target', required=True, help='Target report JSON file')
    replace_parser.add_argument('--visual-id', required=True, help='ID of the visual to replace')
    replace_parser.add_argument('--module', required=True, help='Module file to use for replacement')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a visual from a module')
    add_parser.add_argument('--target', required=True, help='Target report JSON file')
    add_parser.add_argument('--module', required=True, help='Module file to add')
    add_parser.add_argument('--section', type=int, default=0, help='Section index to add to')
    add_parser.add_argument('--x', type=int, help='X position')
    add_parser.add_argument('--y', type=int, help='Y position')
    add_parser.add_argument('--width', type=int, help='Width')
    add_parser.add_argument('--height', type=int, help='Height')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a module file')
    validate_parser.add_argument('--module', required=True, help='Module file to validate')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available modules')
    list_parser.add_argument('--category', help='Filter by category (kpi, charts, filters, layouts)')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create backup of project files')
    backup_parser.add_argument('--file', help='Specific file to backup')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('--backup', required=True, help='Backup file to restore from')
    restore_parser.add_argument('--target', required=True, help='Target file to restore to')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = VisualModuleManager(args.project_path)
    
    # Execute command
    if args.command == 'extract':
        metadata = {
            'name': args.name,
            'category': args.category,
            'description': args.description
        }
        success = manager.extract_visual_as_module(args.source, args.visual_id, args.output, metadata)
        sys.exit(0 if success else 1)
    
    elif args.command == 'replace':
        success = manager.replace_visual_with_module(args.target, args.visual_id, args.module)
        sys.exit(0 if success else 1)
    
    elif args.command == 'add':
        position = None
        if any([args.x, args.y, args.width, args.height]):
            position = {}
            if args.x is not None: position['x'] = args.x
            if args.y is not None: position['y'] = args.y
            if args.width is not None: position['width'] = args.width
            if args.height is not None: position['height'] = args.height
        
        visual_id = manager.add_visual_from_module(args.target, args.module, args.section, position)
        if visual_id:
            print(f"Added visual with ID: {visual_id}")
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == 'validate':
        success = manager.validate_module(args.module)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        modules = manager.list_modules(args.category)
        for module in modules:
            print(f"{module['category']}/{module['filename']}: {module.get('name', 'Unnamed')} (v{module.get('version', 'unknown')})")
    
    elif args.command == 'backup':
        if args.file:
            backup_path = manager.create_backup(args.file)
            sys.exit(0 if backup_path else 1)
        else:
            # Backup all report files in the project
            report_files = []
            for root, dirs, files in os.walk(args.project_path):
                for file in files:
                    if file.endswith('.json') and 'Report' in root:
                        report_files.append(os.path.join(root, file))
            
            success_count = 0
            for file in report_files:
                if manager.create_backup(file):
                    success_count += 1
            
            print(f"Backed up {success_count}/{len(report_files)} files")
            sys.exit(0 if success_count == len(report_files) else 1)
    
    elif args.command == 'restore':
        success = manager.restore_from_backup(args.backup, args.target)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
