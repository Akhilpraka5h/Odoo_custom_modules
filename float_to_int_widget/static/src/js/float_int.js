/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component } from "@odoo/owl";
import { useRef, onWillRender, onMounted } from "@odoo/owl"

export class FloatInt extends Component {
  static template = "float_to_int_widget.FloatIntWidget";
  setup() {
    super.setup();
    this.input = useRef("inputfloatint");
    console.log(this.props.record.data[this.props.name],'1')
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
            type: "selection",
            choices: [
                { label: _t("Up"), value:"up"},
                { label: _t("Down"), value:"down" },
                { label: _t("Default"), value:"default" },
            ],
        },
    ],

FloatInt.component = FloatInt;
FloatInt.supportedTypes = ["float"];
registry.category("fields").add("float_int_widget", FloatInt);
