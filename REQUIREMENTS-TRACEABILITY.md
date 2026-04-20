# Requirements Traceability - EPMO Executive Portfolio Report

| Field | Value |
|-------|-------|
| Project | EPMO Executive Portfolio Report |
| Date | 2026-03-31 |
| Purpose | Trace every explicit current-cycle requirement to evidence, with no assumptions |
| Scope rule | Only requirements explicitly stated in the current docs, meeting notes, or PBIP/TMDL artefacts are included |

## How this file is controlled

This matrix is intentionally strict.

- If a requirement is directly visible in PBIP or TMDL, it is marked as repo-evidenced.
- If a requirement is operational or business-process only, it is marked as docs/notes evidenced.
- If a requirement is known but not yet satisfied in the current build, it is marked open or pending.
- If a requirement belongs to roadmap only, it is marked excluded from the current baseline.

Nothing in this file should be inferred from preferred future architecture.

## Source codes

- `MN` = `Meeting notes.md`
- `KR` = `KNOWLEDGE-REGISTER.md`
- `PO` = `iau-pbip-template/docs/01_ProjectOverview.md`
- `DS` = `iau-pbip-template/docs/02_DataSources.md`
- `OW` = `iau-pbip-template/docs/03_Ownership.md`
- `RS` = `iau-pbip-template/docs/04_RefreshSchedule.md`
- `SM` = `iau-pbip-template/docs/05_SemanticModel.md`
- `SEC` = `iau-pbip-template/docs/06_Security_RLS.md`
- `CL` = `iau-pbip-template/docs/07_ChangeLog.md`
- `BG` = `iau-pbip-template/docs/08_BusinessGlossary.md`
- `DEP` = `iau-pbip-template/docs/09_Dependencies.md`
- `TV` = `iau-pbip-template/docs/10_TestingValidation.md`
- `VM` = `iau-pbip-template/docs/11_VisualModularity.md`
- `LL` = `iau-pbip-template/docs/12_LessonsLearned.md`
- `PBIP` = `epmo report.Report/definition/...`
- `TMDL` = `epmo report.SemanticModel/definition/...`

## Status legend

- `Implemented` = present in the current solution baseline
- `Operational` = current process/business requirement, not necessarily stored in PBIP files
- `Open defect` = known requirement not yet satisfied correctly
- `Pending` = referenced in docs, but not evidenced as implemented in the current build
- `Excluded` = explicitly not part of the current baseline

## Traceability Matrix

