from django import template
from .bad_words import BAD_WORDS

register = template.Library()


@register.filter()
def filter_message(message: str):
    bad_words = BAD_WORDS

    words = message.split()
    filtered_words = []

    for word in words:
        cleaned_word = ''.join(char for char in word if char.isalnum()).lower()
        if cleaned_word in bad_words:
            masked_word = word[0] + ('*' * (len(word)-1))
            filtered_words.append(masked_word)
        else:
            filtered_words.append(word)

    return ' '.join(filtered_words)
