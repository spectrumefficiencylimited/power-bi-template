# Change Log

> **Instructions:** Record all significant changes to this report. Update this log with every deployment to Test or Production.

## Change Log Format

All changes should be recorded using the following format:
- **Version:** Semantic versioning (MAJOR.MINOR.PATCH)
- **Date:** YYYY-MM-DD
- **Author:** Person who made the change
- **Change Type:** Feature / Fix / Enhancement / Breaking Change / Documentation
- **Description:** Clear description of what changed and why

---

## Version History

### Version 1.0.0 — _[YYYY-MM-DD]_ — Initial Release

**Author:** _[Name]_  
**Approved By:** _[Report Owner name]_  
**Work Item:** _[Azure DevOps/Jira link]_

**Summary:**
Initial release of the report with core functionality.

**Changes:**
- Initial data model created with _[X]_ tables
- _[X]_ measures implemented
- _[X]_ report pages created
- RLS configured for _[describe scope]_

**Deployment:**
- [ ] Deployed to Development
- [ ] Deployed to Test/UAT
- [ ] UAT sign-off received
- [ ] Deployed to Production

---

### Version 1.1.0 — _[YYYY-MM-DD]_ — _[Brief Title]_

**Author:** _[Name]_  
**Approved By:** _[Report Owner name]_  
**Work Item:** _[Link]_

**Summary:**
_[One-line summary of this release]_

**Changes:**
| Change Type | Description |
|-------------|-------------|
| Feature | _[Description]_ |
| Enhancement | _[Description]_ |
| Fix | _[Description]_ |

**Impact:**
- _[What users will notice]_
- _[Any breaking changes or migration steps]_

**Deployment:**
- [ ] Deployed to Development
- [ ] Deployed to Test/UAT
- [ ] UAT sign-off received
- [ ] Deployed to Production

---

### Version 1.0.1 — _[YYYY-MM-DD]_ — _[Brief Title]_

**Author:** _[Name]_  
**Approved By:** _[Report Owner name]_  
**Work Item:** _[Link]_

**Summary:**
_[One-line summary]_

**Changes:**
| Change Type | Description |
|-------------|-------------|
| Fix | _[Description]_ |

**Deployment:**
- [ ] Deployed to Development
- [ ] Deployed to Test/UAT
- [ ] UAT sign-off received
- [ ] Deployed to Production

---

_[Copy template for additional versions]_

---

## Pending Changes

_[Track changes that are in development but not yet released]_

| Change | Status | Target Version | Assigned To | Work Item |
|--------|--------|----------------|-------------|-----------|
| _[Description]_ | In Progress / Review | _[e.g., 1.2.0]_ | _[Name]_ | _[Link]_ |
| _[Description]_ | In Progress / Review | _[e.g., 1.2.0]_ | _[Name]_ | _[Link]_ |

## Breaking Changes Register

_[Document any changes that require user action or cause compatibility issues]_

| Version | Breaking Change | Migration Steps | Communication |
|---------|-----------------|-----------------|---------------|
| _[Version]_ | _[What broke]_ | _[Steps to resolve]_ | _[How users were notified]_ |

## Git Commit Reference

For detailed code-level changes, see the Git commit history:

```bash
# View recent commits
git log --oneline -20

# View changes in a specific version
git log v1.0.0..v1.1.0 --oneline
```

---

**Change Log Maintenance:**
- Update this log for every deployment
- Include work item links for traceability
- Get approval before production deployment
- Archive very old entries annually (keep last 2 years visible)
