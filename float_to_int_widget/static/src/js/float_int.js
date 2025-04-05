/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component } from "@odoo/owl";
import { useRef, onWillRender, onMounted } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";

export class FloatInt extends Component {
  static template = "float_to_int_widget.FloatIntWidget";
  static props = {
        ...standardFieldProps,
        rounding: { type: String, optional: true },
    };
  setup() {
    super.setup();
    this.input = useRef("inputfloatint");
    console.log(this.input)
    console.log(this.props)
    useInputField({
      getValue: () => this.props.record.data[this.props.name] || "",
      refName: "inputfloatint",
    });
    onWillRender(() => {
      this.rounded();
    });
    onMounted(() => {
      this.rounded();
    });
  }
  rounded() {
    if (this.input.el) {
      this.props.record.data[this.props.name] = Math.round(this.input.el.value);
    }
  }
}
FloatInt.supportedOptions= [
        {
            label: _t("Round"),
            name: "round",
//            type:"string"
            type: "selection",
            choices: [
                { label: _t("Up"), value:"up"},
                { label: _t("Down"), value:"down" },
                { label: _t("Default"), value:"default" },
            ],
        },
    ],
FloatInt.extractProps = ({ options }) => {
    console.log("Widget options:", options);
    return { rounding: options.rounding };
};
FloatInt.component = FloatInt;
FloatInt.supportedTypes = ["float"];

//export const FloatInt = {
//    component: FloatInt,
//    displayName: _t("FloatInt"),
//    supportedTypes: ['float'],
//    supportedOptions: [
//        {
//            label: _t("Round"),
//            name: "round",
////            type:"string"
//            type: "selection",
//            choices: [
//                { label: _t("Up"), value:"up"},
//                { label: _t("Down"), value:"down" },
//                { label: _t("Default"), value:"default" },
//            ],
//        },
//    ],
//    extractProps: ({ options }) => ({
//    rounding:options.round
//    }),
//};

registry.category("fields").add("float_int_widget", FloatInt);
