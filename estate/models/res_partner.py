from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    offer_ids = fields.One2many(
        'estate.property.offer',
        'partner_id',
        string="Offers"
    )
