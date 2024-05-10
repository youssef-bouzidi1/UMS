# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Groupe(models.Model):
    _name = 'groupe'
    _description = 'Groupe Information'

    name = fields.Char(
        string='Group\'s Name',
        required=True,
    )

    class_id = fields.Many2one('classe', string='Classe ID', required=True)

    student_list = fields.One2many('student','groupe_id',string='List of students')
    capacity = fields.Integer(compute='_compute_capacity',
                              string='Number of student')
    

    @api.depends('student_list')
    def _compute_capacity(self):
        for record in self:
            record.capacity = len(record.student_list)
            
    def show_related_students(self):
        # std_list = self.env['student'].search([('groupe_id','=',self.id)])
        # print(std_list)
        d = 'Students of {}'.format(self.name)
        return {
            'name': d,
            'type': 'ir.actions.act_window',
            # 'view_type': 'tree',
            'view_mode': 'kanban',
            'res_model': 'student',
            'domain': [('groupe_id','=',self.id)],
        }
        
