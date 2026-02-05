# Dashboard Recipe: Hospital Emergency Room (ER) Analytics

## Domain
Healthcare / Emergency / Medical Operations

## Business Objective
Optimize ER operations by analyzing patient volume, wait times, admissions, referrals, demographics, and temporal congestion patterns.

## Dashboards (4)
1. **Monthly View** - Operational Snapshot (Primary Executive Dashboard)
2. **Consolidated View** - Custom Date Range Analysis
3. **Patient Details** - Row-level Analysis & Export
4. **Key Takeaways** - Narrative Insights & Recommendations

---

## 1. Monthly View (Primary Executive Dashboard)

### Global Filters
- **Month–Year** (single select dropdown)
- **Interactive cross-filtering** (click any visual to filter others)

### KPI Strip (with Daily Sparklines)
1. **Number of Patients** - `DISTINCTCOUNT('ER_Data'[Patient ID])`
2. **Average Wait Time** - `AVERAGE('ER_Data'[Patient Wait Time])` (minutes)
3. **Patient Satisfaction Score** - `AVERAGE('ER_Data'[Satisfaction Score])` (1-5 scale)
4. **Number of Patients Referred** - `CALCULATE(COUNTROWS('ER_Data'), 'ER_Data'[Department Referral] <> "None")`

### Core Visuals Layout

#### Row 1: Patient Flow & Admissions
- **Patient Admission Status** (Donut Chart)
  - Admitted vs Not Admitted with percentages
  - Color coding: Green (Admitted), Blue (Not Admitted)

- **% Patients Seen Within 30 Minutes** (Gauge)
  - SLA compliance metric
  - Target: 90% (configurable)
  - Red/Yellow/Green zones

#### Row 2: Demographics
- **Patients by Age Group** (Horizontal Bar Chart)
  - 10-year age bins: 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
  - Sorted by count descending

- **Patients by Gender** (Bar Chart)
  - Simple M/F/Other distribution

- **Patients by Race** (Horizontal Bar Chart)
  - Ethnicity breakdown for equity analysis

#### Row 3: Operational Patterns
- **Patients by Department Referral** (Treemap)
  - Referral patterns to specialist departments
  - Size = patient count, color by department type

- **Patients by Day & Hour Heatmap** (Matrix Visual)
  - Days of week (rows) × Hours (columns)
  - Color intensity = patient volume
  - Critical for staffing optimization

---

## 2. Consolidated View

### Purpose
Same analytical power as Monthly View but with flexible date range selection.

### Configuration
- **Date Range Slicer** (Start Date – End Date)
- **All visuals from Monthly View** (reused layouts)
- **No month restriction** - allows year-over-year, quarter analysis
- **Automatic recalculation** of all KPIs and visuals

---

## 3. Patient Details

### Purpose
Granular, exportable data view for audits, compliance, and departmental reporting.

### Layout
- **Advanced filter panel**: Date, Gender, Race, Admission Status, Department Referral
- **Sortable table** with key patient attributes:
  - Patient ID (anonymized)
  - Admission Date & Time
  - Wait Time (minutes)
  - Age Group
  - Gender
  - Race
  - Admission Status
  - Department Referral
  - Satisfaction Score

### Compliance Note
⚠️ **HIPAA/GDPR Consideration**: Ensure Patient IDs are properly anonymized and access is role-restricted.

---

## 4. Key Takeaways

### Purpose
Developer-authored insights and operational recommendations based on data patterns.

### Content Sections
1. **SLA Performance Summary**
   - Current month vs target performance
   - Trend analysis and alerts

2. **Staffing Optimization Insights**
   - Peak hour identification
   - Capacity vs demand gaps

3. **Demographic Trends**
   - Age group shifts over time
   - Department referral patterns

4. **Actionable Recommendations**
   - Staffing adjustments
   - Process improvements
   - Resource allocation suggestions

---

## Canonical DAX Patterns

### Core Measures

