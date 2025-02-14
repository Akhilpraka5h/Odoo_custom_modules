from odoo import fields, models


class BookImage(models.Model):
    """Book Image model"""
    _name = 'book.image'
    _description = 'Book Image'


    name = fields.Char(string="Name")
    image = fields.Image()
    library_book_id = fields.Many2one(comodel_name='library.book')