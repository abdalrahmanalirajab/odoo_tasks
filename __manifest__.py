# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management System',
    'version': '19.0.2.0.0',
    'category': 'Healthcare',
    'summary': 'HMS with user groups, security rules, and patient reports',
    'author': 'OSD',
    'license': 'LGPL-3',

    'depends': ['base', 'crm', 'contacts'],

    'data': [
        # Security must load first
        'security/hms_groups.xml',
        'security/ir.model.access.csv',
        'security/hms_security_rules.xml',

        # Views
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/customer_views.xml',
        'views/menus.xml',

        # Reports
        'reports/patient_report.xml',
        'reports/patient_report_template.xml',
    ],

    'installable': True,
    'application': True,
}