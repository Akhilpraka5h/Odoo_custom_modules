/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
function uniqueIdGenerator() {
    return Date.now() + Math.random().toString(28).slice(2);
}
function getChunkSize() {
    return window.innerWidth < 768 ? 1 : 4;
}
var LatestBooks = PublicWidget.Widget.extend({
    selector: '.best_latest_books_snippet',
    willStart: async function () {
        const data = await rpc('/latest_library_books', {});
        this.books = data;
    },
    start: function () {
        const refEl = this.$el.find("#latest_book_carousel");
        const unique_id = uniqueIdGenerator();
        const chunkSize = getChunkSize();
        const all_books = this.books.all_books;
        const currency = this.books['currency'];
        const chunkData = _chunk(all_books, chunkSize);
        if (all_books.length !== 0) {
            chunkData[0].is_active = true;
        }
        refEl.html(renderToElement('library_management.latest_book_snippet_carousel', { chunkData,currency }));
        const slide = this.$el.find(`#latest_book_carousel`);
        slide.find('.carousel-control-prev').attr('href', `#carousel${unique_id}`);
        slide.find('.carousel-control-next').attr('href', `#carousel${unique_id}`);
        slide.find('#library_latest_books_carousel').attr('id', `carousel${unique_id}`);

        window.addEventListener("resize", () => {
            this.Resize(refEl, all_books, unique_id);
        });
    },
    Resize: function (refEl, all_books, unique_id) {
        const chunkSize = getChunkSize();
        const currency = this.books['currency'];
        const chunkData = _chunk(all_books, chunkSize);
        if (all_books.length !== 0) {
            chunkData[0].is_active = true;
        }
        refEl.html(renderToElement('library_management.latest_book_snippet_carousel', { chunkData, currency }));
        const slide = this.$el.find(`#latest_book_carousel`);
        slide.find('.carousel-control-prev').attr('href', `#carousel${unique_id}`);
        slide.find('.carousel-control-next').attr('href', `#carousel${unique_id}`);
        slide.find('#library_latest_books_carousel').attr('id', `carousel${unique_id}`);
    }
});
PublicWidget.registry.book_wise_snippet = LatestBooks;
export default LatestBooks;