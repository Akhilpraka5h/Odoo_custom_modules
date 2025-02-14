/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
console.log('Inside js')
var LatestBooks = PublicWidget.Widget.extend({
        selector: '.best_latest_books_snippet',
        willStart: async function () {
            const data = await rpc('/latest_library_books', {})
            this.books=data
        },
        start: function () {
            const refEl = this.$el.find("#latest_book_carousel")
            refEl.html(renderToElement('library_management.latest_book_snippet_carousel', {})
            )
        }
    });
PublicWidget.registry.latest_book_wise_snippet = LatestBooks;
return LatestBooks;
