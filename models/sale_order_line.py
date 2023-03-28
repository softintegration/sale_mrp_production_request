# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    production_request_ids = fields.One2many('mrp.production.request', 'sale_line_id', string='Production Requests')
    qty_to_plan = fields.Float(string='Quantity to plan', compute='_compute_qty_to_plan')
    can_create_production_request = fields.Boolean(compute='_can_create_production_request')
    production_request_ids_count = fields.Integer(compute='_compute_production_request_ids')

    @api.depends('production_request_ids')
    def _compute_qty_to_plan(self):
        for each in self:
            planned_quantity,done_planned_quantity,done_quantity_produced = 0,0,0
            if len(each.production_request_ids) > 1 or not isinstance(each.production_request_ids.id, models.NewId):
                planned_quantity = sum(pr.product_uom_id._compute_quantity(pr.quantity, each.product_uom) for pr in
                                       each.production_request_ids.filtered(
                                           lambda pr: pr.state not in ('cancel', 'draft')))
                # we have to calculate the qty that will never be produced in done production_request_ids
                done_planned_quantity = sum(pr.product_uom_id._compute_quantity(pr.quantity, each.product_uom) for pr in
                                       each.production_request_ids.filtered(
                                           lambda pr: pr.state in ('done',)))
                done_quantity_produced = sum(pr.product_uom_id._compute_quantity(pr.quantity_produced, each.product_uom) for pr in
                                       each.production_request_ids.filtered(
                                           lambda pr: pr.state in ('done',)))
            each.qty_to_plan = each.product_uom_qty - planned_quantity +(done_planned_quantity-done_quantity_produced)

    def _can_create_production_request(self):
        for each in self:
            each.can_create_production_request = each.order_id.state in (
            'sale', 'done') and each.product_id.type == 'product' and float_compare(
                each.qty_to_plan, 0.0, precision_rounding=each.product_uom.rounding) > 0

    @api.depends('production_request_ids')
    def _compute_production_request_ids(self):
        for each in self:
            each.production_request_ids_count = len(each.production_request_ids)


    def show_related_production_requests(self):
        self.ensure_one()
        domain = [('sale_line_id', 'in', self.ids)]
        return {
            'name': _('Manufacturing Requests'),
            'view_mode': 'tree,form',
            'views': [(self.env.ref('mrp_production_request.mrp_production_request_tree_view').id, 'tree'),
                      (self.env.ref('mrp_production_request.mrp_production_request_form_view').id, 'form')],
            'res_model': 'mrp.production.request',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {'search_default_my_requests': 1},
        }