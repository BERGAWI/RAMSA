# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.osv import expression


class ShAccountJournalRestrict(models.Model):
    _inherit = 'account.journal'

    @api.model
    def default_get(self, fields):
        rec = super(ShAccountJournalRestrict, self).default_get(fields)

        users = self.env.company.sh_user_ids.ids
        rec.update({
            'user_ids': [(6, 0, users)]
        })
        return rec

    user_ids = fields.Many2many(
        'res.users', string="Users", copy=False)

    # To apply domain to action_________ 2
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        super(ShAccountJournalRestrict, self)._name_search(
            name, args=None, operator='ilike', limit=100, name_get_uid=None)

        if(
            self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not
            (self.env.user.has_group("base.group_erp_manager"))
        ):
            domain = [
                ("user_ids", "in", self.env.user.id), ('name', 'ilike', name)
            ]
        else:
            domain = [('name', 'ilike', name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    # To apply domain to load menu_________ 1
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        _ = self._context or {}
        if(
            self.env.user.has_group("sh_journal_restrict.group_journal_restrict_feature") and not
            (self.env.user.has_group("base.group_erp_manager"))
        ):
            args += [
                ("user_ids", "in", self.env.user.id),
            ]
        return super(ShAccountJournalRestrict, self).search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )
