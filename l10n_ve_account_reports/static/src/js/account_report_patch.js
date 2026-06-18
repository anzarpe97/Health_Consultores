/** @odoo-module **/

// Use a MutationObserver to safely inject the address without risking import errors
const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        if (mutation.addedNodes.length) {
            const titles = document.querySelectorAll('.o_account_reports_header_title, .o_title');
            if (titles.length > 0) {
                const titleEl = titles[0];
                if (!document.getElementById('l10n_ve_custom_address_inj')) {
                    const injection = `
                        <div id="l10n_ve_custom_address_inj" style="font-weight: bold; background-color: #f2f2f2; padding: 5px 10px; border: 1px solid #ccc; border-radius: 3px; display: inline-block; font-size: 11px; margin-top: 5px; margin-bottom: 10px;">
                            <div>Dirección: AV SANTA LUCIA, AV PRINCIPAL DEL BOSQUE Y AV SANTA ISABEL EDIF CENTRO DORAL PISO 12 OF 0123 URB EL BOSQUE</div>
                            <div>NIF: J-40302187-2</div>
                        </div>
                    `;
                    // Insert right after the company name if possible, or after the title
                    titleEl.insertAdjacentHTML('afterend', injection);
                }
            }
        }
    }
});

// Start observing the document body for appended elements
observer.observe(document.body, { childList: true, subtree: true });
