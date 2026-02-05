# Quick Start: Visual Modules - Agent Generation Guide

> **Agent Instructions**: This guide provides step-by-step instructions for automatically generating a complete visual module system for Power BI PBIP projects. Follow these instructions to create reusable modules, management scripts, and documentation.

## Overview

This template enables agents to automatically generate:
- **Module Libraries**: KPI cards, charts, filters, and layout templates
- **Management Scripts**: Automated tools for module manipulation
- **Documentation**: Usage guides and implementation instructions
- **Validation Tools**: Quality assurance and testing utilities

## Prerequisites for Agent Implementation

### Required Inputs
- **Project Context**: Business domain, organization name, primary use cases
- **Data Model**: Table names, measure names, key dimensions
- **Branding Guidelines**: Color schemes, fonts, logo requirements
- **User Roles**: Executive, operational, analytical user personas
- **Device Requirements**: Desktop, tablet, mobile responsive needs

### Expected Outputs
```
modules/
├── kpi/                    # Generated KPI module templates
├── charts/                 # Generated chart module templates
├── filters/                # Generated filter module templates
├── layouts/                # Generated layout module templates
└── scripts/                # Generated management and utility scripts
```

## Agent Generation Tasks

### Task 1: Generate KPI Module Library

**Input Template Variables**:
```yaml
organization:
  name: "_[Organization Name]_"
  primary_color: "_[Hex Color Code]_"
  secondary_color: "_[Hex Color Code]_"
  font_family: "_[Font Family Name]_"

measures:
  - name: "_[Measure Name]_"
    format: "_[Number Format: percentage|currency|integer|decimal]_"
    target: "_[Target Value or Expression]_"
    warning_threshold: "_[Warning Level]_"
    data_table: "_[Source Table Name]_"
  
user_roles:
  - executive: "_[High-level summary cards]_"
  - operational: "_[Detailed performance metrics]_"
  - analytical: "_[Trend and variance analysis]_"
```

**Generation Instructions**:
```markdown
FOR EACH MEASURE in measures:
  CREATE three module variants:
  
  1. Standard Card: {measure-name}-card.json
     - Card visual type with organizational branding
     - Conditional formatting based on target/warning thresholds
     - Responsive sizing for desktop/tablet/mobile
     - Accessibility attributes (ARIA labels, high contrast)
  
  2. Gauge Visual: {measure-name}-gauge.json (if applicable for percentage/ratio measures)
     - Gauge visual with target indicators
     - Color coding for performance zones
     - Compact layout for dashboard integration
  
  3. Trend Indicator: {measure-name}-trend.json
     - Card with directional arrow and period comparison
     - Previous period comparison calculation
     - Color-coded trend direction (green/red/gray)

  INCLUDE in each module:
  - Complete Power BI JSON configuration
  - Data binding to specified table and measure
  - Organizational color scheme application
  - Mobile-responsive adaptations
  - Usage notes and placement guidelines
```

**Output Files**:
- `modules/kpi/[measure-name]-card.json`
- `modules/kpi/[measure-name]-gauge.json`
- `modules/kpi/[measure-name]-trend.json`

### Task 2: Generate Chart Module Library

**Input Template Variables**:
```yaml
chart_types:
  - type: "line"
    purpose: "trend_analysis"
    dimensions: ["_[Time Dimension]_", "_[Category Dimension]_"]
    measures: ["_[Primary Measure]_", "_[Secondary Measure]_"]
  
  - type: "bar"
    purpose: "comparison"
    dimensions: ["_[Category Dimension]_"]
    measures: ["_[Comparison Measure]_"]
  
  - type: "map"
    purpose: "geographic_analysis"
    dimensions: ["_[Geographic Dimension]_"]
    measures: ["_[Geographic Measure]_"]

interactions:
  drill_through: "_[Enable/Disable]_"
  cross_filtering: "_[Enable/Disable]_"
  tooltips: "_[Custom/Standard]_"
```

**Generation Instructions**:
```markdown
FOR EACH CHART_TYPE in chart_types:
  CREATE standard and responsive variants:
  
  1. Desktop Version: {purpose}-{type}-desktop.json
     - Full feature chart with complete legend and labels
     - Optimized for large screen interaction
     - Detailed tooltips and data labels
  
  2. Mobile Version: {purpose}-{type}-mobile.json
     - Simplified chart with essential elements only
     - Touch-friendly interaction areas
     - Condensed legend and abbreviated labels
  
  3. Accessible Version: {purpose}-{type}-accessible.json
     - High contrast color scheme
     - Pattern-based differentiation in addition to color
     - Enhanced screen reader support

  CONFIGURE each chart with:
  - Appropriate data bindings for specified dimensions/measures
  - Organizational color palette application
  - Responsive behavior definitions
  - Performance optimization settings
```

