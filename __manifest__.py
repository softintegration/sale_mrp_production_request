# -*- coding: utf-8 -*- 


{
    'name': 'Link Sale and Mrp Production request',
    'author': 'Soft-integration',
    'application': True,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.3',
    'category': 'Sale/Manufacturing',
    'demo': [],
    'depends': ['sale','mrp_production_request'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/mrp_production_request_views.xml',
        'wizard/production_requests_create_views.xml'
    ],
    'license': 'LGPL-3',
}
