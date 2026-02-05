# Contributing to PBIP Projects

This document outlines the standards and practices for contributing to Power BI PBIP projects within your organization.

## Getting Started

### Prerequisites

1. **Power BI Desktop** with preview features enabled:
   - File → Options → Preview features
   - Enable "Power BI Project (.pbip) save option"
   - Enable "Store reports using enhanced metadata format (PBIR)"

2. **Visual Studio Code** with extensions:
   - [TMDL Extension](https://marketplace.visualstudio.com/items?itemName=analysis-services.TMDL)
   - GitHub Copilot (optional, requires UniSC account)

3. **Git** configured with your identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@organization.com"
   ```

## Branching Strategy

We follow a simplified Git Flow:

```
main (production)
  │
  └── develop (integration)
        │
        ├── feature/add-new-measure
        ├── feature/update-rls
        └── fix/refresh-timeout
```

### Branch Naming

- `feature/description` - New functionality
- `fix/description` - Bug fixes
- `docs/description` - Documentation only
- `refactor/description` - Code improvements without functionality change

### Workflow

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-new-feature
   ```

2. Make your changes and commit frequently:
   ```bash
   git add .
   git commit -m "Add: Description of change"
   ```

3. Push and create a Pull Request:
   ```bash
   git push -u origin feature/my-new-feature
   ```

4. Request review from at least one team member

5. After approval, merge to `develop`

6. Periodically, `develop` is merged to `main` for production release

## Commit Message Format

Use clear, descriptive commit messages:

```
<type>: <short description>

[optional body with more detail]

[optional footer with work item reference]
```

**Types:**
- `Add:` New feature or content
- `Fix:` Bug fix
- `Update:` Changes to existing functionality
- `Remove:` Removing features or content
- `Docs:` Documentation changes only
- `Refactor:` Code restructuring without functional change

**Examples:**
```
Add: Student retention KPI measure

Implements the retention rate calculation as defined in the business glossary.
Uses academic year cohort tracking methodology.

Work Item: #1234
```

```
Fix: Refresh timeout on large fact table

Increased query timeout and added incremental refresh
to handle growing data volume.
```

## Code Standards

### DAX Measures

- Use meaningful names (PascalCase)
- Include a comment explaining the business logic
- Add proper formatting for readability:

```dax
Student Retention Rate = 
// Purpose: Calculate year-over-year student retention
// Author: [Name], [Date]
VAR CurrentYearStudents = 
    DISTINCTCOUNT(Enrollment[StudentID])
VAR ReturnedStudents = 
    CALCULATE(
        DISTINCTCOUNT(Enrollment[StudentID]),
        FILTER(
            Enrollment,
            Enrollment[IsReturning] = TRUE
        )
    )
RETURN
    DIVIDE(ReturnedStudents, CurrentYearStudents, BLANK())
```

### TMDL Files

- Add descriptions to all tables and measures
- Use consistent naming conventions
- Document relationships and their purpose

### Metadata Documentation

- Complete all sections before requesting production deployment
- Use Australian English spelling
- Keep documentation up to date with every change
- Reference Azure DevOps work items where applicable

## Pull Request Process

### Before Creating a PR

- [ ] All tests pass (refresh works, measures calculate correctly)
- [ ] Documentation updated (Change Log, any affected metadata files)
- [ ] No merge conflicts with `develop`
- [ ] Self-reviewed the diff for any issues

### PR Description Template

```markdown
## Summary
[Brief description of changes]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactor

## Changes Made
- [Change 1]
- [Change 2]

## Testing Done
- [ ] Measures validated against source
- [ ] RLS tested (if applicable)
- [ ] Refresh tested successfully

## Screenshots
[If visual changes, include before/after]

## Work Item
[Link to Azure DevOps item]
```

### Review Checklist

Reviewers should verify:

- [ ] Changes match the described scope
- [ ] Code follows team standards
- [ ] Documentation is complete
- [ ] No sensitive data exposed
- [ ] Performance considerations addressed

## File Handling

### Files to Commit

✅ Always commit:
- `.pbip` files
- All files in `.Report/definition/`
- All files in `.SemanticModel/definition/`
- All files in `/docs/`
- `.gitignore`
- `README.md`

### Files to Never Commit

❌ Never commit (handled by .gitignore):
- `cache.abf` (data cache)
- `.pbi/` folder (local state)
- Any file containing credentials
- Large data files

## Getting Help

- **Technical issues:** Contact the development team
- **Process questions:** Refer to this guide or ask in the Teams channel
- **Template improvements:** Submit a PR to the template repository

## Code of Conduct

- Be respectful and constructive in code reviews
- Document your decisions for future maintainers
- Ask questions—there are no bad questions
- Share knowledge and help others learn

---

**Last Updated:** 2026-02-03  
**Maintained By:** Your Organization
