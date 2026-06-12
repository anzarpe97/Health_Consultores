{
    "name": "Balance de Comprobación (Libro Diario)",
    "version": "17.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Reporte de Balance de Comprobación sin columnas de saldo inicial y final",
    "description": """
        Este módulo agrega una copia del reporte de Balance de Comprobación
        limitando las columnas visualizadas exclusivamente a los movimientos del periodo
        (Debe y Haber), eliminando Balance Inicial y Balance Final.
    """,
    "author": "Marv1nG / Contablesag",
    "depends": ["account_reports", "account_accountant"],
    "data": [
        "security/ir.model.access.csv",
        "data/balance_report_data.xml",
        "views/custom_analysis_views.xml",
        "wizard/libro_diario_wizard_view.xml",
        "data/paperformat_data.xml",
        "report/report_action.xml",
        "report/libro_diario_report.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}
