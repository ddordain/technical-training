from odoo import models, Command

class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        action_sold_override = super().action_sold()

        for record in self:
            six_percent = record.selling_price * 0.06
            administrative_fees = 100.00
            
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': "6% of the selling price",
                        'quantity': 1,
                        'price_unit': six_percent,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': administrative_fees,
                    }),
                ],
            })

        return action_sold_override

