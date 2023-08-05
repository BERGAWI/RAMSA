# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_price = fields.Float(groups="db_sales_custom.group_access_product_cost", )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(groups="db_sales_custom.group_access_product_cost", )
