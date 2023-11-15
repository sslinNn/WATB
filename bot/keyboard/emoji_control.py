import emoji


def remove_emojis(text):
    text_without_emojis = emoji.replace_emoji(text, replace='')
    return text_without_emojis

