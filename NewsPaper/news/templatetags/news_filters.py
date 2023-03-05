from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value, arg='<banned>'):
    banned_words = [ 'пиздец', 'fuck', 'fucking', 'блядь', 'писец']
    if isinstance(value, str) and isinstance(arg, str):
        for i in banned_words:
            value = value.replace(i, arg)
        return value
    else:
        raise ValueError(f'Не применяется для {type(value)} и {type(arg)}')




