# -*- coding: utf-8 -*-

{
    'name': "Abilium Meeting Scheduler",

    'summary': """
        Software to schedule meetings""",

    'description': """
        This software facilitates the scheduling of meetings
    """,

    'author': "PSE-Team",
    'website': "https://www.abilium.io/",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'calendar', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/group_wizard_views.xml',
        'wizard/timeslots_reserved_wizard_views.xml'
    ],

    'demo': [
        #'demo/demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': '0',
}