**Output Files**:
- `modules/charts/[purpose]-[type]-desktop.json`
- `modules/charts/[purpose]-[type]-mobile.json`
- `modules/charts/[purpose]-[type]-accessible.json`

### Task 3: Generate Filter Module Library

**Input Template Variables**:
```yaml
filter_dimensions:
  - dimension: "_[Dimension Name]_"
    type: "_[dropdown|list|range|date]_"
    multi_select: "_[true|false]_"
    default_selection: "_[Default Value or 'all']_"
    source_table: "_[Table Name]_"
    search_enabled: "_[true|false]_"

date_dimensions:
  - dimension: "_[Date Field Name]_"
    fiscal_year: "_[true|false]_"
    default_period: "_[current_month|current_quarter|current_year]_"
    relative_filtering: "_[true|false]_"
```

**Generation Instructions**:
```markdown
FOR EACH FILTER_DIMENSION in filter_dimensions:
  CREATE filter variants based on type:
  
  1. Dropdown Slicer: {dimension-name}-dropdown.json
     - Compact dropdown interface
     - Multi-select capability if specified
     - Search functionality if enabled
     - Organizational styling applied
  
  2. List Slicer: {dimension-name}-list.json
     - Vertical list format for better visibility
     - Checkbox selection for multi-select
     - Scrollable area for long lists
  
  3. Tile Slicer: {dimension-name}-tiles.json (for categories < 10 items)
     - Visual tile-based selection
     - Image support if applicable
     - Touch-friendly for mobile devices

FOR EACH DATE_DIMENSION in date_dimensions:
  CREATE date-specific filters:
  
  1. Date Range Picker: {dimension-name}-range.json
     - Calendar-based selection interface
     - Fiscal year support if specified
     - Relative date options (last 30 days, YTD, etc.)
  
  2. Period Slicer: {dimension-name}-period.json
     - Pre-defined period selections
     - Year-over-year comparison options
     - Quick selection buttons for common periods
```

**Output Files**:
- `modules/filters/[dimension-name]-dropdown.json`
- `modules/filters/[dimension-name]-list.json`
- `modules/filters/[dimension-name]-tiles.json`
- `modules/filters/[date-dimension]-range.json`
- `modules/filters/[date-dimension]-period.json`

### Task 4: Generate Layout Module Library

**Input Template Variables**:
```yaml
layout_types:
  executive:
    focus: "high_level_kpis"
    visual_density: "low"
    interaction_complexity: "minimal"
  
  operational:
    focus: "detailed_metrics"
    visual_density: "medium"
    interaction_complexity: "moderate"
  
  analytical:
    focus: "drill_down_analysis"
    visual_density: "high"
    interaction_complexity: "advanced"

page_structure:
  header_height: "_[Pixels or percentage]_"
  filter_bar_height: "_[Pixels or percentage]_"
  content_area_grid: "_[Columns x Rows]_"
  footer_height: "_[Pixels or percentage]_"
```

**Generation Instructions**:
```markdown
FOR EACH LAYOUT_TYPE in layout_types:
  CREATE responsive layout templates:
  
  1. Desktop Layout: {layout_type}-dashboard-desktop.json
     - Full grid system with optimal spacing
     - Complete header with logo and navigation
     - Comprehensive filter bar
     - Multi-column content area
  
  2. Tablet Layout: {layout_type}-dashboard-tablet.json
     - Adapted grid for medium screens
     - Collapsible filter panel
     - Stacked content areas
     - Touch-optimized interactions
  
  3. Mobile Layout: {layout_type}-dashboard-mobile.json
     - Single-column layout
     - Minimized header and navigation
     - Swipeable filter interface
     - Vertically stacked components

  INCLUDE in each layout:
  - Organizational branding elements
  - Consistent color scheme application
  - Accessibility navigation structure
  - Performance-optimized configuration
```

**Output Files**:
- `modules/layouts/[layout-type]-dashboard-desktop.json`
- `modules/layouts/[layout-type]-dashboard-tablet.json`
- `modules/layouts/[layout-type]-dashboard-mobile.json`

### Task 5: Generate Management Scripts

**Script Generation Requirements**:

**1. Visual Module Manager (`scripts/visual_module_manager.py`)**:
```python
# Agent Generation Instructions:
# - Create complete Python script for module management
# - Include functions: extract, replace, add, backup, restore
# - Add validation and error handling
# - Support batch operations
# - Include logging and audit trails
```

**2. Module Generator (`scripts/module_generator.py`)**:
```python
# Agent Generation Instructions:
# - Create Python script for generating modules from templates
# - Include template variable substitution
# - Support bulk generation from configuration files
# - Add organizational branding application
# - Include quality validation checks
```

