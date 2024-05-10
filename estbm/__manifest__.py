# -*- coding: utf-8 -*-
{
    'name': "estbm",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/student.xml',
        'views/filiere.xml',
        'views/classe.xml',
        'views/teacher.xml',
        'views/chefFiliere.xml',
        'views/module.xml',
        'views/absence.xml',
        #'views/elements.xml',
        'views/semester.xml',
        'reports/student_id_card_template.xml',
        'reports/filiere_sheet_card_template.xml',
        'reports/reports.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
