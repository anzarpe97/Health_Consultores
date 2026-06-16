# -*- coding: utf-8 -*-
{
    'name': 'Balance de Situación',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Reports',
    'summary': 'Reporte de Balance de Situación personalizado',
    'description': """
        Módulo que genera el reporte de Balance de Situación con el formato estándar.
        
        Incluye:
        - Activos Corrientes (Cuentas bancarias, Por cobrar, Prepagos)
        - Activos Adicionales Fijos
        - Activos No Corrientes Extras
        - Pasivos Corrientes (Por pagar)
        - Pasivos Adicionales No Corrientes
        - Capital (Ganancias sin asignar, acumuladas)
    """,
    'author': 'Contables',
    'website': '',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/balance_situacion_wizard_views.xml',
        'report/balance_situacion_report_template.xml',
        'report/balance_situacion_report.xml',
        'views/balance_situacion_menu.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'balance_situacion/static/description/balance_report.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
