# -*- coding: utf-8 -*-

{
    'name': "Abilium Meeting Scheduler",

    'summary': """
        Software to schedule meetings""",

    'description': """
        This software facilitates the scheduling of meetings
    """,

    'author': "PSE-Team",
    # 'icon': 'static/description/icon.png',  #icon will not show in appslist when using this command
    'website': "https://www.abilium.io/",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'calendar', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/group_wizard_views.xml',
        'wizard/timeslots_reserved_wizard_views.xml',
        'wizard/send_guest_view_to_guest_wizard_views.xml',
        'views/views.xml'
    ],

    'demo': [
        #'demo/demo.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': '0',
}
