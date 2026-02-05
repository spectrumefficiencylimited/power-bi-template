# Visual Module Templates

This folder contains reusable visual component templates for Power BI projects. These templates provide a starting point for creating consistent visualizations across your organization.

## Available Templates

### KPI Templates (`kpi/`)
- `_template_metric-card.json` - Standard KPI card for displaying key metrics

### Chart Templates (`charts/`)
- `_template_clustered-bar-chart.json` - Clustered bar chart for category comparisons
- `_template_conversion-funnel.json` - Funnel chart for conversion analysis
- `_template_geographic-heatmap.json` - Map visualization with heat mapping
- `_template_horizontal-bar-chart.json` - Horizontal bar chart
- `_template_trend-line-chart-detailed.json` - Detailed line chart with annotations
- `_template_trend-line-chart.json` - Simple trend line chart

### Filter Templates (`filters/`)
- `_template_dimension-slicer.json` - Standard slicer for filtering data

### Layout Templates (`layouts/`)
- `_template_action-button.json` - Interactive button component
- `_template_executive-dashboard-layout.json` - Executive dashboard layout
- `_template_image-visual.json` - Image/logo placement
- `_template_text-content.json` - Text box for annotations

## How to Use Templates

### 1. Manual Copy and Modify
1. Copy a template file that matches your needs
2. Rename it to describe your specific use case (e.g., `sales-kpi-card.json`)
3. Open the JSON file and modify the visual properties
4. Import or reference in your Power BI project

### 2. Power BI Integration
These templates contain Power BI visual configurations that can be:
- Imported into Power BI Desktop
- Used as starting points for new visuals
- Customized for your specific data model and branding

### 3. Customization Guidelines
- Update data bindings to match your semantic model
- Apply your organization's color scheme
- Adjust sizing and positioning for your layouts
- Test accessibility and mobile responsiveness

## Template Structure

Each template JSON file contains:
- Visual type definition
- Layout and positioning information
- Styling and formatting rules
- Data binding configuration (to be updated for your model)
- Accessibility attributes

## Best Practices

1. **Naming Convention**: Use descriptive names for your customized templates
2. **Documentation**: Document any modifications you make
3. **Testing**: Test all templates thoroughly before deploying to production
4. **Version Control**: Track changes to your customized templates in Git
5. **Consistency**: Maintain consistent styling across all templates

## Advanced Automation

For organizations interested in automated template generation and management, see the [Advanced Documentation](../docs/advanced/) folder for:
- Automated template generation scripts
- Bulk template application tools
- Enterprise template management systems

---
*These templates are provided as starting points and should be customized for your specific requirements.*
