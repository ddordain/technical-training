from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "Tag name must be unique"),
    ]



    name = fields.Char(required=True)
