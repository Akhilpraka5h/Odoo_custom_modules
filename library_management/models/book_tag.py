from odoo import fields, models


class BookTags(models.Model):
    """Book tag"""
    _name = 'book.tag'
    _description = 'Tags for categorize books'
    _rec_name = 'book_tag'

    book_tag = fields.Char(string='Tags', copy=False)
    tag_color = fields.Integer(string='Color', default=0)

    _sql_constraints = [
        ('tag_name', 'unique(book_tag)', 'Already exist')
    ]
