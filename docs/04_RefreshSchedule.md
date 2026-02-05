# Refresh Schedule

> **Instructions:** Document the data refresh configuration for this report. This is essential for troubleshooting and understanding data currency.

## Refresh Summary

| Dataset | Frequency | Window | Last Successful | Status |
|---------|-----------|--------|-----------------|--------|
| _[Semantic model name]_ | Daily / Hourly / Weekly | _[e.g., 06:00 AEST]_ | _[Date/time]_ | Active / Paused |

## Detailed Refresh Configuration

### Primary Dataset: _[Semantic Model Name]_

| Attribute | Value |
|-----------|-------|
| **Dataset Name** | _[Name as shown in Power BI Service]_ |
| **Workspace** | _[Workspace name]_ |
| **Refresh Type** | Scheduled / On-demand / Dataflow-triggered |
| **Frequency** | _[e.g., Daily, Twice daily, Hourly]_ |
| **Schedule Times** | _[e.g., 06:00, 18:00 AEST]_ |
| **Time Zone** | AEST / UTC |
| **Gateway** | _[Gateway name or N/A for cloud sources]_ |
| **Timeout Setting** | _[e.g., 2 hours]_ |

### Refresh Dependencies

```
┌────────────────────┐
│  Source System     │  Available: 05:00 AEST
│  ETL/Dataflow      │  
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Upstream Dataset  │  Refreshes: 05:30 AEST
│  (if applicable)   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  This Dataset      │  Refreshes: 06:00 AEST
│                    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Downstream        │  Depends on this dataset
│  Reports/Datasets  │
└────────────────────┘
```

### Dependency Details

| Dependency | Type | Expected Completion | Impact if Delayed |
|------------|------|--------------------|--------------------|
| _[Source ETL job]_ | Upstream | 05:00 AEST | Refresh fails |
| _[Shared dataset]_ | Upstream | 05:30 AEST | Stale data |
| _[Downstream report]_ | Downstream | After this refresh | Their data delayed |

## Failure Handling

### Notification Configuration

| Event | Notification Method | Recipients |
|-------|---------------------|------------|
| Refresh failure | Email | _[Developer email]_ |
| Refresh failure | Teams channel | _[Channel name/link]_ |
| Consecutive failures (3+) | Escalation email | _[Data Steward, Report Owner]_ |

### Failure Response Procedure

1. **Immediate** (within 15 minutes of alert):
   - Check Power BI Service refresh history for error details
   - Check gateway connectivity (if applicable)
   - Check source system availability

2. **Troubleshooting steps**:
   - Review error message in refresh history
   - Check gateway logs: _[location/how to access]_
   - Verify credentials haven't expired
   - Check for source data issues

3. **Manual refresh** (if needed):
   - Navigate to workspace → Dataset → Refresh now
   - Or use PowerShell: `Invoke-PowerBIRestMethod ...`

4. **Escalation** (if not resolved in 2 hours):
   - Notify Data Steward and Report Owner
   - Create incident ticket: _[Link to ticketing system]_

### Retry Configuration

| Setting | Value |
|---------|-------|
| Auto-retry enabled | Yes / No |
| Retry attempts | _[e.g., 3]_ |
| Retry interval | _[e.g., 30 minutes]_ |

## Incremental Refresh (if configured)

| Setting | Value |
|---------|-------|
| Enabled | Yes / No |
| Range Start Parameter | _[Parameter name]_ |
| Range End Parameter | _[Parameter name]_ |
| Archive Period | _[e.g., 3 years]_ |
| Incremental Period | _[e.g., 10 days]_ |
| Detect Data Changes | Yes / No |
| Only Refresh Complete Days | Yes / No |

## Maintenance Windows

| Window | Schedule | Impact |
|--------|----------|--------|
| Source system maintenance | _[e.g., First Sunday monthly, 02:00-06:00]_ | Refresh may fail |
| Gateway maintenance | _[e.g., Quarterly, notified 2 weeks ahead]_ | All refreshes affected |
| Power BI Service maintenance | _[As announced by Microsoft]_ | Service may be unavailable |

### Planned Maintenance Actions

- [ ] Pause scheduled refresh before maintenance
- [ ] Notify stakeholders of expected data delay
- [ ] Resume and manually trigger refresh after maintenance
- [ ] Verify successful refresh

## Runbooks

### Manual Refresh Runbook

```powershell
# PowerShell example for manual refresh
Connect-PowerBIServiceAccount
$workspace = Get-PowerBIWorkspace -Name "[Workspace Name]"
$dataset = Get-PowerBIDataset -WorkspaceId $workspace.Id -Name "[Dataset Name]"
Invoke-PowerBIRestMethod -Url "datasets/$($dataset.Id)/refreshes" -Method Post
```

### Backfill Procedure

_[Document steps if historical data needs to be reloaded]_

1. _[Step 1]_
2. _[Step 2]_
3. _[Step 3]_

---

**Completion Checklist:**
- [ ] Refresh schedule configured in Power BI Service
- [ ] Failure notifications configured
- [ ] Dependencies documented
- [ ] Failure response procedure documented
- [ ] Runbook tested
