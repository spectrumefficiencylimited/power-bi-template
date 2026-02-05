# Power BI PBIP Template

A comprehensive template for creating and managing Power BI projects using the PBIP (Power BI Project) format. This template provides a structured approach to building, versioning, and collaborating on Power BI solutions.

## What is a Power BI Project?

A Power BI project is the end-to-end process of collecting, transforming, and modeling raw data to create interactive reports and dashboards that provide actionable business insights. These projects involve connecting to data sources (like Excel, SQL, or cloud services), using DAX for calculations, and visualizing data to drive decision-making.

### Key Components of a Power BI Project

**1. Project Structure (.pbip)**  
Power BI Desktop allows saving work as a Project file (.pbip), which stores report and semantic model definitions in a structured, text-based format, facilitating version control and collaboration, particularly via Git.

**2. Data Transformation (Power Query)**  
Cleaning, shaping, and transforming raw data into a structured format suitable for analysis.

**3. Data Modeling & DAX**  
Establishing relationships between tables and creating calculated measures/columns using Data Analysis Expressions (DAX).

**4. Data Visualization**  
Designing intuitive dashboards with charts, graphs, and filters (slicers) to analyze KPIs such as sales, profit, or operational performance.

**5. Deployment**  
Publishing the finished report from Power BI Desktop to the Power BI Service for sharing and collaboration.

## Quick Start

### 1. Create Your Project

1. Click **Use this template** → **Create a new repository**
2. Name your repository (e.g., `sales-dashboard` or `financial-reporting`)
3. Clone your new repository locally

### 2. Initialize Your Power BI Project

```bash
# Navigate to your project folder
cd your-project-name

# Run the initialization script (PowerShell)
.\scripts\init-project.sh "Your Project Name"
```

### 3. Open in Power BI Desktop

1. Open Power BI Desktop
2. Go to **File** → **Open** → **Browse for reports**
3. Select the `.pbip` file in your project folder
4. Start building your solution!

### 4. Project Development Workflow

```
1. Data Connection → Connect to your data sources
2. Data Transformation → Clean and shape your data in Power Query
3. Data Modeling → Create relationships and DAX measures
4. Report Design → Build visualizations and dashboards
5. Testing → Validate calculations and user experience
6. Deployment → Publish to Power BI Service
```

## Project Structure

```
├── README.md                          # Project documentation
├── YourProject.pbip                   # Power BI Project file
├── YourProject.Report/                # Report definition folder
│   └── definition/
│       ├── pages/                     # Page definitions
│       ├── visuals/                   # Visual configurations
│       └── report.json                # Report metadata
├── YourProject.SemanticModel/         # Semantic model folder
│   └── definition/
│       ├── tables/                    # Table definitions
│       ├── relationships/             # Relationship definitions
│       ├── measures/                  # DAX measures
│       └── model.tmdl                 # Model metadata
├── docs/                              # Project documentation
│   ├── 01_ProjectOverview.md          # Business requirements
│   ├── 02_DataSources.md              # Data source information
│   ├── 03_Ownership.md                # Project contacts
│   ├── 04_RefreshSchedule.md          # Data refresh details
│   ├── 05_SemanticModel.md            # Data model documentation
│   ├── 06_Security_RLS.md             # Security configuration
│   ├── 07_ChangeLog.md                # Change tracking
│   ├── 08_BusinessGlossary.md         # Business definitions
│   ├── 09_Dependencies.md             # External dependencies
│   ├── 10_TestingValidation.md        # Testing procedures
│   └── 12_DashboardRecipes.md         # Repeatable dashboard patterns
├── config/                            # Configuration files
│   ├── examples/                      # Example configurations
│   │   └── adidas_sales.yaml          # Retail sales dashboard example
│   └── sample_module_config.yaml      # Template configuration
├── modules/                           # Reusable visual templates
│   ├── kpi/                           # KPI card templates
│   ├── charts/                        # Chart templates  
│   ├── filters/                       # Slicer templates
│   ├── layouts/                       # Layout and interaction templates
│   └── scripts/                       # Validation and generation tools
└── scripts/                           # Utility scripts
    └── init-project.sh                # Project setup script
```

## Working with PBIP Files

### Current Status (February 2026)

**Important:** PBIP (Power BI Project) format is currently in **Preview** with the following status:
- **PBIP Format**: Available as preview feature in Power BI Desktop
- **PBIR (Enhanced Report Format)**: Rolling out as default format in Power BI Service (Jan-Feb 2026)
- **TMDL Support**: Available with VS Code extension for semantic model editing

### Benefits of PBIP Format

- **Version Control**: Text-based format works with Git
- **Collaboration**: Multiple developers can work on the same project
- **Code Review**: Changes can be reviewed line by line
- **Automation**: Can be integrated with CI/CD pipelines
- **Backup**: Easy to backup and restore projects

