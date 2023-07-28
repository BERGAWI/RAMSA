# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class ShResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields):
        rec = super(ShResUsers, self).default_get(fields)

        journals = self.env.company.journal_ids.ids
        rec.update({
            'journal_ids' : [(6,0,journals)]
        })
        return rec

    journal_ids = fields.Many2many(
        'account.journal', string="Journals", copy=False)