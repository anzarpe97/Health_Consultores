from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info', type='http', auth='public')
    def get_info(self, **kwargs):
        # Buscar todas las vistas/plantillas del módulo account_reports
        views = request.env['ir.ui.view'].sudo().search_read(
            [('key', '=like', 'account_reports.%')],
            ['key', 'name', 'type', 'arch']
        )
        
        # Filtrar solo aquellas que parezcan estar relacionadas con PDFs, layouts o headers
        relevant_views = []
        for v in views:
            if 'pdf' in v['key'] or 'print' in v['key'] or 'layout' in v['key'] or 'header' in v['key'] or 'template' in v['key']:
                relevant_views.append(v)
                
        return request.make_response(
            json.dumps(relevant_views, indent=4),
            headers=[('Content-Type', 'application/json')]
        )
