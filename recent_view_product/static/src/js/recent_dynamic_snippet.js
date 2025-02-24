/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice( i, i + size));
    }
    return result;
}
function uniqueIdGenerator() {
    return Date.now() + Math.random().toString(28).slice(2);
}
function getChunkSize() {
    return window.innerWidth < 768 ? 1 : 4;
}
var RecentViewProducts = PublicWidget.Widget.extend({
    selector: '.viewed_products',
    willStart: async function () {
        const data = await rpc('/recent_view_products', {});
        this.products = data;
    },
    start: function () {
        const refEl = this.$el.find("#recent_viewed");
        const unique_id = uniqueIdGenerator();
        const chunkSize = getChunkSize();
        const viewed_product = this.products.viewed_product;
        const chunkData = _chunk(viewed_product, chunkSize);
        if (viewed_product.length !== 0) {
            chunkData[0].is_active = true;
        }
        refEl.html(renderToElement('recent_view_product.user_recently_viewed_products', { chunkData }));
        const slide = this.$el.find(`#recent_viewed`);
        slide.find('.carousel-control-prev').attr('href', `#carousel${unique_id}`);
        slide.find('.carousel-control-next').attr('href', `#carousel${unique_id}`);
        slide.find('#user_viewed_products').attr('id', `carousel${unique_id}`);

        window.addEventListener("resize", () => {
            this.Resize(refEl, viewed_product, unique_id);
        });
    },
    Resize: function (refEl, viewed_product, unique_id) {
        const chunkSize = getChunkSize();
        const chunkData = _chunk(viewed_product, chunkSize);
        if (viewed_product.length !== 0) {
            chunkData[0].is_active = true;
        }
        refEl.html(renderToElement('recent_view_product.user_recently_viewed_products', { chunkData}));
        const slide = this.$el.find(`#recent_viewed`);
        slide.find('.carousel-control-prev').attr('href', `#carousel${unique_id}`);
        slide.find('.carousel-control-next').attr('href', `#carousel${unique_id}`);
        slide.find('#user_viewed_products').attr('id', `carousel${unique_id}`);
    }
});
PublicWidget.registry.book_wise_snippet = RecentViewProducts;
export default RecentViewProducts;