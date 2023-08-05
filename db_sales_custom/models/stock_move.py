# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tests import Form


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_partner_id = fields.Many2one('res.partner', related='picking_id.partner_id')
    picking_source = fields.Char(related='picking_id.origin')

