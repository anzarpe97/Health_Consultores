# -*- coding: utf-8 -*-
{
    'name': "Venezuela - Reportes Financieros (PDF)",
    'summary': """
        Personalización del encabezado de los reportes financieros en PDF
    """,
    'description': """
        Agrega la dirección y NIF de la empresa en el PDF de los reportes financieros.
    """,
    'author': 'Devs by Contables',
    'category': 'Accounting/Localizations',
    'version': '17.0.1.0',
    'depends': ['account_reports'],
    'assets': {
        'web.report_assets_pdf': [
            'l10n_ve_account_reports/static/src/scss/account_report_print.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
}
