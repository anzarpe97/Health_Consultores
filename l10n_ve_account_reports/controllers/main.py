# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        import subprocess
        import odoo
        import os
        module_path = odoo.modules.get_module_path('account_reports')
        try:
            res = subprocess.check_output(['grep', '-r', 't-name', os.path.join(module_path, 'static', 'src', 'components')])
            return request.make_response(res.decode('utf-8', errors='ignore'), headers=[('Content-Type', 'text/plain')])
        except Exception as e:
            return request.make_response(str(e))
