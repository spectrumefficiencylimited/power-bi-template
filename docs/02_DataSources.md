# Data Sources

> **Instructions:** Document all data sources used in this report. This information is critical for troubleshooting, security reviews, and impact analysis.

## Source Systems Overview

| # | Source System | Connection Type | Environment | Data Classification |
|---|---------------|-----------------|-------------|---------------------|
| 1 | _[System name]_ | DirectQuery / Import | Dev / Prod | Public / Internal / Confidential |
| 2 | _[System name]_ | DirectQuery / Import | Dev / Prod | Public / Internal / Confidential |

## Detailed Source Documentation

### Source 1: _[System Name]_

| Attribute | Value |
|-----------|-------|
| **System Name** | _[e.g., Student Management System]_ |
| **Database** | _[e.g., SMS_DW]_ |
| **Schema** | _[e.g., dbo]_ |
| **Connection Type** | Import / DirectQuery / Dual |
| **Gateway Required** | Yes / No |
| **Gateway Name** | _[Gateway name if applicable]_ |
| **Credential Type** | OAuth / Service Account / Key Vault |
| **Credential Reference** | _[Key Vault secret name or credential ID]_ |
| **Data Classification** | Public / Internal / Confidential / Highly Confidential |
| **Refresh Method** | Full / Incremental |
| **Expected Volume** | _[e.g., ~500K rows]_ |
| **Expected Latency** | _[e.g., T+1 day]_ |

#### Tables/Views Used

| Table/View Name | Purpose | Row Count (approx) | Key Columns |
|-----------------|---------|-------------------|-------------|
| _[table_name]_ | _[Why this table is used]_ | _[e.g., 100K]_ | _[Key columns]_ |
| _[table_name]_ | _[Why this table is used]_ | _[e.g., 50K]_ | _[Key columns]_ |

#### Source-Specific Notes

_[Any important notes about this source—e.g., known data quality issues, refresh windows, maintenance schedules]_

---

### Source 2: _[System Name]_

| Attribute | Value |
|-----------|-------|
| **System Name** | _[e.g., Finance System]_ |
| **Database** | _[e.g., FIN_DW]_ |
| **Schema** | _[e.g., reporting]_ |
| **Connection Type** | Import / DirectQuery / Dual |
| **Gateway Required** | Yes / No |
| **Gateway Name** | _[Gateway name if applicable]_ |
| **Credential Type** | OAuth / Service Account / Key Vault |
| **Credential Reference** | _[Key Vault secret name or credential ID]_ |
| **Data Classification** | Public / Internal / Confidential / Highly Confidential |
| **Refresh Method** | Full / Incremental |
| **Expected Volume** | _[e.g., ~200K rows]_ |
| **Expected Latency** | _[e.g., Real-time]_ |

#### Tables/Views Used

| Table/View Name | Purpose | Row Count (approx) | Key Columns |
|-----------------|---------|-------------------|-------------|
| _[table_name]_ | _[Why this table is used]_ | _[e.g., 100K]_ | _[Key columns]_ |

#### Source-Specific Notes

_[Any important notes about this source]_

---

_[Copy the "Source N" section template for additional sources]_

## Connection Strings

> ⚠️ **Security Note:** Never store actual credentials in this file. Reference Key Vault secrets or credential IDs only.

```
# Example connection string format (credentials redacted)
Server=sqlserver.database.windows.net;Database=DatabaseName;Authentication=ActiveDirectoryServicePrincipal
```

## Data Flow Diagram

_[Optional: Include a simple diagram showing data flow from source systems to Power BI]_

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Source System  │────▶│   Gateway    │────▶│  Power BI       │
│  (SQL Server)   │     │  (On-prem)   │     │  Semantic Model │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

## Environment Configuration

| Environment | Purpose | Data Source |
|-------------|---------|-------------|
| Development | Building and testing | Dev database / sample data |
| Test/UAT | User acceptance testing | Test database |
| Production | Live reporting | Production database |

### Environment Parameters

_[Document any parameters that change between environments:]_

| Parameter Name | Dev Value | Test Value | Prod Value |
|----------------|-----------|------------|------------|
| ServerName | _[dev-server]_ | _[test-server]_ | _[prod-server]_ |
| DatabaseName | _[dev-db]_ | _[test-db]_ | _[prod-db]_ |

---

**Completion Checklist:**
- [ ] All data sources documented
- [ ] Connection types specified
- [ ] Data classification assigned
- [ ] Gateway requirements identified
- [ ] Credential references documented (no actual credentials)
- [ ] Environment configuration complete
