{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage hospital patients data',
    'description': 'HMS module to manage patients in a hospital system.',
    'author': 'OSD',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/hms_menus.xml',
    ],
    'installable': True,
    'application': True,
}