# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BalanceSituacionWizard(models.TransientModel):
    _name = 'balance.situacion.wizard'
    _description = 'Asistente - Balance de Situación'

    date_to = fields.Date(
        string='Al (Fecha)',
        required=True,
        default=fields.Date.context_today,
    )
    date_from = fields.Date(string='Fecha Desde')
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        required=True,
        default=lambda self: self.env.company,
    )
    journal_ids = fields.Many2many(
        'account.journal',
        string='Diarios',
        domain="[('company_id','=',company_id)]",
        help='Dejar vacío para incluir TODOS los diarios.',
    )
    only_posted = fields.Boolean(
        string='Solo asientos publicados', default=True
    )
    accrual_basis = fields.Boolean(
        string='Base Accrual', default=True
    )

    def action_generate_report(self):
        """Crea el registro transitorio de cálculo y lanza el PDF."""
        self.ensure_one()
        balance = self.env['balance.situacion'].create({
            'date_to':      self.date_to,
            'date_from':    self.date_from,
            'company_id':   self.company_id.id,
            'journal_ids':  [(6, 0, self.journal_ids.ids)],
            'only_posted':  self.only_posted,
            'accrual_basis': self.accrual_basis,
        })
        data = balance._compute_sections()
        return self.env.ref(
            'balance_situacion_conveca.action_report_balance_situacion'
        ).report_action(balance, data=data)
