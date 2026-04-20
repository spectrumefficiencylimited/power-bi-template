/*
 *  Power BI Visual CLI
 *
 *  Copyright (c) Microsoft Corporation
 *  All rights reserved.
 *  MIT License
 */
"use strict";

import powerbi from "powerbi-visuals-api";
import * as d3 from "d3";
import { FormattingSettingsService } from "powerbi-visuals-utils-formattingmodel";
import "./../style/visual.less";

import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import DataView = powerbi.DataView;
import DataViewValueColumn = powerbi.DataViewValueColumn;

import { VisualFormattingSettingsModel } from "./settings";

interface VarianceDatum {
    category: string;
    actual: number;
    previousYear: number | null;
    variance: number | null;
    variancePct: number | null;
    fill: string;
    actualLabel: string;
    previousYearLabel: string;
    varianceLabel: string;
}

interface ParsedDataView {
    categoryDisplayName: string;
    actualDisplayName: string;
    previousYearDisplayName: string;
    data: VarianceDatum[];
}

export class Visual implements IVisual {
    private container: HTMLElement;
    private emptyState: HTMLElement;
    private svg: d3.Selection<SVGSVGElement, unknown, null, undefined>;
    private formattingSettings: VisualFormattingSettingsModel;
    private formattingSettingsService: FormattingSettingsService;

    constructor(options: VisualConstructorOptions) {
        this.formattingSettingsService = new FormattingSettingsService();

        this.container = document.createElement("div");
        this.container.className = "seff-variance-visual";

        this.emptyState = document.createElement("div");
        this.emptyState.className = "seff-empty-state";
        this.emptyState.textContent = "Add Category, Actual, and Previous year fields to render the SEFF variance visual.";

        this.svg = d3.select(this.container)
            .append("svg")
            .attr("aria-label", "SEFF monthly variance waterfall");

        this.container.appendChild(this.emptyState);
        options.element.appendChild(this.container);
    }

    public update(options: VisualUpdateOptions): void {
        const dataView: DataView | undefined = options.dataViews?.[0];

        this.formattingSettings = this.formattingSettingsService.populateFormattingSettingsModel(
            VisualFormattingSettingsModel,
            dataView
        );

        const parsed = this.parseDataView(dataView);
        this.render(parsed, options.viewport.width, options.viewport.height);
    }

    public getFormattingModel(): powerbi.visuals.FormattingModel {
        return this.formattingSettingsService.buildFormattingModel(this.formattingSettings);
    }

    private parseDataView(dataView: DataView | undefined): ParsedDataView {
        if (!dataView?.categorical?.categories?.length) {
            return {
                categoryDisplayName: "Category",
                actualDisplayName: "Actual",
                previousYearDisplayName: "PY",
                data: []
            };
        }

        const categorical = dataView.categorical;
        const categoryColumn = categorical.categories?.[0];
        const valueColumns = Array.from(categorical.values || []);
        const actualColumn = this.getValueColumnByRole(valueColumns, "actual") || valueColumns[0];
        const previousYearColumn = this.getValueColumnByRole(valueColumns, "previousYear") || valueColumns[1];

        if (!categoryColumn || !actualColumn) {
            return {
                categoryDisplayName: "Category",
                actualDisplayName: "Actual",
                previousYearDisplayName: "PY",
                data: []
            };
        }

        const categoryValues = categoryColumn.values || [];
        const actualValues = actualColumn.values || [];
        const previousYearValues = previousYearColumn?.values || [];
        const data: VarianceDatum[] = [];

        for (let i = 0; i < categoryValues.length; i++) {
            const actual = this.toNumber(actualValues[i]);

            if (actual === null) {
                continue;
            }

            const previousYear = this.toNumber(previousYearValues[i]);
            const variance = previousYear === null ? null : actual - previousYear;
            const variancePct = this.calculateVariancePct(actual, previousYear);

            data.push({
                category: String(categoryValues[i] ?? ""),
                actual,
                previousYear,
                variance,
                variancePct,
                fill: this.resolveVarianceFill(variancePct),
                actualLabel: this.formatCompact(actual),
                previousYearLabel: previousYear === null ? "" : this.formatCompact(previousYear),
                varianceLabel: this.formatVarianceLabel(variancePct, variance)
            });
        }

        return {
            categoryDisplayName: categoryColumn.source?.displayName || "Category",
            actualDisplayName: actualColumn.source?.displayName || "Actual",
            previousYearDisplayName: previousYearColumn?.source?.displayName || "Previous year",
            data
        };
    }

