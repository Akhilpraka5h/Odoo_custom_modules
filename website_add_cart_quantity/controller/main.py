from odoo import http
from odoo.http import route


class AddToCart(http.Controller):

    @route(['/shop/cart/product'], type='http', auth="public", methods=['POST'],
           website=True)
    def cart_update(**kwargs):
        """This route is called when adding a product to cart (no options)."""
        print('haiii')
