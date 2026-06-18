# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        views = request.env['ir.ui.view'].sudo().search_read(
            [('key', '=', 'account_reports.pdf_export_main_table_header')],
            ['arch']
        )
        return request.make_response(views[0]['arch'] if views else 'Not found', headers=[('Content-Type', 'text/plain')])
