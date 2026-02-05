# Dependencies

> **Instructions:** Document all upstream and downstream dependencies for this report. This is critical for impact analysis and change management.

## Dependency Map

```
                         UPSTREAM
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Source System │   │   Dataflow    │   │Shared Dataset │
│   (SQL DB)    │   │   (ADF/PBI)   │   │               │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  THIS REPORT  │
                    │               │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Downstream   │   │  Downstream   │   │   External    │
│   Report 1    │   │   Report 2    │   │   Consumer    │
└───────────────┘   └───────────────┘   └───────────────┘
                            │
                       DOWNSTREAM
```

## Upstream Dependencies

_[Systems, datasets, or processes that THIS report depends on]_

### Source Systems

| System | Type | Owner | Impact if Unavailable |
|--------|------|-------|----------------------|
| _[System name]_ | Database / API / File | _[Team/Contact]_ | _[Refresh fails / Stale data]_ |
| _[System name]_ | Database / API / File | _[Team/Contact]_ | _[Refresh fails / Stale data]_ |

### Dataflows/ETL Processes

| Dataflow/Pipeline | Location | Owner | Refresh Dependency |
|-------------------|----------|-------|-------------------|
| _[Name]_ | _[Workspace/ADF]_ | _[Contact]_ | Must complete before this report refreshes |
| _[Name]_ | _[Workspace/ADF]_ | _[Contact]_ | Must complete before this report refreshes |

### Shared Datasets

| Dataset Name | Workspace | Owner | Tables Used |
|--------------|-----------|-------|-------------|
| _[Dataset]_ | _[Workspace]_ | _[Contact]_ | _[Tables referenced]_ |

### Gateways

| Gateway Name | Type | Location | Managed By |
|--------------|------|----------|------------|
| _[Gateway]_ | On-premises / VNet | _[Server/location]_ | _[Team]_ |

### External APIs/Services

| Service | Purpose | SLA | Fallback |
|---------|---------|-----|----------|
| _[Service]_ | _[Why used]_ | _[Availability SLA]_ | _[What happens if down]_ |

## Downstream Dependencies

_[Reports, applications, or processes that depend on THIS report]_

### Downstream Reports

| Report Name | Workspace | Owner | Dependency Type |
|-------------|-----------|-------|-----------------|
| _[Report]_ | _[Workspace]_ | _[Contact]_ | Live connection / Composite model |
| _[Report]_ | _[Workspace]_ | _[Contact]_ | Live connection / Composite model |

### Subscriptions/Exports

| Subscriber | Type | Frequency | Format |
|------------|------|-----------|--------|
| _[User/Group]_ | Email subscription | _[Daily/Weekly]_ | PDF / PPTX |
| _[Process]_ | Data export | _[Frequency]_ | Excel / CSV |

### External Consumers

| Consumer | Integration Method | Contact | Impact of Changes |
|----------|-------------------|---------|-------------------|
| _[Application/Team]_ | _[API/Export/Embed]_ | _[Contact]_ | _[What breaks if we change]_ |

### Embedded Reports

| Application | Location | Owner | Notes |
|-------------|----------|-------|-------|
| _[App name]_ | _[SharePoint/Teams/Portal]_ | _[Contact]_ | _[Embed details]_ |

## Parameters

| Parameter Name | Current Value | Purpose | Affects |
|----------------|---------------|---------|---------|
| _[Parameter]_ | _[Value]_ | _[Why this parameter]_ | _[What queries use it]_ |
| _[Parameter]_ | _[Value]_ | _[Why this parameter]_ | _[What queries use it]_ |

### Environment-Specific Parameters

| Parameter | Dev | Test | Prod |
|-----------|-----|------|------|
| ServerName | _[dev-server]_ | _[test-server]_ | _[prod-server]_ |
| DatabaseName | _[dev-db]_ | _[test-db]_ | _[prod-db]_ |

## Impact Analysis

### If This Report Changes

| Change Type | Affected Components | Required Actions |
|-------------|---------------------|------------------|
| Schema change | _[List downstream deps]_ | Notify owners, test connections |
| Measure rename | _[Reports using this measure]_ | Update references |
| Table removal | _[Dependent reports]_ | Coordinate migration |

### If Upstream Changes

| Upstream Component | Potential Impact | Mitigation |
|--------------------|------------------|------------|
| _[Source system]_ | _[What could break]_ | _[How to handle]_ |
| _[Shared dataset]_ | _[What could break]_ | _[How to handle]_ |

## Change Notification Matrix

| Component | Change Requires Notification To |
|-----------|--------------------------------|
| This report schema | _[Downstream report owners]_ |
| This report measures | _[Downstream report owners, subscribers]_ |
| Upstream source schema | _[This report developer]_ |
| Gateway maintenance | _[All reports using gateway]_ |

## Dependency Health Checks

### Automated Monitoring

| Check | Tool | Frequency | Alert To |
|-------|------|-----------|----------|
| Refresh success | Power BI Service | Per refresh | _[Email/Teams]_ |
| Source availability | _[Monitoring tool]_ | _[Interval]_ | _[Contact]_ |
| Gateway connectivity | Power BI Admin | Real-time | _[IT team]_ |

### Manual Reviews

| Review | Frequency | Reviewer | Last Completed |
|--------|-----------|----------|----------------|
| Dependency accuracy | Quarterly | Developer | _[Date]_ |
| Unused dependencies | Annually | Developer + Steward | _[Date]_ |

---

**Completion Checklist:**
- [ ] All upstream dependencies documented
- [ ] All downstream dependencies documented
- [ ] Parameters documented with environment values
- [ ] Impact analysis completed
- [ ] Notification matrix agreed with stakeholders
