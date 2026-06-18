from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        from lxml import etree
        # Obtener la vista original (sin herencias) para ver el contenido
        view = request.env.ref('account_reports.company_information')
        
        return request.make_response(
            view.arch,
            headers=[('Content-Type', 'text/xml')]
        )
