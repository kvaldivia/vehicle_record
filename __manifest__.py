# -*- coding: utf-8 -*-
{
    'name': "vehicle_record",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kenny Valdivia",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/vehicle_record_security.xml',
        'data/vehicle_status_cron.xml',
        'views/assets.xml',
        'views/vehicle_record_views.xml',
        'views/vehicle_record_vehicle_views.xml',
        'views/vehicle_record_vehicle_maintenance_views.xml',
    ],
    'css': ['static/src/less/vehicle_record.css'],
    'installable': True,
    'auto_install': False,
    'application': True
}
