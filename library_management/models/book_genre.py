from odoo import fields, models


class BookGenres(models.Model):
    """Book genre"""
    _name = 'book.genre'
    _description = 'Genre'
    _rec_name = 'genre_name'

    genre_name = fields.Char(string='Genre', required=True, copy=False)
    genre_desc = fields.Char(string='Description')

    _sql_constraints = [
        ('genre_name', 'UNIQUE(genre_name)', 'Genre should be unique')
    ]
