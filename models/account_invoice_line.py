# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    amount_tax = fields.Monetary(
        compute='_get_amount_tax',
    )
    amount_total = fields.Monetary(
        compute='_get_amount_total',
    )
    amount_discounted = fields.Monetary(
        compute='_get_amount_discounted',
    )

    @api.depends('invoice_line_tax_ids', 'price_subtotal')
    def _get_amount_tax(self):
        for record in self:
            record.amount_tax = sum(record.invoice_line_tax_ids.mapped('amount')) / 100 * record.price_subtotal

    @api.depends('amount_tax', 'price_subtotal')
    def _get_amount_total(self):
        for record in self:
            record.amount_total = record.price_subtotal + record.amount_tax

    @api.depends('discount', 'price_unit', 'quantity')
    def _get_amount_discounted(self):
        for record in self:
            record.amount_discounted = record.discount / 100 * record.price_unit * record.quantity
