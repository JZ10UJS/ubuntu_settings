# -*- coding: utf-8 -*-
{
    'name': "button_notify",

    'summary': """
        完成button调用后，右上角出现提示信息""",

    'description': """
        完成button调用后，右上角出现提示信息
    """,

    'author': "Zhang Jie",
    'website': "http://www.bankcall.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [
        'templates.xml',
    ],
    'qweb': ['static/*.xml'],
}
