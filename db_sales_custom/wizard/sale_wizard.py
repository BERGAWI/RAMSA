# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime
import xlsxwriter
import base64
import io
from io import BytesIO
import tempfile
import csv
from io import StringIO


class Sales(models.TransientModel):
    _name = "emp.sale.report"

    item_ids = fields.Many2many('sale.order')

    @api.model
    def default_get(self, fields_list):
        res = super(Sales, self).default_get(fields_list)
        request_line_obj = self.env['sale.order']
        request_line_ids = self.env.context.get('active_ids', False)
        active_model = self.env.context.get('active_model', False)
        if not request_line_ids:
            return res
        assert active_model == 'sale.order', \
            'Bad context propagation'
        request_lines = request_line_obj.browse(request_line_ids)
        res['item_ids'] = request_lines
        return res

    def print_sales(self):
        return self.env.ref('db_sales_custom.action_report_export_sale_order').report_action(self)

