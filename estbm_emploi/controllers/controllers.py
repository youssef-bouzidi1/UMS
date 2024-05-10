# -*- coding: utf-8 -*-
# from odoo import http


# class EstbmEmploi(http.Controller):
#     @http.route('/estbm_emploi/estbm_emploi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estbm_emploi/estbm_emploi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('estbm_emploi.listing', {
#             'root': '/estbm_emploi/estbm_emploi',
#             'objects': http.request.env['estbm_emploi.estbm_emploi'].search([]),
#         })

#     @http.route('/estbm_emploi/estbm_emploi/objects/<model("estbm_emploi.estbm_emploi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estbm_emploi.object', {
#             'object': obj
#         })
