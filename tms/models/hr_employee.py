# -*- coding: utf-8 -*-
# Copyright 2012, Israel Cruz Argil, Argil Consulting
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import logging
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
try:
    from sodapy import Socrata
except ImportError:
    _logger.debug('Cannot `import sodapy`.')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    driver = fields.Boolean(
        help='Used to define if this person will be used as a Driver')
    tms_advance_account_id = fields.Many2one(
        'account.account', 'Advance Account')
    tms_loan_account_id = fields.Many2one(
        'account.account', 'Loan Account')
    tms_expense_negative_account_id = fields.Many2one(
        'account.account', 'Negative Balance Account')
    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit')
    driver_license = fields.Char(string="License ID")
    license_type = fields.Char()
    days_to_expire = fields.Integer(compute='_compute_days_to_expire')
    income_percentage = fields.Float()
    license_valid_from = fields.Date()
    license_expiration = fields.Date()
    outsourcing = fields.Boolean(string='Outsourcing?')

    @api.depends('license_expiration')
    def _compute_days_to_expire(self):
        for rec in self:
            if rec.license_expiration:
                date = datetime.strptime(rec.license_expiration, '%Y-%m-%d')
            else:
                date = datetime.now()
            now = datetime.now()
            delta = date - now
            rec.days_to_expire = delta.days if delta.days > 0 else 0

    @api.multi
    def get_driver_license_info(self):
        client = Socrata("www.datossct.gob.mx", None)
        for rec in self:
            try:
                driver_license = client.get(
                    '3qhi-59v6', licencia=rec.driver_license)
                license_valid_from = datetime.strptime(
                    driver_license[0]['fecha_inicio_vigencia'],
                    '%Y-%m-%dT%H:%M:%S.%f')
                license_expiration = datetime.strptime(
                    driver_license[0]['fecha_fin_vigencia'],
                    '%Y-%m-%dT%H:%M:%S.%f')
                rec.license_type = driver_license[0][
                    'categoria_de_la_licencia']
                rec.license_valid_from = license_valid_from
                rec.license_expiration = license_expiration
                client.close()
            except:
                client.close()
                raise ValidationError(_(
                    'The driver license is not in SCT database'))
