import powerbi from "powerbi-visuals-api";
import "./../style/visual.less";
import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
export declare class Visual implements IVisual {
    private container;
    private emptyState;
    private svg;
    private formattingSettings;
    private formattingSettingsService;
    constructor(options: VisualConstructorOptions);
    update(options: VisualUpdateOptions): void;
    getFormattingModel(): powerbi.visuals.FormattingModel;
    private parseDataView;
    private render;
    private renderLegend;
    private getValueColumnByRole;
    private toNumber;
    private calculateVariancePct;
    private resolveVarianceFill;
    private resolveTopAccent;
    private formatCompact;
    private formatVarianceLabel;
    private buildTooltipText;
}
