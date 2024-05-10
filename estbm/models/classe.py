# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Classe(models.Model):
    _name = 'classe'
    _description = 'Classe Information'

    name = fields.Char(
        string='Class Name',
        required=True,
    )

    # the year of the class if it is the first year of the second year
    year = fields.Selection(string='Class Year',
                            selection=[
                                ('1', 'First Year'),
                                ('2', 'Second Year'),
                            ],
                            required=True)
    capacity = fields.Integer(compute='_compute_capacity',
                              string='Number of students')
    filiere_id = fields.Many2one('filiere', string='Filiere ID')

    student_list = fields.One2many('student',
                                   'class_id',
                                   string='List of students')

    group_list = fields.One2many('groupe', 'class_id', string='List of groups')

    hide = fields.Boolean(compute='_compute_hide',
                          string='Hide Generate Button',
                          default=False)

    # emploi_id = fields.Many2one(comodel_name='estbm_emploi.emploi.temps',string="Emploi Temp")
    # emploi_temps_ids = fields.One2many(comodel_name='emploi.temps',inverse_name='class_id',string='Emploi Temp')
    

    semester_1 = fields.Selection(selection=[
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
    ],
                                  string='Semester')

    semester_2 = fields.Selection(selection=[
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
    ],
                                  string='Semester')

    semester = fields.Char(compute='_compute_semester', string='Semester')

    @api.depends('semester_1', 'semester_2')
    def _compute_semester(self):
        for record in self:
            if record.semester_1:
                record.semester = record.semester_1
            elif record.semester_2:
                record.semester = record.semester_2
            else:
                record.semester = False

    @api.onchange('year')
    def onchange_year(self):
        for record in self:
            if record.year == '1':
                record.semester_2 = False
            elif record.year == '2':
                record.semester_1 = False
            else:
                record.semester_1=False
                record.semester_2=False

    @api.depends('hide')
    def _compute_hide(self):
        self.hide = True
        group_admin = self.env.ref('estbm.group_classe_admin').id
            # self.hide = False
            # or len(self.filiere_id.chef_id.user_id.groups_id.browse(self.env.ref('estbm.group_classe_admin').id)) != 0
        print(self.env.user.name,self.env.user.id)
        print(any(g.id==self.env.ref('base.group_erp_manager').id for g in self.env.user.groups_id))
        print(self.env.user.groups_id.browse(self.env.ref('base.group_erp_manager').id))
        if (len(self.group_list) == 0 and self.env.user.id==self.filiere_id.chef_id.user_id.id) or any(g.id==self.env.ref('base.group_erp_manager').id for g in self.env.user.groups_id):
            self.hide = False

    @api.depends('student_list')
    def _compute_capacity(self):
        for record in self:
            record.capacity = len(record.student_list)

    def _chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def generate_groups(self):
        students = self.student_list
        num = 2
        if len(students) > 80:
            num = 4
        split_students = self._chunkIt(students, num)
        group_res = self.env['groupe']
        i = 1
        for gr in split_students:
            name = 'Groupe {}'.format(i)
            i += 1
            group_res.create({
                'name': name,
                'class_id': self.id,
                'student_list': gr,
            })
        print(split_students)
