# Dashboard Recipe: Sales Executive Starter (Adidas Pattern)

## Goal
Beginner-friendly executive summary dashboard with drill-through via slicers and cross-filtering. Based on proven patterns for retail sales analysis.

## Required Fields
- **InvoiceDate** (date) - Transaction date for trend analysis
- **State** (geo) - Geographic dimension for map visualization
- **Region** (category) - Regional grouping for composition charts
- **Product** (category) - Product lines for performance comparison
- **Retailer** (category) - Retailer channels for performance comparison
- **TotalSales** (numeric) - Primary revenue metric
- **OperatingProfit** (numeric) - Profitability metric
- **UnitsSold** (numeric) - Volume metric
- **PricePerUnit** (numeric) - Unit economics (must use AVERAGE aggregation)
- **OperatingMargin** (numeric, 0–1 or %) - Profitability ratio (must use AVERAGE aggregation)

## Dashboard Layout Pattern

### Header Section
- **Title bar**: Company logo + dashboard title
- **KPI Strip**: 5 key performance indicators in horizontal layout

### Main Content Area (2x3 grid)
- **Row 1**: Trend chart (2 columns), Composition chart (1 column)
- **Row 2**: Ranked bar charts (1 column each), Geographic map (1 column)

### Filter Panel
- **Region slicer**: Dropdown with multi-select + "Select all"
- **Date slicer**: Between-style date range selector

## KPI Strip (5 Cards)

| Position | Metric | Field | Aggregation | Format | Display Units | Notes |
|----------|--------|-------|-------------|---------|---------------|-------|
| 1 | Total Sales | TotalSales | SUM | Currency, 0 decimals | Millions | Primary revenue KPI |
| 2 | Operating Profit | OperatingProfit | SUM | Currency, 0 decimals | Millions | Profitability KPI |
| 3 | Units Sold | UnitsSold | SUM | Whole number, 0 decimals | Auto | Volume KPI |
| 4 | Avg Price/Unit | PricePerUnit | **AVERAGE** | Currency, 0 decimals | Auto | Unit economics |
| 5 | Avg Operating Margin | OperatingMargin | **AVERAGE** | **Percentage, 0 decimals** | Auto | Profitability ratio |

## Main Visualizations

### 1. Trend Analysis
- **Type**: Area chart or Line chart with markers
- **Title**: "Total Sales by Month"
- **X-axis**: Invoice Date (Month)
- **Y-axis**: Total Sales (Sum)
- **Features**: Data labels enabled, markers visible
- **Purpose**: Identify seasonal patterns and trends

### 2. Geographic Distribution
- **Type**: Filled map (Shape map)
- **Title**: "Total Sales by State"
- **Location**: State
- **Color**: Total Sales (Sum)
- **Tooltips**: Sales, Profit, Units, Avg Price, Avg Margin
- **Purpose**: Regional performance comparison

### 3. Composition Analysis
- **Type**: Donut chart
- **Title**: "Total Sales by Region"
- **Legend**: Region
- **Values**: Total Sales (Sum)
- **Purpose**: Regional contribution analysis

### 4. Product Performance
- **Type**: Horizontal bar chart
- **Title**: "Total Sales by Product"
- **Axis**: Product
- **Values**: Total Sales (Sum)
- **Sort**: Descending by value
- **Purpose**: Product line performance ranking

### 5. Retailer Performance
- **Type**: Horizontal bar chart
- **Title**: "Total Sales by Retailer"
- **Axis**: Retailer
- **Values**: Total Sales (Sum)
- **Sort**: Descending by value
- **Purpose**: Channel performance ranking

## Interaction Rules

### Cross-Filtering Behavior
- **Primary Rule**: All visual interactions set to **Filter** (not Highlight)
- **Slicer Behavior**: All slicers filter all visuals on the page
- **Chart Interactions**: Clicking any chart filters other charts
- **Rationale**: Enables drill-down analysis rather than just highlighting

### Slicer Configuration
- **Region Slicer**: 
  - Style: Dropdown
  - Multi-select: Enabled
  - Select All: Enabled
  - Placement: Top-right of dashboard
- **Date Slicer**:
  - Style: Between
  - Default: Current year
  - Placement: Below region slicer

## Visual Design Standards

### Color Scheme
- **Primary**: Corporate brand colors
- **KPI Cards**: Consistent background with accent borders
- **Charts**: Sequential color scale for geographic data
- **Bars**: Categorical colors for products/retailers

### Typography
- **Titles**: Bold, consistent font size
- **Data Labels**: Readable, not cluttered
- **Axis Labels**: Clear, abbreviated where necessary

### Formatting Rules
- **Currency**: $ symbol, no decimals, millions format where appropriate
- **Percentages**: % symbol, no decimals
- **Borders**: Subtle borders around visuals for structure
- **Spacing**: Consistent margins between visuals

## Common Insights Pattern

This dashboard pattern typically reveals:

### Temporal Insights
- **Peak Periods**: Holiday seasons (Nov-Dec), summer months
- **Seasonal Patterns**: Back-to-school, spring sports, winter gear cycles

### Geographic Insights
- **Top States**: Typically NY, CA, TX, FL drive highest volumes
- **Regional Leaders**: West Coast often leads in premium products

### Product Insights
- **Best Performers**: Identify top product categories
- **Price Points**: Correlation between price and margin

### Channel Insights
- **Retailer Rankings**: Specialist vs. general retailers
- **Regional Preferences**: Different retailers perform better in different regions

## Implementation Checklist

### Data Preparation
- [ ] Verify all required fields are present
- [ ] Ensure date field is properly formatted
- [ ] Validate geographic data for map visualization
- [ ] Check for data quality issues (nulls, duplicates)

### Visual Creation
- [ ] Create KPI strip with proper aggregations
- [ ] Build trend chart with appropriate time grain
- [ ] Configure map with state-level data
- [ ] Set up composition charts
- [ ] Create ranked bar charts

### Interaction Setup
- [ ] Set all interactions to Filter
- [ ] Configure slicers for multi-select
- [ ] Test cross-filtering behavior
- [ ] Validate tooltip content

### Quality Assurance
- [ ] Run aggregation validation (Avg vs Sum)
- [ ] Verify percentage formatting
- [ ] Check display units and currency formatting
- [ ] Test mobile responsiveness
- [ ] Validate accessibility features

## Variations

### Executive Summary Version
- Focus on top-level KPIs only
- Simplified visualizations
- Fewer interaction options

### Operational Deep-Dive Version
- Additional breakdown dimensions
- More granular time periods
- Enhanced filtering options

### Mobile-Optimized Version
- Stacked layout instead of grid
- Larger touch targets
- Simplified interactions

---

**Recipe Version**: 1.0  
**Based On**: Adidas sales analysis pattern  
**Last Updated**: February 2026  
**Suitable For**: Retail, e-commerce, product sales analysis
