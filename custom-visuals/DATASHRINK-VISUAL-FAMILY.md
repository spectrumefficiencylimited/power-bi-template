# DataShrink Variance Visuals — Family Analysis & Roadmap

> **Purpose.** This is the design contract and roadmap for a licence-free,
> IBCS-aligned family of Power BI custom visuals (Card, Table, Waterfall) that
> replaces the **licensed Zebra BI** visuals used across the estate. It locks the
> **shared AC/PL/FC data contract** every family member speaks, specs each visual,
> and lays out the Zebra → DataShrink migration.
>
> **EDA note (2026-06-16):** grounded in the existing built visual
> (`custom-visuals/seffMonthlyVarianceWaterfall`) and the Zebra usage observed in
> the `sales-pipeline-crm` governance pass. Deductions are tagged **(inferred)**;
> open decisions are called out explicitly.

---

## 1. Document Control

| Field | Value |
|-------|-------|
| **Revision** | 1.0 — first edition (contract locked) |
| **Last updated** | 2026-06-16 |
| **Updated by** | Registrar / visual-analysis pass |
| **Family fingerprint** | 3 target visuals (Card, Table, Waterfall); 1 built (Waterfall v1.0.0, 2-scenario); shared AC/PL/FC contract v1; 8-token theme |

> **Fingerprint — how to recompute.** Count visual projects under
> `custom-visuals/` and, per project, its `pbiviz.json` version and the data roles
> in `capabilities.json`. If the contract version or built-visual count differs
> from above, this doc is stale — re-curate §4 (contract) and §6 (status).

### Revision History

| Revision | Date | Author | Summary |
|---------:|------|--------|---------|
| 1.0 | 2026-06-16 | Registrar | First edition: gap matrix, locked AC/PL/FC shared contract, per-visual specs, Zebra→DataShrink migration plan, roadmap. |

> **Standing rule:** every content-changing rewrite bumps the Revision and adds
> one Revision History row. Contract changes (§4) are **breaking** for any visual
> already built against the prior contract — bump the contract version in the
> fingerprint and note the migration in §4.6.

---

## 2. Why this family exists

Two facts from the `sales-pipeline-crm` audit converge:

1. The report's headline presentation is **entirely Zebra BI** — Cards, Tables and
   Waterfall — which are **commercial, licensed** custom visuals.
2. The embedded Zebra BI **licence key expired 2026-05-01** — before today
   (2026-06-16) — so those visuals are likely **degrading/watermarking in the
   Service right now**. (Worth an audit to confirm the tenant licence state.)

The estate already started the escape hatch: a from-scratch, SEFF-branded
**Monthly Variance Waterfall** custom visual. This doc turns that one-off into a
**coherent three-visual family** with a single shared data contract, so a report
can drop Zebra entirely without a licence dependency.

This is the concrete first step of the **visual-analysis phase** that
`11_VisualModularity` was framed as the launchpad for.

---

## 3. Gap matrix — Zebra components vs DataShrink family

Usage counts are from `sales-pipeline-crm` (the reference report).

| Zebra component | Usage (sales-crm) | What it does | DataShrink status | Gap to close |
|---|---|---|---|---|
| **Zebra BI Cards** | 9× (3 per Home page) | KPI headline — AC with PL/FC reference + variance | ❌ not built | New visual: big-number KPI card, AC + PL/FC variance pills, conditional colour |
| **Zebra BI Tables** | 6× (Home, Home 2, 2× Home 3, 2× hidden DT pages) | Variance table — dimension rows × scenarios | ❌ not built | New visual: rows × AC/PL/variance(abs,%) with in-cell IBCS bars |
| **Zebra BI Waterfall** | 5× (2 Home, 2 Home 2, 1 Home 3) | AC/PL/FC bars + Conversion AC/FC rate overlay + dynamic KPI-name title | ⚠️ partial — `seffMonthlyVarianceWaterfall` v1.0.0 | Existing visual is **2-scenario (AC vs PY)**; needs **3-scenario AC/PL/FC**, a **secondary rate-line overlay**, and a **measure-bound dynamic title** |

**Already reusable across the family (built in the waterfall):** the 8-token SEFF
theme, the 5-band conditional-formatting engine (`lowerIsBetter` + medium/strong
thresholds), compact number formatting, and the d3 render scaffolding.

---

## 4. The shared DataShrink Variance Contract v1 (LOCKED)

Every family member binds the **same data roles** and reads the **same theme +
conditional-formatting** objects. A measure dropped on `Actual` behaves
identically whether the visual is a card, a table or a waterfall. This is what
makes them a family.

### 4.1 Scenario model — AC / PL / FC (+ PY)

