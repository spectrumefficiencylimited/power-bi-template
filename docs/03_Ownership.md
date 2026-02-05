# Ownership & Responsibilities

> **Instructions:** Define clear ownership and responsibilities for this report. All contacts should be notified of their assignment.

## RACI Matrix

| Activity | Report Owner | Data Steward | Developer | Business Sponsor |
|----------|:------------:|:------------:|:---------:|:----------------:|
| Requirements definition | A | C | I | R |
| Data quality decisions | C | R | I | A |
| Technical implementation | I | C | R | I |
| Security/access decisions | A | C | I | R |
| Change approval | A | C | I | R |
| Incident response | I | C | R | A |
| Decommissioning | A | C | I | R |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

## Primary Contacts

### Report Owner

| Field | Value |
|-------|-------|
| **Name** | _[Full name]_ |
| **Role** | _[Job title]_ |
| **Department** | _[Department/Unit]_ |
| **Email** | _[email@organization.com]_ |
| **Phone** | _[Optional]_ |
| **Responsibilities** | Business requirements, user acceptance, change approval |

### Data Steward

| Field | Value |
|-------|-------|
| **Name** | _[Full name]_ |
| **Role** | _[Job title]_ |
| **Department** | _[Department/Unit]_ |
| **Email** | _[email@organization.com]_ |
| **Phone** | _[Optional]_ |
| **Responsibilities** | Data quality, business definitions, data access requests |

### Developer

| Field | Value |
|-------|-------|
| **Name** | _[Full name]_ |
| **Role** | _[Job title]_ |
| **Department** | _[Department/Unit]_ |
| **Email** | _[email@organization.com]_ |
| **Phone** | _[Optional]_ |
| **Responsibilities** | Technical implementation, bug fixes, performance tuning |

### Business Sponsor

| Field | Value |
|-------|-------|
| **Name** | _[Full name]_ |
| **Role** | _[Job title]_ |
| **Department** | _[Department/Unit]_ |
| **Email** | _[email@organization.com]_ |
| **Phone** | _[Optional]_ |
| **Responsibilities** | Strategic alignment, funding, executive escalation |

## Secondary/Backup Contacts

| Role | Primary | Backup | Backup Email |
|------|---------|--------|--------------|
| Report Owner | _[Name]_ | _[Backup name]_ | _[email]_ |
| Data Steward | _[Name]_ | _[Backup name]_ | _[email]_ |
| Developer | _[Name]_ | _[Backup name]_ | _[email]_ |

## Distribution Groups

| Group Purpose | Group Email/Name | Members |
|---------------|------------------|---------|
| Incident notifications | _[email/Teams channel]_ | Developer, Data Steward |
| Change notifications | _[email/Teams channel]_ | All stakeholders |
| User support | _[email/Teams channel]_ | Report Owner, Developer |

## Escalation Path

```
Level 1: Developer
    ↓ (4 hours unresolved)
Level 2: Data Steward + Report Owner
    ↓ (1 business day unresolved)
Level 3: Business Sponsor
    ↓ (Critical business impact)
Level 4: Manager → IT Director
```

### Escalation Criteria

| Severity | Description | Response Time | Escalation Trigger |
|----------|-------------|---------------|-------------------|
| Critical | Report unavailable, data corruption | 1 hour | Immediate to L2 |
| High | Major feature broken, significant data issues | 4 hours | 4 hours to L2 |
| Medium | Minor issues, workaround available | 1 business day | 1 day to L2 |
| Low | Enhancement requests, cosmetic issues | 5 business days | As needed |

## Support Hours

| Support Level | Hours | Contact Method |
|---------------|-------|----------------|
| Standard support | Mon–Fri 8:30–17:00 AEST | Email, Teams |
| After-hours (Critical only) | As needed | Phone to on-call |

## Handover Procedures

### When a contact changes role

1. Current contact notifies team
2. Identify and confirm replacement
3. Update this document
4. Update Power BI workspace permissions
5. Knowledge transfer session (if needed)
6. Update distribution groups

### Documentation to transfer

- [ ] This repository and all documentation
- [ ] Power BI Service workspace access
- [ ] Azure DevOps work items
- [ ] Any related runbooks or procedures

---

**Completion Checklist:**
- [ ] All primary contacts assigned
- [ ] Backup contacts identified
- [ ] All contacts notified of their responsibilities
- [ ] Distribution groups created/documented
- [ ] Escalation path agreed with stakeholders
