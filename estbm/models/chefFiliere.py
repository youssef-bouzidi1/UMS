# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
# import person
def validate_email(mail):
    if mail:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@usms\.ac\.ma$',mail)
        if match == None:
            return False
        return True

class chefFiliere(models.Model):
    _name = 'chef.filiere'
    _description = 'Chef Filiere'

    _inherit = 'person'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee ID',
        ondelete='cascade',
        #   required=True,
        help="Enter related employee")
    dept_id = fields.Many2one('hr.department',
                              string="Department ID",
                              help="Select the related Department")

    # job = fields.Many2one(comodel_name='hr.job',string='Job',related='employee_id.job_id',readonly=True)
    job_id = fields.Many2one('hr.job',
                             'Job position',
                             ondelete='cascade',
                             help="Select your job")

    certificate_level = fields.Selection(string='Certificate Level',
                                         selection=[('lisence', 'Lisence'),
                                                    ('master', 'Master'),
                                                    ('doctorat', 'Doctorat')],
                                         required=True)

    filiere_list = fields.One2many('filiere',
                                   'chef_id',
                                   string='List of filiere')

    @api.model_create_multi
    def create(self, vals):
        vals[0]['name'] = '{} {}'.format(vals[0].get('nom'),
                                         vals[0].get('prenom'))
        vals[0]['display_name'] = '{} {}'.format(vals[0].get('nom'),
                                                 vals[0].get('prenom'))
        ts = super(chefFiliere, self).create(vals)
        return ts

    def write(self, vals):
        vals['name'] = '{} {}'.format(self.nom, self.prenom)
        vals['display_name'] = '{} {}'.format(self.nom, self.prenom)
        res = super().write(vals)
        self.employee_id.name = '{} {}'.format(self.nom, self.prenom)
        self.employee_id.image_1920 = self.image_1920
        self.user_id.name = '{} {}'.format(self.nom, self.prenom)
        if self.email:
            self.user_id.login = self.email
        return res

    def create_teacher_user(self):
        # user_group = self.env.ref("base.group_portal") or False
        tab = []
        tab.append(self.env.ref('estbm.group_student_user').id)
        tab.append(self.env.ref('estbm.group_chef_filiere_user').id)
        tab.append(self.env.ref('estbm.group_teacher_user').id)
        tab.append(self.env.ref('estbm.group_filiere_user').id)
        tab.append(self.env.ref('estbm.group_classe_user').id)
        tab.append(self.env.ref('estbm.group_module_chef_admin').id)
        tab.append(self.env.ref('estbm_emploi.group_emploi_temps_user').id)
        tab.append(self.env.ref('base.group_no_one').id)
        tab.append(self.env.ref('base.group_user').id)
        user_group = self.env['res.groups'].search([('id','in',tab)])
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    # 'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id

    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'image_1920': record.image_1920,
                'birthday': record.date_of_birth,
                'department_id': record.dept_id.id,
                'job_id': record.job_id.id,
                'work_email': record.email,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'employee_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.onchange('email')
    def onchange_email(self):
        if self.email and not validate_email(self.email):
            raise ValidationError('Not a valid E-mail Adress')
        self.user_id.login = self.email
    