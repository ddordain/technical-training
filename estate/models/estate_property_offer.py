from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be strictly positive"),
    ]
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    create_date = fields.Date(default=lambda self: fields.Datetime.today())
    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        if self.status == 'accepted':
            return True

        #the & is optional it's the behavior by default
        offer_already_accepted = self.env['estate.property.offer'].search([
            '&',
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ]) 
        if offer_already_accepted:
            raise UserError("a previous offer has already been accepted") 

        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property type", store=True)

    # override create method to change state property
    # BATCH WARNING 
    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price_new_offer = vals.get('price')
        property = self.env['estate.property'].browse(property_id)
        if property.best_offer is not None:
            if float_compare(property.best_offer,price_new_offer, precision_digits=2) >= 0:
                raise UserError("Price should be higher than previous offers")
        offer = super().create(vals)
        if property.state == 'new':
            property.state = 'offer_received'
        return offer
