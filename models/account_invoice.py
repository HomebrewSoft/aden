# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.invoice'

    amount_total_crc = fields.Monetary(
        currency_field='currency_id',
        compute='_get_amount_total_crc',
    )
    amount_discounted = fields.Monetary(
        currency_field='currency_id',
        compute='_get_amount_discounted',
    )
    amount_subtotal = fields.Monetary(
        currency_field='currency_id',
        compute='_get_amount_subtotal',
    )

    @api.depends('amount_total', 'currency_id')
    def _get_amount_total_crc(self):
        for record in self:
            currency_id = record.currency_id.with_context(date=record.date_invoice)
            record.amount_total_crc = currency_id.compute(record.amount_total, record.company_id.currency_id)

    @api.depends('invoice_line_ids')
    def _get_amount_discounted(self):
        for record in self:
            record.amount_discounted = sum(record.invoice_line_ids.mapped('amount_discounted'))

    @api.depends('amount_untaxed', 'amount_discounted')
    def _get_amount_subtotal(self):
        for record in self:
            record.amount_subtotal = record.amount_untaxed + record.amount_discounted