**3. Validation Tools (`scripts/validation_tools.py`)**:
```python
# Agent Generation Instructions:
# - Create comprehensive validation suite
# - Include JSON schema validation
# - Add visual integrity checks
# - Include performance impact assessment
# - Support accessibility compliance testing
```

**4. Deployment Manager (`scripts/deployment_manager.py`)**:
```python
# Agent Generation Instructions:
# - Create deployment automation script
# - Include staging and production environments
# - Add rollback functionality
# - Include version management
# - Support CI/CD integration
```

### Task 6: Generate Documentation

**Documentation Generation Instructions**:

**1. Module Library Documentation**:
```markdown
FOR EACH MODULE created:
  GENERATE documentation including:
  - Purpose and business context
  - Data requirements and dependencies  
  - Usage examples and best practices
  - Customization options and variants
  - Performance characteristics
  - Accessibility features
  - Integration guidelines
```

**2. Implementation Guide**:
```markdown
CREATE comprehensive implementation guide:
- Module installation procedures
- Configuration and customization options
- Integration with existing reports
- Troubleshooting and support information
- Performance optimization guidelines
- Best practices and recommendations
```

**3. API Reference**:
```markdown
GENERATE technical reference documentation:
- Script function references
- Module schema definitions
- Configuration file formats
- Command-line interface documentation
- Error codes and troubleshooting
```

## Agent Execution Workflow

### Step 1: Environment Setup
```bash
# Agent should create project structure
mkdir -p modules/{kpi,charts,filters,layouts,scripts}
mkdir -p docs
mkdir -p backups
```

### Step 2: Input Validation
```yaml
# Validate all required input parameters
# Check for missing values
# Verify data model references
# Confirm branding guidelines
```

### Step 3: Module Generation
```python
# Execute generation tasks in sequence
# Apply organizational branding consistently
# Validate generated modules
# Create module documentation
```

### Step 4: Script Generation
```python
# Generate management and utility scripts
# Include comprehensive error handling
# Add logging and audit capabilities
# Create deployment automation
```

### Step 5: Documentation Creation
```markdown
# Generate user documentation
# Create technical reference materials
# Include usage examples and tutorials
# Provide troubleshooting guides
```

### Step 6: Quality Assurance
```python
# Run comprehensive validation suite
# Check accessibility compliance
# Verify performance characteristics
# Validate integration capabilities
```

## Validation and Testing

### Automated Validation Checklist

**Agent should verify**:
- [ ] All modules have valid JSON structure
- [ ] Data bindings reference existing tables/measures
- [ ] Organizational branding is consistently applied
- [ ] Responsive behavior is properly configured
- [ ] Accessibility standards are met
- [ ] Performance requirements are satisfied
- [ ] Documentation is complete and accurate
- [ ] Scripts function correctly with sample data
- [ ] Integration tests pass successfully
- [ ] Error handling works as expected

### Manual Verification Steps

**Human reviewer should check**:
- [ ] Visual aesthetics match organizational standards
- [ ] Business logic is correctly implemented
- [ ] User experience flows are intuitive
- [ ] Performance meets practical requirements
- [ ] Documentation is clear and comprehensive
- [ ] Scripts handle edge cases appropriately

## Troubleshooting Guide

### Common Issues and Solutions

**JSON Validation Errors**:
```bash
# Use built-in validation tools
python scripts/validation_tools.py validate --module [path]
```

**Data Binding Failures**:
```markdown
- Verify table and measure names match data model
- Check for typos in field references
- Confirm data types are compatible
- Validate relationship connections
```

**Performance Issues**:
```markdown
- Review visual complexity and data volume
- Optimize DAX expressions if needed
- Consider data aggregation strategies
- Implement incremental refresh where appropriate
```

**Integration Problems**:
```markdown
- Check Power BI Desktop version compatibility
- Verify PBIP feature enablement
- Confirm file permissions and access
- Validate backup and restore procedures
```

## Support and Resources

### Generated Documentation Location
- Module Library Reference: `docs/module-library.md`
- Implementation Guide: `docs/implementation-guide.md`
- API Reference: `docs/api-reference.md`
- Troubleshooting Guide: `docs/troubleshooting.md`

### Script Help and Usage
```bash
# All generated scripts include help documentation
python scripts/visual_module_manager.py --help
python scripts/module_generator.py --help
python scripts/validation_tools.py --help
python scripts/deployment_manager.py --help
```

---

**Template Instructions Complete**  
**Agent Implementation Ready**: ✅  
**Template Version**: 2.0  
**Created**: 2026-02-03  
**Agent Compatibility**: Full automation supported
