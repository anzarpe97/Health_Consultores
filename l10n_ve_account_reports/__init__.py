from odoo import api
from odoo.exceptions import UserError

def post_init_hook(env):
    views = env['ir.model.data'].search([('module', '=', 'account_reports'), ('model', '=', 'ir.ui.view')])
    names = views.mapped('name')
    raise UserError(f"PLANTILLAS DISPONIBLES: {', '.join(names)}")
