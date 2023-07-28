# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.osv import expression

class SaleOrder(models.Model):
    _inherit = "sale.order"

    salesperson_ids = fields.Many2many(
        'res.users',
        string="Authorized persons",
        related="partner_id.salesperson_ids"
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_warning(self):
        super(SaleOrder, self)._onchange_partner_id_warning()
        res = super(SaleOrder, self)._compute_fiscal_position_id()
        if self.partner_id.salesperson_ids:
            self.salesperson_ids=[(6, 0, self.partner_id.salesperson_ids.ids)]
        else:
            self.salesperson_ids=[]


    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        result.update({'salesperson_ids': [(6, 0, self.salesperson_ids.ids)]})
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        super(SaleOrder, self)._name_search(
            name, args=None, operator='ilike', limit=100, name_get_uid=None)

        if (self.env.user.has_group("sales_person_customer_access.group_restricted_customer")):
            domain = [("salesperson_ids", "in", self.env.user.id),('name', 'ilike', name)]
        else:
            domain = [('name', 'ilike', name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    # To apply domain to load menu_________ 1
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        _ = self._context or {}
        if (self.env.user.has_group("sales_person_customer_access.group_restricted_customer")):
            args += [
                ("salesperson_ids", "in", self.env.user.id),
            ]
        return super(SaleOrder, self).search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"


    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        res.update({'salesperson_ids': [(6, 0, sale_orders.salesperson_ids.ids)]})
        return res
