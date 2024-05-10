# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class filiere(models.Model):
    _name = 'filiere'
    _description = 'Filiere Information'

    name_fil = fields.Char(string='Name',
                       required=True,
                       help="Name of the filiere")
    
    
    name = fields.Char(compute='_compute_name', string='Nom de Filiere')
    
    @api.depends('name_fil','type')
    def _compute_name(self):
        for record in self:
            if record.name_fil and record.type:
                record.name = '{}-{}'.format(record.type.upper(),record.name_fil)
            else :
                record.name = None
            
    
    nick_name = fields.Char(string='NickName',required=True,help='Enter the NickName')
    
    

    code = fields.Char(string="Code", readonly=True)
    
    image = fields.Binary(string='Image')

    description = fields.Text(string="Objectif",
                              required=True,
                              help="Enter objectif of the facilty")
    
    competence = fields.Text(string="Competence",
                              required=True,
                              help="Enter competence of the facilty")
    
    debouche = fields.Text(string="Debouche",
                              required=True,
                              help="Enter Debouche of the facilty")
    
    semester_ids = fields.One2many('semester','filiere_id',string='Semester IDs',required=True)
    
    def _check_semesters(self,semesters):
        for s1 in semesters:
            for s2 in semesters:
                if s1!=s2:
                    if s1.name==s2.name and s1.module_id==s2.module_id and s1.element_id==s2.element_id and s1.filiere_id==s2.filiere_id:
                        raise ValidationError('You cannot have the same element and module in the same semester for the same filiere')
                    if s1.name==s2.name and s1.filiere_id==s2.filiere_id and s1.module_count!=s2.module_count:
                        raise ValidationError('You cannot have a different number of modules for the same semester')
    
    @api.onchange('semester_ids')
    def onchange_semester_ids(self):
        for record in self:
            self._check_semesters(record.semester_ids)
    
    
    # year = fields.Selection(string='Number Of Years',
    #                         selection=[
    #                             ('1', '1'),
    #                             ('2', '2'),
    #                             ('3', '3'),
    #                             ('4', '4'),
    #                         ],
    #                         required=True)
    
    # type of the filiere if DUT or Lisence 
    type = fields.Selection(selection=[
        ('dut','DUT'),
        ('lisence','Lisence'),
    ],string="Filiere Type",required=True)
    
    # number of year 
    year_count = fields.Char(compute='_compute_year_count', string='year')
    
    @api.depends('type')
    def _compute_year_count(self):
        for record in self:
            if record.type == 'dut':
                record.year_count = '2 Years'
            elif record.type == 'lisence':
                record.year_count = '1 Year'
            else:
                record.year_count = None
    

    chef_id = fields.Many2one('chef.filiere',
                              string='Responsable',
                              ondelete='cascade',required=True,help="Select the responsable of the filiere")
    dept_id = fields.Many2one('hr.department',
                              string="Department ID",
                              help="Select the related Department")
    # student_list = fields.One2many('student','filiere_id',string='List of students')
    class_list = fields.One2many('classe','filiere_id',string='List of Classes')

    _sql_constraints = [
        ('unique_facility_code', 'unique(code)', 'Code should be unique!!'),
        ('unique_facility_name', 'unique(name)', 'Name should be unique!!')
    ]

    # student_list = fields.One2many('student',
    #                                'filiere_id',
    #                                string='Student List')
    # student_list = fields.Many2many('student','filiere_id',string='Student List')

    # student_count = fields.Integer(compute='_compute_student_count',
    #                                string='Number Of Students')

    # @api.depends('student_count')
    # def _compute_student_count(self):
    #     for record in self:
    #         record.student_count = len(record.student_list)

    @api.model
    def create(self, vals):
        """
            Create a new record for a model filiere
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        vals['code'] = self.env['ir.sequence'].get('filiere.sequence.code')
        fil = super().create(vals)
        # fil.code = self.env['ir.sequence'].get('filiere.sequence.code')

        return fil

    # copying the student
    def copy(self, default=None):
        default = {
            'name':
            '{} copy ({})'.format(
                self.name,
                self.env['ir.sequence'].get('filiere.sequence.copy')),
            'code':
            self.env['ir.sequence'].get('filiere.sequence.code')
        }
        res = super().copy(default)

        return res