```dax
Number of Patients = 
DISTINCTCOUNT('ER_Data'[Patient ID])

Avg Wait Time (min) = 
AVERAGE('ER_Data'[Patient Wait Time])

Patient Satisfaction Score = 
AVERAGE('ER_Data'[Satisfaction Score])

Patients Referred = 
CALCULATE(
    COUNTROWS('ER_Data'),
    'ER_Data'[Department Referral] <> "None"
)

% Seen Within 30 Min = 
DIVIDE(
    CALCULATE(
        COUNTROWS('ER_Data'),
        'ER_Data'[Patient Wait Time] <= 30
    ),
    COUNTROWS('ER_Data'),
    0
)
```

### Calculated Columns

```dax
Admission Status = 
IF(
    'ER_Data'[Patient Admission Flag] = TRUE(),
    "Admitted",
    "Not Admitted"
)

Age Group = 
SWITCH(
    TRUE(),
    'ER_Data'[Age] < 10, "0–9",
    'ER_Data'[Age] < 20, "10–19",
    'ER_Data'[Age] < 30, "20–29",
    'ER_Data'[Age] < 40, "30–39",
    'ER_Data'[Age] < 50, "40–49",
    'ER_Data'[Age] < 60, "50–59",
    'ER_Data'[Age] < 70, "60–69",
    'ER_Data'[Age] < 80, "70–79",
    "80+"
)

Patient Admission Date = 
DATE(
    YEAR('ER_Data'[Patient Admission DateTime]),
    MONTH('ER_Data'[Patient Admission DateTime]),
    DAY('ER_Data'[Patient Admission DateTime])
)

Seen Within 30 Min = 
IF('ER_Data'[Patient Wait Time] <= 30, 1, 0)
```

---

## Data Model Requirements

### Critical Relationships
1. **Calendar Table** (Required)
   - `Date Table[Date]` → `ER_Data[Patient Admission Date]`
   - Cardinality: One to Many
   - Cross filter direction: Single

### Data Quality Rules
- ❌ **Never join DateTime directly to Date fields**
- ✅ **Always split DateTime into separate Date and Time columns**
- ✅ **Use proper Calendar table for time intelligence**
- ✅ **Validate SLA thresholds are configurable, not hard-coded**

### Required Columns
- `Patient ID` (Primary key, anonymized)
- `Patient Admission DateTime` (Full timestamp)
- `Patient Admission Date` (Date only, calculated)
- `Patient Wait Time` (Minutes, numeric)
- `Age` (Years, numeric)
- `Gender` (Text: M/F/Other)
- `Race` (Text, standardized values)
- `Patient Admission Flag` (Boolean)
- `Department Referral` (Text, "None" for no referral)
- `Satisfaction Score` (Numeric 1-5)

---

## Visual Specifications

### KPI Strip Configuration
- **Layout**: Horizontal strip, 4 cards
- **Card dimensions**: 220px wide × 120px tall
- **Spacing**: 20px gap between cards
- **Sparklines**: 7-day trend for each KPI

### Color Palette (Healthcare Theme)
- **Primary**: `#0078D4` (Medical Blue)
- **Success**: `#107C10` (Healthy Green)
- **Warning**: `#FF8C00` (Alert Orange)
- **Critical**: `#D13438` (Emergency Red)
- **Neutral**: `#F3F2F1` (Clean White)

### Interaction Rules
1. **All slicers filter all visuals** (except Key Takeaways)
2. **Visual-to-visual filtering**: Enabled for all charts
3. **No highlighting behavior** (convert all to filtering)
4. **Patient Details table**: Not affected by visual interactions

---

## Implementation Notes

### Phase 1: Core Dashboard (Monthly View)
1. Create KPI strip with sparklines
2. Build patient flow visuals (admission status, SLA compliance)
3. Add demographic analysis charts
4. Implement day/hour heatmap

### Phase 2: Extended Views
1. Clone Monthly View for Consolidated View
2. Add date range slicer functionality
3. Create Patient Details table with filters

### Phase 3: Insights & Polish
1. Develop Key Takeaways content
2. Apply healthcare color theme
3. Configure all interaction rules
4. Add HIPAA compliance notes

### Testing Checklist
- [ ] All KPIs calculate correctly
- [ ] Date filtering works across all visuals
- [ ] SLA compliance gauge shows proper thresholds
- [ ] Heatmap highlights peak congestion times
- [ ] Patient Details export functions properly
- [ ] No DateTime join issues in data model
