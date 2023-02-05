# -*- coding: utf-8 -*- 

import datetime

from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    sale_order_ids = fields.Many2many('sale.order',compute='_compute_sale_order_ids')

    @api.depends('mrp_production_request_ids')
    def _compute_sale_order_ids(self):
        for each in self:
            each.sale_order_ids = each.mrp_production_request_ids.mapped("sale_id")



