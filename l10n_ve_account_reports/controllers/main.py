from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        import odoo
        import os
        module_path = odoo.modules.get_module_path('account_reports')
        target_file = os.path.join(module_path, 'models', 'account_report.py')
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            content = str(e)
            
        return request.make_response(
            content,
            headers=[('Content-Type', 'text/plain')]
        )
