from adminlteui.core import AdminlteConfig, MenuItem


# https://github.com/wuyue92tree/django-adminlte-ui/blob/master/docs/en/guide.md
class MyAdminlteConfig(AdminlteConfig):
    copyright = "Marcelo Vasconcellos"
    search_form = False
    welcome_sign = 'Seja bem-vindo'
    main_menu = [
        MenuItem(
            label='esocial.Certificados',
            name='Certificados',
            menu_type='model',
            icon="fa-certificate",
            url="#"),
        MenuItem(
            label='esocial.Eventos',
            name='Eventos',
            menu_type='model',
            icon="fa-file-o",
            url="#"),
        MenuItem(
            label='esocial.Transmissor',
            name='Transmissores',
            menu_type='model',
            icon="fa-send-o",
            url="#"),
        MenuItem(
            label='esocial.TransmissorEventos',
            name='Lotes',
            menu_type='model',
            icon="fa-arrow-circle-right",
            url="#"),
        MenuItem(
            label='autenticacao',
            name='Controle de acesso',
            icon='fa-key',
            child=[
                MenuItem(
                    label='auth.Group',
                    name='Grupos',
                    menu_type='model',
                    icon="fa-users",
                    url="#"),
                MenuItem(
                    label='authtoken.Token',
                    name='Token',
                    menu_type='link',
                    icon="fa-asterisk",
                    url="/authtoken/tokenproxy/"),
                MenuItem(
                    label='users.User',
                    name='Usuários',
                    menu_type='model',
                    icon="fa-user", url="#"),
            ]),
    ]
