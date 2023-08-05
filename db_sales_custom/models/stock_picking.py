# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tests import Form


class StockPicking(models.Model):
    _inherit = "stock.picking"

    total_demand_qty = fields.Float(string='إجمالى الكميات المطلوبه', compute='_compute_total_qty')
    total_done_qty = fields.Float(string='إجمالى الكميات المستلمه', compute='_compute_total_qty')
    total_lines = fields.Float(string='عدد اﻻصناف', compute='_compute_total_qty')

    @api.depends('move_ids_without_package')
    def _compute_total_qty(self):
        for rec in self:
            total_lines = total_done_qty = total_demand_qty = 0.0
            if rec.move_ids_without_package:
                total_demand_qty = sum(rec.move_ids_without_package.mapped('product_uom_qty'))
                total_done_qty = sum(rec.move_ids_without_package.mapped('quantity_done'))
                total_lines = len(rec.move_ids_without_package)

            rec.total_demand_qty = total_demand_qty
            rec.total_done_qty = total_done_qty
            rec.total_lines = total_lines
