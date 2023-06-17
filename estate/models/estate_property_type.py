from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type" # . translated in _ in postgres 
    _description = "Estate property type" 

    name = fields.Char(required=True)
