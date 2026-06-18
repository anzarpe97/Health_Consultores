from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        # Obtener la vista combinada (con todas las herencias aplicadas)
        view = request.env.ref('account_reports.pdf_export_main')
        arch = view.sudo()._get_combined_arch()
        
        return request.make_response(
            arch,
            headers=[('Content-Type', 'text/xml')]
        )
