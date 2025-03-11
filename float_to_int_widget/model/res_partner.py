# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    """Inherit partner model"""
    _inherit = 'res.partner'

    round_value = fields.Float(string='Round value')
