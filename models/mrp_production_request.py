# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpProductionRequest(models.Model):
    _inherit = 'mrp.production.request'

    sale_id = fields.Many2one('sale.order','Sales order',index=True)
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line', index=True)
    partner_id = fields.Many2one('res.partner', string='Customer',related='sale_id.partner_id',readonly=True,store=True,index=True)
    client_order_ref = fields.Char(string='Customer Reference', related='sale_id.client_order_ref',readonly=True)