# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import float_round


class BalanceSituacion(models.TransientModel):
    """
    Modelo transitorio que calcula y agrupa las cuentas contables
    para el reporte de Balance de Situación.
    
    Estructura del balance (según imagen CONVECA):
    ─────────────────────────────────────────────
    ACTIVOS
      Activos corrientes
        Cuentas bancarias y en efectivo
        Por cobrar
        Activos corrientes          (otros)
        Prepagos
      Activos adicionales fijos
      Activos no corrientes extras
    PASIVOS
      Pasivos corrientes
        Pasivos corrientes          (otros)
        Por pagar
      Pasivos adicionales no corrientes
    CAPITAL
      Ganancias sin asignar
        Ganancias no asignadas del año actual
          Ganancias del año actual
          Ganancias asignadas del año actual
        Ganancias no asignados de años anteriores
      Ganancias acumuladas
    PASIVOS + CAPITAL
    """
    _name = 'balance.situacion'
    _description = 'Balance de Situación'

    # ── Filtros del reporte ──────────────────────────────────────────────────
    date_from = fields.Date(string='Fecha Desde')
    date_to   = fields.Date(string='Fecha Hasta', default=fields.Date.context_today)
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        default=lambda self: self.env.company
    )
    journal_ids = fields.Many2many(
        'account.journal', string='Diarios',
        help='Dejar vacío para incluir todos los diarios.'
    )
    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Cuentas Analíticas',
        help='Dejar vacío para todas.'
    )
    only_posted = fields.Boolean(
        string='Solo asientos publicados', default=True
    )
    accrual_basis = fields.Boolean(
        string='Base Accrual', default=True
    )

    # ────────────────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────────────────
    def _get_domain(self):
        """Dominio base para filtrar move lines."""
        domain = [
            ('company_id', '=', self.company_id.id),
            ('date', '<=', self.date_to),
            ('move_id.move_type', 'in', ['entry']),
        ]
        if self.only_posted:
            domain.append(('move_id.state', '=', 'posted'))
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.journal_ids:
            domain.append(('journal_id', 'in', self.journal_ids.ids))
        return domain

    def _balance_by_account_types(self, account_types):
        """
        Retorna el saldo neto (débito - crédito) de todas las líneas
        cuyo tipo de cuenta (account.account.type) esté en account_types.
        """
        domain = self._get_domain()
        domain.append(('account_id.account_type', 'in', account_types))
        lines = self.env['account.move.line'].search(domain)
        return sum(l.debit - l.credit for l in lines)

    def _balance_by_account_codes(self, prefixes):
        """
        Retorna el saldo neto de cuentas cuyo código empiece
        con alguno de los prefijos indicados.
        """
        domain = self._get_domain()
        prefix_domain = []
        for p in prefixes:
            prefix_domain += [('account_id.code', '=like', p + '%')]
        if len(prefixes) > 1:
            import functools, operator
            combined = functools.reduce(operator.or_, [
                [('account_id.code', '=like', p + '%')] for p in prefixes
            ])
            # Odoo domain OR
            or_domain = []
            for p in prefixes:
                or_domain.append(('account_id.code', '=like', p + '%'))
            # Build OR: ['|', cond1, cond2, ...]
            full_or = []
            for i in range(len(prefixes) - 1):
                full_or.append('|')
            full_or += [('account_id.code', '=like', p + '%') for p in prefixes]
            domain = domain + full_or
        else:
            domain.append(('account_id.code', '=like', prefixes[0] + '%'))
        lines = self.env['account.move.line'].search(domain)
        return sum(l.debit - l.credit for l in lines)

    # ────────────────────────────────────────────────────────────────────────
    # Cálculo de secciones
    # ────────────────────────────────────────────────────────────────────────
    def _compute_sections(self):
        """
        Calcula todos los totales del balance y devuelve un dict
        listo para pasar al template QWeb.
        """
        # ── ACTIVOS CORRIENTES ───────────────────────────────────────────
        cuentas_bancarias = self._balance_by_account_types(['asset_cash'])
        por_cobrar        = self._balance_by_account_types(['asset_receivable'])
        activos_ctes_otros = self._balance_by_account_types(['asset_current'])
        prepagos          = self._balance_by_account_types(['asset_prepayments'])

        total_activos_corrientes = (
            cuentas_bancarias + por_cobrar + activos_ctes_otros + prepagos
        )

        # ── ACTIVOS FIJOS / NO CORRIENTES ───────────────────────────────
        activos_fijos       = self._balance_by_account_types(['asset_fixed'])
        activos_no_ctes_ext = self._balance_by_account_types(['asset_non_current'])

        total_activos = total_activos_corrientes + activos_fijos + activos_no_ctes_ext

        # ── PASIVOS CORRIENTES ───────────────────────────────────────────
        pasivos_ctes_otros = abs(self._balance_by_account_types(['liability_current']))
        por_pagar          = abs(self._balance_by_account_types(['liability_payable']))

        total_pasivos_corrientes = pasivos_ctes_otros + por_pagar

        # ── PASIVOS NO CORRIENTES ────────────────────────────────────────
        pasivos_no_ctes = abs(self._balance_by_account_types(['liability_non_current']))

        total_pasivos = total_pasivos_corrientes + pasivos_no_ctes

        # ── CAPITAL ──────────────────────────────────────────────────────
        gan_anio_actual      = abs(self._balance_by_account_types(['income', 'income_other']))
        gan_asignadas_actual = 0.0   # Normalmente $0 al inicio del ejercicio
        gan_no_asig_actual   = gan_anio_actual - gan_asignadas_actual
        gan_anios_ant        = abs(self._balance_by_account_types(['equity_unaffected']))
        ganancias_acumuladas = abs(self._balance_by_account_types(['equity']))

        ganancias_sin_asignar = gan_no_asig_actual + gan_anios_ant
        total_capital = ganancias_sin_asignar + ganancias_acumuladas

        total_pasivos_capital = total_pasivos + total_capital

        return {
            # Meta
            'company':    self.company_id,
            'date_to':    self.date_to,
            'date_from':  self.date_from,
            'only_posted': self.only_posted,
            'accrual':    self.accrual_basis,
            # ACTIVOS
            'total_activos':             total_activos,
            'total_activos_corrientes':  total_activos_corrientes,
            'cuentas_bancarias':         cuentas_bancarias,
            'por_cobrar':                por_cobrar,
            'activos_ctes_otros':        activos_ctes_otros,
            'prepagos':                  prepagos,
            'activos_fijos':             activos_fijos,
            'activos_no_ctes_ext':       activos_no_ctes_ext,
            # PASIVOS
            'total_pasivos':             total_pasivos,
            'total_pasivos_corrientes':  total_pasivos_corrientes,
            'pasivos_ctes_otros':        pasivos_ctes_otros,
            'por_pagar':                 por_pagar,
            'pasivos_no_ctes':           pasivos_no_ctes,
            # CAPITAL
            'total_capital':             total_capital,
            'ganancias_sin_asignar':     ganancias_sin_asignar,
            'gan_no_asig_actual':        gan_no_asig_actual,
            'gan_anio_actual':           gan_anio_actual,
            'gan_asignadas_actual':      gan_asignadas_actual,
            'gan_anios_ant':             -gan_anios_ant,  # negativo como en el reporte
            'ganancias_acumuladas':      ganancias_acumuladas,
            # TOTAL FINAL
            'total_pasivos_capital':     total_pasivos_capital,
        }

    def action_print_report(self):
        """Acción llamada desde el wizard para imprimir el PDF."""
        data = self._compute_sections()
        return self.env.ref(
            'balance_situacion_conveca.action_report_balance_situacion'
        ).report_action(self, data=data)
