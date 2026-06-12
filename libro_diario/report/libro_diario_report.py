from odoo import models, api, _


class ReportLibroDiarioDocument(models.AbstractModel):
    _name = "report.libro_diario.report_libro_diario_document"
    _description = "Reporte Diario Legal"

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            return {}

        date_from = data.get("date_from")
        date_to = data.get("date_to")
        company_id = data.get("company_id")

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
            GROUP BY aa.id, aa.code, aa.name
            HAVING SUM(aml.debit) != 0 OR SUM(aml.credit) != 0
            ORDER BY aa.code
        """

        self.env.cr.execute(query, [date_from, date_to, company_id])
        lines_data = self.env.cr.dictfetchall()

        # Get translated account names
        account_ids = [line["account_id"] for line in lines_data]
        # Fetch accounts as recordset to automatically get translated names
        accounts = self.env["account.account"].browse(account_ids)
        # Create a mapping of account_id -> translated_name
        account_names = {acc.id: acc.name for acc in accounts}

        lines = []
        for line in lines_data:
            line["account_name"] = account_names.get(
                line["account_id"], line["account_name"]
            )
            lines.append(line)

        # Calculate totals
        total_debit = sum(line["total_debit"] for line in lines)
        total_credit = sum(line["total_credit"] for line in lines)

        return {
            "doc_ids": docids,
            "doc_model": "libro.diario.wizard",
            "data": data,
            "lines": lines,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "company": self.env["res.company"].browse(company_id),
            "date_from": date_from,
            "date_to": date_to,
        }
