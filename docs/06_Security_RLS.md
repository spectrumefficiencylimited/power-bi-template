# Security & Row-Level Security (RLS)

> **Instructions:** Document all security configurations including RLS roles, workspace permissions, and data sensitivity controls.

## Security Overview

| Aspect | Status | Details |
|--------|--------|---------|
| Row-Level Security | Enabled / Not Required | _[Brief description]_ |
| Object-Level Security | Enabled / Not Required | _[Brief description]_ |
| Sensitivity Labels | Applied / Not Applied | _[Label name]_ |
| Workspace Access | Configured | _[See details below]_ |

## Data Classification

| Data Element | Classification | Justification |
|--------------|----------------|---------------|
| _[Table/Column]_ | Public / Internal / Confidential / Highly Confidential | _[Why this classification]_ |
| _[Table/Column]_ | Public / Internal / Confidential / Highly Confidential | _[Why this classification]_ |

### Classification Definitions

- **Public:** Can be shared externally
- **Internal:** UniSC staff only
- **Confidential:** Need-to-know basis, specific roles
- **Highly Confidential:** Restricted, approval required

## Row-Level Security (RLS)

### RLS Roles

| Role Name | Purpose | Filter Logic | Target Tables |
|-----------|---------|--------------|---------------|
| _[Role name]_ | _[Who should see what]_ | _[Brief description]_ | _[Tables filtered]_ |
| _[Role name]_ | _[Who should see what]_ | _[Brief description]_ _[Tables filtered]_ |

### Role Details

#### Role: _[Role Name 1]_

| Attribute | Value |
|-----------|-------|
| **Role Name** | _[Name as defined in model]_ |
| **Purpose** | _[Business reason for this role]_ |
| **Users See** | _[What data users in this role can see]_ |

**DAX Filter Expression:**

```dax
// Table: [TableName]
// Filter: Users only see their own department's data
[DepartmentCode] = USERPRINCIPALNAME()
```

**Mapped Users/Groups:**

| Type | Name | Email/ID |
|------|------|----------|
| Azure AD Group | _[Group name]_ | _[Group ID or email]_ |
| User | _[User name]_ | _[user@organization.com]_ |

**Testing Verification:**
- [ ] Tested with user from this role
- [ ] Verified correct data filtering
- [ ] Verified no data leakage
- Date tested: _[YYYY-MM-DD]_

---

#### Role: _[Role Name 2]_

_[Repeat structure for each role]_

---

### RLS Testing Matrix

| Test Scenario | Role | Expected Result | Actual Result | Pass/Fail |
|---------------|------|-----------------|---------------|-----------|
| _[User from Dept A]_ | _[Role]_ | Sees only Dept A data | _[Result]_ | ✅ / ❌ |
| _[User from Dept B]_ | _[Role]_ | Sees only Dept B data | _[Result]_ | ✅ / ❌ |
| _[Admin user]_ | _[Role]_ | Sees all data | _[Result]_ | ✅ / ❌ |

### Testing RLS

To test RLS in Power BI Desktop:
1. Go to **Modeling** → **View as**
2. Select the role to test
3. Optionally enter a specific user principal name
4. Verify data filtering is correct

## Object-Level Security (OLS)

_[If OLS is used, document which tables/columns are restricted and to whom]_

| Object | Type | Restricted From | Reason |
|--------|------|-----------------|--------|
| _[Table/Column]_ | Table / Column | _[Role names]_ | _[Reason]_ |

## Workspace Permissions

### Workspace: _[Workspace Name]_

| Role | Members | Permissions |
|------|---------|-------------|
| Admin | _[Users/Groups]_ | Full control |
| Member | _[Users/Groups]_ | Edit, publish, share |
| Contributor | _[Users/Groups]_ | Edit, publish |
| Viewer | _[Users/Groups]_ | View only |

### App Permissions (if published as app)

| Audience | Access Type | RLS Role Applied |
|----------|-------------|------------------|
| _[Group/Users]_ | View | _[Role name or None]_ |
| _[Group/Users]_ | View | _[Role name or None]_ |

## Sensitivity Labels

| Label Applied | Scope | Encryption | Watermark |
|---------------|-------|------------|-----------|
| _[Label name]_ | Entire report / Specific pages | Yes / No | Yes / No |

### Label Requirements

- [ ] Appropriate label selected based on data classification
- [ ] Label approved by Data Steward
- [ ] Users understand label restrictions

## Data Loss Prevention (DLP)

_[Document any DLP policies that apply to this report]_

| Policy | Rule | Action |
|--------|------|--------|
| _[Policy name]_ | _[What triggers it]_ | _[Block/Warn/Audit]_ |

## Access Request Process

### New User Access

1. User submits request to: _[Process/System/Contact]_
2. Report Owner approves business need
3. Data Steward verifies appropriate access level
4. IT/Admin grants workspace access
5. User added to appropriate RLS role (if applicable)

### Access Review

| Review Frequency | Reviewer | Last Review | Next Review |
|------------------|----------|-------------|-------------|
| Quarterly / Annually | _[Role/Name]_ | _[Date]_ | _[Date]_ |

## Audit & Compliance

### Audit Log Access

- Power BI Admin Portal: Activity logs
- Microsoft 365 Compliance Center: Unified audit log
- Azure Log Analytics (if configured)

### Key Events to Monitor

- [ ] Report views by user
- [ ] Data exports
- [ ] Sharing activities
- [ ] Permission changes

---

**Completion Checklist:**
- [ ] Data classification completed
- [ ] RLS roles defined and tested
- [ ] Workspace permissions configured
- [ ] Sensitivity labels applied (if required)
- [ ] Access request process documented
- [ ] Security review completed by: _[Name, Date]_
