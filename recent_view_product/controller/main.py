from odoo.http import request, Controller, route


class RecentlyViewProducts(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/recent_view_products'], type="json", auth="user",
           website=True)
    def recently_view_products(self):
        """Function to get Recently view Products"""
        website = request.env['website'].sudo().get_current_website()
        excluded_products = website.sale_get_order().order_line.product_id.ids
        products = request.env['product.product'].sudo()
        visitor = request.env['website.visitor'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)

        tracked_products = request.env['website.track'].sudo()._read_group([
            ('visitor_id', '=', visitor.id),
            ('product_id', '!=', False),
            ('product_id.website_published', '=', True),
            ('product_id', 'not in', excluded_products),
        ], ['product_id'], limit=8, order='visit_datetime:max DESC')

        product_ids = [product.id for [product] in tracked_products]
        recent_products = products.search_read(
            [('id', 'in', product_ids)],
            ['name', 'image_1920', ]
        )
        return {
            'viewed_product': recent_products,
            'website': website.id,
        }
