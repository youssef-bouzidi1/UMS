
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class Test1(models.Model):
    _name = 'test1'
    _description = 'Test'


    name = fields.Char(
        string='Name',
        required=True,
    )
    
    ele_id = fields.Many2one('element.module',string='ayoub ID')

    

