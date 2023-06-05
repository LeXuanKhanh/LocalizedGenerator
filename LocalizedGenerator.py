from functools import partial, wraps
from typing import List
from GeneratorConfig import GeneratorConfig
from TranslateContent import TranslateContent
from GGTransLanguage import GGTRANS_LANGUAGE
import os.path
import time
import asyncio
import io

contents: List[TranslateContent] = []
totalContentToTranslate = 0
translatedContentCount = 0
config = GeneratorConfig.shared()
    
# ========= MAIN =========
async def main():
    config.loadFromJson()
    
    myfile = open(config.inputFile)
    myfileContent = ''
    for line in myfile:
        if not line.strip():
            continue
        item = TranslateContent(line)
        contents.append(item)
        myfileContent = myfileContent + line
    print(myfileContent)
    print()

    await beginTranslateV2()
    
    if config.isModifyingExistingLocalizedFilesIOS:
        modifyExistingFiles('ios')
    else:
        writeFile('ios')
        
    if config.isModifyingExistingLocalizedFilesAndroid:
        modifyExistingFiles('android')
    else:
        writeFile('android')
    
async def beginTranslateV2():
    global totalContentToTranslate
    global translatedContentCount
    
    print(f'generating localized using {config.translatorUsed()}')
    totalContentToTranslate = len(list(filter(lambda x: x.isComment == False,contents))) * len(GeneratorConfig.shared().outputLanguages)
    translatedContentCount = 0
    translatingIndex = 0
    
    asyncPartition = []
    partitionCount = 0
    for language in config.outputLanguages:
        translatingIndex = 0
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
                partitionCount += 1
            asyncPartition.append(beginTranslateItem(item=item, language=language))
            
            if (partitionCount == config.partitionSize):
                print(f'begin translate current partition')
                await asyncio.gather(*asyncPartition)
                print()
                asyncPartition = []
                partitionCount = 0
                
                if (GeneratorConfig.shared().sleepTime != 0):
                    print(f'start timeout sleeping in {GeneratorConfig.shared().sleepTime}')
                    await asyncSleep(GeneratorConfig.shared().sleepTime)
                
    if (partitionCount != 0):
        print(f'begin translate remaining works')
        await asyncio.gather(*asyncPartition)
        print()
        asyncPartition = []
        partitionCount = 0
    print(f'done generating localized')
        
async def beginTranslateItem(item: TranslateContent, language: str):
    global translatedContentCount
    await item.translateAsync(language=language)
    if (item.isComment != True):
        translatedContentCount += 1
        print(f"translated {translatedContentCount}/{totalContentToTranslate}", end='\r')
    
def writeFile(platform: str):
    filePath = config.outputIOSFile if platform == "ios" else config.outputAndroidFile
    permission = os.path.exists(filePath) and 'w' or 'x'
    if permission == 'w':
        file = open(filePath, permission)
        file.close()
    file = open(filePath, permission)
    
    print(f'writing file for {platform} localized')
    translatingIndex = 0
    for language in config.outputLanguages:
        translatingIndex = 0
        file.write(f'//{GGTRANS_LANGUAGE[language]}\n')
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
            result = item.resultContent(language=language, platform=platform)
            file.write(f'{result}\n')
        file.write('\n')
    file.close()
    
def modifyExistingFiles(platform: str):
    print(f'modifying existing files for {platform} localized')
    for (index, language) in  enumerate(config.outputLanguages):
        filePaths: list[str]
        if (platform == "android"):
            filePaths: list[str] = config.outputModifyFilesAndroid[index].paths
        else:
            filePaths: list[str] = config.outputModifyFilesIOS[index].paths
            
        for filePath in filePaths:
            if not os.path.exists(filePath):
                print(f"{filePath} doesn't exist")
                exit(1)
            file = open(filePath, "rb+")
            file.seek(0, io.SEEK_END)
            if platform == "android":
                try:  # catch OSError in case of a one line file
                    file.seek(-len('</resources>'.encode('utf8'))-1, io.SEEK_CUR)
                except IOError:
                    pass
            else:
                file.write('\n'.encode('utf8'))
                
            translatingIndex = 0
            for (index, item) in enumerate(contents):
                if (item.isComment != True):
                    translatingIndex += 1
                result = item.resultContent(language=language, platform=platform)
                file.write(f'    {result}\n'.encode('utf8'))
                
            if platform == "android":
                file.write('</resources>'.encode('utf8'))
            file.close()
        
def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 

asyncSleep = async_wrap(time.sleep)
        
if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')