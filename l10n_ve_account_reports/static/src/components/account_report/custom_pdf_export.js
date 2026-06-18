/** @odoo-module **/

import { AccountReport } from "@account_reports/components/account_report/account_report";
import { patch } from "@web/core/utils/patch";

patch(AccountReport.prototype, {
    exportCustomPdf() {
        return this.env.services.orm.call(
            "account.report", 
            "export_custom_pdf", 
            [this.controller.action.context.id || this.controller.options.report_id, this.controller.options]
        ).then((action) => {
            return this.env.services.action.doAction(action);
        });
    }
});
