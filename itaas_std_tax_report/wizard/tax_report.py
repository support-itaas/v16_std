# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017  Technaureus Info Solutions(<http://technaureus.com/>).

from odoo import models, fields, api, _
from datetime import datetime
#from StringIO import StringIO
from io import BytesIO
import base64
from odoo.exceptions import UserError
from odoo.tools import misc
import xlwt
from decimal import *
from dateutil.relativedelta import relativedelta
import calendar
from io import StringIO
import xlsxwriter

class tax_report(models.TransientModel):
    _name = 'tax.report'

    def _get_year(self):
        curr_date = datetime.now()
        last_year = curr_date.year - 1 + 543
        current_year = curr_date.year + 543
        next_year = curr_date.year + 1 + 543

        return [(last_year, last_year), (current_year, current_year), (next_year, next_year)]

    date_from = fields.Date(string='Date From',required=True)
    date_to = fields.Date(string='Date To',required=True)
    month = fields.Selection([
        ('1','มกราคม'),
        ('2','กุมภาพันธ์'),
        ('3', 'มีนาคม'),
        ('4', 'เมษายน'),
        ('5', 'พฤษภาคม'),
        ('6', 'มิถุนายน'),
        ('7', 'กรกฏาคม'),
        ('8', 'สิงหาคม'),
        ('9', 'กันยายน'),
        ('10', 'ตุลาคม'),
        ('11', 'พฤศจิกายน'),
        ('12', 'ธันวาคม'),
    ],string='Month',required=True)
    year = fields.Integer(string='Year')

    report_type = fields.Selection([('sale','ภาษีขาย'),('purchase','ภาษีซื้อ')],default='sale',string='Report Type', required=True)
    company_id = fields.Many2one('res.company')

    vat_0 = fields.Boolean('Vat 0')
    vat_7 = fields.Boolean('Vat 7')
    vat_exmpted = fields.Boolean('Vat Exmpted')


    @api.model
    def default_get(self, fields):
        res = super(tax_report,self).default_get(fields)
        curr_date = datetime.now()
        from_date = datetime(curr_date.year,curr_date.month,1).date() or False
        to_date = datetime(curr_date.year,curr_date.month,calendar.monthrange(curr_date.year, curr_date.month)[1]).date() or False
        year = curr_date.year + 543
        company_id = self.env.company.id
        res.update({'year': year,'month':str(curr_date.month),
                    'date_from': str(from_date),
                    'date_to': str(to_date),'company_id': company_id,})
        print (res)
        return res

    @api.onchange('month','year')
    def onchange_month_year(self):
        if self.month and self.year:
            select_month = self.month
            select_year = self.year - 543
            month_day = calendar.monthrange(select_year, int(select_month))[1]
            from_date = datetime(select_year, int(select_month), 1).date() or False
            to_date = datetime(select_year, int(select_month), month_day).date() or False
            self.date_from = from_date
            self.date_to = to_date



    def print_report_pdf(self):
        print('print_report_pdf')
    #     if self.vat_0 and self.vat_7 and self.vat_exmpted:
    #         raise UserError(_("Please set only one vat !!! ุ"))
    #
    #     data = {'date_from': self.date_from, 'date_to': self.date_to, 'report_type': self.report_type, 'tax_id': self.tax_id.id, 'company_id': self.company_id,'vat_0':self.vat_0,'vat_7':self.vat_7,'vat_exmpted':self.vat_exmpted}
    #     if data['report_type'] == 'sale':
    #         return self.env.ref('itaas_print_tax_report.action_sale_tax_report_id').report_action([], data=data)
    #     else:
    #         return self.env.ref('itaas_print_tax_report.action_purchase_tax_report_id').report_action([], data=data)




    def print_report_sale(self):
        print('print_report_xls_sale')
        fl = BytesIO()
        workbook = xlsxwriter.Workbook(fl)
        name = self.report_type + '_tax_report'
        namexls = str(self.report_type) + '_tax_report' + '.xls'
        worksheet = workbook.add_worksheet(name)

        for_left_bold_no_border = workbook.add_format({'align': 'left', 'bold': True})
        for_center_bold_no_border = workbook.add_format({'align': 'center', 'bold': True})
        for_right_bold_no_border = workbook.add_format({'align': 'right', 'bold': True})

        for_left_no_border = workbook.add_format({'align': 'left'})
        for_center_no_border = workbook.add_format({'align': 'center'})
        for_right_no_border = workbook.add_format({'align': 'right'})

        for_left_bold = workbook.add_format({'align': 'left', 'bold': True, 'border': True})
        for_center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': True})
        for_right_bold = workbook.add_format({'align': 'right', 'bold': True, 'border': True})

        for_left = workbook.add_format({'align': 'left', 'border': True})
        for_center = workbook.add_format({'align': 'center', 'border': True})
        for_right = workbook.add_format({'align': 'right', 'border': True , 'num_format': '#,##0.00'})

        for_right_bold_no_border_date = workbook.add_format({'align': 'right', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_right_border_num_format = workbook.add_format({'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format({'align': 'right', 'bold': True, 'border': True, 'num_format': '#,##0.00'})

        for_center_bold_no_border_date = workbook.add_format(
            {'align': 'center', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_left_bold_no_border_date = workbook.add_format({'align': 'left', 'bold': True, 'num_format': 'dd/mm/yy'})

        for_center_date = workbook.add_format({'align': 'center', 'border': True, 'num_format': 'dd/mm/yyyy'})

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)

        month = self.month
        if month:
            if month == '1':
                monthth = 'มกราคม'
            elif month == '2':
                monthth = 'กุมภาพันธ์'
            elif month == '3':
                monthth = 'มีนาคม'
            elif month == '3':
                monthth = 'มีนาคม'
            elif month == '4':
                monthth = 'เมษายน'
            elif month == '5':
                monthth = 'พฤษภาคม'
            elif month == '6':
                monthth = 'มิถุนายน'
            elif month == '7':
                monthth = 'กรกฏาคม'
            elif month == '8':
                monthth = 'สิงหาคม'
            elif month == '9':
                monthth = 'กันยายน'
            elif month == '10':
                monthth = 'ตุลาคม'
            elif month == '11':
                monthth = 'พฤศจิกายน'
            else:
                monthth = 'ธันวาคม'

        year = self.year
        company_id = self.env.company
        inv_row = 3
        worksheet.write(inv_row, 0, 'เดือนภาษี', for_left_bold_no_border)
        worksheet.write(inv_row, 1, monthth, for_left_no_border)
        worksheet.write(inv_row, 4, 'ปี', for_left_bold_no_border)
        worksheet.write(inv_row, 5, year, for_left_no_border)

        inv_row += 1
        worksheet.write(inv_row, 0, 'ชื่อผู้ประกอบการ', for_left_bold_no_border)
        worksheet.write(inv_row, 1, company_id.name, for_left_no_border)
        worksheet.write(inv_row, 4, 'เลขประจำผู้เสียภาษีอากร', for_left_bold_no_border)
        worksheet.write(inv_row, 5, company_id.vat, for_left_no_border)

        inv_row += 1
        worksheet.write(inv_row, 0, 'ชื่อสถานประกอบการ', for_left_bold_no_border)
        worksheet.write(inv_row, 1, company_id.name, for_left_no_border)
        worksheet.write(inv_row, 4, 'สำนักงานใหญ่ / สาขา', for_left_bold_no_border)
        if company_id.branch_no:
            if company_id.branch_no == '00000':
                branch_no = 'สำนักงานใหญ่'
            else:
                branch_no = 'สาขา' + ' ' + company_id.branch_no
            worksheet.write(inv_row, 5, branch_no, for_left_no_border)
        else:
            worksheet.write(inv_row, 5, 'สำนักงานใหญ่', for_left_no_border)


        inv_row += 1
        worksheet.write(inv_row, 0, 'สถานประกอบการ', for_left_bold_no_border)
        company_address = company_id.get_company_full_address_text()
        worksheet.write(inv_row, 1,company_address , for_left_no_border)

        inv_row += 3
        inv_row_merge_head = inv_row + 1
        worksheet.merge_range('A' + str(inv_row) + ':A' + str(inv_row_merge_head), "ลำดับที่", for_center_bold)
        worksheet.merge_range('B' + str(inv_row) + ':C' + str(inv_row), "ใบกำกับภาษี", for_center_bold)
        worksheet.write('B' + str(inv_row_merge_head), 'วัน เดือน ปี', for_center_bold)
        worksheet.write('C' + str(inv_row_merge_head), 'เลขที่', for_center_bold)
        worksheet.merge_range('D' + str(inv_row) + ':D' + str(inv_row_merge_head), "ชื่อผู้ซื้อสินค้า/ผู้รับบริการ",
                              for_center_bold)
        worksheet.merge_range('E' + str(inv_row) + ':E' + str(inv_row_merge_head),
                              'เลขประจำตัวผู้เสียภาษีอากร\nของผู้ซื้อสินค้า/ผู้รับบริการ', for_center_bold)
        worksheet.merge_range('F' + str(inv_row) + ':G' + str(inv_row), "สถานประกอบการ", for_center_bold)
        worksheet.write('F' + str(inv_row_merge_head), 'สำนักงานใหญ่', for_center_bold)
        worksheet.write('G' + str(inv_row_merge_head), 'สาขาที่', for_center_bold)
        worksheet.merge_range('H' + str(inv_row) + ':H' + str(inv_row_merge_head), "มูลค่าสินค้าหรือบริการ",
                              for_center_bold)
        worksheet.merge_range('I' + str(inv_row) + ':I' + str(inv_row_merge_head), "จำนวนเงินภาษีมูลค่าเพิ่ม",
                              for_center_bold)
        worksheet.merge_range('J' + str(inv_row) + ':J' + str(inv_row_merge_head), "รวม",
                              for_center_bold)
        worksheet.merge_range('K' + str(inv_row) + ':K' + str(inv_row_merge_head), "หมายเหตุ",
                              for_center_bold)
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'report_type': self.report_type,
            'company_id': self.company_id,
            'vat_0':self.vat_0,
            'vat_7':self.vat_7,
        }
        report_values = self.env['report.itaas_std_tax_report.sale_tax_report_id']._get_report_values(self,data=data)
        move_ids = report_values.get('docs')
        worksheet.merge_range('A1:I1', "รายงานภาษีขาย", for_center_bold_no_border)

        #Variable
        sl_no = 1
        amount_untaxed = 0
        amount_vat = 0
        amount_total = 0

        for inv in move_ids:
            inv_row += 1
            worksheet.write(inv_row, 0, sl_no, for_center)
            worksheet.write(inv_row, 1, inv['date'] or '', for_center_date)
            worksheet.write(inv_row, 2, inv['name'], for_center)

            worksheet.write(inv_row, 3, inv['partner'], for_left)
            worksheet.write(inv_row, 4, inv['vat'], for_left)

            if inv['branch'] == '00000':
                worksheet.write(inv_row, 5, inv['branch'], for_right)
                worksheet.write(inv_row, 6, '', for_left)
            else:
                worksheet.write(inv_row, 5, '', for_left)
                worksheet.write(inv_row, 6, inv['branch'], for_right)

            if inv['state'] != 'cancel':
                if inv['type'] == 'out_refund':

                    worksheet.write(inv_row, 7, inv['amount_untaxed'] * (-1), for_right)
                    amount_untaxed = amount_untaxed + (inv['amount_untaxed'] * (-1))
                    amount_vat = amount_vat + (inv['amount_tax'] * (-1))
                    amount_total = amount_total + (inv['amount_total'] * (-1))
                    worksheet.write(inv_row, 8, inv['amount_tax'] * (-1), for_right)
                    worksheet.write(inv_row, 9, inv['amount_total'] * (-1), for_right)
                else:
                    worksheet.write(inv_row, 7, inv['amount_untaxed'], for_right)
                    amount_untaxed = amount_untaxed + inv['amount_untaxed']
                    amount_vat = amount_vat + inv['amount_tax']
                    amount_total = amount_total + inv['amount_total']
                    worksheet.write(inv_row, 8, inv['amount_tax'], for_right)
                    worksheet.write(inv_row, 9, inv['amount_total'], for_right)

            if inv['state'] == 'cancel':
                worksheet.write(inv_row, 7, 0, for_right)
                worksheet.write(inv_row, 8, 0, for_right)
                worksheet.write(inv_row, 9, 0, for_right)
                worksheet.write(inv_row, 10, 'ยกเลิก (Cancel)', for_right)
            else:
                worksheet.write(inv_row, 10, ' ', for_right)

            sl_no += 1

        inv_row += 1
        worksheet.write(inv_row, 6, 'Total', for_center_bold)
        worksheet.write(inv_row, 7, amount_untaxed, for_right_bold_border_num_format)
        worksheet.write(inv_row, 8, amount_vat, for_right_bold_border_num_format)
        worksheet.write(inv_row, 9, amount_total, for_right_bold_border_num_format)

        workbook.close()
        buf = fl.getvalue()
        # vals = {'name': namexls, 'report_file': base64.encodestring(buf)}
        vals = {'name': namexls, 'report_file': base64.encodebytes(buf)}
        self._cr.execute("TRUNCATE tax_excel_export CASCADE")
        wizard_id = self.env['tax.excel.export'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.excel.export',
            'target': 'new',
            'res_id': wizard_id.id,
        }



    def print_report_purchase(self):
        print('print_report_purchase')
        print('print_report_xls')
        fl = BytesIO()
        workbook = xlsxwriter.Workbook(fl)
        name = self.report_type + '_tax_report'
        namexls = str(self.report_type) + '_tax_report' + '.xls'
        worksheet = workbook.add_worksheet(name)

        for_left_bold_no_border = workbook.add_format({'align': 'left', 'bold': True})
        for_center_bold_no_border = workbook.add_format({'align': 'center', 'bold': True})
        for_right_bold_no_border = workbook.add_format({'align': 'right', 'bold': True})

        for_left_no_border = workbook.add_format({'align': 'left'})
        for_center_no_border = workbook.add_format({'align': 'center'})
        for_right_no_border = workbook.add_format({'align': 'right'})

        for_left_bold = workbook.add_format({'align': 'left', 'bold': True, 'border': True})
        for_center_bold = workbook.add_format({'align': 'center', 'bold': True, 'border': True})
        for_right_bold = workbook.add_format({'align': 'right', 'bold': True, 'border': True})

        for_left = workbook.add_format({'align': 'left', 'border': True})
        for_center = workbook.add_format({'align': 'center', 'border': True})
        for_right = workbook.add_format({'align': 'right', 'border': True, 'num_format': '#,##0.00'})

        for_right_bold_no_border_date = workbook.add_format({'align': 'right', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_right_border_num_format = workbook.add_format({'align': 'right', 'border': True, 'num_format': '#,##0.00'})
        for_right_bold_border_num_format = workbook.add_format(
            {'align': 'right', 'bold': True, 'border': True, 'num_format': '#,##0.00'})

        for_center_bold_no_border_date = workbook.add_format(
            {'align': 'center', 'bold': True, 'num_format': 'dd/mm/yy'})
        for_left_bold_no_border_date = workbook.add_format({'align': 'left', 'bold': True, 'num_format': 'dd/mm/yy'})

        for_center_date = workbook.add_format({'align': 'center', 'border': True, 'num_format': 'dd/mm/yyyy'})

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)

        month = self.month
        print(month)
        print('==============')

        if month:
            if month == '1':
                monthth = 'มกราคม'
            elif month == '2':
                monthth = 'กุมภาพันธ์'
            elif month == '3':
                monthth = 'มีนาคม'
            elif month == '3':
                monthth = 'มีนาคม'
            elif month == '4':
                monthth = 'เมษายน'
            elif month == '5':
                monthth = 'พฤษภาคม'
            elif month == '6':
                monthth = 'มิถุนายน'
            elif month == '7':
                monthth = 'กรกฏาคม'
            elif month == '8':
                monthth = 'สิงหาคม'
            elif month == '9':
                monthth = 'กันยายน'
            elif month == '10':
                monthth = 'ตุลาคม'
            elif month == '11':
                monthth = 'พฤศจิกายน'
            else:
                monthth = 'ธันวาคม'

        year = self.year
        company_id = self.env.company

        inv_row = 3
        worksheet.write(inv_row, 0, 'เดือนภาษี', for_left_bold_no_border)
        worksheet.write(inv_row, 1, monthth, for_left_no_border)
        worksheet.write(inv_row, 4, 'ปี', for_left_bold_no_border)
        worksheet.write(inv_row, 5, year, for_left_no_border)

        inv_row += 1
        worksheet.write(inv_row, 0, 'ชื่อผู้ประกอบการ', for_left_bold_no_border)
        worksheet.write(inv_row, 1, company_id.name, for_left_no_border)
        worksheet.write(inv_row, 4, 'เลขประจำผู้เสียภาษีอากร', for_left_bold_no_border)
        worksheet.write(inv_row, 5, company_id.vat, for_left_no_border)

        inv_row += 1
        worksheet.write(inv_row, 0, 'ชื่อสถานประกอบการ', for_left_bold_no_border)
        worksheet.write(inv_row, 1, company_id.name, for_left_no_border)
        worksheet.write(inv_row, 4, 'สำนักงานใหญ่ / สาขา', for_left_bold_no_border)
        if company_id.branch_no:
            if company_id.branch_no == '00000':
                branch_no = 'สำนักงานใหญ่'
            else:
                branch_no = 'สาขา' + ' ' + company_id.branch_no
            # branch_no = company_id.branch_no if company_id.branch_no == '00000' else 'สำนักงานใหญ่'
            worksheet.write(inv_row, 5, branch_no, for_left_no_border)
        else:
            worksheet.write(inv_row, 5, 'สำนักงานใหญ่', for_left_no_border)

        inv_row += 1
        worksheet.write(inv_row, 0, 'สถานประกอบการ', for_left_bold_no_border)
        company_address = company_id.get_company_full_address_text()
        worksheet.write(inv_row, 1, company_address, for_left_no_border)

        inv_row += 3
        inv_row_merge_head = inv_row + 1
        worksheet.merge_range('A' + str(inv_row) + ':A' + str(inv_row_merge_head), "ลำดับที่", for_center_bold)
        worksheet.merge_range('B' + str(inv_row) + ':C' + str(inv_row), "ใบกำกับภาษี", for_center_bold)
        worksheet.write('B' + str(inv_row_merge_head), 'วัน เดือน ปี', for_center_bold)
        worksheet.write('C' + str(inv_row_merge_head), 'เลขที่', for_center_bold)
        worksheet.merge_range('D' + str(inv_row) + ':D' + str(inv_row_merge_head), "ชื่อผู้ซื้อสินค้า/ผู้รับบริการ",
                              for_center_bold)
        worksheet.merge_range('E' + str(inv_row) + ':E' + str(inv_row_merge_head),
                              'เลขประจำตัวผู้เสียภาษีอากร\nของผู้ซื้อสินค้า/ผู้รับบริการ', for_center_bold)
        worksheet.merge_range('F' + str(inv_row) + ':G' + str(inv_row), "สถานประกอบการ", for_center_bold)
        worksheet.write('F' + str(inv_row_merge_head), 'สำนักงานใหญ่', for_center_bold)
        worksheet.write('G' + str(inv_row_merge_head), 'สาขาที่', for_center_bold)
        worksheet.merge_range('H' + str(inv_row) + ':H' + str(inv_row_merge_head), "มูลค่าสินค้าหรือบริการ",
                              for_center_bold)
        worksheet.merge_range('I' + str(inv_row) + ':I' + str(inv_row_merge_head), "จำนวนเงินภาษีมูลค่าเพิ่ม",
                              for_center_bold)
        worksheet.merge_range('J' + str(inv_row) + ':J' + str(inv_row_merge_head), "รวม",
                              for_center_bold)
        worksheet.merge_range('K' + str(inv_row) + ':K' + str(inv_row_merge_head), "หมายเหตุ",
                              for_center_bold)

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'report_type': self.report_type,
            'company_id': self.company_id,
            'vat_0':self.vat_0,
            'vat_7':self.vat_7,
        }
        report_values = self.env['report.itaas_std_tax_report.purchase_tax_report_id']._get_report_values(self,
                                                                                                            data=data)
        move_lines = report_values.get('docs')
        print('move_lines : ', move_lines)

        worksheet.merge_range('A1:I1', "รายงานภาษีซื้อ", for_center_bold_no_border)
        amount_total = 0
        before_total = 0
        amount_tax_total = 0
        if move_lines:
            sl_no = 1
            for ml in move_lines:
                print('ml:', ml)
                inv_row += 1
                worksheet.write(inv_row, 0, sl_no, for_center)
                worksheet.write(inv_row, 1, ml['date'] or '', for_center_date)
                worksheet.write(inv_row, 2, ml['ref'], for_left)
                worksheet.write(inv_row, 3, ml['partner'].name, for_left)
                worksheet.write(inv_row, 4, ml['vat'], for_left)
                if ml['branch'] == '00000':
                    worksheet.write(inv_row, 5, ml['branch'], for_right)
                    worksheet.write(inv_row, 6, '', for_left)
                else:
                    worksheet.write(inv_row, 5, ' ', for_left)
                    worksheet.write(inv_row, 6, ml['branch'], for_right)
                if ml['debit']:
                    amount_tax = ml['debit']
                elif ml['credit']:
                    amount_tax = ml['credit']
                else:
                    amount_tax = 0
                if ml['amount_untaxed']:
                    if ml['type'] == 'in_refund':
                        if ml['amount_untaxed'] > 0:
                            amount_untax = ml['amount_untaxed'] * (-1)
                        else:
                            amount_untax = ml['amount_untaxed']
                    else:
                        amount_untax = ml['amount_untaxed']
                else:
                    amount_untax = amount_tax * 100 / 7
                if ml['type'] == 'in_refund':
                    if ml['state'] == 'cancel':
                        if ml['debit']:
                            worksheet.write(inv_row, 7, '0.00', for_right_border_num_format)
                        else:
                            worksheet.write(inv_row, 7, '0.00', for_right_border_num_format)
                            before_total += amount_untax
                    else:
                        if ml['debit']:
                            worksheet.write(inv_row, 7, amount_untax, for_right_border_num_format)
                            before_total += amount_untax
                        else:
                            worksheet.write(inv_row, 7, amount_untax, for_right_border_num_format)
                            before_total += amount_untax
                else:
                    if ml['state'] == 'cancel':
                        if ml['debit']:
                            worksheet.write(inv_row, 7, '0.00', for_right_border_num_format)
                        else:
                            worksheet.write(inv_row, 7, '0.00', for_right_border_num_format)
                            before_total += amount_untax
                    else:
                        if ml['debit']:
                            worksheet.write(inv_row, 7, amount_untax, for_right_border_num_format)
                            before_total += amount_untax
                        else:
                            worksheet.write(inv_row, 7, amount_untax, for_right_border_num_format)
                            before_total += amount_untax

                if ml['type'] == 'in_refund':
                    if ml['state'] == 'cancel':
                        if ml['debit']:
                            debit_credit = ml['debit']
                        elif ml['credit']:
                            debit_credit = ml['credit']
                        worksheet.write(inv_row, 8, '0.00', for_right_border_num_format)
                        worksheet.write(inv_row, 9, '0.00', for_right_border_num_format)
                        amount_total += '0.00' + amount_untax
                        worksheet.write(inv_row, 10, 'ยกเลิก (Cancel)', for_right)
                    else:
                        if ml['debit']:
                            debit_credit = ml['debit']
                        elif ml['credit']:
                            debit_credit = ml['credit']
                        else:
                            debit_credit = 0
                        worksheet.write(inv_row, 8, ml['debit'] or ml['credit'] * (-1), for_right_border_num_format)
                        worksheet.write(inv_row, 9, (debit_credit * (-1) + amount_untax),
                                        for_right_border_num_format)
                        amount_total += (debit_credit * (-1)) + amount_untax
                        worksheet.write(inv_row, 10, 'ยกเลิก (Cancel)', for_right)
                        worksheet.write(inv_row, 10, ml['note'], for_right)

                else:
                    if ml['state'] == 'cancel':
                        worksheet.write(inv_row, 8, '0.00', for_right_border_num_format)
                        worksheet.write(inv_row, 9, '0.00', for_right_border_num_format)
                        worksheet.write(inv_row, 10, 'ยกเลิก (Cancel)', for_right)
                    else:
                        worksheet.write(inv_row, 8, ml['debit'] or ml['credit'], for_right_border_num_format)
                        worksheet.write(inv_row, 9, ml['debit'] + ml['credit'] + amount_untax,
                                        for_right_border_num_format)
                        amount_total += ml['debit'] + ml['credit'] + amount_untax
                        worksheet.write(inv_row, 10, ml['note'], for_right)

                sl_no += 1
                if ml['type'] == 'in_refund':
                    if ml['state'] != 'cancel':
                        amount_tax_total += ml['debit'] * (-1)
                        amount_tax_total += ml['credit'] * (-1)
                else:
                    if ml['state'] != 'cancel':
                        amount_tax_total += ml['debit']
                        amount_tax_total += ml['credit']
            inv_row += 1
            worksheet.write(inv_row, 6, 'Total', for_center_bold)
            worksheet.write(inv_row, 7, before_total, for_right_bold_border_num_format)
            worksheet.write(inv_row, 8, amount_tax_total, for_right_bold_border_num_format)
            worksheet.write(inv_row, 9, amount_total, for_right_bold_border_num_format)

        workbook.close()
        buf = fl.getvalue()
        # vals = {'name': namexls, 'report_file': base64.encodestring(buf)}
        vals = {'name': namexls, 'report_file': base64.encodebytes(buf)}
        self._cr.execute("TRUNCATE tax_excel_export CASCADE")
        wizard_id = self.env['tax.excel.export'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.excel.export',
            'target': 'new',
            'res_id': wizard_id.id,
        }

class tax_excel_export(models.TransientModel):
    _name = 'tax.excel.export'

    report_file = fields.Binary('File')
    name = fields.Char(string='File Name', size=32)


    def action_back(self):
        if self._context is None:
            self._context = {}
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.report',
            'target': 'new',
        }


class pnd53_report(models.TransientModel):
    _name = 'pnd53.report'
    date_from = fields.Date(string='Date From',required=True)
    date_to = fields.Date(string='Date To',required=True)
    report_type = fields.Selection([('personal', 'ภงด3'), ('company', 'ภงด53')],string='Report Type', required=True)
    month = fields.Char(string='Month')
    company_id = fields.Many2one('res.company')

    @api.model
    def default_get(self, fields):
        res = super(pnd53_report, self).default_get(fields)
        curr_date = datetime.now()
        from_date = datetime(curr_date.year, curr_date.month, 1).date() or False
        to_date = datetime(curr_date.year, curr_date.month, curr_date.day).date() or False
        res.update({'date_from': str(from_date), 'date_to': str(to_date)})
        return res

    def print_pnd53_report(self):
        print('bbbbbbbbbbb')
        # data = {}
        data = {'date_from': self.date_from, 'date_to': self.date_to, 'report_type': self.report_type,
                'month': self.month, 'company_id': self.company_id}
        # data['form'] = self.read(['date_from', 'date_to', 'report_type', 'month','company_id'])[0]

        if data['report_type'] == 'company':
            # return self.env['report'].get_action(self, 'thai_accounting.report_pnd53_id', data=data)
            return self.env.ref('itaas_print_tax_report.action_report_pnd53_id').report_action(self, data=data)
        elif data['report_type'] == 'personal':
            # return self.env['report'].get_action(self, 'thai_accounting.report_pnd3_id', data=data)
            return self.env.ref('itaas_print_tax_report.action_report_pnd3_id').report_action(self, data=data)
        else:
            # return self.env['report'].get_action(self, 'thai_accounting.report_pnd2_id', data=data)
            return self.env.ref('itaas_print_tax_report.action_report_pnd2_id').report_action(self, data=data)

    # @api.multi
    def print_pnd53_report_to_text(self):

        context = dict(self._context or {})
        file_type = context.get('file')

        fl = StringIO()
        workbook = xlwt.Workbook(encoding='utf-8')

        font = xlwt.Font()
        font.bold = True
        font.bold = True
        for_right = xlwt.easyxf(
            "font: name  Times New Roman,color black,  height 180;  align: horiz right,vertical center; borders: top thin, bottom thin, left thin, right thin")
        for_right.num_format_str = '#,###.00'
        for_right_bold = xlwt.easyxf(
            "font: bold 1, name  Times New Roman,color black,  height 180;  align: horiz right,vertical center; borders: top thin, bottom thin, left thin, right thin")
        for_right_bold.num_format_str = '#,###.00'
        for_center = xlwt.easyxf(
            "font: name  Times New Roman, color black,  height 180; align: horiz center,vertical center,wrap on; borders: top thin, bottom thin, left thin, right thin")
        for_left = xlwt.easyxf(
            "font: name  Times New Roman,color black,  height 180;  align: horiz left,vertical center; borders: top thin, bottom thin, left thin, right thin")
        for_center_bold = xlwt.easyxf(
            "font: bold 1, name  Times New Roman, color black, height 180;  align: horiz center,vertical center,wrap on; borders: top thin, bottom thin, left thin, right thin")
        for_left_bold_no_border = xlwt.easyxf(
            "font: bold 1, name  Times New Roman, color black, height 180;  align: horiz left,vertical center;")

        GREEN_TABLE_HEADER = xlwt.easyxf(
            'font: bold 1, name  Times New Roman, height 300,color black;'
            'align: vertical center, horizontal center, wrap on;'
            'borders: top thin, bottom thin, left thin, right thin;'
            'pattern:  pattern_fore_colour white, pattern_back_colour white'
        )

        alignment = xlwt.Alignment()  # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
        style = xlwt.easyxf('align: wrap yes')
        style.num_format_str = '#,###.00'
        # cr, uid, context = self.env.args
        final_text = ""
        final_text_body = ""

        # -------------------------------------- PND 3 ----------------------------------------
        if self.report_type == 'personal':

            move_line_ids = self.env['account.move.line'].search(
                [('date_maturity', '>=', self.date_from), ('date_maturity', '<=', self.date_to),
                 ('wht_type.name', '=', 'personal'), ('wht_tax', '!=', False), ('account_id.wht', '=', True)],
                order='date_maturity ASC')
            move_ids = ""
            inv_row = 1
            for move in move_line_ids:
                move_ids += str(inv_row) + '|'
                if move.tax_onetime:
                    move_ids += str(move.tax_onetime) + '|'
                elif not move.name_onetime:
                    if move.partner_id.is_onetime:
                        move_ids += str(move.tax_onetime) + '|'
                    elif not move.partner_id.is_onetime:
                        move_ids += str(move.partner_id.vat) + '|'

                if move.name_onetime:
                    name_temp = move.name_onetime.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                elif not move.name_onetime:
                    name_temp = move.name_onetime.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                elif move.partner_id.title:
                    title_name = move.partner_id.title.name
                    name_temp = move.partner_id.name.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                    # last_name = name_temp[1:]
                else:
                    name_temp = move.partner_id.name.split(' ')
                    # name = " ".join(name_temp[1:])

                    if len(name_temp) >= 3:
                        title_name = name_temp[0]
                        first_name = name_temp[1]
                        last_name = name_temp[2]
                    elif len(name_temp) == 2:
                        title_name = name_temp[0]
                        first_name = name_temp[1]
                        last_name = " "
                    else:
                        title_name = " "
                        first_name = name_temp[0]
                        last_name = " "

                move_ids += str(title_name) + '|'
                move_ids += str(first_name) + '|'
                move_ids += str(last_name) + '|'

                address = self.get_partner_full_address_text(move.partner_id)
                address_text = ' '.join(address)
                move_ids += address_text[0:30] + '|'


                # if move.partner_id.street:
                #     move_ids += str(move.partner_id.street)[0:30]
                #     move_ids += str(move.partner_id.street2)[0:30]
                #     move_ids += str(move.partner_id.city)[0:30]
                #     move_ids += str(move.partner_id.state_id.name)[0:40]
                #     move_ids += str(move.partner_id.zip)[0:5] + '|'
                # else:
                #     move_ids += '|'
                # else:
                #     move_ids += '|'
                # if move.partner_id.street2:
                #     move_ids += str(move.partner_id.street2)[0:30]
                # else:
                #     move_ids += '|'
                # if move.partner_id.city:
                #     move_ids += str(move.partner_id.city)[0:30]
                # else:
                #     move_ids += '|'
                # if move.partner_id.state_id and move.partner_id.state_id.name:
                #     move_ids += str(move.partner_id.state_id.name)[0:40]
                # else:
                #     move_ids += '|'
                # if move.partner_id.zip:
                #     move_ids += str(move.partner_id.zip)[0:5] + '|'
                # else:
                #     move_ids += '|'

                if move.date_maturity:
                    # date = datetime.strptime(move.date_maturity, "%Y-%m-%d").date()
                    date = move.date_maturity
                    if len(str(date.day)) < 2:
                        day = '0' + str(date.day)
                    else:
                        day = str(date.day)
                    if len(str(date.month)) < 2:
                        month = '0' + str(date.month)
                    else:
                        month = str(date.month)
                    date_payment = day + '/' + month + '/' + str(date.year + 543)
                if date_payment:
                    move_ids += date_payment + '|'
                else:
                    move_ids += '|'
                # move_ids += strToDate(move.date_maturity).strftime("%d/%m/%Y") + '|'
                move_ids += str(move.name) + '|'

                if move.wht_type:
                    wht_type = str(move.wht_tax.amount)[0]
                    # if str(move.wht_tax.amount) == '1%':
                    #     wht_type = '1'
                    # elif move.wht_type == '2%':
                    #     wht_type = '2'
                    # elif move.wht_type == '3%':
                    #     wht_type = '3'
                    # elif move.wht_type == '5%':
                    #     wht_type = '5'

                move_ids += str(wht_type) + '|'
                move_ids += str(move.amount_before_tax) + '|'
                move_ids += str(move.credit) + '|'

                if inv_row != len(move_line_ids):
                    move_ids += '1' + "\r\n"
                else:
                    move_ids += '1'

                # worksheet.write(inv_row, 0, move_ids, for_left)
                final_text = final_text_body + str(move_ids)

                inv_row += 1

        # -------------------------------------- PND 53 ----------------------------------------
        elif self.report_type == 'company':
            move_line_ids = self.env['account.move.line'].search(
                [('date_maturity', '>=', self.date_from), ('date_maturity', '<=', self.date_to),
                 ('wht_type.name', '=', 'company'), ('wht_tax', '!=', False), ('account_id.wht', '=', True)],
                order='date_maturity,wht_reference ASC')
            move_ids = ""
            inv_row = 1
            for move in move_line_ids:
                move_ids += str(inv_row) + '|'
                if move.tax_onetime:
                    move_ids += str(move.tax_onetime) + '|'
                elif not move.name_onetime:
                    if move.partner_id.is_onetime:
                        move_ids += str(move.tax_onetime) + '|'
                    elif not move.partner_id.is_onetime:
                        move_ids += str(move.partner_id.vat) + '|'

                if move.name_onetime:
                    name_temp = move.name_onetime.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                elif not move.name_onetime:
                    name_temp = move.name_onetime.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                elif move.partner_id.title:
                    title_name = move.partner_id.title.name
                    name_temp = move.partner_id.name.split(' ')
                    first_name = name_temp[0]
                    last_name = " ".join(name_temp[1:])
                    # last_name = name_temp[1:]
                else:
                    name_temp = move.partner_id.name.split(' ')
                    # name = " ".join(name_temp[1:])

                    if len(name_temp) >= 3:
                        title_name = name_temp[0]
                        first_name = name_temp[1]
                        last_name = name_temp[2]
                    elif len(name_temp) == 2:
                        title_name = name_temp[0]
                        first_name = name_temp[1]
                        last_name = " "
                    else:
                        title_name = " "
                        first_name = name_temp[0]
                        last_name = " "

                move_ids += str(title_name) + '|'
                move_ids += str(first_name) + '|'
                move_ids += str(last_name) + '|'

                address = self.get_partner_full_address_text(move.partner_id)
                address_text = ' '.join(address)
                move_ids += address_text[0:30] + '|'


                # if move.partner_id.street:
                #     move_ids += str(move.partner_id.street)[0:30]
                #     move_ids += str(move.partner_id.street2)[0:30]
                #     move_ids += str(move.partner_id.city)[0:30]
                #     move_ids += str(move.partner_id.state_id.name)[0:40]
                #     move_ids += str(move.partner_id.zip)[0:5] + '|'
                # else:
                #     move_ids += '|'
                # else:
                #     move_ids += '|'
                # if move.partner_id.street2:
                #     move_ids += str(move.partner_id.street2)[0:30]
                # else:
                #     move_ids += '|'
                # if move.partner_id.city:
                #     move_ids += str(move.partner_id.city)[0:30]
                # else:
                #     move_ids += '|'
                # if move.partner_id.state_id and move.partner_id.state_id.name:
                #     move_ids += str(move.partner_id.state_id.name)[0:40]
                # else:
                #     move_ids += '|'
                # if move.partner_id.zip:
                #     move_ids += str(move.partner_id.zip)[0:5] + '|'
                # else:
                #     move_ids += '|'

                if move.date_maturity:
                    # date = datetime.strptime(move.date_maturity, "%Y-%m-%d").date()
                    date = move.date_maturity
                    if len(str(date.day)) < 2:
                        day = '0' + str(date.day)
                    else:
                        day = str(date.day)
                    if len(str(date.month)) < 2:
                        month = '0' + str(date.month)
                    else:
                        month = str(date.month)
                    date_payment = day + '/' + month + '/' + str(date.year + 543)
                if date_payment:
                    move_ids += date_payment + '|'
                else:
                    move_ids += '|'
                # move_ids += strToDate(move.date_maturity).strftime("%d/%m/%Y") + '|'
                move_ids += str(move.name) + '|'

                if move.wht_type:
                    wht_type = str(move.wht_tax.amount)[0]
                    # if str(move.wht_tax.amount) == '1%':
                    #     wht_type = '1'
                    # elif move.wht_type == '2%':
                    #     wht_type = '2'
                    # elif move.wht_type == '3%':
                    #     wht_type = '3'
                    # elif move.wht_type == '5%':
                    #     wht_type = '5'

                move_ids += str(wht_type) + '|'
                move_ids += str(move.amount_before_tax) + '|'
                move_ids += str(move.credit) + '|'

                if inv_row != len(move_line_ids):
                    move_ids += '1' + "\r\n"
                else:
                    move_ids += '1'

                # worksheet.write(inv_row, 0, move_ids, for_left)
                final_text = final_text_body + str(move_ids)

                inv_row += 1

        # ------------------------------------ End PND 53 -------------------------------------------------

        else:
            raise UserError(_('There is record this date range.'))
        if not final_text:
            raise UserError(_('There is record this date range.'))

        values = {
            'name': "Witholding Report.txt",
            'res_model': 'ir.ui.view',
            'res_id': False,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode((final_text).encode("utf-8")),
        }
        attachment_id = self.env['ir.attachment'].sudo().create(values)
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        # '/web/content/' + attachment.id + '?download=true'

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

