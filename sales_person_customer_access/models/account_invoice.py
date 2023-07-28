# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.move"

    salesperson_ids = fields.Many2many(
        'res.users',
        string="Authorized persons"
    )
