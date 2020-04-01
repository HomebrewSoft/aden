# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.invoice'

    rate_id = fields.Many2one(
        comodel_name='res.currency.rate',
        compute='_get_rate_id',
    )

    @api.depends('date_invoice', 'currency_id')
    def _get_rate_id(self):
        for record in self:
            record.rate_id = self.env['res.currency.rate'].search(
                [
                    ('currency_id', '=', record.currency_id.id),
                    ('write_date', '<=', record.date_invoice),
                ],
                order='write_date DESC',
            )
