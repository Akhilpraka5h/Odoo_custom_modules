# -*- coding: utf-8 -*-
from io import BytesIO
import base64, openpyxl
from odoo import fields, models
from odoo.exceptions import UserError


class ImportLotSerial(models.Model):
    _name = 'import.lot.serial'

    file_name = fields.Binary(string='File', required=True)
    file_name_name = fields.Char(string='File Name')

    def import_lot_serial_number_action(self):
        if not self.file_name:
            raise UserError("Please upload a valid file.")
        try:
            file_data = base64.b64decode(self.file_name)
            book = openpyxl.load_workbook(filename=BytesIO(file_data),
                                          read_only=True)
            sheet = book.active
            rows = sheet.iter_rows(min_row=2, values_only=True)
            headers = sheet.iter_rows(min_row=1, max_row=1, values_only=True)
            record_count = 0
            product = None
            company = None
            location = None
            for header in headers:
                lot_no = header.index('Lot/Serial Number')
                product_no = header.index('Product')
                company_no = header.index('Company')
                reference_no = header.index('Internal Reference')
                location_no = header.index('Location')
                standard_price_no = header.index('Cost')
                note_no = header.index('Description')

            for record in rows:
                lot_name = record[lot_no]
                product_name = record[product_no]
                company_name = record[company_no]
                reference = record[reference_no]
                location_name = record[location_no]
                standard_price = record[standard_price_no]
                note = record[note_no]

                if not lot_name:
                    raise UserError(
                        f"Lot/serial Number cannot be empty in row '{record_count + 1}'")
                elif product_name:
                    product = self.env['product.product'].search(
                        [('name', '=', product_name)],
                        limit=1)
                    if not product:
                        raise UserError(
                            f"The product '{product_name}' does not exist.")
                elif company_name:
                    company = self.env['res.company'].search(
                        [('name', '=', company_name)],
                        limit=1)
                    if not company:
                        raise UserError(
                            f"The company '{company_name}' does not exist.")
                elif location:
                    location = self.env['stock.location'].search(
                        [('complete_name', '=', location_name)],
                        limit=1)
                    if not location:
                        raise UserError(
                            f"The location '{location_name}' does not exist.")

                self.env['stock.lot'].create([{'name': lot_name,
                                               'product_id': product.id if product else 0,
                                               'company_id': company.id if company else 0,
                                               'ref': reference,
                                               'location_id': location.id if location else 0,
                                               'standard_price': standard_price,
                                               'note': note,
                                               }])
                record_count += 1
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'sticky': True,
                    'message': (
                        f"{record_count} record(s) successfully imported."),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        except Exception as e:
            raise UserError(f"Error processing file: {str(e)}")