### Best Practices

1. **Use Descriptive Names**: Name your measures, tables, and visuals clearly
2. **Document Everything**: Use the docs folder to explain business logic
3. **Version Control**: Commit changes regularly with meaningful messages
4. **Test Thoroughly**: Validate all calculations and visualizations
5. **Follow Naming Conventions**: Be consistent with naming across your project

## Common Power BI Project Types

### Operational Dashboards
- Real-time monitoring of business operations
- KPI tracking and alerts
- Performance metrics visualization

### Executive Reporting
- High-level business summaries
- Strategic KPI monitoring
- Trend analysis and forecasting

### Analytical Reports
- Deep-dive analysis capabilities
- Interactive exploration tools
- Self-service analytics

### Financial Reporting
- P&L statements and balance sheets
- Budget vs. actual analysis
- Financial KPI tracking

## Dashboard Patterns & Recipes

This template includes proven dashboard patterns based on real-world implementations:

### Sales Executive Starter (Adidas Pattern)
A comprehensive executive sales dashboard featuring:
- **5-Card KPI Strip**: Total Sales, Operating Profit, Units Sold, Avg Price/Unit, Avg Operating Margin
- **Trend Analysis**: Monthly sales performance with seasonal patterns
- **Geographic Distribution**: State-level sales mapping
- **Product & Channel Performance**: Ranked bar charts for products and retailers
- **Smart Interactions**: Filter-based cross-filtering for drill-down analysis

**Key Learning**: Proper aggregation is critical - use **AVERAGE** for price/unit and margins, not SUM.

See `docs/12_DashboardRecipes.md` and `config/examples/adidas_sales.yaml` for detailed implementation.

### Validation & Quality Assurance
The template includes validation tools that catch common mistakes:
```bash
# Validate your PBIP project for common issues
python modules/scripts/validation_tools.py /path/to/your/project

# Common issues detected:
# - Wrong aggregation (Sum vs Average for prices/margins)
# - Missing percentage formatting
# - Incorrect interaction behavior
```

## Dashboard Patterns

This template supports two proven dashboard patterns with comprehensive examples:

### 🏬 Sales Analytics (Adidas Pattern)
**Executive Sales Dashboard** - Retail performance monitoring
- **KPIs**: Sales Revenue, Units Sold, Operating Margin, Avg Price per Unit
- **Visuals**: Time series, geographic distribution, product performance
- **Features**: Mobile-friendly design, drill-down capabilities, variance analysis
- **Use Case**: Monthly/quarterly business reviews, territory performance tracking

**Configuration**: [`config/examples/adidas_sales.yaml`](./config/examples/adidas_sales.yaml)  
**Documentation**: [`docs/12_DashboardRecipes.md`](./docs/12_DashboardRecipes.md)

### 🏥 Healthcare Analytics (Hospital ER Pattern)
**Emergency Department Operations** - Patient flow and performance optimization
- **KPIs**: Patient Count (DISTINCTCOUNT), Avg Wait Time, SLA Compliance, Satisfaction Score  
- **Visuals**: Day/hour heatmap, demographic analysis, department referrals, gauge charts
- **Features**: Time intelligence, SLA monitoring, compliance validation, demographic equity tracking
- **Use Case**: Operational efficiency, capacity planning, quality improvement, regulatory reporting

**Configuration**: [`config/examples/hospital_er.yaml`](./config/examples/hospital_er.yaml)  
**Documentation**: [`docs/13_DashboardRecipes_Hospital_ER.md`](./docs/13_DashboardRecipes_Hospital_ER.md)

### 🔧 Module Generation & Validation

Both patterns include:
- **Reusable Visual Templates** - Domain-specific chart and KPI configurations
- **Validation Tools** - Automated checks for aggregation rules, formatting, interactions
- **Code Generation** - YAML-to-JSON module conversion with domain-specific validation
- **Best Practice Enforcement** - Prevents common mistakes through automated validation

**Generate Modules**:
```bash
cd modules/scripts
py module_generator.py "../../config/examples/adidas_sales.yaml" --validate
py module_generator.py "../../config/examples/hospital_er.yaml" --validate
```

## Prerequisites

Before using this template, ensure you have:

- [ ] **Power BI Desktop** with PBIP preview features enabled
- [ ] **Visual Studio Code** (recommended for editing TMDL files)
- [ ] **Git** installed and configured
- [ ] Access to your organization's Azure DevOps or GitHub repository

### Enabling PBIP in Power BI Desktop

1. Open Power BI Desktop
2. Go to **File → Options and settings → Options → Preview features**
3. Enable:
   - ☑️ Power BI Project (.pbip) save option
   - ☑️ Store reports using enhanced metadata format (PBIR)
4. Click **OK** and restart Power BI Desktop

