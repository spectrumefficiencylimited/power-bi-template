# Testing & Validation

> **Instructions:** Document all testing performed before production deployment. This provides an audit trail and ensures quality.

## Testing Summary

| Test Phase | Status | Tester | Date | Sign-off |
|------------|--------|--------|------|----------|
| Unit Testing | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |
| Integration Testing | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |
| Data Validation | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |
| UAT | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |
| Performance Testing | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |
| Security Testing | Not Started / In Progress / Complete | _[Name]_ | _[Date]_ | ☐ |

## Test Environment

| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| Development | Developer testing | Sample/Dev data | Developer only |
| Test/UAT | User acceptance | Production copy or representative | Testers, business users |
| Production | Live use | Production data | All authorised users |

---

## Unit Testing

### Measure Tests

| Measure Name | Test Scenario | Expected Result | Actual Result | Pass/Fail |
|--------------|---------------|-----------------|---------------|-----------|
| _[Measure]_ | _[Specific filter/context]_ | _[Expected value]_ | _[Actual]_ | ✅ / ❌ |
| _[Measure]_ | _[Specific filter/context]_ | _[Expected value]_ | _[Actual]_ | ✅ / ❌ |
| _[Measure]_ | _[Edge case: null values]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |
| _[Measure]_ | _[Edge case: no data]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |

### Visual Tests

| Visual/Page | Test Scenario | Expected Behaviour | Actual | Pass/Fail |
|-------------|---------------|--------------------|--------|-----------|
| _[Page/Visual]_ | _[Interaction test]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |
| _[Page/Visual]_ | _[Filter test]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |
| _[Page/Visual]_ | _[Drill-through]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |

---

## Data Validation

### Row Count Reconciliation

| Table | Source Count | Power BI Count | Variance | Acceptable? |
|-------|--------------|----------------|----------|-------------|
| _[Table]_ | _[Count]_ | _[Count]_ | _[Diff]_ | ✅ / ❌ |
| _[Table]_ | _[Count]_ | _[Count]_ | _[Diff]_ | ✅ / ❌ |

### Aggregate Reconciliation

| Metric | Source Value | Power BI Value | Variance | Acceptable? |
|--------|--------------|----------------|----------|-------------|
| _[Total Sales]_ | _[Value]_ | _[Value]_ | _[Diff]_ | ✅ / ❌ |
| _[Count Students]_ | _[Value]_ | _[Value]_ | _[Diff]_ | ✅ / ❌ |

### Data Quality Checks

| Check | Rule | Result | Notes |
|-------|------|--------|-------|
| Null key values | No nulls in primary keys | Pass / Fail | _[Details]_ |
| Duplicate records | No duplicates in fact tables | Pass / Fail | _[Details]_ |
| Referential integrity | All FKs have matching PKs | Pass / Fail | _[Details]_ |
| Date range | Data within expected range | Pass / Fail | _[Details]_ |
| Outliers | Values within expected bounds | Pass / Fail | _[Details]_ |

### Historical Comparison

| Metric | Previous Report | This Report | Variance | Explanation |
|--------|-----------------|-------------|----------|-------------|
| _[Metric]_ | _[Value]_ | _[Value]_ | _[Diff]_ | _[Why different]_ |

---

## Integration Testing

### Refresh Testing

| Test | Expected | Actual | Pass/Fail |
|------|----------|--------|-----------|
| Full refresh completes | < _[X]_ minutes | _[Actual time]_ | ✅ / ❌ |
| Incremental refresh (if used) | Refreshes only new data | _[Behaviour]_ | ✅ / ❌ |
| Refresh with source unavailable | Fails gracefully with alert | _[Behaviour]_ | ✅ / ❌ |

### Gateway Testing

| Test | Expected | Actual | Pass/Fail |
|------|----------|--------|-----------|
| Connection through gateway | Successful | _[Result]_ | ✅ / ❌ |
| Gateway failover (if applicable) | Automatic failover | _[Result]_ | ✅ / ❌ |

---

## User Acceptance Testing (UAT)

### UAT Participants

| Name | Role | Department | UAT Date |
|------|------|------------|----------|
| _[Name]_ | _[Role]_ | _[Dept]_ | _[Date]_ |
| _[Name]_ | _[Role]_ | _[Dept]_ | _[Date]_ |

### UAT Test Cases

