# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tests import Form


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_available_qty = fields.Float(
        string="الكميه المتاحه",
        compute='_compute_product_available_qty', )

    @api.depends('product_id')
    def _compute_product_available_qty(self):
        for rec in self:
            product_available_qty = 0.0
            if rec.product_id:
                product_available_qty = sum(self.env['stock.quant'].search([('warehouse_id', '=', rec.warehouse_id.id),
                                                                            ('product_id', '=',
                                                                             rec.product_id.id), ]).mapped(
                    'available_quantity'))
            rec.product_available_qty = product_available_qty


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    total_qty = fields.Float(string='إجمالى الكميات', compute='_compute_total_qty')
    total_lines = fields.Float(string='عدد اﻻصناف', compute='_compute_total_qty')


    @api.depends('order_line')
    def _compute_total_qty(self):
        for rec in self:
            total_lines = total_qty = 0.0
            if rec.order_line:
                total_qty = sum(rec.order_line.mapped('product_qty'))
                total_lines = len(rec.order_line)
            rec.total_qty = total_qty
            rec.total_lines = total_lines