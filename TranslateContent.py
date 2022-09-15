import asyncio
from functools import partial, wraps
from googletrans import Translator
import json

class TranslateContent:
    key: str = ''
    content: str = ''
    isComment: bool = False
    translator = Translator()
    translatedContentsIOS = dict()
    translatedContentsAndroid = dict()
    
    def __init__(self, line: str):
        self.translatedContentsIOS = dict()
        self.translatedContentsAndroid = dict()
        if line.startswith('/*') or line.startswith('//'):
            self.key = line[:-1]
            self.isComment = True
            return
        
        parts = line.split(' = ')
        self.key = parts[0][1:].split("\"")[0]
        self.content = parts[1][1:].split("\"")[0]
        self.translatedContentsIOS['en'] = self.content
        self.translatedContentsAndroid['en'] = self.content
       
        #print(type(self.translatedContents))
        #print(json.dumps(self.translatedContents, indent = 4))
        #print(self.translatedContents)
    
    # "log_in" = "Log In"
    def outputTranslateIOS(self, language: str):
        if (self.isComment):
            return self.key
        result = self.translator.translate(self.content, dest=language, src='en')
        return f"\"{self.key}\" = \"{result.text}\";"
    
    # <string name="log_in">Log In</string>
    def outputTranslateAndroid(self, language: str):
        if (self.isComment):
            return self.key
        result = self.translator.translate(self.content, dest=language, src='en')
        return f"<string name=\"{self.key}\">{result.text}</string>"
        
    def translate(self, language: str):
        if (self.isComment):
            self.translatedContentsIOS[language] = self.key
            self.translatedContentsAndroid[language] = self.key
            return
        result = self.translator.translate(self.content, dest=language, src='en')
        self.translatedContentsIOS[language] = f"\"{self.key}\" = \"{result.text}\";"
        self.translatedContentsAndroid[language] = f"<string name=\"{self.key}\">{result.text}</string>"
        
    def async_wrap(func):
        @wraps(func)
        async def run(*args, loop=None, executor=None, **kwargs):
            if loop is None:
                loop = asyncio.get_event_loop()
            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return run 
        
    translateAsync = async_wrap(translate)
    
    def resultContent(self, language: str, platform: str):
        if (self.isComment):
            return self.key
        
        if (platform == "ios"):
            return self.translatedContentsIOS[language]
        
        return self.translatedContentsAndroid[language]

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}