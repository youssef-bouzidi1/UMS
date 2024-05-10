# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import calendar
from datetime import datetime

from numpy import record 
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

week_days = [(calendar.day_name[0], _(calendar.day_name[0])),
             (calendar.day_name[1], _(calendar.day_name[1])),
             (calendar.day_name[2], _(calendar.day_name[2])),
             (calendar.day_name[3], _(calendar.day_name[3])),
             (calendar.day_name[4], _(calendar.day_name[4])),
             (calendar.day_name[5], _(calendar.day_name[5])),
             (calendar.day_name[6], _(calendar.day_name[6]))]


class Seance(models.Model):
    _name = 'seance'
    _description = 'Seance Information'

    name = fields.Char(compute='_compute_name', string='name')

    @api.depends('name')
    def _compute_name(self):
        self.name = 'hello'

    element_id = fields.Many2one('element.module', string='Element Module')
    teacher_id = fields.Many2one('teacher', string='Teacher')
    temps_id = fields.Many2one('seance.temps',string='Temps ID')
    # jour_ids = fields.Many2many('seance.jour',
    #                             'seance_jour_rel',
    #                             'seance_id',
    #                             'jour_id',
    #                             string='List of Days')



class SeanceJour(models.Model):
    _name = 'seance.jour'
    _description = 'Seance Jour'

    day = fields.Selection([
        ('0', calendar.day_name[0]),
        ('1', calendar.day_name[1]),
        ('2', calendar.day_name[2]),
        ('3', calendar.day_name[3]),
        ('4', calendar.day_name[4]),
        ('5', calendar.day_name[5]),
        ('6', calendar.day_name[6]),
    ],
                           'Day',
                           required=True)
    emploi_id = fields.Many2one('emploi.temps',string='Emploi ID',required=True)
    element_id = fields.Many2one('element.module', string='Element Module',required=True)
    teacher_id = fields.Many2one('teacher', string='Teacher',required=True)
    temps_id = fields.Many2one('seance.temps',string='Temps ID',required=True)
    start_time = fields.Datetime(string='Start Time',related='temps_id.start_time',readonly=True)


class SeanceTemps(models.Model):
    _name = 'seance.temps'
    _description = 'Seance Temps'

    name = fields.Char(compute='_compute_name', string='Name')

    @api.depends('name')
    def _compute_name(self):
        for record in self:
            record.name= '{}:{}-{}:{}'.format(record.start_hour,record.start_minute,record.end_hour,record.end_minute)

    start_hour = fields.Selection(selection=[
            ('8' ,'8' ),
            ('9' ,'9' ),
            ('10','10'),
            ('11','11'),
            ('12','12'),
            ('13','13'),
            ('14','14'),
            ('15','15'),
            ('16','16'),
            ('17','17'),
        ],string='Start Hour',required=True)
    
    
    
    start_minute = fields.Selection([('00', '00'), ('30', '30')],
                              'Start Minute',
                              required=True)
    start_time = fields.Datetime(compute='_compute_start_time', string='start time')
    
    @api.depends('start_hour','start_minute')
    def _compute_start_time(self):
        for record in self:
            record.start_time = None
            if record.start_hour and record.start_minute:
                t = '{}:{}'.format(record.start_hour,record.start_minute)
                record.start_time = datetime.strptime(t,'%H:%M')
                # record.start_time = fields.datetime.strptime(t,'%H:%M')
    
    
    end_hour = fields.Selection(selection=[
            ('9' ,'9' ),
            ('10','10'),
            ('11','11'),
            ('12','12'),
            ('13','13'),
            ('14','14'),
            ('15','15'),
            ('16','16'),
            ('17','17'),
            ('18','18'),
        ],string='End Hour',required=True)
    
    end_minute = fields.Selection([('00', '00'), ('30', '30')],
                              'End Minute',
                              required=True)
    
    
    duration = fields.Float(compute='_compute_duration', string='duration',readonly=True)
    
    @api.depends('start_hour','start_minute','end_hour','end_minute')
    def _compute_duration(self):
        for record in self:
            if record.start_hour and record.end_hour and record.start_minute and record.end_minute:
                start_time = '{}:{}'.format(record.start_hour,record.start_minute)
                end_time = '{}:{}'.format(record.end_hour,record.end_minute)
                d1 = datetime.strptime(start_time,'%H:%M')
                d2 = datetime.strptime(end_time,'%H:%M')
                res = d2-d1
                minutes = res.total_seconds()/3600
                if minutes<=0:
                    raise ValidationError('The end time is greater then the start time!!!')
                record.duration = minutes
                # print(start_time,end_time,record.duration)
            else:
                record.duration = None
    
    # duration = fields.Float('Duration')
    # seance_id = fields.Many2one('seance',string='Seance ID')
    # jour_id = fields.Many2one('seance.jour',string='Jour ID')
    
    
    
    
class Teacher(models.Model):
    
    _inherit = 'teacher'
    
    seance_ids = fields.One2many('seance.jour','teacher_id',string='List of Sessions')
    
    
