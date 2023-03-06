# just a local note: remember to use python 3 -m pip to instal lib, this is only way to recognize the library
import asyncio
from functools import partial, wraps
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             MyMemoryTranslator)
from GGTransLanguage import GGTRANS_LANGUAGE
from GeneratorConfig import GeneratorConfig
from MMTransLanguage import MMTRANS_LANGUAGE
from MSTransLanguage import MSTRANS_LANGUAGE

class TranslateContent:
    key: str = ''
    content: str = ''
    isComment: bool = False
    translatedContentsIOS = dict()
    translatedContentsAndroid = dict()
    config = GeneratorConfig.shared()
    
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
                 
    def translateWithGoogle(self, language: str):
        if (self.isComment):
            self.translatedContentsIOS[language] = self.key
            self.translatedContentsAndroid[language] = self.key
            return
        try:  
            translator: GoogleTranslator = GoogleTranslator(source='auto', target=language)
            result = translator.translate(text=self.content)
            self.setResult(language, result)
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
            print("try again with translator")
          
    def translateWithMymemory(self, language: str):
        if (self.isComment):
            self.translatedContentsIOS[language] = self.key
            self.translatedContentsAndroid[language] = self.key
            return
        try: 
            ggLanguage = GGTRANS_LANGUAGE[language].replace("(", '').replace(')', '').lower() # remove () for matching
            mmKey = ""
            for key in MMTRANS_LANGUAGE:
                #print(f"gg:{ggLanguage} ggL:{GGTRANS_LANGUAGE[language]} ms:{key} mmL:{MMTRANS_LANGUAGE[mmKey]}")
                if (ggLanguage in key or key in ggLanguage or MMTRANS_LANGUAGE[key] == language):
                    mmKey = key
                    break
            #print("end find")    
            
            mmLanguage = MMTRANS_LANGUAGE[mmKey]
            translator: MyMemoryTranslator  = MyMemoryTranslator(source='en', target=mmLanguage)
            result = translator.translate(text=self.content)
            self.setResult(language, result)
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
            print("try again with translator")
            
    # https://learn.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-translate
    def translateWithMicrosoft(self, language: str):
        if (self.isComment):
            self.translatedContentsIOS[language] = self.key
            self.translatedContentsAndroid[language] = self.key
            return
        
        try: 
            ggLanguage = GGTRANS_LANGUAGE[language].replace("(", '').replace(')', '').lower() # remove () for matching
            msKey = ""
            
            #print("begin find")
            # find equal language key in ms language
            for key in MSTRANS_LANGUAGE:
                #print(f"gg:{ggLanguage} ggL:{GGTRANS_LANGUAGE[language]} ms:{key} msL:{MSTRANS_LANGUAGE[msKey]}")
                if (ggLanguage in key or key in ggLanguage or MSTRANS_LANGUAGE[key] == language):
                    msKey = key
                    break
            #print("end find")    
            
            msLanguage = MSTRANS_LANGUAGE[msKey]
            translator = MicrosoftTranslator(
                api_key= self.config.microsoftTranslatorKeys[0], 
                region= self.config.microsoftTranslatorRegion, 
                source="en", target=msLanguage)
            result = translator.translate(text=self.content)
            self.setResult(language, result)
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
            print(f"error when tranlate to {language} try again with translator")
            
    def translateWithMicrosoftMultikeys(self, language: str):
        if (self.isComment):
            self.translatedContentsIOS[language] = self.key
            self.translatedContentsAndroid[language] = self.key
            return
        
        ggLanguage = GGTRANS_LANGUAGE[language].replace("(", '').replace(')', '').lower() # remove () for matching
        msKey = ""
            
        #print("begin find")
        # find equal language key in ms language
        for key in MSTRANS_LANGUAGE:
            #print(f"gg:{ggLanguage} ggL:{GGTRANS_LANGUAGE[language]} ms:{key} msL:{MSTRANS_LANGUAGE[msKey]}")
            if (ggLanguage in key or key in ggLanguage or MSTRANS_LANGUAGE[key] == language):
                msKey = key
                break
        #print("end find")    
        
        msLanguage = MSTRANS_LANGUAGE[msKey]
        
        for (index, itemKey) in enumerate(self.config.microsoftTranslatorKeys):
            isSuccess = False
            try: 
                translator = MicrosoftTranslator(
                api_key=itemKey, 
                region= self.config.microsoftTranslatorRegion, 
                source="en", target=msLanguage)
                result = translator.translate(text=self.content)
                self.setResult(language, result)
                isSuccess = True
                # print(f"TRANSLATE SUCCESSFUL MS key: {itemKey} when translate to {language} with content {self.content}")
            except Exception as e:
                nextIndex = index + 1 < len(self.config.microsoftTranslatorKeys) and index + 1 or -1
                nextIndexDescription = nextIndex != -1 and f"try again with next key f{self.config.microsoftTranslatorKeys[nextIndex]}" or ""
                # print(f"HANDLE ERROR: Error at MS key: {itemKey} when translate to {language} with content {self.content} ,{nextIndexDescription} \nDETAIL: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n")
                print(f"HANDLE ERROR: Error at MS key: {itemKey}, {nextIndexDescription} \nDETAIL: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n")
            if (isSuccess):
                break

    
    def translateAdvanced(self, language: str):
        return 
    
    def setResult(self, language: str, text: str):
        self.translatedContentsIOS[language] = f"\"{self.key}\" = \"{text}\";"
        self.translatedContentsAndroid[language] = f"<string name=\"{self.key}\">{text}</string>"
    
    def async_wrap(func):
        @wraps(func)
        async def run(*args, loop=None, executor=None, **kwargs):
            if loop is None:
                loop = asyncio.get_event_loop()
            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return run 
        
    translateAsync = async_wrap(translateWithMicrosoftMultikeys)
    
    def resultContent(self, language: str, platform: str):
        if (self.isComment):
            return self.key
        
        if (platform == "ios"):
            return self.translatedContentsIOS[language]
        
        return self.translatedContentsAndroid[language]