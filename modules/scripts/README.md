# Module Generation Scripts

This folder contains tools for generating and validating Power BI visual modules from configuration files.

## Scripts

### `validation_tools.py` 
Validates PBIP projects for common mistakes based on real-world learnings:
- Detects wrong aggregations (Sum vs Average for prices/margins)
- Checks formatting issues (missing % for margins)
- Validates interaction behavior
- Scans both JSON (report definitions) and TMDL (semantic model) files

**Usage:**
```bash
python validation_tools.py /path/to/your/project
```

### `module_generator.py`
Generates visual modules from YAML configuration files like the Adidas sales example:
- Creates KPI strips with proper validation rules
- Generates individual visual configurations  
- Creates slicer definitions
- Produces interaction rule templates

**Usage:**
```bash
python module_generator.py ../config/examples/adidas_sales.yaml --validate
```

## Example Workflow

1. **Create Configuration**: Use `config/examples/adidas_sales.yaml` as template
2. **Generate Modules**: Run module_generator.py with your config
3. **Validate Project**: Run validation_tools.py on your PBIP project
4. **Fix Issues**: Address any validation errors found
5. **Deploy**: Use generated modules in your Power BI project

## Requirements

- Python 3.8+
- PyYAML package: `pip install pyyaml`

## Validation Rules

Based on Adidas dashboard pattern learnings:
- **Price fields**: Must use AVERAGE aggregation, not SUM
- **Margin fields**: Must use AVERAGE aggregation with percentage format
- **Currency fields**: Should use appropriate display units (Millions/Thousands)
- **Interactions**: Should use Filter behavior, not Highlight

These rules prevent common mistakes that lead to incorrect business insights.
