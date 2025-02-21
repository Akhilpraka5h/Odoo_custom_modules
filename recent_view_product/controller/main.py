from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, Controller, route

class CustomWebsiteSale(WebsiteSale):

    @route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(
        self, product_id, add_qty=1, set_qty=0, product_custom_attribute_values=None,
        no_variant_attribute_value_ids=None, **kwargs
    ):
        response = super().cart_update(
            product_id, add_qty, set_qty, product_custom_attribute_values,
            no_variant_attribute_value_ids, **kwargs
        )
        print('Hii')

        return response

class RecentViewProducts(Controller):
    """Retrieve data from the backend and pass to the view"""

    @route(['/recent_view_products'], type="json", auth="user",
           website=True)
    def recent_view_products(self, limit=10 ):
        print('hiiii')
        print(request.env['website.snippet.filter'].sudo()._get_products_latest_viewed(self, website, limit, domain, **kwargs))