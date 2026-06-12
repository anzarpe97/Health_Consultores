from odoo import models, fields, api, _


class LibroDiarioWizard(models.TransientModel):
    _name = "libro.diario.wizard"
    _description = "Wizard para Libro Diario Legal"

    date_from = fields.Date(string="Fecha Inicio", required=True)
    date_to = fields.Date(string="Fecha Fin", required=True)
    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
    )

    def print_report(self):
        data = {
            "date_from": self.date_from,
            "date_to": self.date_to,
            "company_id": self.company_id.id,
        }
        return self.env.ref(
            "libro_diario.action_report_libro_diario_legal"
        ).report_action(self, data=data)