The estate's reports compare **Actual / Plan / Forecast** (the IBCS scenario
triad), with **Previous Year** as an optional fourth reference. The existing
waterfall's AC-vs-PY model is a **subset** of this; the family generalises to:

| Code | Scenario | Role name | Kind | Max | Required |
|------|----------|-----------|------|----:|----------|
| **AC** | Actual | `actual` | Measure | 1 | **Yes** |
| **PL** | Plan / Budget | `plan` | Measure | 1 | No |
| **FC** | Forecast | `forecast` | Measure | 1 | No |
| **PY** | Previous Year | `previousYear` | Measure | 1 | No |
| — | Category (axis/rows) | `category` | Grouping | 1 | No¹ |
| — | Overlay rate (e.g. Conversion) | `overlayRate` | Measure | 1 | No |
| — | Dynamic title (text measure) | `titleMeasure` | Measure | 1 | No |

¹ `category` is required for Table/Waterfall, optional for Card (a card can render
a single aggregate with no axis).

> **Backward-compatibility:** the existing waterfall's roles (`category`,
> `actual`, `previousYear`) are a strict subset — keep those role **names** so the
> waterfall upgrades in place without breaking existing bindings; `plan`,
> `forecast`, `overlayRate`, `titleMeasure` are **new optional** roles.

### 4.2 Reference & variance semantics

A visual computes variance of `actual` against a **reference scenario**, chosen by
a formatting setting `referenceScenario ∈ {PL, FC, PY}` (default: **PL** if
present, else **PY**, else **FC**). For each datum:

- **Δ abs** = `actual − reference`
- **Δ %** = `(actual − reference) / |reference|` (guard reference = 0 → ±1 or 0)
- Colour band is driven by Δ% through the existing 5-band engine, oriented by
  `lowerIsBetter`.

IBCS convention: variance is the *story*; the reference is a thin tick/line, the
actual is the solid bar/number. (Already how the waterfall renders.)

### 4.3 Conditional-formatting object (shared, already built)

`conditionalFormatting`: `lowerIsBetter` (bool), `mediumThresholdPct` (num, def 3),
`strongThresholdPct` (num, def 10). Reused verbatim from the waterfall.

### 4.4 Theme object (shared, already built — 8 tokens)

`theme`: `positiveStrongColor #17785F`, `positiveSoftColor #7DBF9C`,
`neutralColor #BEBAB4`, `negativeSoftColor #E88A7D`, `negativeStrongColor #C5302A`,
`referenceLineColor #404040`, `backgroundColor #F5F1EA`, `accentColor #D59438`.
IBCS-tuned. **Extract this into a shared module** (`src/theme.ts`) so all three
visuals import one palette + one `resolveVarianceFill()` rather than copying.

### 4.5 dataView mapping & formatting

- **Mapping:** `categorical` — categories `for in category`, values = the bound
  scenario measures (`actual`, `plan`, `forecast`, `previousYear`, `overlayRate`)
  selected by role; conditions cap each measure role at max 1.
- **Number formatting:** honour the model's format string where available; fall
  back to compact (`Intl.NumberFormat … notation:"compact"`). The overlay rate
  formats as a percentage independent of the bar scale.
- **Dynamic title:** if `titleMeasure` is bound, render its (text) value as the
  visual title; else fall back to `"{actual} vs {reference}"` (current waterfall
  behaviour). This is how the Zebra "Selected filter KPI name" label is replaced.

### 4.6 Contract versioning

This is **contract v1**. Any change to role names/kinds or the variance semantics
is a **breaking** change: bump the contract version (fingerprint §1), update every
built visual, and record the migration here. Additive optional roles are
non-breaking.

---

## 5. Per-visual specifications

All three import the shared theme + conditional-formatting + the AC/PL/FC contract.

### 5.1 DataShrink Variance Card (replaces Zebra BI Cards — 9×)

- **Roles used:** `actual` (required), `plan`/`forecast`/`previousYear` (≥1 as
  reference), `titleMeasure` (optional), `category` optional (small-multiple).
- **Layout:** large AC number; one or two **variance pills** (Δ% vs reference,
  conditionally coloured); a thin reference sub-label (PL/FC/PY value); optional
  sparkline if `category` present (inferred — phase 2). SEFF accent rule + cream
  background.
- **Formatting cards:** Theme, Conditional Formatting, Labels (title, pills,
  reference value, font size), Layout (pill style, number scale).
- **Acceptance:** renders AC + at least one variance pill with correct band colour;
  dynamic title from `titleMeasure`; no licence; matches the 3-per-page Home usage.

### 5.2 DataShrink Variance Table (replaces Zebra BI Tables — 6×)

- **Roles used:** `category` (rows, required), `actual` (required), reference
  (`plan`/`previousYear`/`forecast`), optional `overlayRate`.
