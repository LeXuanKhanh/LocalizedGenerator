from GeneratorConfig import GeneratorConfig

class TranslatorErrorCounter:
    config = GeneratorConfig.shared()
    googleTrans = 0
    microsoftTrans = 0
    mymemoryTrans = 0
    
    __instance = None
    @staticmethod 
    def shared():
        """ Static access method. """
        if TranslatorErrorCounter.__instance == None:
            TranslatorErrorCounter()
        return TranslatorErrorCounter.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if TranslatorErrorCounter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TranslatorErrorCounter.__instance = self
            
    def isGoogleErrorReachedMaxLimit(self):
        return self.googleTrans >= self.config.googleTransMaxErrorCount
    
    def isMicrosoftErrorReachedMaxLimit(self):
        return self.microsoftTrans >= self.config.microsoftTransMaxErrorCount
    
    def isMymemoryErrorReachedMaxLimit(self):
        return self.mymemoryTrans >= self.config.mymemoryTransMaxErrorCount
    
    