    private render(parsed: ParsedDataView, width: number, height: number): void {
        this.svg.selectAll("*").remove();

        if (!parsed.data.length || width < 120 || height < 120) {
            this.emptyState.style.display = "flex";
            this.svg.style("display", "none");
            return;
        }

        this.emptyState.style.display = "none";
        this.svg.style("display", "block");
        this.svg.attr("width", width).attr("height", height);

        const theme = this.formattingSettings.themeCard;
        const labels = this.formattingSettings.labelsCard;
        const layout = this.formattingSettings.layoutCard;

        const fontSize = labels.fontSize.value;
        const headerHeight = labels.showTitle.value ? 52 : 24;
        const legendHeight = labels.showLegend.value && width > 640 ? 24 : 0;
        const margin = {
            top: headerHeight + legendHeight,
            right: 20,
            bottom: width < 520 ? 74 : 58,
            left: 48
        };

        const chartWidth = Math.max(width - margin.left - margin.right, 10);
        const chartHeight = Math.max(height - margin.top - margin.bottom, 10);
        const root = this.svg.append("g");

        root.append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", width)
            .attr("height", height)
            .attr("rx", layout.cornerRadius.value)
            .attr("ry", layout.cornerRadius.value)
            .attr("fill", theme.backgroundColor.value.value);

        root.append("line")
            .attr("x1", 20)
            .attr("x2", width - 20)
            .attr("y1", 14)
            .attr("y2", 14)
            .attr("stroke", theme.accentColor.value.value)
            .attr("stroke-width", 4)
            .attr("stroke-linecap", "round");

        if (labels.showTitle.value) {
            root.append("text")
                .attr("x", 20)
                .attr("y", 38)
                .attr("fill", theme.referenceLineColor.value.value)
                .attr("font-size", 15)
                .attr("font-weight", 600)
                .text(`${parsed.actualDisplayName} vs ${parsed.previousYearDisplayName}`);
        }

        if (labels.showLegend.value && width > 640) {
            this.renderLegend(root, width, theme.referenceLineColor.value.value);
        }

        const values = parsed.data.flatMap((datum) =>
            datum.previousYear === null ? [datum.actual, 0] : [datum.actual, datum.previousYear, 0]
        );
        let domainMin = d3.min(values) ?? 0;
        let domainMax = d3.max(values) ?? 0;

        if (domainMin === domainMax) {
            const pad = Math.max(Math.abs(domainMax) * 0.1, 1);
            domainMin -= pad;
            domainMax += pad;
        } else {
            const pad = (domainMax - domainMin) * 0.08;
            domainMin -= pad;
            domainMax += pad;
        }

        const xScale = d3.scaleBand<string>()
            .domain(parsed.data.map((datum) => datum.category))
            .range([margin.left, margin.left + chartWidth])
            .padding(0.24);

        const yScale = d3.scaleLinear()
            .domain([domainMin, domainMax])
            .range([margin.top + chartHeight, margin.top])
            .nice();

        const zeroY = yScale(0);

        root.append("line")
            .attr("x1", margin.left)
            .attr("x2", margin.left + chartWidth)
            .attr("y1", zeroY)
            .attr("y2", zeroY)
            .attr("stroke", theme.referenceLineColor.value.value)
            .attr("stroke-opacity", 0.25)
            .attr("stroke-width", 1.5);

        const gridValues = yScale.ticks(4);
        root.append("g")
            .selectAll("line")
            .data(gridValues)
            .enter()
            .append("line")
            .attr("x1", margin.left)
            .attr("x2", margin.left + chartWidth)
            .attr("y1", (value) => yScale(value))
            .attr("y2", (value) => yScale(value))
            .attr("stroke", theme.referenceLineColor.value.value)
            .attr("stroke-opacity", (value) => value === 0 ? 0 : 0.08)
            .attr("stroke-width", 1);

        root.append("g")
            .selectAll("text")
            .data(gridValues)
            .enter()
            .append("text")
            .attr("x", margin.left - 8)
            .attr("y", (value) => yScale(value) + 4)
            .attr("text-anchor", "end")
            .attr("font-size", 10)
            .attr("fill", theme.referenceLineColor.value.value)
            .attr("fill-opacity", 0.8)
            .text((value) => this.formatCompact(value));

        const group = root.append("g")
            .selectAll("g")
            .data(parsed.data)
            .enter()
            .append("g")
            .attr("transform", (datum) => `translate(${xScale(datum.category) || 0},0)`);

        const bandWidth = xScale.bandwidth();
        const barWidth = bandWidth * Math.min(Math.max(layout.barWidthPercent.value, 20), 90) / 100;
        const barOffset = (bandWidth - barWidth) / 2;
        const referenceTickWidth = bandWidth * 0.82;

        group.each((datum, index, nodes) => {
            const currentGroup = d3.select(nodes[index]);
            const centerX = bandWidth / 2;
            const actualY = yScale(datum.actual);
            const actualHeight = Math.max(Math.abs(zeroY - actualY), 2);
            const barY = Math.min(actualY, zeroY);
            const barFill = datum.fill;

            if (datum.previousYear !== null) {
                const referenceY = yScale(datum.previousYear);

                currentGroup.append("line")
                    .attr("x1", centerX - referenceTickWidth / 2)
                    .attr("x2", centerX + referenceTickWidth / 2)
                    .attr("y1", referenceY)
                    .attr("y2", referenceY)
                    .attr("stroke", theme.referenceLineColor.value.value)
                    .attr("stroke-width", 2.5)
                    .attr("stroke-linecap", "round")
                    .attr("stroke-opacity", 0.95);

                if (layout.showConnectorLines.value) {
                    currentGroup.append("line")
                        .attr("x1", centerX)
                        .attr("x2", centerX)
                        .attr("y1", referenceY)
                        .attr("y2", actualY)
                        .attr("stroke", barFill)
                        .attr("stroke-width", 1.5)
                        .attr("stroke-dasharray", "4,3")
                        .attr("stroke-opacity", 0.9);
                }

                if (labels.showReferenceLabels.value && bandWidth > 64) {
                    currentGroup.append("text")
                        .attr("x", bandWidth - 1)
                        .attr("y", referenceY - 6)
                        .attr("text-anchor", "end")
                        .attr("font-size", Math.max(fontSize - 2, 9))
                        .attr("fill", theme.referenceLineColor.value.value)
                        .text(datum.previousYearLabel);
                }
            }

            currentGroup.append("rect")
                .attr("x", barOffset)
                .attr("y", barY)
                .attr("width", barWidth)
                .attr("height", actualHeight)
                .attr("rx", Math.min(layout.cornerRadius.value, barWidth / 2))
                .attr("ry", Math.min(layout.cornerRadius.value, barWidth / 2))
                .attr("fill", barFill)
                .attr("opacity", 0.96);

            currentGroup.append("rect")
                .attr("x", barOffset)
                .attr("y", barY)
                .attr("width", barWidth)
                .attr("height", 4)
                .attr("rx", Math.min(layout.cornerRadius.value, barWidth / 2))
                .attr("fill", this.resolveTopAccent(barFill));

            currentGroup.append("title").text(this.buildTooltipText(datum, parsed.actualDisplayName, parsed.previousYearDisplayName));

            if (labels.showActualLabels.value) {
                currentGroup.append("text")
                    .attr("x", centerX)
                    .attr("y", datum.actual >= 0 ? barY - 8 : barY + actualHeight + fontSize + 2)
                    .attr("text-anchor", "middle")
                    .attr("font-size", fontSize)
                    .attr("font-weight", 600)
                    .attr("fill", theme.referenceLineColor.value.value)
                    .text(datum.actualLabel);
            }

            if (labels.showVarianceLabels.value && datum.varianceLabel) {
                const varianceY = datum.previousYear === null
                    ? barY - 24
                    : Math.min(actualY, yScale(datum.previousYear)) - 10;

                currentGroup.append("text")
                    .attr("x", centerX)
                    .attr("y", varianceY)
                    .attr("text-anchor", "middle")
                    .attr("font-size", Math.max(fontSize - 1, 10))
                    .attr("font-weight", 700)
                    .attr("fill", barFill)
                    .text(datum.varianceLabel);
            }

            const categoryText = currentGroup.append("text")
                .attr("x", centerX)
                .attr("y", margin.top + chartHeight + (width < 520 ? 28 : 22))
                .attr("text-anchor", "middle")
                .attr("font-size", fontSize)
                .attr("fill", theme.referenceLineColor.value.value)
                .text(datum.category);

            if (bandWidth < 54) {
                categoryText
                    .attr("transform", `translate(${centerX},${margin.top + chartHeight + 22}) rotate(-40)`)
                    .attr("text-anchor", "end")
                    .attr("x", 0)
                    .attr("y", 0);
            }
        });
    }

