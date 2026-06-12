from odoo import models, api, _


class CustomTrialBalanceHandler(models.AbstractModel):
    """Custom Handler for Trial Balance (Libro Diario)."""

    _name = "custom.trial.balance.handler"
    _inherit = "account.report.custom.handler"
    _description = "Custom Trial Balance Handler (Libro Diario)"

    def _get_lines(
        self, report, options, all_column_groups_expression_totals=None, warnings=None
    ):
        """Generate lines with real debit/credit values using SQL."""

        # Get date range
        date_from = options.get("date", {}).get("date_from")
        date_to = options.get("date", {}).get("date_to")
        company_id = self.env.company.id
        currency = self.env.company.currency_id

        if not date_from or not date_to:
            return []

        # 1. Query for Account Totals
        query = """
            SELECT 
                aa.id as account_id,
                aa.code as account_code,
                aa.name as account_name,
                COALESCE(SUM(aml.debit), 0) as total_debit,
                COALESCE(SUM(aml.credit), 0) as total_credit
            FROM account_move_line aml
            JOIN account_account aa ON aml.account_id = aa.id
            JOIN account_move am ON aml.move_id = am.id
            WHERE aml.date >= %s 
              AND aml.date <= %s
              AND aml.company_id = %s
              AND am.state = 'posted'
        """
        params = [date_from, date_to, company_id]

        # Apply journal filter
        if options.get("journals"):
            journal_ids = [j["id"] for j in options["journals"] if j.get("selected")]
            if journal_ids:
                query += " AND aml.journal_id IN %s"
                params.append(tuple(journal_ids))

        query += """
            GROUP BY aa.id, aa.code, aa.name
            HAVING SUM(aml.debit) != 0 OR SUM(aml.credit) != 0
            ORDER BY aa.code
        """

        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        # Get translated names
        if results:
            account_ids = [r["account_id"] for r in results]
            accounts = self.env["account.account"].browse(account_ids)
            account_names = {a.id: a.name for a in accounts}
        else:
            account_names = {}

        # Check unfolded lines
        unfolded_lines = options.get("unfolded_lines") or []

        lines = []
        total_debit = 0.0
        total_credit = 0.0

        for row in results:
            total_debit += row["total_debit"]
            total_credit += row["total_credit"]

            # Account Line ID
            account_line_id = report._get_generic_line_id(
                "account.account", row["account_id"]
            )
            is_unfolded = account_line_id in unfolded_lines

            # Format values (Explicit currency to fix AssertionError)
            debit_formatted = report.format_value(
                options, row["total_debit"], figure_type="monetary", currency=currency
            )
            credit_formatted = report.format_value(
                options, row["total_credit"], figure_type="monetary", currency=currency
            )

            account_name = account_names.get(row["account_id"], row["account_name"])

            line = {
                "id": account_line_id,
                "name": f"{row['account_code']} {account_name}",
                "level": 2,
                "unfoldable": True,
                "unfolded": is_unfolded,
                "caret_options": "account.account",
                "columns": [
                    {
                        "name": debit_formatted,
                        "no_format": row["total_debit"],
                        "class": "number",
                    },
                    {
                        "name": credit_formatted,
                        "no_format": row["total_credit"],
                        "class": "number",
                    },
                ],
            }
            lines.append(line)

            # 2. Drill-down for unfolded accounts
            if is_unfolded:
                # Query details for this account
                detail_query = """
                    SELECT 
                        aml.id,
                        aml.date,
                        aml.name as label,
                        am.name as move_name,
                        COALESCE(aml.debit, 0) as debit,
                        COALESCE(aml.credit, 0) as credit
                    FROM account_move_line aml
                    JOIN account_move am ON aml.move_id = am.id
                    WHERE aml.account_id = %s
                      AND aml.date >= %s 
                      AND aml.date <= %s
                      AND aml.company_id = %s
                      AND am.state = 'posted'
                """
                detail_params = [row["account_id"], date_from, date_to, company_id]

                # Apply journal filter to details too
                if options.get("journals"):
                    journal_ids = [
                        j["id"] for j in options["journals"] if j.get("selected")
                    ]
                    if journal_ids:
                        detail_query += " AND aml.journal_id IN %s"
                        detail_params.append(tuple(journal_ids))

                detail_query += " ORDER BY aml.date, am.name"

                self.env.cr.execute(detail_query, detail_params)
                details = self.env.cr.dictfetchall()

                for det in details:
                    det_debit_fmt = report.format_value(
                        options, det["debit"], figure_type="monetary", currency=currency
                    )
                    det_credit_fmt = report.format_value(
                        options,
                        det["credit"],
                        figure_type="monetary",
                        currency=currency,
                    )

                    label = det["label"] or ""
                    move_name = det["move_name"] or ""
                    display_name = f"{det['date']} | {move_name} | {label}"

                    detail_line = {
                        "id": report._get_generic_line_id(
                            "account.move.line",
                            det["id"],
                            parent_line_id=account_line_id,
                        ),
                        "name": display_name,
                        "level": 3,
                        "parent_id": account_line_id,
                        "columns": [
                            {
                                "name": det_debit_fmt,
                                "no_format": det["debit"],
                                "class": "number",
                            },
                            {
                                "name": det_credit_fmt,
                                "no_format": det["credit"],
                                "class": "number",
                            },
                        ],
                    }
                    lines.append(detail_line)

        # Add total line
        total_line = {
            "id": report._get_generic_line_id(None, None, markup="total"),
            "name": _("Total"),
            "level": 1,
            "unfoldable": False,
            "unfolded": False,
            "class": "total",
            "columns": [
                {
                    "name": report.format_value(
                        options, total_debit, figure_type="monetary", currency=currency
                    ),
                    "no_format": total_debit,
                    "class": "number",
                },
                {
                    "name": report.format_value(
                        options, total_credit, figure_type="monetary", currency=currency
                    ),
                    "no_format": total_credit,
                    "class": "number",
                },
            ],
        }
        lines.append(total_line)

        return lines

    def _custom_options_initializer(self, report, options, previous_options=None):
        super()._custom_options_initializer(report, options, previous_options)


class AccountReport(models.Model):
    _inherit = "account.report"

    def _get_lines(self, options, **kwargs):
        """Global override to intercept custom report execution."""

        # Check if the current report uses our custom handler
        if (
            self.custom_handler_model_id
            and self.custom_handler_model_id.model == "custom.trial.balance.handler"
        ):
            return self.env["custom.trial.balance.handler"]._get_lines(self, options)

        return super()._get_lines(options, **kwargs)
