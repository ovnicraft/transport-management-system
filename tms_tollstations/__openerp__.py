# -*- coding: utf-8 -*-
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Highway tollstations",
    'summary': "Highway tollstations",
    "author": "Jarsa Sistemas",
    "website": "https://www.jarsa.com.mx",
    'category': 'Transport',
    'version': '9.0.0.1.0',
    'depends': ['tms'],
    "license": "AGPL-3",
    'data': [
        'views/tms_expense_line_view.xml',
        'views/tms_toll_data_view.xml',
        'views/fleet_vehicle_view.xml',
        'wizards/tms_toll_import.xml',
        'reports/report_highway.xml',
    ],
    "installable": True,
}