| ID | Requirement | Source(s) | Evidence basis | Current state | Evidence note |
|---|---|---|---|---|---|
| `REQ-001` | The live source system for the report is Microsoft Dataverse at `orgca18cfd3.crm6.dynamics.com`. | `MN`, `PO`, `DS`, `KR`, `TMDL` | Repo + docs | `Implemented` | `epmo_project.tmdl` and `epmo_milestone.tmdl` partitions use `CommonDataService.Database("orgca18cfd3.crm6.dynamics.com")`. |
| `REQ-002` | The current semantic model is Import mode and the live implementation boundary is PBIP/TMDL, not a Synapse warehouse. | `PO`, `DS`, `SM`, `KR`, `TMDL` | Repo + docs | `Implemented` | Import partitions are present in TMDL; current docs describe Dataverse-backed PBIP as the live build. |
| `REQ-003` | `epmo_project` is the central table and `Project_Status_Unpivoted` is a current implemented derived table used by the model. | `SM`, `KR`, `TMDL` | Repo + docs | `Implemented` | `epmo_project.tmdl` and `Project_Status_Unpivoted.tmdl` are present in the current model definition. |
| `REQ-004` | `systemuser` is used to resolve user IDs to readable names for project manager identification. | `MN`, `DS`, `SM`, `KR`, `TMDL` | Repo + docs | `Implemented` | `relationships.tmdl` includes `epmo_projectepmouser.createdby -> systemuser.systemuserid`; docs and notes describe Michael maintaining `systemuser`. |
| `REQ-005` | The current report contains 8 pages in the defined order. | `PO`, `DS`, `KR`, `PBIP` | Repo + docs | `Implemented` | `pages/pages.json` plus the page metadata confirm 8 pages from `0_1. Home Page` to `5. Support Documentation By Portfolio`. |
| `REQ-006` | The Home Page acts as the entry page and navigates users to `0_2. Exec Summary`. | `MN`, `KR`, `PBIP` | Repo + notes | `Implemented` | Home-page navigation visual `ReportSection/visuals/4b6558e689cc1ad5444b/visual.json` uses `PageNavigation`; meeting notes describe the same landing behaviour. |
| `REQ-007` | The report visual design uses PowerPoint-exported backgrounds and SVG icon assets rather than fully native Power BI page chrome. | `MN`, `PO`, `KR`, `PBIP` | Repo + notes | `Implemented` | `report.json` registers PNG and SVG assets; meeting notes state the backgrounds were created in PowerPoint and imported into Power BI. |
| `REQ-008` | `0_2. Exec Summary` exists as a current report page and is the executive entry point before detailed pages. | `PO`, `KR`, `PBIP` | Repo + docs | `Implemented` | `pages/dd21f10f18d25fd0c675/page.json` confirms display name `0_2. Exec Summary`; current narrative visual exists on that page. |
| `REQ-009` | The Exec Summary page must provide navigation to the detailed report pages. | `MN`, `KR`, `PBIP` | Repo + notes | `Implemented` | Exec Summary visuals navigate to Overview, Executive Insights, Financial Performance, Delivery Performance, Risk Exposure, and Support Documentation By Portfolio. |
| `REQ-010` | Users must be able to analyse the portfolio by portfolio value. | `MN`, `PO`, `KR`, `PBIP` | Repo + notes | `Implemented` | Meeting notes describe portfolio filtering; current report visuals query `epmo_project.epmo_portfolioname` on Executive Insights and related pages. |
| `REQ-011` | Quarterly reporting in the app follows six steps: classification, RAG statuses, milestones, budget, risks, and external obligations. | `MN`, `KR` | Docs/notes | `Operational` | This workflow is stated in the meeting notes and carried into the grounded documentation. |
| `REQ-012` | Overall project status follows the "most severe indicator wins" business rule. | `MN`, `KR` | Docs/notes | `Operational` | Priscila's explanation in the meeting notes defines the rule; the register preserves it as the current business rule. |
| `REQ-013` | The canonical reporting status set is `On Track`, `At Risk`, `Significant Concerns`, and `Not Assessed`. | `PO`, `KR`, `TMDL` | Repo + docs | `Implemented` | The docs govern the display set; TMDL contains the current overall status measures and status columns. |
| `REQ-014` | Additional explanatory questions are only required when a project is `At Risk` or `Significant Concerns`. | `MN`, `KR` | Docs/notes | `Operational` | This is an app workflow rule from the meeting notes and should not be reinterpreted as missing data for `On Track` projects. |
| `REQ-015` | Project managers only see and edit their own assigned projects in the app; admins can access all projects. | `MN`, `PO`, `KR` | Docs/notes | `Operational` | The access rule is described in meeting notes and current docs; it is primarily enforced in Dataverse/app permissions rather than PBIP. |
| `REQ-016` | The report refresh must remain manual, quarterly, and triggered by Michael Newsome after the 1 p.m. PM submission deadline. | `MN`, `DS`, `RS`, `KR` | Docs/notes | `Operational` | Refresh runbook and meeting notes align on manual post-1 p.m. refresh by Michael Newsome. |
| `REQ-017` | The refreshed report is validated before executive use. | `MN`, `RS`, `KR` | Docs/notes | `Operational` | Current workflow states Priscila and Andrei review the refreshed report before executive summary and distribution. |
| `REQ-018` | Delivery Performance must include milestone tracking and late-project metrics. | `PO`, `KR`, `PBIP`, `TMDL` | Repo + docs | `Implemented` | Delivery page visuals use milestone measures including `Latest Milestone Date`, `Milestone Delay (Days)`, and `Late Projects Count`. |
| `REQ-019` | Delivery Performance RAG status reporting must use the current unpivoted indicator table. | `SM`, `KR`, `PBIP`, `TMDL` | Repo + docs | `Implemented` | Delivery visual `2a268ba08a0e15411266` queries `Project_Status_Unpivoted.Status Display Name` and `Status Value`. |
| `REQ-020` | `Late Projects Count` must exclude blank milestone dates. | `MN`, `PO`, `KR`, `TMDL` | Repo + docs | `Open defect` | `epmo_milestone.tmdl` contains `Late Projects Count`, and meeting notes plus docs confirm the current bug that blanks are being counted incorrectly. |
| `REQ-021` | Development and testing currently run against the production Dataverse environment because no separate dev/test environment exists. | `PO`, `DS`, `KR` | Docs/notes | `Operational` | Current docs explicitly state there is no separate dev/test Dataverse environment. |
| `REQ-022` | Report-level Power BI RLS must not be described as live unless it is evidenced in the PBIP/model. | `PO`, `KR` | Docs/notes | `Pending` | Current documentation states RLS is a pending action; the current PBIP baseline does not evidence implemented report-level RLS. |
| `REQ-023` | Synapse silver/gold modelling and automated refresh must be treated as future-state roadmap only. | `MN`, `PO`, `RS`, `KR` | Docs/notes | `Excluded` | Future warehouse integration and automation are discussed as later enhancements, not the current live build. |
| `REQ-024` | Benefit realisation reporting must not be treated as part of the current baseline until a confirmed source and implementation exist. | `PO`, `KR` | Docs/notes | `Excluded` | Current docs explicitly call benefit realisation unconfirmed or not yet built. |
| `REQ-025` | The project card feature is optional and not a core deliverable for the current cycle. | `MN`, `KR` | Docs/notes | `Excluded` | Meeting notes describe the project card as good-to-have only. |
| `REQ-026` | Operational ownership must remain explicitly assigned across the report owner, data steward, developer, and designer roles. | `OW`, `KR` | Docs/notes | `Operational` | `03_Ownership.md` assigns responsibilities and RACI coverage across Priscila, Michael Newsome, Andrei, and Sachin. |
| `REQ-027` | Power BI report access must remain restricted to the pilot and executive audience until report-level RLS is implemented and tested. | `SEC`, `KR` | Docs/notes | `Operational` | `06_Security_RLS.md` states current mitigation is restricted report access because Import-mode Power BI can expose the full dataset. |
| `REQ-028` | Sensitivity labels for the report and semantic model are required before production distribution, but are not yet applied. | `SEC` | Docs/notes | `Pending` | `06_Security_RLS.md` marks sensitivity labels as not yet applied and required before production distribution. |
| `REQ-029` | The current Dataverse-to-Power BI connection requires no on-premises or VNet gateway. | `DS`, `RS`, `DEP`, `KR` | Docs/notes | `Operational` | Current source, refresh, and dependency docs all describe the connection as cloud-to-cloud with no gateway. |
| `REQ-030` | Exact mapping between the documented Q2 indicator framework and the current Dataverse/TMDL field set must be confirmed before model or documentation changes are made. | `BG`, `KR`, `TMDL` | Repo + docs | `Pending` | `08_BusinessGlossary.md` describes a broader Q2 indicator framing that is not fully reconciled with the current `Project_Status_Unpivoted` mapping in TMDL. |
| `REQ-031` | UAT and production-readiness validation remain required before broader production distribution. | `TV`, `CL`, `SEC` | Docs/notes | `Pending` | `10_TestingValidation.md` and `07_ChangeLog.md` show UAT and production deployment are still incomplete; `06_Security_RLS.md` also keeps broader distribution gated. |

