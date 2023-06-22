# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime,timedelta,date

from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT



class report_sale_tax_report(models.AbstractModel):
    _name = 'report.itaas_std_tax_report.sale_tax_report_id'


    def _get_result_sale_tax(self,data):
        domain = [('tax_invoice_date', '>=', data['date_from']),
                  ('tax_invoice_date', '<=', data['date_to']),
                  ('state', 'in', ('posted', 'cancel')),
                  ('move_type', 'in', ('out_invoice', 'out_refund'))]
        docs = self.env['account.move'].search(domain)
        return docs

    def _get_data_sale_tax_filter(self,move_ids,type):
        print('_get_data_sale_tax_filter')
        print('move_ids:',move_ids)
        print('type:',type)
        data_temp = []
        if type == 'vat_0':
            print('vat_0')
            tax_ids = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 0),
                                                  ('type_tax_use', '=', 'sale')])
            for move_id in move_ids:
                for tax_id in tax_ids:
                    if move_id.invoice_line_ids.filtered(lambda a: a.tax_ids.id == tax_id.id):
                        date = move_id.tax_invoice_date
                        if move_id.currency_id.id == self.env.user.company_id.currency_id.id:
                            amount_untaxed = move_id.amount_untaxed
                            amount_tax = move_id.amount_tax
                            amount_total = move_id.amount_total
                            untaxed_amount_after_discount = move_id.amount_untaxed
                        else:
                            rate = self.env['res.currency.rate'].search(
                                [('name', '<=', move_id.invoice_date), ('company_id', '=', self.env.company.id)], limit=1)
                            print('rate:', rate)
                            rate = rate.rate
                            amount_untaxed = move_id.amount_untaxed / rate
                            amount_tax = move_id.amount_tax / rate
                            amount_total = move_id.amount_total / rate
                            untaxed_amount_after_discount = move_id.amount_untaxed / rate
                        move_ids = {
                            'date': date.strftime("%d/%m/%Y"),
                            'name': move_id.tax_inv_number or move_id.name,
                            'partner': move_id.partner_id.name,
                            'untaxed_amount_after_discount': untaxed_amount_after_discount,
                            'vat': move_id.partner_id.vat,
                            'branch': move_id.partner_id.branch_no,
                            'amount_untaxed': amount_untaxed,
                            'amount_tax': amount_tax,
                            'amount_total': amount_total,
                            'move_id': move_id,
                            'state': move_id.state,
                            'type': move_id.move_type,
                            'invoice_line': move_id.invoice_line_ids,
                        }
                        data_temp.append(move_ids)
        elif type == 'vat_7':
            print('vat_7')
            tax_ids = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 7),
                                                  ('type_tax_use', '=', 'sale')])
            for move_id in move_ids:
                for tax_id in tax_ids:
                    if move_id.invoice_line_ids.filtered(lambda a: a.tax_ids.id == tax_id.id):
                        date = move_id.tax_invoice_date
                        if move_id.currency_id.id == self.env.user.company_id.currency_id.id:
                            amount_untaxed = move_id.amount_untaxed
                            amount_tax = move_id.amount_tax
                            amount_total = move_id.amount_total
                            untaxed_amount_after_discount = move_id.amount_untaxed
                        else:
                            rate = self.env['res.currency.rate'].search(
                                [('name', '<=', move_id.invoice_date),
                                 ('company_id', '=', self.env.company.id)], limit=1)
                            rate = rate.rate
                            amount_untaxed = move_id.amount_untaxed / rate
                            amount_tax = move_id.amount_tax / rate
                            amount_total = move_id.amount_total / rate
                            untaxed_amount_after_discount = move_id.amount_untaxed / rate
                        move_ids = {
                            'date': date.strftime("%d/%m/%Y"),
                            'name': move_id.tax_inv_number or move_id.name,
                            'partner': move_id.partner_id.name,
                            'untaxed_amount_after_discount': untaxed_amount_after_discount,
                            'vat': move_id.partner_id.vat,
                            'branch': move_id.partner_id.branch_no,
                            'amount_untaxed': amount_untaxed,
                            'amount_tax': amount_tax,
                            'amount_total': amount_total,
                            'move_id': move_id,
                            'state': move_id.state,
                            'type': move_id.move_type,
                            'invoice_line': move_id.invoice_line_ids,
                        }
                        data_temp.append(move_ids)
        else:
            print('vat_all')
            for move_id in move_ids:
                date = move_id.tax_invoice_date
                if move_id.currency_id.id == self.env.user.company_id.currency_id.id:
                    amount_untaxed = move_id.amount_untaxed
                    amount_tax = move_id.amount_tax
                    amount_total = move_id.amount_total
                    untaxed_amount_after_discount = move_id.amount_untaxed
                else:
                    rate = self.env['res.currency.rate'].search([('name', '<=', move_id.invoice_date), ('company_id', '=', self.env.company.id)], limit=1)
                    rate = rate.rate
                    print('rate:', rate)
                    amount_untaxed = move_id.amount_untaxed / rate
                    amount_tax = move_id.amount_tax / rate
                    amount_total = move_id.amount_total / rate
                    untaxed_amount_after_discount = move_id.amount_untaxed / rate
                move_ids = {
                    'date': date.strftime("%d/%m/%Y"),
                    'name': move_id.tax_inv_number or move_id.name,
                    'partner': move_id.partner_id.name,
                    'untaxed_amount_after_discount': untaxed_amount_after_discount,
                    'vat': move_id.partner_id.vat,
                    'branch': move_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'move_id': move_id,
                    'state': move_id.state,
                    'type': move_id.move_type,
                    'invoice_line': move_id.invoice_line_ids,
                }
                data_temp.append(move_ids)
        return data_temp

    @api.model
    def _get_report_values(self, docids, data=None):
        print('_get_report_values_sale')
        print('Data:',data)
        data_result = []
        company_id = self.env.company
        if 'operating_unit' in data and data['operating_unit']:
            print('Case Ou')
        else:
            print('Case Not Ou')
            result = self._get_result_sale_tax(data)
            if 'vat_0' in data and data['vat_0']:
                is_vat = 'vat_0'
                print('Case_vat_0_sale')
                data_result = self._get_data_sale_tax_filter(result,is_vat)
            elif 'vat_7' in data and data['vat_7']:
                is_vat = 'vat_7'
                print('Case_vat_7_sale')
                data_result = self._get_data_sale_tax_filter(result,is_vat)
            else:
                print('Case_all_vat_sale')
                is_vat = 'vat_all'
                data_result = self._get_data_sale_tax_filter(result,is_vat)
        if not data_result:
            raise UserError(_('Document is empty.'))
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': data_result,
            'company_id': company_id,
            'data': data,
        }
