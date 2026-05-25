
{
    'name': 'Hospital Management System',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Manage patients, departments, doctors and CRM integration',
    'author': 'OSD',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'contacts',
        'account',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctors_views.xml',
        'views/customer_views.xml',
        'views/hms_menus.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}