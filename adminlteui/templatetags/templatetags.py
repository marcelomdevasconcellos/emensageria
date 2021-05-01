from django import template

register = template.Library()


@register.filter('test')
def test(obj):
    try:
        print()
        print(obj.widget.__dict__)
    except:
        pass
    return ''


@register.filter('div_cols')
def div_cols(field):
    if not field.is_readonly:
        if 'cols' in field.field.form.Meta.model.__dict__ \
            and field.field.name in field.field.form.Meta.model.cols:
            return field.field.form.Meta.model.cols[field.field.name]
    else:
        if 'cols' in field.model_admin.model.__dict__ \
            and field.field['name'] in field.model_admin.model.cols:
            return field.model_admin.model.cols[field.field['name']]
    return 3
