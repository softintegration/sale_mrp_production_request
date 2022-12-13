# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpProductionRequest(models.Model):
    _inherit = 'mrp.production.request'

    sale_id = fields.Many2one('sale.order','Sales order',index=True)
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line', index=True)
