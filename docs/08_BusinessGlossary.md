# Business Glossary

> **Instructions:** Define all business terms, KPIs, and metrics used in this report. This ensures consistent understanding across all users and maintainers.

## How to Use This Glossary

- All terms should have clear, business-friendly definitions
- Link to the enterprise glossary where terms are already defined
- Include calculation logic for derived metrics
- Note any data quality considerations

---

## Key Performance Indicators (KPIs)

| KPI Name | Definition | Calculation | Target | Data Source |
|----------|------------|-------------|--------|-------------|
| _[KPI Name]_ | _[Business definition]_ | _[How calculated]_ | _[Target value]_ | _[Source table]_ |
| _[KPI Name]_ | _[Business definition]_ | _[How calculated]_ | _[Target value]_ | _[Source table]_ |
| _[KPI Name]_ | _[Business definition]_ | _[How calculated]_ | _[Target value]_ | _[Source table]_ |

### KPI Details

#### _[KPI Name 1]_

| Attribute | Value |
|-----------|-------|
| **Display Name** | _[Name shown in report]_ |
| **Business Definition** | _[Plain English definition]_ |
| **Owner** | _[Who defines/owns this metric]_ |
| **Update Frequency** | _[How often it changes]_ |

**Calculation:**
```
Formula: [Numerator] / [Denominator] × 100

Where:
- Numerator: [Describe what's counted]
- Denominator: [Describe the base]
```

**Business Rules:**
- _[Rule 1: e.g., Excludes cancelled records]_
- _[Rule 2: e.g., Only includes active students]_

**Data Quality Notes:**
- _[Any known issues or caveats]_

**Related Terms:** _[Link to related glossary terms]_

---

#### _[KPI Name 2]_

_[Repeat structure for each KPI]_

---

## Business Terms

### A

#### _[Term]_
**Definition:** _[Clear business definition]_  
**Also Known As:** _[Aliases or alternative names]_  
**Example:** _[Concrete example]_  
**Source:** _[Where this term/data comes from]_

---

### B

#### _[Term]_
**Definition:** _[Clear business definition]_  
**Also Known As:** _[Aliases]_  
**Example:** _[Example]_  
**Source:** _[Source]_

---

### C-Z

_[Continue alphabetically as needed]_

---

## Dimension Definitions

### Time/Date Dimensions

| Term | Definition | Format | Example |
|------|------------|--------|---------|
| Academic Year | _[Definition]_ | _[YYYY]_ | 2025 |
| Study Period | _[Definition]_ | _[Code format]_ | SP1, SP2 |
| Census Date | _[Definition]_ | _[Date format]_ | 31 March 2025 |

### Entity Dimensions

| Term | Definition | Grain | Example |
|------|------------|-------|---------|
| Student | _[Definition]_ | _[What one record represents]_ | _[Example]_ |
| Course | _[Definition]_ | _[What one record represents]_ | _[Example]_ |
| Program | _[Definition]_ | _[What one record represents]_ | _[Example]_ |

## Calculated Metrics

| Metric | Formula | Unit | Example Value |
|--------|---------|------|---------------|
| _[Metric]_ | _[Calculation]_ | Count / % / $ | _[e.g., 85%]_ |
| _[Metric]_ | _[Calculation]_ | Count / % / $ | _[e.g., 1,234]_ |

## Status/Category Definitions

### _[Status Field Name]_

| Value | Code | Definition | Include in KPIs? |
|-------|------|------------|------------------|
| _[Status]_ | _[Code]_ | _[What this status means]_ | Yes / No |
| _[Status]_ | _[Code]_ | _[What this status means]_ | Yes / No |
| _[Status]_ | _[Code]_ | _[What this status means]_ | Yes / No |

## Business Rules

### Inclusion/Exclusion Rules

| Rule Name | Description | Applied To |
|-----------|-------------|------------|
| _[Rule]_ | _[What's included/excluded and why]_ | _[Measures/visuals affected]_ |
| _[Rule]_ | _[What's included/excluded and why]_ | _[Measures/visuals affected]_ |

### Aggregation Rules

| Metric | Aggregation Method | Notes |
|--------|-------------------|-------|
| _[Metric]_ | SUM / AVG / COUNT / DISTINCTCOUNT | _[Special handling]_ |
| _[Metric]_ | SUM / AVG / COUNT / DISTINCTCOUNT | _[Special handling]_ |

## Data Quality Flags

| Flag | Definition | Impact |
|------|------------|--------|
| _[Flag]_ | _[When this flag appears]_ | _[How users should interpret]_ |
| _[Flag]_ | _[When this flag appears]_ | _[How users should interpret]_ |

## External References

| Term | Enterprise Glossary Link | Notes |
|------|--------------------------|-------|
| _[Term]_ | _[URL to enterprise definition]_ | _[Any differences]_ |
| _[Term]_ | _[URL to enterprise definition]_ | _[Any differences]_ |

---

**Glossary Maintenance:**
- Review with Data Steward quarterly
- Update when business rules change
- Align with enterprise glossary
- Last reviewed: _[Date]_ by _[Name]_
