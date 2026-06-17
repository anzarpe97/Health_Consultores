from odoo import api
from odoo.exceptions import UserError

def post_init_hook(env):
    view = env.ref('account_reports.pdf_export_main', raise_if_not_found=False)
    if view:
        xml_content = view.arch_db
        raise UserError(f"XML_DE_LA_PLANTILLA:\n{xml_content}")
    else:
        raise UserError("La plantilla no se encontro")
