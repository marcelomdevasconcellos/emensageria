from django.urls import reverse
from django import template

register = template.Library()


@register.filter('test')
def test(obj):
    try:
        print()
        print(obj.__dict__)
    except:
        print('erro')
    return ''


@register.filter('to_slug')
def to_slug(txt):
    from slugify import slugify
    return slugify(txt)


@register.filter('to_str')
def to_str(int):
    return str(int)


@register.filter('minus_one')
def minus_one(obj):
    return int(obj) - 1


@register.filter('div_cols')
def div_cols(field):
    COLUMN_DEFAULT = 4
    if not field.is_readonly:
        if field.field.name == 'permissions':
            return 8
        elif 'cols' in field.field.form.Meta.model.__dict__ \
                and field.field.name in field.field.form.Meta.model.cols:
            return field.field.form.Meta.model.cols[field.field.name]
    else:
        if field.field.get('name') == 'permissions':
            return 8
        elif 'cols' in field.model_admin.model.__dict__ \
                and field.field['name'] in field.model_admin.model.cols:
            return field.model_admin.model.cols[field.field['name']]
    return COLUMN_DEFAULT


@register.filter('input_type')
def input_type(ob):
    '''
    Extract form field type
    :param ob: form field
    :return: string of form field widget type
    '''
    return ob.field.widget.__class__.__name__


@register.filter(name='add_classes')
def add_classes(value, arg):
    '''
    Add provided classes to form field
    :param value: form field
    :param arg: string of classes seperated by ' '
    :return: edited field
    '''
    css_classes = value.field.widget.attrs.get('class', '')
    # check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    # prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    # join back to single string
    return value.as_widget(attrs={'class': ' '.join(css_classes)})


@register.filter(name='get_add_link')
def get_add_link(value):
    # assistidosprocessos_processo-0-assistido
    if 'assistidosprocessos_assistido' in value:
        return '/admin/atendimento/processos/add/?_popup=1'
    elif 'assistidosprocessos_processo' in value:
        return '/admin/atendimento/assistidos/add/?_popup=1'
    return None


@register.filter(name='get_edit_link')
def get_edit_link(value):
    # assistidosprocessos_processo-0-assistido
    if 'assistidosprocessos_assistido' in value:
        return '/admin/atendimento/processos/add/?_popup=1'
    elif 'assistidosprocessos_processo' in value:
        return '/admin/atendimento/assistidos/add/?_popup=1'
    return None


@register.filter(name='can_edit')
def can_edit(value):
    # assistidosprocessos_processo-0-assistido
    if 'assistidosprocessos_assistido' in value:
        return False
    elif 'assistidosprocessos_processo' in value:
        return False
    return True


@register.filter(name='iframe')
def iframe(value):
    import urllib
    return urllib.request.urlopen(value).read()
