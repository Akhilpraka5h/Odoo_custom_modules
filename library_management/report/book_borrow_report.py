from odoo import api, models, fields
import io
import xlsxwriter


class LibraryReport(models.AbstractModel):
    _name = 'report.library_management.book_checkout_line_report_template'
    _description = 'Library Report'

    date = fields.Datetime.now()

    @api.model
    def _get_report_values(self, docids, data=None):
        """Book Checkout Report PDF"""
        query = """
                SELECT 
                    orl.order_id, 
                    bk.book_title,
                    pr.name,
                    ch.checkout_id, 
                    ch.checkout_date,
                    ch.due_date, 
                    ch.return_date, 
                    STRING_AGG(gen.genre_name, ', ') AS genre_names  
                FROM library_book AS bk
                INNER JOIN book_checkout_line AS orl ON orl.book_id = bk.id
                INNER JOIN book_checkout AS ch ON ch.id = orl.order_id
                INNER JOIN res_partner AS pr ON pr.id = ch.partner_name_id
                LEFT JOIN book_genre_library_book_rel AS bkgr ON bkgr.library_book_id = bk.id
                LEFT JOIN book_genre AS gen ON bkgr.book_genre_id = gen.id  
                where 1=1
                """

        docs = self.env['book.checkout.line'].browse(docids)
        if not docs:
            if data['partner']:
                query += f" AND pr.id = {data['partner']}"
            if data['book']:
                query += f" AND bk.id = {data['book']}"
            if data['checkout_date']:
                query += f" AND ch.checkout_date >= '{data['checkout_date']}'"
            if data['return_date']:
                query += f" AND ch.return_date <= '{data['return_date']}'"
            if data['genre']:
                if len(data['genre']) == 1:
                    query += (f" AND bk.id IN (SELECT library_book_id FROM "
                              f"book_genre_library_book_rel "
                              f"WHERE book_genre_id = {data['genre'][0]})")
                else:
                    query += (f" AND bk.id IN (SELECT library_book_id FROM "
                              f"book_genre_library_book_rel "
                              f"WHERE book_genre_id IN {tuple(data['genre'])})")

        query += """
                    GROUP BY orl.order_id, bk.book_title, pr.name, 
                    ch.checkout_id, ch.checkout_date, ch.due_date, ch.return_date 
                    ORDER BY orl.order_id
                """

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data['report'] = report

        return {
            'doc_ids': docids,
            'doc_model': 'book.checkout.line',
            'docs': docs,
            'data': data,
            'filters': data['filters'] if not docs else '',
        }

    def get_xlsx_report(self, data, response):
        """Create xlsx Report """
        filters = data['filters']
        report = data['report']
        company = data['company']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        table_head = workbook.add_format(
            {'font_size': '12px', 'bold': True, 'align': 'center'})
        cell_format = workbook.add_format(
            {'bold': True, 'font_size': '12px', 'align': 'center'})
        filter_format = workbook.add_format(
            {'font_size': '11px', })
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '25px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})

        sheet.merge_range('A1:D1', company['name'], filter_format)
        sheet.merge_range('A2:D2', company['street'], filter_format)
        sheet.merge_range('A3:D3',
                          company['city'] + ' ' + company['state'] + ' ' +
                          company['zip'], filter_format)
        sheet.merge_range('A4:D4', company['country'], filter_format)
        sheet.write(0,13, 'Date:', cell_format)
        sheet.merge_range('O1:Q1', filters['date'], filter_format)

        sheet.merge_range('E6:O7', 'Book Borrow History Report', head)
        if filters['Member']:
            sheet.merge_range('A8:B8', 'Member:', cell_format)
            sheet.merge_range('C8:D8', filters['Member'], filter_format)
        if filters['Book']:
            sheet.merge_range('A9:B9', 'Book:', cell_format)
            sheet.merge_range('C9:D9', filters['Book'], filter_format)
        if filters['Genres']:
            sheet.merge_range('A10:B10', 'Genres:', cell_format)
            sheet.merge_range('C10:D10', filters['Genres'], filter_format)
        if filters['Checkout']:
            sheet.merge_range('A11:B11', 'Checkout Date:', cell_format)
            sheet.merge_range('C11:D11', filters['Checkout'], filter_format)
        if filters['Return']:
            sheet.merge_range('A12:B12', 'Return Date:', cell_format)
            sheet.merge_range('C12:D12', filters['Return'], filter_format)


        sheet.merge_range('A14:B14', 'Reference ID', table_head)
        sheet.merge_range('C14:D14', 'Members', table_head)
        sheet.merge_range('E14:F14', 'Books', table_head)
        sheet.merge_range('G14:H14', 'Genres', table_head)
        sheet.merge_range('I14:J14', 'Checkout Date', table_head)
        sheet.merge_range('K14:L14', 'Return Date', table_head)

        row = 15
        for record in report:
            sheet.merge_range(f"A{row}:B{row}", record['checkout_id'], txt)
            sheet.merge_range(f"C{row}:D{row}", record['name'], txt)
            sheet.merge_range(f"E{row}:F{row}", record['book_title'], txt)
            sheet.merge_range(f"G{row}:H{row}", record['genre_names'], txt)
            sheet.merge_range(f"I{row}:J{row}", record['checkout_date'], txt)
            sheet.merge_range(f"K{row}:L{row}", record['return_date'], txt)
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
