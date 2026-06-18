from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        views = request.env['ir.ui.view'].sudo().search_read(
            [('key', 'ilike', 'company_information')],
            ['key', 'name', 'type', 'arch']
        )
        if not views:
            views = request.env['ir.ui.view'].sudo().search_read(
                [('arch', 'ilike', 'company_information')],
                ['key', 'name', 'type', 'arch']
            )
            
        import json
        return request.make_response(
            json.dumps(views, indent=4),
            headers=[('Content-Type', 'application/json')]
        )
