from odoo import models, fields, api, tools


class CustomTrialBalanceAnalysis(models.Model):
    """
    SQL View Analysis for Trial Balance Movements.
    Shows real Debit/Credit sums per account based on selected filters.
    """

    _name = "custom.trial.balance.analysis"
    _description = "Análisis de Movimientos (Debe/Haber)"
    _auto = False
    _rec_name = "account_id"
    _order = "account_code"

    date = fields.Date(string="Fecha", readonly=True)
    account_id = fields.Many2one("account.account", string="Cuenta", readonly=True)
    account_code = fields.Char(string="Código de Cuenta", readonly=True)
    journal_id = fields.Many2one("account.journal", string="Diario", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)
    move_id = fields.Many2one("account.move", string="Asiento", readonly=True)

    debit = fields.Monetary(
        string="Debe", readonly=True, currency_field="company_currency_id"
    )
    credit = fields.Monetary(
        string="Haber", readonly=True, currency_field="company_currency_id"
    )
    balance = fields.Monetary(
        string="Balance", readonly=True, currency_field="company_currency_id"
    )

    company_currency_id = fields.Many2one(
        "res.currency", string="Moneda de Compañía", readonly=True
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    aml.id AS id,
                    aml.date AS date,
                    aml.account_id AS account_id,
                    aa.code AS account_code,
                    aml.journal_id AS journal_id,
                    aml.company_id AS company_id,
                    aml.move_id AS move_id,
                    aml.currency_id AS company_currency_id,
                    COALESCE(aml.debit, 0) AS debit,
                    COALESCE(aml.credit, 0) AS credit,
                    COALESCE(aml.balance, 0) AS balance
                FROM account_move_line aml
                JOIN account_move am ON aml.move_id = am.id
                JOIN account_account aa ON aml.account_id = aa.id
                WHERE am.state = 'posted'
            )
        """
            % self._table
        )