    private renderLegend(
        root: d3.Selection<SVGGElement, unknown, null, undefined>,
        width: number,
        textColor: string
    ): void {
        const conditional = this.formattingSettings.conditionalFormattingCard;
        const legend = root.append("g")
            .attr("transform", `translate(${Math.max(width - 330, 320)}, 34)`);

        const lowerIsBetter = conditional.lowerIsBetter.value;
        const items = [
            { label: lowerIsBetter ? "Strong down" : "Strong up", fill: this.formattingSettings.themeCard.positiveStrongColor.value.value },
            { label: "Neutral", fill: this.formattingSettings.themeCard.neutralColor.value.value },
            { label: lowerIsBetter ? "Strong up" : "Strong down", fill: this.formattingSettings.themeCard.negativeStrongColor.value.value }
        ];

        items.forEach((item, index) => {
            const itemGroup = legend.append("g")
                .attr("transform", `translate(${index * 94}, 0)`);

            itemGroup.append("rect")
                .attr("width", 14)
                .attr("height", 14)
                .attr("rx", 4)
                .attr("fill", item.fill);

            itemGroup.append("text")
                .attr("x", 20)
                .attr("y", 11)
                .attr("font-size", 10)
                .attr("fill", textColor)
                .text(item.label);
        });

        legend.append("text")
            .attr("x", 0)
            .attr("y", 28)
            .attr("font-size", 10)
            .attr("fill", textColor)
            .attr("fill-opacity", 0.8)
            .text(conditional.lowerIsBetter.value ? "Conditional rule: lower variance is better." : "Conditional rule: higher variance is better.");
    }

