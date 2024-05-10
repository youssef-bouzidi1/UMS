# -*- coding: utf-8 -*-
# from odoo import http


# class Estbm(http.Controller):
#     @http.route('/estbm/estbm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estbm/estbm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('estbm.listing', {
#             'root': '/estbm/estbm',
#             'objects': http.request.env['estbm.estbm'].search([]),
#         })

#     @http.route('/estbm/estbm/objects/<model("estbm.estbm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estbm.object', {
#             'object': obj
#         })
