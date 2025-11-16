from deep_translator import GoogleTranslator

class Translator:
    @classmethod
    def translatePlainText(cls, msg, source='en', target='pt'):
        return GoogleTranslator(source=source, target=target).translate(msg)