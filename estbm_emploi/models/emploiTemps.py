# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EmploiTemps(models.Model):
    _name = 'emploi.temps'
    _description = 'Emploi Temps'

    name = fields.Char(compute='_compute_name', string='name')

    @api.depends('name')
    def _compute_name(self):
        for record in self:
            year = '1ére Année' if record.class_id.year == '1' else '2ème Année'
            # record.name = 'hello'
            record.name = '{}-{}-{}'.format(
                record.class_id.filiere_id.name, year,record.semester)
            if record.groupe_id:
                record.name += '-{}'.format(record.groupe_id.name)
            # record.name = 'Emploi de temps de {}'.format(record.class_id.name)

    class_id = fields.Many2one('classe',
                               string='Target Class',
                            #    ondelete='cascade',
                               required=True)

    # class_list = fields.One2many('classe',
    #                              'emploi_id',
    #                              string='List of Classes')

    year = fields.Selection(related='class_id.year', string="Year")

    semester = fields.Char(related='class_id.semester', string='Semester')
    # semester = fields.Selection(related='class_id.semester', string="Semester")
    # dept_id = fields.Char(compute='_compute_dept_id', string='Department ID')

    # @api.depends('class_list')
    # def _compute_dept_id(self):
    #     for record in self:
    #         if len(record.class_list) > 0:
    #             record.dept_id = record.class_list[0].filiere_id.dept_id.name
    #         else:
    #             record.dept_id = None

    # dept_id = fields.Many2one(related='class_list.filiere_id.dept_id',
    #                           string="Department ID")

    college_year = fields.Char(
        string='Anne Universitaire',
        default='%s/%s' %
        (fields.date.today().year - 1, fields.date.today().year),
        readonly=True)

    start_date = fields.Date(string='The start date', required=True)
    
    total_hours = fields.Integer(compute='_compute_total_hours', string='Total Hours')
    
    # emploi_days = []
    # emploi_days = [record.day_0,record.day_1,record.day_2,record.day_3,record.day_4,record.day_5]
    
    
    @api.depends('day_0','day_1','day_2','day_3','day_4','day_5')
    def _compute_total_hours(self):
        for record in self:
            # record.emploi_days = [record.day_0,record.day_1,record.day_2,record.day_3,record.day_4,record.day_5]
            tab=[]
            tab.append(sum(record.day_0.mapped('temps_id').mapped('duration')))
            tab.append(sum(record.day_1.mapped('temps_id').mapped('duration')))
            tab.append(sum(record.day_2.mapped('temps_id').mapped('duration')))
            tab.append(sum(record.day_3.mapped('temps_id').mapped('duration')))
            tab.append(sum(record.day_4.mapped('temps_id').mapped('duration')))
            tab.append(sum(record.day_5.mapped('temps_id').mapped('duration')))
            record.total_hours = sum(tab)
            print(sum(tab))
    


    def _string_to_datetime(self, str):
        date1, date2 = str.split('-')
        date1 = fields.datetime.strptime(date1, '%H:%M')
        date2 = fields.datetime.strptime(date2, '%H:%M')
        return [date1, date2]

    def _check_days(self, day, day_num):
        for jour in day:
            for j in day:
                if j!=jour:
                    if self._string_to_datetime(j.temps_id.name)[0]<=self._string_to_datetime(jour.temps_id.name)[0]<=self._string_to_datetime(j.temps_id.name)[1]:
                        raise ValidationError('You cannot have 2 sessions with the same date and time!!!!')

        # test if there have the same temps_id
        tab = day
        res = [t.temps_id.id for t in tab]
        if len(res) != len(set(res)):
            raise ValidationError(
                'You cannot have 2 sessions with the same date and time!!!')

    day_0 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 0',
                            domain=[('day', '=', '0')])

    @api.onchange('day_0')
    def onchange_day_0(self):
        for record in self:
            record._check_days(record.day_0, '0')

    # @api.constrains('day_0')
    # def _check_day_0(self):
    #     for record in self:
    #         record._check_days(record.day_0,'0')

    # @api.onchange('day_0')
    # def onchange_day_0(self):
    #     return {'domain': {'day_0': [('temps_id', '=', False)]}}

    day_1 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 1',
                            domain=[('day', '=', '1')])

    @api.onchange('day_1')
    def onchange_day_1(self):
        for record in self:
            record._check_days(record.day_1, '1')

    # @api.onchange('day_1')
    # def onchange_day_1(self):
    #     print('hello--------------ayoub')
    # return {'domain': {'day_0': [('temps_id', '=', 1)]}}

    day_2 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 2',
                            domain=[('day', '=', '2')])

    @api.onchange('day_2')
    def onchange_day_2(self):
        for record in self:
            record._check_days(record.day_2, '2')

    day_3 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 3',
                            domain=[('day', '=', '3')])

    @api.onchange('day_3')
    def onchange_day_3(self):
        for record in self:
            record._check_days(record.day_3, '3')

    day_4 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 4',
                            domain=[('day', '=', '4')])

    @api.onchange('day_4')
    def onchange_day_4(self):
        for record in self:
            record._check_days(record.day_4, '4')

    day_5 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 5',
                            domain=[('day', '=', '5')])

    @api.onchange('day_5')
    def onchange_day_5(self):
        for record in self:
            record._check_days(record.day_5, '5')

    day_6 = fields.One2many('seance.jour',
                            'emploi_id',
                            string='Emploi Day 6',
                            domain=[('day', '=', '6')])

    @api.onchange('day_6')
    def onchange_day_6(self):
        for record in self:
            record._check_days(record.day_6, '6')
            
    groupe_id = fields.Many2one('groupe', string='Groupe ID')
    
    has_groupe = fields.Boolean(string='Specifie a Group',required=True)
    




class Classe(models.Model):
    
    _inherit = 'classe'
    
    emploi_ids = fields.One2many(comodel_name='emploi.temps',inverse_name='class_id',string='Emploi Temp')
    
class Student(models.Model):
    
    _inherit = 'student'
    
    emploi_ids = fields.One2many(related='class_id.emploi_ids',string='Sessions')
    
    
    
class Groupe(models.Model):
    
    _inherit = 'groupe'
    
    emploi_id = fields.Many2one( 'emploi.temps', compute='compute_emploi_temps', inverse='gropue_inverse',string='Emploi ID')
    emploi_ids = fields.One2many('emploi.temps', 'groupe_id')

    @api.depends('emploi_ids')
    def compute_emploi_temps(self):
        self.ensure_one()
        if len(self.emploi_ids) > 0:
            self.emploi_id = self.emploi_ids[0]

    def gropue_inverse(self):
        self.ensure_one()
        if len(self.emploi_ids) > 0:
            # delete previous reference
            asset = self.env['emploi.temps'].browse(self.emploi_ids[0].id)
            asset.groupe_id = False
        # set new reference
        self.emploi_id.groupe_id = self