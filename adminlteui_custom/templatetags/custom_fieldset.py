from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter('div_name')
def div_name(
        name):
    if name:
        name = name.replace(' ', '_')
        return name.lower() + '_div'
    else:
        return "main_div"


@register.filter('not_none')
def not_none(
        obj):
    if obj is None:
        return "-"
    return obj


@register.filter('test')
def test(
        obj):
    try:
        print(obj.__dict__)
    except Exception as e:
        print('erro:', e)
    return ''


@register.filter('tab_organize')
def tab_organize(
        modelName):
    try:
        if modelName.tab:
            return False
    except Exception as e:
        print('erro:', e)
        return True


@register.filter('to_slug')
def to_slug(
        txt):
    return slugify(txt)


@register.filter('to_str')
def to_str(
        int):
    return str(int)


@register.filter('bootstrap_cols_number')
def bootstrap_cols_number(
        field):
    # Example: <div class="col-md-{{ field|bootstrap_cols_number }}">
    COLUMN_DEFAULT = 4
    if not field.is_readonly:
        if 'cols' in field.field.form.Meta.model.__dict__ \
                and field.field.name in field.field.form.Meta.model.cols:
            return field.field.form.Meta.model.cols[field.field.name]
    else:
        if 'cols' in field.model_admin.model.__dict__ \
                and field.field['name'] in field.model_admin.model.cols:
            return field.model_admin.model.cols[field.field['name']]
    return COLUMN_DEFAULT
