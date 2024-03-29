import json
import time

from OutputModifyFile import OutputModifyFile
class GeneratorConfig:
    configFile = 'generator_config.json'
    debugMode = False
    
    inputFile = "input.txt"
    outputIOSFile = "output_ios.txt"
    outputAndroidFile = 'output_android.txt'
    
    inputLanguage = "en"
    outputLanguages = ["en"]
    
    # determine translate works will execute asynchronously at the same time, minimum value is 1
    # if partitionSize is set to 1 then the translator will work synchronously
    partitionSize = 1
    # delay time between partition works in seconds to avoid timeout, if set to 0 then it will skip delay
    sleepTime = 0
    
    isGoogleTranslatorEnabled = True
    isMicrosoftTranslatorEnabled = True

    isMicrosoftTranslatorEnabled = True
    microsoftTranslatorKeys = []
    microsoftTranslatorRegion = "southeastasia"

    isMymemoryTranslatorEnabled = True
    
    googleTransMaxErrorCount = 3
    microsoftTransMaxErrorCount = 3
    mymemoryTransMaxErrorCount = 3
    
    # when enable mofify existing files feature, all the files declare in the json config must be the same order 
    # and the same amount of the declared output languages
    isModifyingExistingLocalizedFilesIOS = False
    isModifyingExistingLocalizedFilesAndroid = False
    outputModifyFilesIOS: list[OutputModifyFile] = []
    outputModifyFilesAndroid: list[OutputModifyFile] = []

    __instance = None
    @staticmethod 
    def shared():
        """ Static access method. """
        if GeneratorConfig.__instance == None:
            GeneratorConfig()
        return GeneratorConfig.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if GeneratorConfig.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GeneratorConfig.__instance = self
    
    def loadFromJson(self):
        f = open(self.configFile)
        data: dict() = json.load(f)
        #print(json.dumps(data, indent=2))
        f.close()
        
        self.debugMode = data["debug"]
        
        self.inputLanguage = data["input_language"]
        self.outputLanguages = data["output_languages"]
        
        self.inputFile = data["input_file"]
        self.outputIOSFile = data["output_ios_file"]
        self.outputAndroidFile = data["output_android_file"]
        
        self.partitionSize = data["partition_size"]
        self.sleepTime = data["sleep_time"]
        
        self.isGoogleTranslatorEnabled = data["google_translator_config"]["is_enabled"]
        
        self.isMicrosoftTranslatorEnabled = data["microsoft_translator_config"]["is_enabled"]
        self.microsoftTranslatorKeys = data["microsoft_translator_config"]["keys"]
        self.microsoftTranslatorRegion = data["microsoft_translator_config"]["region"]

        self.isMymemoryTranslatorEnabled = data["mymemory_translator"]["is_enabled"]
        
        self.isModifyingExistingLocalizedFilesIOS = data["is_modifying_existing_localized_files_ios"]
        self.isModifyingExistingLocalizedFilesAndroid = data["is_modifying_existing_localized_files_android"]
        
        for item in data["output_modify_files_ios"]:
            outputModifyFile = OutputModifyFile(item)
            self.outputModifyFilesIOS.append(outputModifyFile)
            
        for item in data["output_modify_files_android"]:
            outputModifyFile = OutputModifyFile(item)
            self.outputModifyFilesAndroid.append(outputModifyFile)
        
        # validating 
        if (self.isModifyingExistingLocalizedFilesIOS and len(self.outputLanguages) != len(self.outputModifyFilesIOS)):
                print(f"the amount of outputModifyIOSFiles {len(self.outputModifyFilesIOS)} "
                      f"is not the same as outputLanguages {len(self.outputLanguages)}")
                exit(1)
        if (self.isModifyingExistingLocalizedFilesAndroid and len(self.outputLanguages) != len(self.outputModifyFilesAndroid)):
                print(f"or outputModifyAndroidFiles {len(self.outputModifyFilesAndroid)} " +
                      f"is not the same as outputLanguages {len(self.outputLanguages)}")
                exit(1)        
    def translatorUsed(self):
        if self.isGoogleTranslatorEnabled:
            return 'GoogleTranslator'
        if self.isMicrosoftTranslatorEnabled:
            return 'MicrosoftTranslator'   
        if self.isMymemoryTranslatorEnabled:
            return 'MymemoryTranslator'            

# test        
def main():
    GeneratorConfig.shared().loadFromJson()
    attrs: dict = vars(GeneratorConfig.shared())
    print(json.dumps(attrs, indent=2))
    print("outputModifyFilesIOS:")
    for item in GeneratorConfig.shared().outputModifyFilesIOS:
        js = vars(item)
        print(json.dumps(js, indent=2))
        
    print("outputModifyFilesAndroid:")
    for item in GeneratorConfig.shared().outputModifyFilesAndroid:
        js = vars(item)
        print(json.dumps(js, indent=2))

if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')