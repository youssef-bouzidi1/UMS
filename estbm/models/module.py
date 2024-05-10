
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Module(models.Model):
    _name = 'module'
    _description = 'Module Informations'



    name = fields.Char(
        string='Name',
        required=True,
    )
    filiere_id = fields.Many2one('filiere',string='Filiere ID',required=True)
    

    semester_ids = fields.One2many('semester','module_id',string='Semester IDs',required=True)
   
    
    def _check_semesters(self,semesters):
        for s1 in semesters:
            for s2 in semesters:
                if s1!=s2:
                    if s1.name==s2.name and s1.module_id==s2.module_id and s1.element_id==s2.element_id and s1.filiere_id==s2.filiere_id:
                        raise ValidationError('You cannot have the same element and module in the same semester for the same filiere!!')
                    if s1.name==s2.name and s1.filiere_id==s2.filiere_id and s1.module_count!=s2.module_count:
                        raise ValidationError('You cannot have a different number of modules for the same semester!!')
    
    @api.onchange('semester_ids')
    def onchange_semester_ids(self):
        for record in self:
            self._check_semesters(record.semester_ids)
    
    # number_hour = fields.Integer(string='Number of Hours')
    # number_elements = fields.Integer(string='Number of Elements')
    number_elements = fields.Integer(compute='_compute_number_elements', string='Number of Elements')
    module_hours = fields.Integer(compute='_compute_module_hours', string='Module Hours')
    
    @api.depends('semester_ids')
    def _compute_number_elements(self):
        for record in self:
            record.number_elements = len(record.semester_ids.mapped('element_id'))

    @api.depends('semester_ids')
    def _compute_module_hours(self):
        for record in self:
            record.module_hours = sum(record.semester_ids.search([
                    '&', ('module_id', '=', record.name),
                    ('filiere_id', '=', record.filiere_id.id)
                ]).mapped('element_hours'))

    
    
    