- **Layout:** row per category; columns = AC, reference, **Δ abs**, **Δ %**, with an
  **in-cell horizontal variance bar** (IBCS) coloured by band; numeric right-align;
  total row. Region→Country hierarchy support (the hidden DT pages use a 2-level
  hierarchy) — phase 2 (inferred).
- **Formatting cards:** Theme, Conditional Formatting, Columns (which of AC/ref/Δabs/Δ%
  to show, in-cell bar on/off), Labels, Layout.
- **Acceptance:** renders rows × scenarios with correct Δ and band colour; handles
  the absolute and percent variants seen on the DT pages.

### 5.3 DataShrink Variance Waterfall (extend `seffMonthlyVarianceWaterfall` — 5×)

Build **on the existing v1.0.0**, don't restart. Add:
1. **3rd scenario** — `plan` (and/or `forecast`) so bars/ticks express AC vs PL vs
   FC, not just AC vs PY. Generalise `referenceScenario`.
2. **Secondary rate overlay** — `overlayRate` as a line/marker on a **secondary
   axis** (the Conversion AC / Conversion FC rate the Zebra waterfall overlays).
3. **Dynamic title** — `titleMeasure` (Selected filter KPI name).
- **Acceptance:** existing AC-vs-PY bindings still render unchanged; new optional
  roles light up the 3-scenario + overlay + dynamic-title behaviour.

---

## 6. Build status & sequencing

| Phase | Deliverable | Status |
|------:|-------------|--------|
| 0 | **Contract v1 locked** (this doc §4) + extract shared `theme.ts`/variance module | ▶ contract locked; shared-module extraction = next |
| 1 | **Waterfall** → AC/PL/FC + overlay + dynamic title (extend v1) | ⬜ |
| 2 | **Card** (new) — highest count (9×), canonical KPI headline | ⬜ |
| 3 | **Table** (new) — variance table (6×), incl. DT hierarchy | ⬜ |
| 4 | **Migration** — swap Zebra→DataShrink in sales-pipeline-crm, verify, re-audit | ⬜ |

Recommended order rationale: lock contract → extend the *existing* artifact
(lowest risk, proves the contract generalises) → then the two new visuals → then
migrate. (Card could be pulled earlier if licence pressure demands the headline
KPIs first — it is the most numerous component.)

---

## 7. Zebra → DataShrink migration plan (sales-pipeline-crm reference)

Migration is a **report-layer** change → the **Composer** authors it (visual
insert/replace), dry-run first; the **Modeler** is not involved (no model change).
The binding map (Zebra field role → DataShrink contract role):

| Zebra binding | DataShrink role | Notes |
|---|---|---|
| Values: AC | `actual` | required |
| Values: PL | `plan` | reference (default) |
| Values: FC | `forecast` | optional reference |
| Values: Conversion AC / Conversion FC | `overlayRate` | waterfall secondary axis |
| Category / Group (Country, Customer, Product, KPI name) | `category` | table rows / waterfall axis |
| "Selected filter KPI name" label | `titleMeasure` | dynamic title |

Per-visual swap counts to replace: **9 cards, 6 tables, 5 waterfalls = 20 visuals**
across 6 pages (incl. the 2 hidden DT pages). Each replacement preserves position
and bindings; validate render + variance parity against the (lapsed-licence) Zebra
originals before deleting them.

---

## 8. Open decisions (need a human call)

1. **Brand name — SEFF vs DataShrink.** The built visual is **SEFF**-branded
   (folder `seffMonthlyVarianceWaterfall`, guid, displayName "SEFF Monthly
   Variance Waterfall", theme card "SEFF Theme", author "SEFF"). This roadmap
   uses **DataShrink** for the family per the latest steer. **Decide before
   building visuals #2/#3** so the family is consistent: (a) rebrand the waterfall
   to DataShrink (new guid = re-import in reports), or (b) keep SEFF and name the
   family SEFF. _[TODO: human decision]_
2. **Reference-scenario default** — confirm PL-first (vs PY-first) matches how the
   business reads variance. _[TODO: human input]_
3. **Conversion overlay axis** — confirm Conversion is a rate (%) on a secondary
   axis vs a separate small panel. _[TODO: human input]_
4. **AppSource vs org store** — distribution channel for the finished family
   (affects guid/signing). _[TODO: human input]_

---

## 9. Related

- Built visual: `custom-visuals/seffMonthlyVarianceWaterfall/` (README, `capabilities.json`, `src/visual.ts`, `src/settings.ts`).
- Reference report: `sales-pipeline-crm/docs/` — esp. `09_Dependencies.md` (Zebra licence/deps), `11_VisualModularity.md` (as-built visual reuse), `12_DashboardRecipes.md` (per-page visual usage).
- Estate component library: `power-bi-template/modules/` (where stamped DataShrink components would live for reuse).
