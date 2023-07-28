# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    journal_ids = fields.Many2many('account.journal', string="Journals")
    sh_user_ids = fields.Many2many('res.users', string="Users")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    journal_ids = fields.Many2many(
        related='company_id.journal_ids', readonly=False)
    sh_user_ids = fields.Many2many(
        related='company_id.sh_user_ids', readonly=False)
