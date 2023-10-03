from deep_translator import GoogleTranslator


def run_translate(phrase, from_lang, to_lang):
    translated = GoogleTranslator(source=from_lang, target=to_lang).translate(phrase)
    return translated
