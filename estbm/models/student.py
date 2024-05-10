# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Student(models.Model):
    _name = 'student'
    _description = 'Student Information'

    _inherit = 'person'

    @api.model
    def _default_student_code(self):
        self.student_code = self.env['ir.sequence'].get(
            'student_sequence.code')

    student_code = fields.Char(
        string="Student Code",
        #    default=_default_student_code,
        readonly=True)

    CNE = fields.Char(string='CNE',
                      required=True,
                      help="The student's national code")

    admission_date = fields.Date('Admission Date',
                                 default=fields.Date.today(),
                                 help='Enter student admission date')
    
    # this field will just be used in the student card for showing the year 
    card_year = fields.Char(compute='_compute_card_year', string='card year')
    
    @api.depends('admission_date')
    def _compute_card_year(self):
        for record in self:
            record.card_year = '{}/{}'.format(record.admission_date.year-1,record.admission_date.year)
    

    father_name = fields.Char(string="Father")
    mother_name = fields.Char(string="Mother")
    class_id = fields.Many2one('classe', string='Student Class', required=True)
    class_name = fields.Char('Class Name',
                             related='class_id.name',
                             readonly=True)
    # filiere_id = fields.Many2one('filiere',
    #                              related='class_id.filiere_id',
    #                              string='Filiere ID',
    #                              readonly=False)
    filiere_id = fields.Many2one('filiere',
                                 string='Filiere ID',required=True)
    year = fields.Selection(string='Student\'s Year',
                            related='class_id.year',
                            selection=[
                                ('1', 'First Year'),
                                ('2', 'Second Year'),
                            ],
                            store=True)
    name_fil = fields.Char(string='Description Filiere',
                                      related='filiere_id.name_fil',
                                      readonly=True)
    groupe_id = fields.Many2one('groupe', string='Group ID')

    @api.onchange('filiere_id')
    def onchange_filiere_id(self):
        print(self.filiere_id)
        print(self.env['classe'].search([('filiere_id', '=', self.filiere_id.id)]).mapped('id'))
        # self.class_id = None
        ids = self.env['classe'].search([('filiere_id', '=', self.filiere_id.id)]).mapped('id')
        self.class_id=None
        # print(self.class_id)
        return {'domain': {'class_id': [('filiere_id', '=', self.filiere_id.id)]}}
        # return {'domain': {'class_id': [('id', 'in', ids)]}}


    @api.onchange('class_id')
    def _onchange_class_id(self):
        self.groupe_id = None
        return {'domain': {'groupe_id': [('class_id', '=', self.class_id.id)]}}

    def name_get(self):
        """ This method used to customize display name of the record """
        result = []
        for record in self:
            rec_name = "%s %s" % (record.nom, record.prenom)
            result.append((record.id, rec_name))
        return result

    @api.model_create_multi
    def create(self, vals):
        vals[0]['name'] = '{} {}'.format(vals[0].get('nom'),
                                         vals[0].get('prenom'))
        vals[0]['display_name'] = '{} {}'.format(vals[0].get('nom'),
                                                 vals[0].get('prenom'))
        std = super(Student, self).create(vals)
        std.student_code = self.env['ir.sequence'].get('student.sequence.code')
        return std

    # def write(self, vals):
    #     vals['name']='{} {}'.format(vals.get('nom'),vals.get('prenom'))
    #     vals['display_name']='{} {}'.format(vals.get('nom'),vals.get('prenom'))
    #     std = super().write(vals)
    #     return std

    def create_student_user(self):
        # user_group = self.env.ref("estbm.group_student_user") or False
        tab = []
        tab.append(self.env.ref('estbm.group_student_user').id)
        tab.append(self.env.ref('estbm.group_chef_filiere_user').id)
        tab.append(self.env.ref('base.group_no_one').id)
        tab.append(self.env.ref('base.group_user').id)
        tab.append(self.env.ref('estbm.group_filiere_user').id)
        tab.append(self.env.ref('estbm.group_classe_user').id)
        tab.append(self.env.ref('estbm.group_teacher_user').id)
        tab.append(self.env.ref('estbm.group_module_user').id)
        tab.append(self.env.ref('estbm_emploi.group_emploi_temps_user').id)
        tab.append(self.env.ref('estbm.group_only_student_mine').id)
        user_group = self.env['res.groups'].search([('id','in',tab)])
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'student_id':self.id,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id

    def delete(self):
        self.unlink()

    def copy_student(self):
        default = {}
        self.copy(default)

    def copy(self, default=None):
        default = {
            'student_code':
            self.env['ir.sequence'].get('student.sequence.code')
        }
        res = super().copy(default)
        return res

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            # match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@usms\.ac\.ma$',
                             self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail Adress')
            self.user_id.login = self.email

    def change_password(self):
        self.user_id.notify_danger('hello')

        # return {
        #     # 'name': _(' Human Readable String'),
        #     'res_model':'res.users',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('estbm.ayoub_form').id,
        #     'context':{
        #         'default_login':self.user_id.login
        #     }
        # }

        # return {
        #     # 'name': _(' Human Readable String'),
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'res.partner',
        #     'view_id': self.env.ref('base.view_partner_form').id
        # }

        # self.user_id.change_password('kali','ayoubkali')
        
    # @api.multi
    def write(self, values):
        res = super().write(values)
        if self.image_1920:
            self.user_id.image_1920 = self.image_1920
        # res.image_1920 = values['image_1920']
        return res





class ResUsers(models.Model):
    _inherit = 'res.users'

    student_id = fields.Many2one('student',string='Your Informations')
