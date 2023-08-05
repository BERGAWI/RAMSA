# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_unit = fields.Float(
        string="سعر المنتج",
        compute='_compute_price_unit',
        digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)

    product_available_qty = fields.Float(
        string="الكميه المتاحه",
        compute='_compute_product_available_qty', )
    can_edit_price = fields.Boolean(compute='_compute_can_edit_price')

    def _compute_can_edit_price(self):
        for rec in self:
            rec.can_edit_price = self.env.user.has_group('db_sales_custom.group_access_unit_price')

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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(
        selection=[
            ('draft', "قيد التجهيز"),
            ('sent', "تم الارسال"),
            ('package', "جملة"),
            ('sale', "قيد التوصيل"),
            ('delivered', "تم التسليم"),
            ('returned', "تم الإرجاع"),
            ('done', "مقفله"),
            ('cancel', "تم الالغاء"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    delivery_address = fields.Char(string='العنوان', required=True)
    mobile_number = fields.Char(string='رقم الهاتف', required=True)
    sales_representative_id = fields.Many2one('sale.representative', string='مندوب توصيل', required=True)
    total_qty = fields.Float(string='إجمالى الكميات', compute='_compute_total_qty')
    total_lines = fields.Float(string='عدد اﻻصناف', compute='_compute_total_qty')
    partner_phone = fields.Char(related='partner_id.phone', string="هاتف العميل")

    @api.depends('order_line')
    def _compute_total_qty(self):
        for rec in self:
            total_qty = total_lines = 0.0
            if rec.order_line:
                total_qty = sum(rec.order_line.mapped('product_uom_qty'))
                total_lines = len(rec.order_line)
            rec.total_qty = total_qty
            rec.total_lines = total_lines

    @api.constrains('mobile_number')
    def _mobile_number_constraints(self):
        if self.mobile_number and len(self.mobile_number) != 10:
            raise ValidationError(_('Mobile Number Must be just 10 Digits'))

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({
            'delivery_address': self.delivery_address,
            'mobile_number': self.mobile_number,
            'sales_representative_id': self.sales_representative_id.id,
        })
        return res

    def action_return_delivery(self):
        # return_picking_vals = {'picking_id': self.picking_ids.ids[0], }
        # return_picking_obj = self.env['stock.return.picking'].with_context(picking_id=self.picking_ids.ids[0],
        #                                                                    active_model='stock.picking', ).create(
        #     return_picking_vals)

        # return_picking_obj._onchange_picking_id()
        # returned_pickings_vals = return_picking_obj.create_returns()
        # returned_pickings = self.env['stock.picking'].browse(returned_pickings_vals['res_id'])
        # returned_pickings.action_set_quantities_to_reservation()
        # returned_pickings.action_assign()
        # returned_pickings._action_done()

        for picking in self.picking_ids:
            picking.action_cancel()
        self.state = 'returned'

    def action_done_all(self):
        self.action_delivery()
        order_invoice = self._create_invoices()
        order_invoice.action_post()
        default_payment_journal = self.company_id.so_payment_journal_id
        payment_register_vals = {'payment_date': order_invoice.date,
                                 'journal_id': default_payment_journal.id, }
        payment_register_obj = self.env['account.payment.register'].with_context(active_ids=order_invoice.ids,
                                                                                 active_model='account.move').create(
            payment_register_vals)
        payment_register_obj._create_payments()
        self.state = 'delivered'

    def action_delivery(self):
        for rec in self:
            for line in rec.order_line:
                if line.product_id.detailed_type == 'product' and line.product_uom_qty > line.product_id.qty_available:
                    raise ValidationError(_('Please Check This Product Qty \'%s\'.') % (line.product_id.name,))
            rec.action_confirm()
            default_location_dest = self.company_id.so_delivery_location_id
            rec.picking_ids.location_dest_id = default_location_dest
            for picking in rec.picking_ids:
                for line in picking.move_ids_without_package:
                    line.quantity_done = line.product_uom_qty
                    line.forecast_availability = line.product_uom_qty
                picking.action_set_quantities_to_reservation()
                picking.action_assign()
                picking._action_done()

    def action_package(self):
        for rec in self:
            rec.state = 'package'
