/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class Reset extends Component {
  static template = "owl_counter.reset";
  static props = {
    count_reset: { type: Function, optional: true },
  };
}
