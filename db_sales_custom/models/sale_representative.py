# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleRepresentative(models.Model):
    _name = "sale.representative"

    name = fields.Char(string='Name', required=True)
    mobile_number = fields.Char(string='Mobile Number')
    representative_company_id = fields.Many2one('representative.company', string='Company')
    sale_orders_count = fields.Integer(string='Sale Orders', compute='_compute_sale_orders_count')
    sale_ids = fields.One2many('sale.order','sales_representative_id')

    @api.constrains('mobile_number')
    def _mobile_number_constraints(self):
        if self.mobile_number and len(self.mobile_number) != 10:
            raise ValidationError(_('Mobile Number Must be just 10 Digits'))

    def _compute_sale_orders_count(self):
        for rec in self:
            rec.sale_orders_count = self.env['sale.order'].search_count([('sales_representative_id', '=', rec.id)])


    def action_view_sale_orders(self):
        recs = self.mapped('sale_ids')
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        if len(recs) > 1:
            action['domain'] = [('id', 'in', recs.ids)]
        elif len(recs) == 1:
            action['views'] = [(
                self.env.ref('sale.view_order_form').id, 'form'
            )]
            action['res_id'] = recs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

