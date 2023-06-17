from odoo import fields, models

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

    active = fields.Boolean()

    state = fields.Selection(
        default="New",
        selection=[('New', 'New'),
                   ('Offer Received', 'Offer Received'),
                   ('Offer Accepted', 'Offer Accepted'),
                   ('Sold', 'Sold'),
                   ('Canceled', 'Canceled')]
    )
