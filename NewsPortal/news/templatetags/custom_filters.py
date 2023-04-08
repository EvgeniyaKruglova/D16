from django import template


register = template.Library()

BAD_WORDS = ['вредная','плохая','драла','бор']

@register.filter()
def censor (value):
    if isinstance (value,str):
        for bw in BAD_WORDS:
            value = value.lower().replace(bw[1:].lower(),'*'*len(bw[1:]))
        return f'{value} '
    else:
        raise TypeError (f'Ошибка! {type(value)} не подходит')
