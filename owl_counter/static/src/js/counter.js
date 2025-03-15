/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { Reset } from "./reset";

class MyClientAction extends Component {
  static template = "owl_counter.counter";
  static components = {...MyClientAction,
  Reset,
  }
  setup() {
    this.state = useState({ value: 0 });
  }
  increment() {
    this.state.value++;
  }
  decrement() {
    if (this.state.value > 0) {
      this.state.value--;
    }
  }
  reset() {
  console.log(this.state,'aaaaaaaaa')
    this.state.value = 0;
  }
}

registry.category("actions").add("owl_counter.counter", MyClientAction);
