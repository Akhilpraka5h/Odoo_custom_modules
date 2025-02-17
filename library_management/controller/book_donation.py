from odoo.http import request, Controller, route
from odoo import fields
import base64


class WebFormController(Controller):
    """Controller for retrieve data from the form"""
    @route('/book_donation', type='http', auth='user', website=True)
    def web_book_donation(self):
        """Render the form to book donation"""
        return request.render('library_management.web_book_donation_template',
                              {'authors': request.env['book.author'].sudo().search(
                                  []),
                                  'publishers': request.env[
                                      'book.publisher'].sudo().search(
                                      [])})

    @route('/book_donation/submit', type='http', auth='user', website=True,
           methods=['POST'])
    def web_book_donation_form_submit(self, **post):
        """Retrieve the data filled in the web form and create book"""
        author = request.env['book.author'].sudo().browse(
            int(post.get('author')))
        publisher = request.env['book.publisher'].sudo().browse(
            int(post.get('publisher')))
        file = post.get('images')
        attachment_ids = []
        cover_image_id = 0
        if file:
            images = request.httprequest.files.getlist('images')
            for image in images:
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': image.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(image.read()),
                    'res_model': 'library.book',
                })
                attachment_ids.append(attachment.id)
            cover_image_id = request.env['ir.attachment'].sudo().browse(
                attachment_ids[0])
            book_images_id = request.env['ir.attachment'].sudo().browse(
                attachment_ids[1:])
        book_id = request.env['library.book'].sudo().create({
            'book_title': post.get('name'),
            'condition': post.get('condition'),
            'description': post.get('desc'),
            'book_author_id': author.id,
            'book_publisher_id': publisher.id,
            'book_status': "coming_soon",
            'image_attachment_ids': [fields.Command.set(attachment_ids)],
            'book_cover_image': cover_image_id.datas if file else 0,
            'contributor_id': request.env.user.partner_id.id,
        })
        if len(attachment_ids) > 1:
            for img in book_images_id:
                request.env['book.image'].sudo().create({
                    'library_book_id': book_id.id,
                    'image': img.datas,
                })
        return request.redirect('/contactus-thank-you')

