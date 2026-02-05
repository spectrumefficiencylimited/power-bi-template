# Semantic Model Documentation

> **Instructions:** Document all tables, measures, and relationships in the semantic model. This is your technical reference for the data model.

## Model Overview

| Attribute | Value |
|-----------|-------|
| **Model Name** | _[Semantic model name]_ |
| **Compatibility Level** | _[e.g., 1550]_ |
| **Default Culture** | _[e.g., en-AU]_ |
| **Storage Mode** | Import / DirectQuery / Composite |
| **Total Tables** | _[Count]_ |
| **Total Measures** | _[Count]_ |
| **Total Relationships** | _[Count]_ |

## Data Model Diagram

_[Include a screenshot or diagram of the model relationships from Power BI Desktop]_

```
                    ┌─────────────┐
                    │  Calendar   │ (Date table)
                    └──────┬──────┘
                           │ 1:*
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Dim_Student  │  │  Dim_Course   │  │  Dim_Location │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │ 1:*              │ 1:*              │ 1:*
        └──────────────────┼──────────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │ Fact_Enrollment │
                    └─────────────────┘
```

## Tables

### Table Inventory

| Table Name | Type | Storage Mode | Row Count | Description |
|------------|------|--------------|-----------|-------------|
| _[Table name]_ | Fact / Dimension / Bridge | Import / DQ | _[~count]_ | _[Purpose]_ |
| _[Table name]_ | Fact / Dimension / Bridge | Import / DQ | _[~count]_ | _[Purpose]_ |
| _[Table name]_ | Fact / Dimension / Bridge | Import / DQ | _[~count]_ | _[Purpose]_ |

### Table Details

#### _[Table Name 1]_

| Attribute | Value |
|-----------|-------|
| **Table Type** | Fact / Dimension / Bridge / Calculated |
| **Source** | _[Source system/table]_ |
| **Storage Mode** | Import / DirectQuery |
| **Row Count** | _[Approximate]_ |
| **Description** | _[Business purpose of this table]_ |

**Columns:**

| Column Name | Data Type | Description | Source Column |
|-------------|-----------|-------------|---------------|
| _[Column]_ | Int64 / String / DateTime / Decimal | _[Description]_ | _[Source]_ |
| _[Column]_ | Int64 / String / DateTime / Decimal | _[Description]_ | _[Source]_ |
| _[Column]_ | Int64 / String / DateTime / Decimal | _[Description]_ | _[Source]_ |

---

#### _[Table Name 2]_

_[Repeat structure for each table]_

---

## Measures

### Measure Inventory

| Measure Name | Display Folder | Format | Description |
|--------------|----------------|--------|-------------|
| _[Measure]_ | _[Folder]_ | _[#,##0]_ | _[Business description]_ |
| _[Measure]_ | _[Folder]_ | _[0.0%]_ | _[Business description]_ |

### Measure Details

#### _[Measure Name 1]_

| Attribute | Value |
|-----------|-------|
| **Display Name** | _[Name shown to users]_ |
| **Display Folder** | _[Folder path]_ |
| **Format String** | _[e.g., #,##0 or 0.0%]_ |
| **Description** | _[Business definition]_ |

**DAX Expression:**
```dax
[Measure Name] = 
    // Purpose: [Explain what this calculates]
    // Used in: [Which visuals/reports use this]
    CALCULATE(
        SUM(TableName[Column]),
        FilterExpression
    )
```

**Business Logic:**
- _[Explain the business rules applied]_
- _[Note any edge cases or exceptions]_

**Dependencies:**
- Requires: _[Other measures or columns this depends on]_
- Used by: _[Measures that depend on this]_

---

#### _[Measure Name 2]_

_[Repeat structure for each measure]_

---

## Calculation Groups (if used)

### _[Calculation Group Name]_

| Attribute | Value |
|-----------|-------|
| **Purpose** | _[Why this calculation group exists]_ |
| **Precedence** | _[Number]_ |

**Calculation Items:**

| Item Name | Expression | Description |
|-----------|------------|-------------|
| _[Item]_ | `SELECTEDMEASURE()` | _[Description]_ |
| _[Item]_ | `CALCULATE(SELECTEDMEASURE(), ...)` | _[Description]_ |

## Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross-filter | Active |
|------------|-------------|----------|-----------|-------------|--------------|--------|
| _[Table]_ | _[Column]_ | _[Table]_ | _[Column]_ | 1:* / *:1 / *:* | Single / Both | Yes/No |
| _[Table]_ | _[Column]_ | _[Table]_ | _[Column]_ | 1:* / *:1 / *:* | Single / Both | Yes/No |

### Relationship Notes

- _[Explain any inactive relationships and when they're used]_
- _[Note any bi-directional filtering considerations]_
- _[Document any role-playing dimensions]_

## Hierarchies

| Hierarchy Name | Table | Levels | Description |
|----------------|-------|--------|-------------|
| _[Hierarchy]_ | _[Table]_ | Level1 → Level2 → Level3 | _[Purpose]_ |

## Performance Considerations

### Large Tables
- _[Note any tables with >1M rows]_
- _[Document partitioning strategy if used]_

### DirectQuery Considerations
- _[Note any DQ tables and performance implications]_
- _[Document aggregation tables if used]_

### Optimization Applied
- _[List any specific optimizations]_
- _[Note columns removed from model]_

## TMDL File Reference

The semantic model definition files are located in:
```
Project.Name.SemanticModel/
└── definition/
    ├── model.tmdl           # Model-level settings
    ├── tables/              # One .tmdl file per table
    └── relationships/       # Relationship definitions
```

---

**Completion Checklist:**
- [ ] All tables documented
- [ ] All measures documented with DAX and business logic
- [ ] Relationships documented
- [ ] Model diagram included
- [ ] Performance considerations noted
