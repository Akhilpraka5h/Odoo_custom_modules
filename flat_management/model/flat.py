from odoo import fields, models


class Flat(models.Model):
    """Flat model"""
    _name = 'flat'
    _description = 'Flat model'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    flat_management_id= fields.Many2one(comodel_name='flat.management')