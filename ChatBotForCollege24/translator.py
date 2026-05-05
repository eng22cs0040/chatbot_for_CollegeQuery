from googletrans import Translator
from langdetect import detect

translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_english(text):
    return translator.translate(text, dest='en').text

def translate_from_english(text, lang):
    return translator.translate(text, dest=lang).text