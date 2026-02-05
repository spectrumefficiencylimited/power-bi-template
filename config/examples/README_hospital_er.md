# Hospital ER Analytics Configuration

This configuration demonstrates the Healthcare dashboard pattern for Hospital Emergency Room analytics, featuring a 4-dashboard structure optimized for operational efficiency and patient care management.

## Generated Modules

Running the module generator on this configuration produces:

### KPI Strip
- **Number of Patients** (DISTINCTCOUNT) - Unique patients treated
- **Avg Wait Time** (AVERAGE) - Patient wait time in minutes
- **Satisfaction Score** (AVERAGE) - Patient satisfaction rating
- **Patients Referred** (COUNTROWS_FILTERED) - Referrals to other departments  
- **% Seen < 30 min** (PERCENTAGE) - SLA compliance metric

### Healthcare-Specific Visuals
- **Matrix Heatmap** - Patient volume by day of week and hour
- **Gauge Charts** - SLA compliance with color-coded thresholds
- **Bar Charts** - Patient distribution by demographics and status
- **Donut Charts** - Gender and race distribution analysis

### Slicers & Filters
- Month-Year dropdown for primary navigation
- Date range selector for flexible analysis
- Admission status and gender filters for detailed views

### Interaction Rules
- Cross-filtering enabled for comprehensive analysis
- KPI cards non-interactive for clarity
- Time-based heatmap drives other visuals

## Validation Features

The healthcare configuration includes domain-specific validation:

### Data Model Validation ✅
- ❌ **DateTime Joins** - Flags improper DateTime field usage in relationships
- ❌ **Calendar Table** - Requires proper calendar table for time intelligence
- ❌ **Patient Counts** - Ensures DISTINCTCOUNT aggregation for patient metrics

### Healthcare Compliance 🏥
- ⚠️ **SLA Parameterization** - Warns about hard-coded SLA thresholds
- 🚨 **HIPAA Compliance** - Flags missing privacy protections in patient detail views
- ✅ **Aggregation Rules** - Validates proper healthcare-specific aggregations

## Domain-Specific Features

### Medical Color Palette
- Primary: #0066CC (Medical Blue)
- Success: #28A745 (SLA Met)
- Alert: #DC3545 (Critical Issues)
- Light: #F8F9FA (Neutral Background)

### Healthcare Analytics Patterns
- **Time Intelligence** - Proper date/time modeling for patient flow
- **Patient Metrics** - DISTINCTCOUNT aggregations to avoid double-counting
- **SLA Monitoring** - Parameterized thresholds for flexibility
- **Demographics** - Equitable care distribution analysis

### DAX Patterns Included
```dax
Number of Patients := DISTINCTCOUNT ( 'ER_Data'[Patient ID] )

Avg Wait Time (min) := AVERAGE ( 'ER_Data'[Patient Wait Time] )

% Seen Within 30 Min := 
DIVIDE (
    CALCULATE ( COUNTROWS ( 'ER_Data' ), 'ER_Data'[Patient Wait Time] <= 30 ),
    COUNTROWS ( 'ER_Data' )
)

Age Group := 
SWITCH (
    TRUE(),
    'ER_Data'[Age] < 10, "0–9",
    'ER_Data'[Age] < 20, "10–19",
    ...
    "80+"
)
```

## Usage

1. **Generate Modules**:
   ```bash
   py module_generator.py hospital_er.yaml --validate
   ```

2. **Apply to PBIP Project**:
   - Copy generated JSON modules to your PBIP definition folders
   - Implement suggested DAX patterns in semantic model
   - Configure RLS for patient data protection

3. **Customize for Your Environment**:
   - Update field names to match your data model
   - Adjust SLA thresholds via parameters
   - Modify color scheme if needed

## Compliance Notes

- **HIPAA**: Implement RLS and audit logging for patient data access
- **Joint Commission**: Supports patient flow and quality metrics requirements
- **CMS**: Aligns with quality reporting standards

This configuration provides a production-ready foundation for healthcare analytics while maintaining compliance and governance standards.
