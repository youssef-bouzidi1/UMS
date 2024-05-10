
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class ayoub(models.Model):
    _name = 'ayoub'
    _description = 'ayoub'


    name = fields.Char(
        string='Name',
        required=True,
    )

    def print_ayoub(self):
        print('hello from the scheduled action ----------------------------------')
