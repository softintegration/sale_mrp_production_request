# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpProductionRequest(models.Model):
    _inherit = 'mrp.production.request'

    sale_id = fields.Many2one('sale.order','Sales order',index=True)
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Line', index=True)
    partner_id = fields.Many2one('res.partner', string='Customer',related='sale_id.partner_id',readonly=True,store=True,index=True)
    client_order_ref = fields.Char(string='Customer Reference', related='sale_id.client_order_ref',readonly=True)

    def _prepare_mrp_production(self, quantity=False, product_uom_id=False):
        res = super(MrpProductionRequest,self)._prepare_mrp_production(quantity=quantity,product_uom_id=product_uom_id)
        if not self._module_si_sale_mrp_installed():
            return res
        # In the case of si_sale_mrp is installed,we have to set the necessary links between source Sale orders and created Production
        # TODO: is this rule correct? we have to check later
        # all the generated manufacturing orders must be for the same partner
        partner_id = self.mapped("partner_id")
        if len(partner_id) > 1:
            raise ValidationError(_("Can not create Manufacturing order for different partners!"))
        res.update({
                'partner_id': self.partner_id and self.partner_id.id
            })
        return res

    @api.model
    def _module_si_sale_mrp_installed(self):
        "This method return True if the si_sale_mrp module is installed"
        return 'si_sale_mrp' in self.env['ir.module.module']._installed().keys()


        
        