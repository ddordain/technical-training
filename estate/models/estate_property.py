from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property" # . translated in _ in postgres 
    _description = "Estate property" 

    name = fields.Char(required=True, default="Unknown") # VARCHAR
    description = fields.Text() # TEXT
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.today(), months=3)) # DATE
    expected_price = fields.Float(required=True) # FLOAT
    selling_price = fields.Float(readonly=True, copy=False) # FLOAT
    bedrooms = fields.Integer(default=2) # INT
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean() # BOOLEAN
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')]
    ) # no equivalent in SQL
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer = fields.Integer(compute='_compute_best_price')

    active = fields.Boolean()

    state = fields.Selection(
        default="New",
        selection=[('New', 'New'),
                   ('Offer Received', 'Offer Received'),
                   ('Offer Accepted', 'Offer Accepted'),
                   ('Sold', 'Sold'),
                   ('Canceled', 'Canceled')])

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tags_id = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many('estate.property.offer',
                                'property_id',
                                string="Offers")

    @api.depends('living_area', 'garden_area') 
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped('price')
            if offer_prices:
                record.best_offer = max(offer_prices)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        if self.state == 'Sold':
            raise UserError("Sold properties cannot be canceled") 
        else:
            self.state = 'Canceled'
        return True

    def action_sold(self):
        if self.state == 'Canceled':
            raise UserError("Canceled properties cannot be sold")
        else:
            self.state = 'Sold'
        return True
