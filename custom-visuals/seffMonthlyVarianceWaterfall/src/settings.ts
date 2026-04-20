/*
 *  Power BI Visualizations
 *
 *  Copyright (c) Microsoft Corporation
 *  All rights reserved.
 *  MIT License
 */

"use strict";

import { formattingSettings } from "powerbi-visuals-utils-formattingmodel";

import FormattingSettingsCard = formattingSettings.SimpleCard;
import FormattingSettingsSlice = formattingSettings.Slice;
import FormattingSettingsModel = formattingSettings.Model;

class ThemeCardSettings extends FormattingSettingsCard {
    positiveStrongColor = new formattingSettings.ColorPicker({
        name: "positiveStrongColor",
        displayName: "Positive strong",
        value: { value: "#17785F" }
    });

    positiveSoftColor = new formattingSettings.ColorPicker({
        name: "positiveSoftColor",
        displayName: "Positive soft",
        value: { value: "#7DBF9C" }
    });

    neutralColor = new formattingSettings.ColorPicker({
        name: "neutralColor",
        displayName: "Neutral",
        value: { value: "#BEBAB4" }
    });

    negativeSoftColor = new formattingSettings.ColorPicker({
        name: "negativeSoftColor",
        displayName: "Negative soft",
        value: { value: "#E88A7D" }
    });

    negativeStrongColor = new formattingSettings.ColorPicker({
        name: "negativeStrongColor",
        displayName: "Negative strong",
        value: { value: "#C5302A" }
    });

    referenceLineColor = new formattingSettings.ColorPicker({
        name: "referenceLineColor",
        displayName: "Reference line",
        value: { value: "#404040" }
    });

    backgroundColor = new formattingSettings.ColorPicker({
        name: "backgroundColor",
        displayName: "Background",
        value: { value: "#F5F1EA" }
    });

    accentColor = new formattingSettings.ColorPicker({
        name: "accentColor",
        displayName: "Accent",
        value: { value: "#D59438" }
    });

    name: string = "theme";
    displayName: string = "SEFF Theme";
    slices: Array<FormattingSettingsSlice> = [
        this.positiveStrongColor,
        this.positiveSoftColor,
        this.neutralColor,
        this.negativeSoftColor,
        this.negativeStrongColor,
        this.referenceLineColor,
        this.backgroundColor,
        this.accentColor
    ];
}

class ConditionalFormattingCardSettings extends FormattingSettingsCard {
    lowerIsBetter = new formattingSettings.ToggleSwitch({
        name: "lowerIsBetter",
        displayName: "Lower is better",
        value: false
    });

    mediumThresholdPct = new formattingSettings.NumUpDown({
        name: "mediumThresholdPct",
        displayName: "Medium threshold %",
        value: 3
    });

    strongThresholdPct = new formattingSettings.NumUpDown({
        name: "strongThresholdPct",
        displayName: "Strong threshold %",
        value: 10
    });

    name: string = "conditionalFormatting";
    displayName: string = "Conditional Formatting";
    slices: Array<FormattingSettingsSlice> = [
        this.lowerIsBetter,
        this.mediumThresholdPct,
        this.strongThresholdPct
    ];
}

class LabelsCardSettings extends FormattingSettingsCard {
    showTitle = new formattingSettings.ToggleSwitch({
        name: "showTitle",
        displayName: "Show title",
        value: true
    });

    showLegend = new formattingSettings.ToggleSwitch({
        name: "showLegend",
        displayName: "Show legend",
        value: true
    });

    showActualLabels = new formattingSettings.ToggleSwitch({
        name: "showActualLabels",
        displayName: "Show actual labels",
        value: true
    });

    showReferenceLabels = new formattingSettings.ToggleSwitch({
        name: "showReferenceLabels",
        displayName: "Show reference labels",
        value: true
    });

    showVarianceLabels = new formattingSettings.ToggleSwitch({
        name: "showVarianceLabels",
        displayName: "Show variance labels",
        value: true
    });

    fontSize = new formattingSettings.NumUpDown({
        name: "fontSize",
        displayName: "Label font size",
        value: 12
    });

    name: string = "labels";
    displayName: string = "Labels";
    slices: Array<FormattingSettingsSlice> = [
        this.showTitle,
        this.showLegend,
        this.showActualLabels,
        this.showReferenceLabels,
        this.showVarianceLabels,
        this.fontSize
    ];
}

class LayoutCardSettings extends FormattingSettingsCard {
    barWidthPercent = new formattingSettings.NumUpDown({
        name: "barWidthPercent",
        displayName: "Bar width %",
        value: 58
    });

    cornerRadius = new formattingSettings.NumUpDown({
        name: "cornerRadius",
        displayName: "Corner radius",
        value: 0
    });

    showConnectorLines = new formattingSettings.ToggleSwitch({
        name: "showConnectorLines",
        displayName: "Show connector lines",
        value: true
    });

    name: string = "layout";
    displayName: string = "Layout";
    slices: Array<FormattingSettingsSlice> = [
        this.barWidthPercent,
        this.cornerRadius,
        this.showConnectorLines
    ];
}

export class VisualFormattingSettingsModel extends FormattingSettingsModel {
    themeCard = new ThemeCardSettings();
    conditionalFormattingCard = new ConditionalFormattingCardSettings();
    labelsCard = new LabelsCardSettings();
    layoutCard = new LayoutCardSettings();

    cards = [
        this.themeCard,
        this.conditionalFormattingCard,
        this.labelsCard,
        this.layoutCard
    ];
}