    private getValueColumnByRole(columns: DataViewValueColumn[], roleName: string): DataViewValueColumn | undefined {
        return columns.find((column) => Boolean(column?.source?.roles?.[roleName]));
    }

    private toNumber(value: powerbi.PrimitiveValue): number | null {
        if (value === null || value === undefined) {
            return null;
        }

        const numberValue = Number(value);
        return Number.isFinite(numberValue) ? numberValue : null;
    }

    private calculateVariancePct(actual: number, previousYear: number | null): number | null {
        if (previousYear === null) {
            return null;
        }

        if (previousYear === 0) {
            return actual === 0 ? 0 : Math.sign(actual);
        }

        return (actual - previousYear) / Math.abs(previousYear);
    }

    private resolveVarianceFill(variancePct: number | null): string {
        const theme = this.formattingSettings?.themeCard;
        const conditional = this.formattingSettings?.conditionalFormattingCard;

        if (!theme || variancePct === null) {
            return "#C7C1B7";
        }

        const strong = Math.abs(conditional.strongThresholdPct.value) / 100;
        const medium = Math.abs(conditional.mediumThresholdPct.value) / 100;
        const directionScore = conditional.lowerIsBetter.value ? -variancePct : variancePct;

        if (directionScore >= strong) {
            return theme.positiveStrongColor.value.value;
        }

        if (directionScore >= medium) {
            return theme.positiveSoftColor.value.value;
        }

        if (directionScore <= -strong) {
            return theme.negativeStrongColor.value.value;
        }

        if (directionScore <= -medium) {
            return theme.negativeSoftColor.value.value;
        }

        return theme.neutralColor.value.value;
    }

    private resolveTopAccent(fill: string): string {
        const color = d3.color(fill);
        return color ? color.darker(0.8).formatHex() : fill;
    }

    private formatCompact(value: number): string {
        return new Intl.NumberFormat("en-US", {
            notation: "compact",
            maximumFractionDigits: 1
        }).format(value);
    }

    private formatVarianceLabel(variancePct: number | null, variance: number | null): string {
        if (variancePct === null || variance === null) {
            return "";
        }

        if (!Number.isFinite(variancePct)) {
            return variance === 0 ? "0%" : variance > 0 ? "new" : "drop";
        }

        const percentage = Math.abs(variancePct * 100);
        const sign = variancePct > 0 ? "+" : variancePct < 0 ? "-" : "";
        return `${sign}${percentage.toFixed(1)}%`;
    }

    private buildTooltipText(datum: VarianceDatum, actualName: string, previousYearName: string): string {
        const lines = [
            datum.category,
            `${actualName}: ${datum.actualLabel}`
        ];

        if (datum.previousYear !== null) {
            lines.push(`${previousYearName}: ${datum.previousYearLabel}`);
        }

        if (datum.varianceLabel) {
            lines.push(`Variance: ${datum.varianceLabel}`);
        }

        return lines.join("\n");
    }
}
