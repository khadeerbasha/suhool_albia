# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Added Slip Reference in Warehouse Operations',
    'version': '14.0',
    'category': 'Stock',
    'description': """Added Slip Reference in Warehouse Operations""",
    'depends': ['stock','account'],
    'data': ['views/slip_ref_views.xml'],
    'installable': True,
    'auto_install': True,
}
