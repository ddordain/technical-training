from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type" # . translated in _ in postgres 
    _description = "Estate property type" 
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Type name must be unique"),
    ]
    _order = "sequence, name"

    name = fields.Char(required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id', string= 'Properties')

    sequence = fields.Integer('Sequence', default=1)

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute="_compute_offer_count", store=True)

    # compute on the fly ? why i dont match 
    @api.depends("property_ids", "offer_ids")
    def _compute_offer_count(self):
        offer_list = self.env["estate.property.offer"]
        for record in self:
            record.offer_count = offer_list.search_count([("property_type_id", "=", record.id)])

    def action_show_offers(self):
        action = self.env.ref('estate.action_show_offer').read()[0]
        action['domain'] = [('property_type_id', '=', self.id)]
        return action
