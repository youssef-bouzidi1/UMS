# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import re
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

def validate_email(mail):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@usms\.ac\.ma$',mail)
    if match == None:
        return False
    return True

class Person(models.Model):
    _name = 'person'
    _description = 'person Information'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    # _inherit = 'res.users'

    _inherits = {'res.partner': 'partner_id'}


    nom = fields.Char(
        string='nom',
        required=True,
        help="First Name of the student",
    )
    prenom = fields.Char(
        string='prenom',
        required=True,
        help="Last Name of the student",
    )
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')

    partner_id = fields.Many2one('res.partner',
                              'Partner ID',
                              ondelete="cascade",
                              required=True,
                              delegate=True,
                              help='Select related partner of the student')
    
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")

    CIN = fields.Char(string='CIN',
                      required=True,
                      help="National Identity Card")

    phone = fields.Integer(string='Phone Number', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Gender',
                              required=True,
                              help='Select person gender')

    @api.constrains('date_of_birth')
    def _check_date_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.date.today(
            ):
                raise ValidationError('the date must be less then today !!!!')

    age = fields.Integer(compute='_compute_age',
                         string='age',
                         readonly=True,
                         help='Enter student age')

    @api.depends('date_of_birth')
    def _compute_age(self):
        '''Method to calculate student age'''
        current_dt = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.date_of_birth and rec.date_of_birth < current_dt:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                if age_calc > 0.0:
                    rec.age = age_calc

    # @api.model
    # def create(self, vals):
    #     vals['name'] = '{} {}'.format(vals.get('nom'), vals.get('prenom'))
    #     vals['display_name'] = '{} {}'.format(vals.get('nom'), vals.get('prenom'))
    #     print('hello---------------------------------')
    #     std = super(Student, self).create(vals)
    #     std.user_id.partner_id.name = 'ayoub nouri'
    #     std.image_1920 = vals['image_1920']
    #     return std

    