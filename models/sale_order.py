# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    production_request_ids = fields.One2many('mrp.production.request', 'sale_id', string='Production Requests')
    production_request_ids_count = fields.Integer(compute='_compute_production_request_ids')
    can_create_production_request = fields.Boolean(compute='_can_create_production_request')

    @api.depends('state','order_line')
    def _can_create_production_request(self):
        for each in self:
            each.can_create_production_request = any(ol.can_create_production_request for ol in each.order_line)

    @api.depends('production_request_ids')
    def _compute_production_request_ids(self):
        for each in self:
            each.production_request_ids_count = len(each.production_request_ids)

    def _prepare_production_request_items(self):
        self.ensure_one()
        production_lines = []
        for line in self.order_line.filtered(lambda l:l.can_create_production_request):
            production_lines.append((0,0,{
                'product_id':line.product_id.id,
                'quantity':line.qty_to_plan,
                'quantity_to_do':line.qty_to_plan,
                'product_uom_id':line.product_uom.id,
                'sale_line_id':line.id,
            }))
        return production_lines

    def action_create_production_requests(self):
        new_wizard = self.env['production.requests.create'].create({
            'item_ids':self._prepare_production_request_items()
        })
        view_id = self.env.ref('sale_mrp_production_request.view_production_requests_create').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Production Requests'),
            'view_mode': 'form',
            'res_model': 'production.requests.create',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    def show_related_production_requests(self):
        self.ensure_one()
        domain = [('sale_id', 'in', self.ids)]
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









