# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Semester(models.Model):
    _name = 'semester'
    _description = 'Semester Informations'

    # name = fields.Char(
    #     string='Semester Name',
    #     required=True,
    # )
    name = fields.Selection(selection=[
        ('S1', 'Semester 1'),
        ('S2', 'Semester 2'),
        ('S3', 'Semester 3'),
        ('S4', 'Semester 4'),
        ('S5', 'Semester 5'),
        ('S6', 'Semester 6'),
    ],
                            string='Semester',
                            required=True)

    module_id = fields.Many2one('module', string='Module ID', required=True)
    element_id = fields.Char(string='Element name')
    filiere_id = fields.Many2one('filiere', string='Filiere ID', required=True)
    teacher_id = fields.Many2one('teacher', string='Teacher ID', required=True)
    module_count = fields.Integer(string='Modules')

    element_hours = fields.Integer(string='Element Hours')

    module_hours = fields.Integer(compute='_compute_module_hours',
                                  string='Module Hours')
    element_coeff = fields.Float(string='Element coefficient')

    @api.depends('element_hours')
    def _compute_module_hours(self):
        for record in self:
            record.module_hours = sum(
                record.module_id.semester_ids.search([
                    '&', ('module_id', '=', record.module_id.id),
                    ('filiere_id', '=', record.filiere_id.id)
                ]).mapped('element_hours'))
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    def _check_semesters(self, record, semesters):
        # for s1 in semesters:
        for s2 in semesters:
            if record.id.origin != s2.id:
                if record.name == s2.name and record.module_id == s2.module_id and record.element_id == s2.element_id and record.filiere_id == s2.filiere_id:
                    raise ValidationError(
                        'You cannot have the same element and module in the same semester for the same filiere'
                    )
                if record.name == s2.name and record.filiere_id == s2.filiere_id and record.module_count != s2.module_count:
                    raise ValidationError(
                        'You cannot have a different number of modules for the same semester'
                    )

    @api.onchange('name', 'module_id', 'element_id', 'filiere_id',
                  'element_coeff','module_count')
    def onchange_validate(self):
        for record in self:
            semester_ids = self.env['semester'].search([
                '&', ('name', '=', record.name),
                ('filiere_id', '=', record.filiere_id.id)
            ])
            self._check_semesters(record, semester_ids)

    # @api.depends('name')
    # def _compute_module_ref(self):
    #     j=1
    #     for record in self:
    #         tab=self.env['semester'].search(['&',('name','=',record.name),('filiere_id','=',record.filiere_id.id)])
    #         tab2=[t.module_ref for t in tab]
    #         tab2.sort()
    #         print(tab2)
    #         # print(self.env['semester'].search(['&',('name','=',record.name),('filiere_id','=',record.filiere_id.id)],order='name desc'))
    #         # if not record.filiere_id.id in tab:
    #         #     semesters = self.env['semester'].sudo().search([('filiere_id','=',record.filiere_id.id)],order='name')
    #         #     i=1
    #         #     for s in semesters:
    #         #         s.sudo().write({'module_ref':'M{}'.format(i)})
    #         #         i+=1
    #         # tab.append(record.filiere_id.id)
    #         # modules_list = self.env['module'].search([])
    #         # for m in modules_list:
    #         #     print(m.semester_ids.search(['&',('name','=',record.name),('filiere_id','=',record.filiere_id.id)]))
    #         # print(modules_list)
    #         if len(tab2)==0 or any(t==False for t in tab2):
    #             record.module_ref = 'M1'
    #         else:
    #             record.module_ref = 'M{}'.format((int(tab2[-1][1])+1))

    # @api.onchange('module_id', 'element_id', 'filiere_id', 'name')
    # def onchange_module_id(self):
    #     semesters = self.env['semester'].search([])
    #     # print(semesters)
    #     for record in self:
    #         for s in semesters:
    #             if record.id.origin!=s.id :
    #                 if record.name == s.name:
    #                     if record.module_id.id == s.module_id.id:
    #                         if s.element_id.id == record.element_id.id:
    #                             if (record.filiere_id.id == s.filiere_id.id or s.filiere_id.id == record.filiere_id.id.origin):
    #                                 print('there are equal--------')
    # print(
    #     any(record != s and record.name == s.name and record.module_id == s.module_id and s.element_id == record.element_id and record.filiere_id == s.filiere_id for s in semesters))
