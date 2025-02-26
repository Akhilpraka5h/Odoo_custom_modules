import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                rating: { type: String, optional: true },
            },
        },
    },
});

patch(PosOrderline.prototype, {
    setup(vals) {
        this.rating = this.product_id.rating || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            rating: this.get_product().rating || "",
        };
    },
});
