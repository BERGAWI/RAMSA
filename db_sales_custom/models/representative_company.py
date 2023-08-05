# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RepresentativeCompany(models.Model):
    _name = "representative.company"

    name = fields.Char(string='اﻻسم', required=True)
    mobile_number = fields.Char(string='رقم الهاتف')

    @api.constrains('mobile_number')
    def _mobile_number_constraints(self):
        if self.mobile_number and len(self.mobile_number) != 10:
            raise ValidationError(_('Mobile Number Must be just 10 Digits'))