| TC# | Test Case | Steps | Expected Result | Actual Result | Status |
|-----|-----------|-------|-----------------|---------------|--------|
| UAT-001 | _[Description]_ | _[Steps]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |
| UAT-002 | _[Description]_ | _[Steps]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |
| UAT-003 | _[Description]_ | _[Steps]_ | _[Expected]_ | _[Actual]_ | ✅ / ❌ |

### UAT Issues/Feedback

| Issue# | Description | Severity | Resolution | Status |
|--------|-------------|----------|------------|--------|
| _[#]_ | _[Issue description]_ | High/Medium/Low | _[How resolved]_ | Open/Closed |

### UAT Sign-off

| Role | Name | Sign-off Date | Signature |
|------|------|---------------|-----------|
| Report Owner | _[Name]_ | _[Date]_ | ☐ Approved |
| Data Steward | _[Name]_ | _[Date]_ | ☐ Approved |
| Business Sponsor | _[Name]_ | _[Date]_ | ☐ Approved |

---

## Performance Testing

### Load Times

| Scenario | Target | Actual | Pass/Fail |
|----------|--------|--------|-----------|
| Initial report load | < _[X]_ seconds | _[Actual]_ | ✅ / ❌ |
| Page navigation | < _[X]_ seconds | _[Actual]_ | ✅ / ❌ |
| Filter application | < _[X]_ seconds | _[Actual]_ | ✅ / ❌ |
| Cross-filter interaction | < _[X]_ seconds | _[Actual]_ | ✅ / ❌ |

### DAX Query Performance

| Query/Measure | Target | Actual | Optimisation Notes |
|---------------|--------|--------|-------------------|
| _[Measure]_ | < _[X]_ ms | _[Actual]_ | _[Notes]_ |
| _[Measure]_ | < _[X]_ ms | _[Actual]_ | _[Notes]_ |

### Concurrent User Testing

| User Count | Response Time | Behaviour | Pass/Fail |
|------------|---------------|-----------|-----------|
| 10 users | _[Time]_ | _[Behaviour]_ | ✅ / ❌ |
| 50 users | _[Time]_ | _[Behaviour]_ | ✅ / ❌ |

---

## Security Testing

### RLS Testing

| Role | User | Expected Data | Actual Data | Pass/Fail |
|------|------|---------------|-------------|-----------|
| _[Role]_ | _[Test user]_ | _[What they should see]_ | _[What they saw]_ | ✅ / ❌ |
| _[Role]_ | _[Test user]_ | _[What they should see]_ | _[What they saw]_ | ✅ / ❌ |

### Permission Testing

| Test | Expected | Actual | Pass/Fail |
|------|----------|--------|-----------|
| Viewer cannot edit | No edit options visible | _[Result]_ | ✅ / ❌ |
| Contributor can edit | Edit options available | _[Result]_ | ✅ / ❌ |
| Export permissions | As configured | _[Result]_ | ✅ / ❌ |

---

## Pre-Production Checklist

### Technical Readiness

- [ ] All unit tests passed
- [ ] All data validation checks passed
- [ ] Refresh tested successfully
- [ ] Performance meets targets
- [ ] RLS tested and verified
- [ ] Error handling verified

### Documentation Readiness

- [ ] All metadata documentation complete
- [ ] Change log updated
- [ ] User guide available (if required)

### Business Readiness

- [ ] UAT completed and signed off
- [ ] Report Owner approval received
- [ ] Data Steward approval received
- [ ] Training completed (if required)
- [ ] Communication plan executed

## Production Deployment Approval

| Approver | Name | Date | Approval |
|----------|------|------|----------|
| Developer | _[Name]_ | _[Date]_ | ☐ Ready for deployment |
| Report Owner | _[Name]_ | _[Date]_ | ☐ Approved for production |
| Data Steward | _[Name]_ | _[Date]_ | ☐ Data quality confirmed |

**Deployment Date:** _[Target date]_  
**Deployed By:** _[Name]_  
**Deployment Verified:** ☐ Yes

---

## Post-Deployment Verification

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Report accessible | All users can access | _[Result]_ | ✅ / ❌ |
| Data refreshed | Current data displayed | _[Result]_ | ✅ / ❌ |
| Subscriptions working | Emails sent | _[Result]_ | ✅ / ❌ |
| Embedded views working | Loads correctly | _[Result]_ | ✅ / ❌ |

**Post-deployment issues:** _[None / List issues]_
