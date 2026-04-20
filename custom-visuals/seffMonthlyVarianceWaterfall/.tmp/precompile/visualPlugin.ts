import { Visual } from "../../src/visual";
import powerbiVisualsApi from "powerbi-visuals-api";
import IVisualPlugin = powerbiVisualsApi.visuals.plugins.IVisualPlugin;
import VisualConstructorOptions = powerbiVisualsApi.extensibility.visual.VisualConstructorOptions;
import DialogConstructorOptions = powerbiVisualsApi.extensibility.visual.DialogConstructorOptions;
var powerbiKey: any = "powerbi";
var powerbi: any = window[powerbiKey];
var seffMonthlyVarianceWaterfall271F6AC03A664E5EA88D4F6C2E186AB8: IVisualPlugin = {
    name: 'seffMonthlyVarianceWaterfall271F6AC03A664E5EA88D4F6C2E186AB8',
    displayName: 'SEFF Monthly Variance Waterfall',
    class: 'Visual',
    apiVersion: '5.3.0',
    create: (options?: VisualConstructorOptions) => {
        if (Visual) {
            return new Visual(options);
        }
        throw 'Visual instance not found';
    },
    createModalDialog: (dialogId: string, options: DialogConstructorOptions, initialState: object) => {
        const dialogRegistry = (<any>globalThis).dialogRegistry;
        if (dialogId in dialogRegistry) {
            new dialogRegistry[dialogId](options, initialState);
        }
    },
    custom: true
};
if (typeof powerbi !== "undefined") {
    powerbi.visuals = powerbi.visuals || {};
    powerbi.visuals.plugins = powerbi.visuals.plugins || {};
    powerbi.visuals.plugins["seffMonthlyVarianceWaterfall271F6AC03A664E5EA88D4F6C2E186AB8"] = seffMonthlyVarianceWaterfall271F6AC03A664E5EA88D4F6C2E186AB8;
}
export default seffMonthlyVarianceWaterfall271F6AC03A664E5EA88D4F6C2E186AB8;