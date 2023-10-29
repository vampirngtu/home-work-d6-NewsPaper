from django import template

register = template.Library()

@register.filter(name='censor')
def censor(text):
    if isinstance(text, str):
        stop_word = ['бля','Бля','БЛЯ']
        text_word = text.split()
        text_censor = []
        for word in text_word:
            if word not in stop_word:
                text_censor.append(word)
        return ' '.join(text_censor)
    else:
        raise ValueError(f'{type(text)} не является строкой')