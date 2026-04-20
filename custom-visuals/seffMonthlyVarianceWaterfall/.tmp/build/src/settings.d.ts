import { formattingSettings } from "powerbi-visuals-utils-formattingmodel";
import FormattingSettingsCard = formattingSettings.SimpleCard;
import FormattingSettingsSlice = formattingSettings.Slice;
import FormattingSettingsModel = formattingSettings.Model;
declare class ThemeCardSettings extends FormattingSettingsCard {
    positiveStrongColor: formattingSettings.ColorPicker;
    positiveSoftColor: formattingSettings.ColorPicker;
    neutralColor: formattingSettings.ColorPicker;
    negativeSoftColor: formattingSettings.ColorPicker;
    negativeStrongColor: formattingSettings.ColorPicker;
    referenceLineColor: formattingSettings.ColorPicker;
    backgroundColor: formattingSettings.ColorPicker;
    accentColor: formattingSettings.ColorPicker;
    name: string;
    displayName: string;
    slices: Array<FormattingSettingsSlice>;
}
declare class ConditionalFormattingCardSettings extends FormattingSettingsCard {
    lowerIsBetter: formattingSettings.ToggleSwitch;
    mediumThresholdPct: formattingSettings.NumUpDown;
    strongThresholdPct: formattingSettings.NumUpDown;
    name: string;
    displayName: string;
    slices: Array<FormattingSettingsSlice>;
}
declare class LabelsCardSettings extends FormattingSettingsCard {
    showTitle: formattingSettings.ToggleSwitch;
    showLegend: formattingSettings.ToggleSwitch;
    showActualLabels: formattingSettings.ToggleSwitch;
    showReferenceLabels: formattingSettings.ToggleSwitch;
    showVarianceLabels: formattingSettings.ToggleSwitch;
    fontSize: formattingSettings.NumUpDown;
    name: string;
    displayName: string;
    slices: Array<FormattingSettingsSlice>;
}
declare class LayoutCardSettings extends FormattingSettingsCard {
    barWidthPercent: formattingSettings.NumUpDown;
    cornerRadius: formattingSettings.NumUpDown;
    showConnectorLines: formattingSettings.ToggleSwitch;
    name: string;
    displayName: string;
    slices: Array<FormattingSettingsSlice>;
}
export declare class VisualFormattingSettingsModel extends FormattingSettingsModel {
    themeCard: ThemeCardSettings;
    conditionalFormattingCard: ConditionalFormattingCardSettings;
    labelsCard: LabelsCardSettings;
    layoutCard: LayoutCardSettings;
    cards: (ThemeCardSettings | ConditionalFormattingCardSettings | LabelsCardSettings | LayoutCardSettings)[];
}
export {};
