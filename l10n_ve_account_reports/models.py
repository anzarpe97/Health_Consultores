from odoo import models

class AccountReport(models.Model):
    _inherit = 'account.report'

    def _get_html_data_for_pdf_export(self, options):
        res = super()._get_html_data_for_pdf_export(options)
        new_res = []
        for bodies, footer, is_landscape in res:
            new_bodies = []
            for body in bodies:
                body_str = body.decode('utf-8') if isinstance(body, bytes) else body
                
                injection = """
                <div style="margin-top: 5px; margin-bottom: 10px; font-size: 13px;">
                    <div style="font-weight: bold; background-color: #f2f2f2; padding: 5px 10px; border: 1px solid #ccc; border-radius: 3px; display: inline-block;">
                        <div>Dirección: AV SANTA LUCIA, AV PRINCIPAL DEL BOSQUE Y AV SANTA ISABEL EDIF CENTRO DORAL PISO 12 OF 0123 URB EL BOSQUE</div>
                        <div>NIF: J-40302187-2</div>
                    </div>
                </div>
                """
                
                # Try to inject after company name
                if "HEALTH 1105 CONSULTORES, C.A" in body_str:
                    body_str = body_str.replace(
                        "HEALTH 1105 CONSULTORES, C.A", 
                        "HEALTH 1105 CONSULTORES, C.A" + injection
                    )
                elif '<div class="row o_header_font">' in body_str:
                    body_str = body_str.replace(
                        '<div class="row o_header_font">', 
                        '<div class="row o_header_font">' + injection
                    )
                else:
                    # fallback
                    body_str = body_str.replace('<header>', '<header>' + injection)
                        
                new_bodies.append(body_str.encode('utf-8') if isinstance(body, bytes) else body_str)
            new_res.append((new_bodies, footer, is_landscape))
        return iter(new_res)
