# SEFF Monthly Variance Waterfall

This is a starter Power BI custom visual that recreates a Zebra-style monthly variance chart with SEFF-owned branding, conditional formatting, and a clean from-scratch renderer.

It is designed as the first reusable SEFF chart family:

- Category on the x-axis
- Actual as the main bar
- Previous year as the reference tick
- Variance-driven color logic
- Configurable thresholds and inversion rules

## Data roles

- `Category`: grouping field such as month or account
- `Actual`: current value
- `Previous year`: comparison value

## Formatting pane

- `SEFF Theme`
- `Conditional Formatting`
- `Labels`
- `Layout`

The conditional formatting logic uses these rules:

- `lowerIsBetter = false`: positive variance is good
- `lowerIsBetter = true`: negative variance is good
- `mediumThresholdPct`: threshold for soft positive or negative state
- `strongThresholdPct`: threshold for strong positive or negative state

## Default palette

Aligned with ZBI Charts IBCS conventions — vivid green/red variance encoding, neutral dark reference, SEFF warm background.

| Token | Hex | Role |
|-------|-----|------|
| Positive strong | `#17785F` | Variance ≥ strong threshold (good) |
| Positive soft | `#7DBF9C` | Variance ≥ medium threshold (good) |
| Neutral | `#BEBAB4` | Variance within thresholds |
| Negative soft | `#E88A7D` | Variance ≥ medium threshold (bad) |
| Negative strong | `#C5302A` | Variance ≥ strong threshold (bad) |
| Reference line | `#404040` | PY tick, axis, grid, label text |
| Background | `#F5F1EA` | Visual container fill (SEFF warm cream) |
| Accent | `#D59438` | Top accent rule (SEFF amber) |

> **ZBI alignment:** negative strong moved from terracotta `#C5543D` to unambiguous red `#C5302A`. Neutral cooled from warm beige `#C7C1B7` to `#BEBAB4`. Reference line moved to near-black `#404040` matching IBCS anthracite. Corner radius default is `0` (IBCS rectangular bars).

## Commands

```powershell
npm install
npm start
npm run package
```

## Sample contract

See [samples/overview-monthly-variance-sample.json](samples/overview-monthly-variance-sample.json) for a small external sample payload that mirrors the visual's expected contract outside Power BI.
