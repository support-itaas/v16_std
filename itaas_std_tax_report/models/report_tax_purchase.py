# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime,timedelta,date

from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT



class report_sale_tax_report(models.AbstractModel):
    _name = 'report.itaas_std_tax_report.purchase_tax_report_id'


    def _get_result_purchase_tax(self,data):
        print('_get_result_purchase_tax')
        doc = []
        # Case ปรกติ ====================================================ิ
        if 'operating_unit' in data and data['operating_unit']:
            print('CASE_1_OU')
            domain = [('account_id.purchase_tax_report', '=', True),
                      ('tax_inv_date', '>=', data['date_from']),
                      ('tax_inv_date', '<=', data['date_to']),
                      ('move_id.state', 'in', ('posted', 'cancel')),
                      ('date_maturity', '=', False),
                      ('move_id.move_type', 'in', ('in_invoice', 'in_refund', 'entry')),
                      ('operating_unit_id', 'in', data['operating_unit'])]
        else:
            print('CASE_1_NOT_OU')
            domain = [('account_id.purchase_tax_report', '=', True),
                      ('tax_inv_date', '>=', data['date_from']),
                      ('tax_inv_date', '<=', data['date_to']),
                      ('move_id.state', 'in', ('posted', 'cancel')),
                      ('date_maturity', '=', False),
                      ('move_id.move_type', 'in', ('in_invoice', 'in_refund', 'entry'))]

        if data['vat_0'] == True:
            print('Case_vat_0')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 0),
                                                  ('type_tax_use', '=', 'purchase')])
            print('tax:', tax)
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids and x.debit == 0 and x.credit == 0):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)
                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)
        elif data['vat_7'] == True:
            print('Case_vat_7')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 7.0000),
                                                  ('type_tax_use', '=', 'purchase')])
            print('tax:', tax)
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)
        else:
            print('Case_vat_all')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('type_tax_use', '=', 'purchase')])
            print('tax:', tax)
            account_ids = tax[0].invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            print('docs:', docs)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)
                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)


        # Case ข้ามเดือน ===================================================
        if 'operating_unit' in data and data['operating_unit']:
            print('CASE_2_OU')
            domain = [('account_id.purchase_tax_report', '=', True),
                      ('date_maturity', '>=', data['date_from']),
                      ('date_maturity', '<=', data['date_to']),
                      ('move_id.state', '=', 'posted'),
                      ('date_maturity', '!=', False),
                      ('is_special_tax', '=', False),
                      ('operating_unit_id', 'in', data['operating_unit'])]
        else:
            print('CASE_2_NOT_OU')
            domain = [('account_id.purchase_tax_report', '=', True),
                      ('date_maturity', '>=', data['date_from']),
                      ('date_maturity', '<=', data['date_to']),
                      ('move_id.state', '=', 'posted'),
                      ('date_maturity', '!=', False),
                      ('is_special_tax', '=', False)]
        if data['vat_0'] == True:
            print('Case_vat_0')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 0),
                                                  ('type_tax_use', '=', 'purchase')])
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date

                if not date_t2:
                    raise UserError(_("Please check date for item %s" % move_line_id.move_id.name))
                if move_line_id.ref_new:
                    ref = move_line_id.ref_new
                else:
                    ref = move_line_id.ref

                if not ref:
                    raise UserError(_("Please check ref for item %s" % move_line_id.move_id.name))
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,

                }
                doc.append(move_line_ids)
        elif data['vat_7'] == True:
            print('Case_vat_7')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 7.0000),
                                                  ('type_tax_use', '=', 'purchase')])
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids):
                print('move_line_id:', move_line_id.id)
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)
                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)
        else:
            print('Case_vat_all')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('type_tax_use', '=', 'purchase')])
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs.filtered(lambda x: x.account_id in account_ids):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)

        #Case กลับรายการ ===================================================
        if 'operating_unit' in data and data['operating_unit']:
            print('CASE_2_OU')
            domain = [('account_id.purchase_tax_report', '=',True),
                      ('tax_inv_date', '>=', data['date_from']),
                      ('tax_inv_date', '<=', data['date_to']),
                      ('move_id.state', 'in', ('posted','cancel')),
                      ('date_maturity', '=', False),
                      ('tax_line_id.type_tax_use','=','purchase'),
                      ('is_special_tax', '=', True),
                      ('operating_unit_id', 'in', data['operating_unit'])
                      ]
        else:
            print('CASE_2_NOT_OU')
            domain = [('account_id.purchase_tax_report', '=',True),
                      ('tax_inv_date', '>=', data['date_from']),
                      ('tax_inv_date', '<=', data['date_to']),
                      ('move_id.state', 'in', ('posted','cancel')),
                      ('date_maturity', '=', False),
                      ('tax_line_id.type_tax_use','=','purchase'),
                      ('is_special_tax', '=', True)]

        if data['vat_0'] == True:
            print('Case_vat_0')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 0),
                                                  ('type_tax_use', '=', 'purchase')])
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            print('docs_specail:', docs)
            for move_line_id in docs.filtered(lambda x: x.tax_line_id.amount == 0):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)
                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,
                }
                doc.append(move_line_ids)
        elif data['vat_7'] == True:
            print('Case_vat_7')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('amount', '=', 7.0000),
                                                  ('type_tax_use', '=', 'purchase')])
            print('tax:', tax)
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            print('docs_specail:', docs)
            for move_line_id in docs.filtered(lambda x: x.tax_line_id.amount == 0):
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date


                ref = move_line_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,

                }
                doc.append(move_line_ids)
        else:
            print('Case_vat_all')
            tax = self.env['account.tax'].search([('tax_report', '=', True),
                                                  ('type_tax_use', '=', 'purchase')])
            account_ids = tax.invoice_repartition_line_ids.filtered(lambda x: x.account_id).mapped('account_id')
            docs = self.env['account.move.line'].search(domain)
            for move_line_id in docs:
                if move_line_id.date_vat_new:
                    date_t2 = move_line_id.date_vat_new
                else:
                    date_t2 = move_line_id.tax_inv_date
                ref = move_line_id.move_id.ref
                if move_line_id.move_id.move_type == 'in_refund':
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount * (-1)
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax * (-1)
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7) * (-1)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit * (-1)
                    else:
                        amount_tax = move_line_id.credit * (-1)
                else:
                    if move_line_id.tax_base_amount:
                        amount_untaxed = move_line_id.tax_base_amount
                    elif move_line_id.amount_before_tax:
                        amount_untaxed = move_line_id.amount_before_tax
                    else:
                        amount_untaxed = abs(move_line_id.balance) * (100 / 7)

                    if move_line_id.debit:
                        amount_tax = move_line_id.debit
                    else:
                        amount_tax = move_line_id.credit
                amount_total = amount_untaxed + amount_tax
                move_line_ids = {
                    'date': date_t2,
                    'ref': ref,
                    'partner': move_line_id.partner_id,
                    'vat': move_line_id.partner_id.vat,
                    'branch': move_line_id.partner_id.branch_no,
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_total,
                    'debit': move_line_id.debit,
                    'credit': move_line_id.credit,
                    'note': move_line_id.move_id.name,
                    'type': move_line_id.move_id.move_type,
                    'move_id': move_line_id.move_id,
                    'state': move_line_id.move_id.state,

                }
                doc.append(move_line_ids)
        if doc:
            doc.sort(key=lambda k: (k['date'], k['ref']), reverse=False)
        return doc

    @api.model
    def _get_report_values(self, docids, data=None):
        print('_get_report_values_sale')
        company_id = self.env.company
        result = self._get_result_purchase_tax(data)
        print('result_result',result)

        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': result,
            'company_id': company_id,
            'data': data,
        }
