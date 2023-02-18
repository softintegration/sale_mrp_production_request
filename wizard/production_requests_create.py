# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class ProductionRequestsCreate(models.TransientModel):
    _name = 'production.requests.create'

    check_all = fields.Boolean(string='Check all',default=False)
    item_ids = fields.One2many('production.requests.create.item','request_id')

    @api.onchange('check_all')
    def _onchange_check_all(self):
        for item in self.item_ids:
            item.checked = self.check_all


    def apply(self):
        if len(self.item_ids.filtered(lambda it:it.checked)) == 0:
            raise ValidationError(_("At least one line must be selected!"))
        production_requests_dict_list = []
        for item in self.item_ids.filtered(lambda it:it.checked):
            if float_compare(item.quantity_to_do,0.0, precision_rounding=item.product_uom_id.rounding) <=0:
                raise ValidationError(_('Quantity to do must be positive!'))
            if float_compare(item.quantity_to_do,item.sale_line_id.qty_to_plan, precision_rounding=item.product_uom_id.rounding) >0:
                raise ValidationError(_('Quantity to do must be less than or equal to Quantity to plan!'))
            if not item.date_desired:
                raise ValidationError(_('Desired Date is required!'))
            production_requests_dict_list.append(self._prepare_production_request(item))
        return self._create_production_request(production_requests_dict_list)

    def _create_production_request(self,production_requests_dict_list):
        production_requests = self.env['mrp.production.request'].create(production_requests_dict_list)
        # TODO:we have to check again if this is good approach
        for req in production_requests:
            req._onchange_product_id()
        production_requests.action_make_waiting()


    def _prepare_production_request(self,item):
        return {
            'product_id':item.product_id.id,
            'product_uom_id':item.product_uom_id.id,
            'date_request':fields.Datetime.now(),
            'date_desired':item.date_desired,
            'quantity':item.quantity_to_do,
            'sale_line_id':item.sale_line_id.id,
            'sale_id':item.sale_line_id.order_id.id,
            'origin':item.sale_line_id.order_id.name
        }




class ProductionRequestsCreateItem(models.TransientModel):
    _name = 'production.requests.create.item'

    checked = fields.Boolean(string='Check',default=False)
    request_id = fields.Many2one('production.requests.create')
    product_id = fields.Many2one('product.product',string='Product',required=True)
    quantity = fields.Float(string="Quantity to plan", digits='Product Unit of Measure')
    quantity_to_do = fields.Float(string="Quantity to do", digits='Product Unit of Measure', requied=True)
    product_uom_id = fields.Many2one('uom.uom', 'Product Unit of Measure',required=True)
    date_desired = fields.Datetime('Desired Date')
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line', required=True)
