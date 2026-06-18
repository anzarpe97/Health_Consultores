# coding: utf-8
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class AccountWhIslrRates(models.Model):
    _name = 'account.wh.islr.rates'
    _description = 'Rates'

    name = fields.Char(string='Tasa',  size=256,
            help="Nombre de tasa de retención para los conceptos de la retención")
    code = fields.Char(
            'Código de concepto', size=3, required=True, help="Código Conceptual")
    base = fields.Float(
            'Sin importe de impuestos', required=True,
            help="Porcentaje de la cantidad sobre la cual aplicar la retención",
            digits=(16, 2))
    minimum= fields.Float(
            'Min. Cantidad', required=True,
          #  digits=(16, 2),
            help="Cantidad mínima, a partir de la cual determinará si esta"
                 "retenido")
    wh_perc= fields.Float(
            'Factor', required=True,
            digits=(16, 2),
            help="El porcentaje que se aplica a los ingresos imponibles sujetos a impuestos que arroja la"
                 "cantidad a retener")
    subtract= fields.Float(
            'Sustracción en unidades impositivas', required=True,
            digits=(16, 2),
            help="Cantidad a restar de la cantidad total a retener "
                 "Cantidad Porcentaje de retención ..... Este sustraendo solamente"
                 "aplicado la primera vez que realiza una retención", compute='_subtract')
    residence= fields.Boolean(
            'Residencia',
            help="Indica si una persona es residente, en comparación con la "
                 "dirección de la empresa")
    nature =fields.Boolean(
            'Natural', help="Indica si una persona es natural o Juridica")
    concept_id= fields.Many2one(
            'account.wh.islr.concept', 'Withhold  Concept', required=False,
            ondelete='cascade',
            help="Concepto de retención asociado a esta tasa")
    rate2 = fields.Boolean(
            'Tasa 2', help='Tasa utilizada para entidades extranjeras')

    def _subtract(self):
        for rec in self:
            ut = self.env['account.ut'].search([], limit=1, order='date desc')
            ut_amount = ut.amount if ut else 0.0
            
            if 'PJ' in rec.name or 'PNNR' in rec.name:
                rec.subtract = 0.0
            elif 'PINU' in rec.name:
                if rec.wh_perc == 15.0:
                    rec.subtract = 0.0
                elif rec.wh_perc == 22.0:
                    rec.subtract = 140.0 * ut_amount
                elif rec.wh_perc == 34.0:
                    rec.subtract = 500.0 * ut_amount
                else:
                    rec.subtract = 0.0
            else:
                if rec.minimum > 0:
                    rec.subtract = rec.minimum * ut_amount * (rec.wh_perc / 100.0)
                else:
                    rec.subtract = 0.0

    def _get_name(self):
        """ Get the name of the withholding concept rate
        """
        res = {}
        for rate in self:
            if rate.nature:
                if rate.residence:
                    name = 'Persona' + ' ' + 'Natural' + ' ' + 'Residente'
                else:
                    name = 'Persona' + ' ' + 'Natural' + ' ' + 'No Residente'
            else:
                if rate.residence:
                    name = 'Persona' + ' ' + 'Juridica' + ' ' + 'Domiciliada'
                else:
                    name = 'Persona' + ' ' + 'Juridica' + ' ' + \
                        'No Domiciliada'
            res[rate.id] = name
        return res