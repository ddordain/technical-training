from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Tag name must be unique"),
    ]
    _order = "name"



    name = fields.Char(required=True)
    color = fields.Integer()
