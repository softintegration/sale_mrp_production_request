# -*- coding: utf-8 -*- 

import datetime

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    sale_order_ids = fields.Many2many('sale.order',compute='_compute_sale_order_ids')
    sale_order_line_ids = fields.One2many('mrp.production.sale.order','mrp_production_id',store=True)

    @api.depends('mrp_production_request_ids')
    def _compute_sale_order_ids(self):
        for each in self:
            each.sale_order_ids = each.mrp_production_request_ids.mapped("sale_id")
            if len(each.sale_order_ids) and not each.sale_order_line_ids:
                each.write({'sale_order_line_ids':[(0, 0, {'mrp_production_id': each.id,
                         'sale_order_id': sale_order.id}) for sale_order in
                 each.mrp_production_request_ids.mapped("sale_id")]})




class MrpProductionSaleOrder(models.Model):
    _name = 'mrp.production.sale.order'

    mrp_production_id = fields.Many2one('mrp.production',string='Manufacturing',required=True)
    sale_order_id = fields.Many2one('sale.order',string='name',required=True)
    state = fields.Selection(related='mrp_production_id.state')
    client_order_ref = fields.Char(related='sale_order_id.client_order_ref')
    sequence = fields.Integer(help='Used to order Sale orders', default=10,)
    qty_producing_allocated = fields.Float(string="Allocated Quantity Producing",
        default=0.0, digits='Product Unit of Measure', required=False, tracking=True,readonly=False,
        states={'done': [('readonly', True)],'cancel': [('readonly', True)]})






