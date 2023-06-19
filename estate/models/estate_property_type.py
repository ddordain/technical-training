from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type" # . translated in _ in postgres 
    _description = "Estate property type" 
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Type name must be unique"),
    ]

    name = fields.Char(required=True)
