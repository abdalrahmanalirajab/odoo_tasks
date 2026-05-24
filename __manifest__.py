{
    'name': 'Hospital Management System',
    'version': '2.0',
    'summary': 'Manage hospital patients, departments and doctors',
    'author': 'OSD',
    'category': 'Healthcare',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctors_views.xml',
        'views/hms_menus.xml',
    ],
    'installable': True,
    'application': True,
}

