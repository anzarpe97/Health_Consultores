# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class DebugController(http.Controller):
    @http.route('/debug/account_reports_info_combined', type='http', auth='public')
    def get_info_combined(self, **kwargs):
        # Render the template to string
        html = request.env['ir.qweb']._render('account_reports.company_information', {
            'options': {'companies': [{'name': 'TEST COMPANY'}]},
            'env': request.env,
            'company': request.env.company,
        })
        return request.make_response(html, headers=[('Content-Type', 'text/html')])
