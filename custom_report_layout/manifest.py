# -*- coding: utf-8 -*-
{
    'name': 'Custom External Layout (Odoo 17)',
    'summary': 'Modificaciones globales para el encabezado estándar de los reportes',
    'version': '17.0.1.0.0',  # Formato oficial de Odoo 17
    'category': 'Technical',
    'author': 'Anderson Salazar',
    'depends': ['web'],       # Dependencia obligatoria de Odoo Web
    'data': [
        'views/report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',      # Recomendado en Odoo 17
}