**Important Notes:**
- **TMDL Edits**: After editing TMDL files externally (e.g., in VS Code), restart Power BI Desktop to reload changes
- **PBIR Default**: Microsoft is rolling out PBIR as the default report format (Jan-Feb 2026)
- **Preview Features**: Keep preview features enabled for latest PBIP functionality

## Project Setup Workflow

### 1. Initialize Your Project

After cloning/creating from template:

```bash
.\scripts\init-project.sh "Your Project Name"
```

This will:
- Rename folders and files to match your project name
- Update references in the `.pbip` file
- Prepare metadata files for editing

### 2. Configure Your Semantic Model

1. Open the `.pbip` file in Power BI Desktop
2. Add your data connections and build your model
3. Save frequently—changes are tracked in Git

### 3. Complete Project Documentation

Work through each file in `/docs` in order:

| Priority | File | Purpose |
|----------|------|---------|
| 🔴 High | `01_ProjectOverview.md` | Define purpose and audience |
| 🔴 High | `02_DataSources.md` | Document all data connections |
| 🔴 High | `03_Ownership.md` | Assign responsibilities |
| 🟡 Medium | `04_RefreshSchedule.md` | Define refresh strategy |
| 🟡 Medium | `05_SemanticModel.md` | Document measures and tables |
| 🟡 Medium | `06_Security_RLS.md` | Configure row-level security |
| 🟢 Ongoing | `07_ChangeLog.md` | Track all changes |
| 🟢 Ongoing | `08_BusinessGlossary.md` | Define business terms |
| 🟢 Ongoing | `09_Dependencies.md` | Map data lineage |
| 🔵 Pre-release | `10_TestingValidation.md` | Document test results |

### 4. Version Control

```bash
git add .
git commit -m "Initial project setup: [Your Project Name]"
git push origin main
```

## Working with the Template

### Essential Files to Customize

1. **Project.Template.pbip** - Rename this to match your project
2. **docs/01_ProjectOverview.md** - Define your project's purpose and scope
3. **docs/02_DataSources.md** - Document your data connections
4. **docs/03_Ownership.md** - Assign project responsibilities

### Development Best Practices

- **Commit Often**: Save your work to Git regularly
- **Document Changes**: Update the changelog with each modification
- **Test Thoroughly**: Validate all calculations and visualizations
- **Follow Naming Conventions**: Use clear, consistent names for all objects
- **Review Security**: Ensure appropriate data access controls

## Collaboration Workflow

### For Development Teams

1. **Branching Strategy**: Use feature branches for new development
2. **Code Reviews**: Review changes before merging to main branch
3. **Testing**: Validate all changes in a test environment first
4. **Documentation**: Keep all documentation up to date

### For Business Users

1. **Requirements**: Clearly define needs in the project overview
2. **Testing**: Participate in user acceptance testing
3. **Feedback**: Provide regular feedback during development
4. **Training**: Complete training on the final solution

## Support and Resources

### Template Documentation
- Review all files in the `/docs` folder for project guidance
- Check the business glossary for term definitions
- Follow the testing procedures before deployment

### Power BI Resources
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [DAX Function Reference](https://docs.microsoft.com/en-us/dax/)
- [Power Query Documentation](https://docs.microsoft.com/en-us/powerquery-m/)
- [PBIP Format Guide](https://docs.microsoft.com/en-us/power-bi/developer/projects/)

### Getting Help
- Create an issue in this repository
- Contact your team via Microsoft Teams
- Email: your.team@organization.com

## Advanced Features

For organizations looking to implement advanced automation and module-based development, see the [Advanced Documentation](docs/advanced/) folder for:

- Automated PBIP analysis and migration tools
- Reusable visual component systems
- Enterprise deployment workflows
- Advanced collaboration patterns

## Quick Implementation: Adidas Sales Pattern

To quickly implement the proven sales executive dashboard pattern:

1. **Copy Example Configuration**:
   ```bash
   cp config/examples/adidas_sales.yaml config/my_sales_dashboard.yaml
   ```

2. **Customize for Your Data**:
   - Update field names to match your data model
   - Adjust branding colors to your organization
   - Modify KPI definitions as needed

3. **Generate Visual Modules**:
   ```bash
   cd modules/scripts
   python module_generator.py ../../config/my_sales_dashboard.yaml --validate
   ```

4. **Apply to Power BI**:
   - Use generated JSON templates as visual configuration guides
   - Set up KPI strip with proper aggregations (AVERAGE for prices/margins)
   - Configure interactions to use Filter (not Highlight)

5. **Validate Implementation**:
   ```bash
   python validation_tools.py /path/to/your/project
   ```

This approach gives you a production-ready executive dashboard in under an hour, with built-in validation to prevent common mistakes.

---

**Template Version:** 1.0  
**Last Updated:** February 2026  
**Compatible with:** Power BI Desktop (Latest)
