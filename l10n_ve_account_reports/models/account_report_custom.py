# -*- coding: utf-8 -*-
from odoo import models, api, _

class AccountReport(models.Model):
    _inherit = 'account.report'

    def get_report_information(self, options):
        """Inyectar el nuevo botón PDF Personalizado en las opciones del reporte"""
        res = super().get_report_information(options)
        if 'options' in res and 'buttons' in res['options']:
            # Agregamos el botón
            res['options']['buttons'].append({
                'name': 'PDF Personalizado',
                'sequence': 15,
                'action': 'export_custom_pdf',
                'file_export_type': _('PDF')
            })
            # Ordenamos por secuencia
            res['options']['buttons'] = sorted(res['options']['buttons'], key=lambda x: x.get('sequence', 100))
        return res

    def export_custom_pdf(self, options):
        """Acción que se ejecuta al presionar el botón PDF Personalizado"""
        # Obtenemos la acción estándar de exportar a PDF
        action = self.export_to_pdf(options)
        
        # Le inyectamos una variable en 'options' para saber que es el personalizado.
        if isinstance(action, dict) and 'data' in action and 'options' in action['data']:
            action['data']['options']['custom_pdf_header'] = True
            
        return action

    def get_html(self, options):
        """Sobrescribimos get_html para inyectar nuestro membrete en el HTML antes de generar el PDF"""
        html = super().get_html(options)
        
        # Solo inyectamos si viene de nuestro botón personalizado
        if options.get('custom_pdf_header'):
            is_bytes = isinstance(html, bytes)
            if is_bytes:
                html_str = html.decode('utf-8')
            else:
                html_str = html

            # Membrete a inyectar
            custom_header = """
            <div style="font-family: Arial, sans-serif; margin-bottom: 20px; text-align: left; padding: 20px;">
                <h4 style="margin: 0; font-weight: bold; font-size: 18px;">HEALTH CONSULTORES, C.A.</h4>
                <p style="margin: 0; font-size: 14px;"><strong>NIF:</strong> J-41261358-8</p>
                <p style="margin: 0; font-size: 14px;"><strong>Dir:</strong> Av. Francisco de Miranda, Centro Seguros Sudamerica, Piso 4, Oficina 4D, El Rosal, Caracas</p>
            </div>
            <hr style="border: 1px solid #ddd; margin-bottom: 20px;"/>
            """
            
            # Buscar un lugar seguro para inyectar (al principio del body o del div principal)
            if '<div class="o_account_reports_body">' in html_str:
                html_str = html_str.replace('<div class="o_account_reports_body">', '<div class="o_account_reports_body">' + custom_header, 1)
            elif '<div class="page">' in html_str:
                html_str = html_str.replace('<div class="page">', '<div class="page">' + custom_header, 1)
            elif '<body' in html_str:
                body_idx = html_str.find('<body')
                end_bracket = html_str.find('>', body_idx)
                if end_bracket != -1:
                    html_str = html_str[:end_bracket+1] + custom_header + html_str[end_bracket+1:]
                else:
                    html_str = custom_header + html_str
            else:
                # Si no encontramos ningún tag conocido, lo ponemos al principio
                html_str = custom_header + html_str
                
            if is_bytes:
                return html_str.encode('utf-8')
            return html_str
            
        return html
