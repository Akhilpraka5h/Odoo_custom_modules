/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";
//export function _chunk(array, size) {
//    const result = [];
//    for (let i = 0; i < array.length; i += size) {
//        result.push(array.slice(i, i + size));
//    }
//    return result;
//}
//var LatestBooks = PublicWidget.Widget.extend({
//        selector: '.best_latest_books_snippet',
//        willStart: async function () {
//            const data = await jsonrpc('/latest_library_books', {})
//            const [books] = data
//            Object.assign(this, {
//                books
//            })
//        },
//        start: function () {
//            const refEl = this.$el.find("#latest_book_carousel")
//            const { books} = this
//            const chunkData = chunk(products, 4)
//            refEl.html(renderToElement('library_management.latest_book_snippet_carousel', {
//                chunkData
//            }))
//        }
//    });
//PublicWidget.registry.products_category_wise_snippet = LatestBooks;
//return LatestBooks;

//var Dynamic=PublicWidget.Widget.extend({
//selector:'.best_latest_books_snippet',
//willStart:async function(){
//var self=this;
//await jsonrpc('/latest_library_books')}.then((data)=>{this.data;
//});
//},
//start: function(){
//var chunks=_chunk(this.data,4)
//chunk[0].is_active=true
//this.$el.find('#latest_book_carousel').html(
//renderToElement('library_management.latest_book_snippet_carousel',{
//chunks
//})
//)
//},
//)
let DynamicSnippets = publicWidget.Widget.extend({
   selector: '.best_latest_books_snippet',
   start: function(){
       jsonrpc('/latest_library_books', {}).then((res)=>{
           if (res){
               this.$el.find("#total").html(renderToElement('library_management.latest_book_snippet_carousel', {res: res}))
           }
       })
   }
});
publicWidget.registry.DynamicSnippets = DynamicSnippets;