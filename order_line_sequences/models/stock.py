
from odoo import api, fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    sequence_number = fields.Integer(string='#', compute='_compute_sequence_number', help='Line Numbers')

    @api.depends('picking_id')
    def _compute_sequence_number(self):
        """Function to compute line numbers"""
        for ids in self.mapped('picking_id'):
            sequence_number = 1
            for lines in ids.move_ids_without_package:
                lines.sequence_number = sequence_number
                sequence_number += 1
