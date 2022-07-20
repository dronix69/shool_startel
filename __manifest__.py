{
    'name': "Shool_Startel",
    'version': '15.0.4.0.0',
    'sequence': 1,
    'summary': """
        Módulo CRM para la gestión de registro escuela conductores""",

    'description': """
        Módulo CRM para la gestión de registro escuela conductores...
    """,

    'author': "Daniel Ferrada",
    'website': "http://startel.cl",
    
    'category': 'Escuela de Conduccion',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'sale_management', 'hr', 'mail'],

    # always loaded
    'data': [
        'security/certificado_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/templates_nomina.xml',
        'report/templates_card.xml',
        'report/templates_contrato.xml',
        'report/templates_certificado.xml',
        'report/templates_practica.xml',
        'views/views_certificado.xml',
        'views/views_menu.xml',
        'views/views_cursos.xml',
        'views/inherit_respartner.xml',
        'views/inherit_sale.xml',
        'views/views_simulador.xml',
        'views/views_practicas.xml',
        'views/views_compras.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_qweb':['shool_startel/static/src/xml/digital_signs.xml'],
        'web.assets_backend': ['shool_startel/static/src/js/digital_signs.js'],
    }
}
