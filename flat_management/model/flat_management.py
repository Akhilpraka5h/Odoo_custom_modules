from odoo import fields,models


class FlatManagement(models.Model):
    """Flat management model for selling flats"""
    _name = 'flat.management'
    _description = 'Flat Management for sale'

    name = fields.Char(string='Name')
    flat_ids= fields.One2many(comodel_name='flat', inverse_name='flat_management_id', string='Flats')