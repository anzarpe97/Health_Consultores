# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        report = request.env['account.report'].sudo().search([('name', 'ilike', 'Estado de resultados')], limit=1)
        if not report:
            report = request.env['account.report'].sudo().search([('name', 'ilike', 'Profit and loss')], limit=1)
        if not report:
            return request.make_response("Report not found")
            
        options = report.get_options()
        html_data = list(report._get_html_data_for_pdf_export(options))
        
        bodies = html_data[0][0]
        body_str = bodies[0].decode('utf-8') if isinstance(bodies[0], bytes) else bodies[0]
        
        return request.make_response(body_str, headers=[('Content-Type', 'text/html')])
