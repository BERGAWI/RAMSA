# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_address = fields.Char(string='Address')
    mobile_number = fields.Char(string='Mobile Number')
    sales_representative_id = fields.Many2one('sale.representative', string='Sales Representative')

    total_qty = fields.Float(string='إجمالى الكميات', compute='_compute_total_qty')
    total_lines = fields.Float(string='عدد اﻻصناف', compute='_compute_total_qty')

    @api.depends('invoice_line_ids')
    def _compute_total_qty(self):
        for rec in self:
            total_qty = total_lines = 0.0
            if rec.invoice_line_ids:
                total_qty = sum(rec.invoice_line_ids.mapped('quantity'))
                total_lines = len(rec.invoice_line_ids)
            rec.total_qty = total_qty
            rec.total_lines = total_lines
