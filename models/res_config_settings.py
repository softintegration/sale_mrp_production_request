# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    module_stock_picking_reserve_restrict_lot = fields.Boolean("Reserve only Sale order origin lots",
        help="Reserve only the Lot/serials related to the Sale order origin.")

