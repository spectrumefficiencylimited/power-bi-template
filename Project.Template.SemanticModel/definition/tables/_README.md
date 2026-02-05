# Tables Directory

This folder contains TMDL definitions for each table in the semantic model.

When you add tables in Power BI Desktop and save, individual `.tmdl` files will appear here—one per table.

## Naming Conventions

- Use PascalCase for table names (e.g., `StudentEnrollment`, `CourseDetails`)
- Prefix fact tables with `Fact_` or use a clear naming pattern
- Prefix dimension tables with `Dim_` or use a clear naming pattern
- Date tables should be clearly identified (e.g., `Calendar`, `DateDimension`)

## Documentation Requirements

Each table should have:
- A description in the TMDL file
- Column descriptions for business-critical fields
- Documentation in `/docs/05_SemanticModel.md`

## Example Table Structure

```tmdl
table StudentEnrollment
    description: "Fact table containing student enrollment records by term"
    lineageTag: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    column StudentID
        description: "Unique identifier for each student"
        dataType: int64
        formatString: 0
        lineageTag: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        summarizeBy: none
        sourceColumn: StudentID
```
