{
    'name': 'Custom File Manager',
    'version': '1.0',
    'summary': 'Manages Files within Odoo',
    'sequence': 10,
    'description': """Custom module to manage files""",
    'category': 'Tools',
    'website': 'https://www.yourcompany.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/file_manager_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
