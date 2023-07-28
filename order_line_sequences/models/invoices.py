from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sequence_number = fields.Integer(string='#', help='Line Numbers', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type') == 'product':
                move = self.env['account.move'].browse(vals.get('move_id'))
                number = move.next_line_number
                vals['sequence_number'] = number
                move.next_line_number += 1
        return super(AccountMoveLine, self).create(vals_list)


class AccountMove(models.Model):
    _inherit = 'account.move'

    next_line_number = fields.Integer(string='#', help='Line Numbers', readonly=True, default=1)

    @api.onchange('invoice_line_ids')
    def _onchange_sequence_number(self):
        """Function to Just Show line numbers incrementing"""
        sequence_number = 1
        for line in self.invoice_line_ids:
            line.sequence_number = sequence_number
            sequence_number += 1
