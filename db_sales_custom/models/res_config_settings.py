# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    so_delivery_location_id = fields.Many2one('stock.location',
                                              string="Default Virtual Delivery Location", )

    so_payment_journal_id = fields.Many2one('account.journal', string="Default Payment Journal", )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_delivery_location_id = fields.Many2one('stock.location',
                                              domain="[('usage', '=', 'customer')]",
                                              string="Default Virtual Delivery Location",
                                              related='company_id.so_delivery_location_id', readonly=False)

    so_payment_journal_id = fields.Many2one('account.journal',
                                            domain="[('type', 'in', ('bank','cash'))]",
                                            string="Default Payment Journal",
                                            related='company_id.so_payment_journal_id', readonly=False)
