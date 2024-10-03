{
    'name': "calendarioEmplatados",
    'summary': "Prueba calendario",
    'description': "Prueba de calendario para Emplatados Web",
    'category': 'Tools',
    'author': "Marina",
    'website': "http://www.sistelin.es",
    'version': '1.1',
    'depends': ['base', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/calendario_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css',
            'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js',
            'calendarioEmplatados/static/src/css/styles.css',
            'calendarioEmplatados/static/src/js/custom_area.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}

