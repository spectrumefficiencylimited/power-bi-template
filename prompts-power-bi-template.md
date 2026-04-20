# Prompt Pack - power-bi-template

| Field | Value |
|-------|-------|
| Project | power-bi-template |
| Folder | `power-bi-template` |
| Report directory | `Project.Template.Report` |
| Model directory | `Project.Template.SemanticModel` |
| Date | 2026-04-15 |
| Purpose | Capture current PBIP folder rules and support cross-folder modular extraction |
| Status | Current-build aligned |

## Purpose

This prompt pack is built from the actual PBIP artefacts in the `power-bi-template` folder. It is used to extract source, model, pages, visuals, and transformation rules before comparing with additional folders.

## Read first before using any prompt

- `power-bi-template/KNOWLEDGE-REGISTER.md`
- `power-bi-template/prompts-power-bi-template.md`

## Non-negotiable rules

1. Treat the current folder PBIP artefacts as the source of truth.
2. Do not assume a warehouse, Synapse, or automation unless it exists in this folder.
3. Preserve actual page names, display options, and visual types.
4. Capture M query source patterns and DAX measure names exactly as implemented.
5. Document custom visuals and any license-dependent visual features.

## Prompt contract format

Each prompt should include:
1. Module
2. Job
3. Reads from
4. Produces
5. Constraints

## Recommended sequence

1. Folder scan and build summary
2. Source and transformation validation
3. Semantic model and relationship validation
4. Page inventory and visual contract
5. Visual formatting and custom visual validation
6. DAX and measures extraction
7. Prompt library authoring

## Prompt 1

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 2

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 3

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 4

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 5

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 6

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 7

Use this section to turn the folder's scanned rules into a reusable prompt module.

## Prompt 8

Use this section to turn the folder's scanned rules into a reusable prompt module.