## Coverage Summary

| Current state | Count |
|---|---:|
| `Implemented` | 13 |
| `Operational` | 10 |
| `Open defect` | 1 |
| `Pending` | 4 |
| `Excluded` | 3 |

Total explicit mapped requirements in the current baseline: `31`.

## Current-cycle Deliverable Coverage

| Deliverable from `KNOWLEDGE-REGISTER.md` | Requirement IDs covered |
|---|---|
| Grounded documentation baseline | `REQ-001` to `REQ-010`, `REQ-021` to `REQ-024` |
| Executive Summary narrative | `REQ-008`, `REQ-009`, `REQ-017` |
| Delivery Performance bug fix | `REQ-018` to `REQ-020` |
| Semantic model validation | `REQ-001` to `REQ-004`, `REQ-013`, `REQ-018`, `REQ-019` |
| Access and refresh alignment | `REQ-015` to `REQ-017`, `REQ-021`, `REQ-022`, `REQ-026` to `REQ-029`, `REQ-031` |
| Support documentation workflow | `REQ-017` and the page/report baseline in `REQ-005` to `REQ-010` |

## Meeting notes extraction summary

This section answers the practical question: which statements from `Meeting notes.md` are actual requirements, and which are status notes, defects, or roadmap items?

| Meeting-note theme | Treatment in this matrix | Requirement ID(s) |
|---|---|---|
| PowerPoint backgrounds and editable SVG assets | Current-build visual requirement | `REQ-007` |
| Home Page click-through to `0_2. Exec Summary` | Current-build navigation requirement | `REQ-006` |
| Portfolio filtering in report views | Current-build interaction requirement | `REQ-010` |
| Six-step quarterly reporting wizard | Operational business requirement | `REQ-011` |
| Most severe indicator drives overall project status | Operational business rule requirement | `REQ-012` |
| Follow-up questions only for `At Risk` or `Significant Concerns` | Operational workflow requirement | `REQ-014` |
| PM-only edit scope and admin full access | Operational access requirement | `REQ-015` |
| Manual refresh after the `1 p.m.` deadline | Operational process requirement | `REQ-016` |
| Refreshed report must be validated before executive use | Operational process requirement | `REQ-017` |
| Late-project logic must exclude blanks | Open defect requirement | `REQ-020` |
| Project card feature | Explicitly not a core current-cycle requirement | `REQ-025` |
| Data warehouse integration and automation discussion | Future-state only, excluded from current baseline | `REQ-023` |

The following note items are useful KER context but are not promoted to standalone baseline requirements in this matrix:

- the transient count of `14` projects received
- temporary empty visuals before the manual refresh completes
- discussion of a possible table of contents or mirrored layout
- named task ownership and Thursday timing, which are execution notes rather than enduring product requirements

## Consulted Docs That Add Caution Or Guidance

Not every consulted file adds a new baseline requirement.

- `07_ChangeLog.md` helps confirm current release status and pending items.
- `11_VisualModularity.md` mixes current resource facts with reusable template guidance, so PBIP artefacts still take precedence.
- `12_LessonsLearned.md` provides implementation guardrails and known patterns, not evidence of additional live features.

## What this matrix says clearly

- The current live solution is grounded in Dataverse, PBIP, and TMDL artefacts, not in a future Synapse design.
- Most current-cycle requirements are already implemented or operationally defined.
- The main confirmed current defect is `REQ-020` for blank milestone dates in `Late Projects Count`.
- The main control point to keep honest in future documentation is `REQ-022`: do not claim report-level RLS unless the PBIP/model proves it.
- The full `01` to `12` documentation set has now been consulted, but only explicitly supported items have been promoted into the traceability baseline.
