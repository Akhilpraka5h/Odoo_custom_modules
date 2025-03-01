from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"
    _description = "Point of Sale Orders"
