from functools import partial, wraps
from typing import List
from GeneratorConfig import GeneratorConfig
from TranslateContent import TranslateContent
from GGTransLanguage import GGTRANS_LANGUAGE
import os.path
import time
import asyncio

contents: List[TranslateContent] = []
totalContentToTranslate = 0
translatedContentCount = 0
    
# ========= MAIN =========
async def main():
    GeneratorConfig.shared().loadFromJson()
    
    myfile = open(GeneratorConfig.shared().inputFile)
    myfileContent = ''
    for line in myfile:
        if not line.strip():
            continue
        item = TranslateContent(line)
        contents.append(item)
        myfileContent = myfileContent + line
    print(myfileContent)
    print()

    #await beginTranslate()
    await beginTranslateV2()
    writeFile('ios')
    writeFile('android')

async def beginTranslate():
    global totalContentToTranslate
    global translatedContentCount
    
    print(f'generating localized')
    totalContentToTranslate = len(list(filter(lambda x: x.isComment == False,contents))) * len(GeneratorConfig.shared().outputLanguages)
    translatedContentCount = 0
    
    asyncWorks = []
    translatingIndex = 0
    for language in GeneratorConfig.shared().outputLanguages:
        translatingIndex = 0
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
            asyncWorks.append(beginTranslateItem(item=item, language=language))
    await asyncio.gather(*asyncWorks)
    print(f'done generating localized')
    
async def beginTranslateV2():
    global totalContentToTranslate
    global translatedContentCount
    
    print(f'generating localized')
    totalContentToTranslate = len(list(filter(lambda x: x.isComment == False,contents))) * len(GeneratorConfig.shared().outputLanguages)
    translatedContentCount = 0
    translatingIndex = 0
    
    asyncPartition = []
    partitionCount = 0
    for language in GeneratorConfig.shared().outputLanguages:
        translatingIndex = 0
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
                partitionCount += 1
            asyncPartition.append(beginTranslateItem(item=item, language=language))
            
            if (partitionCount == GeneratorConfig.shared().partitionSize):
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
    filePath = GeneratorConfig.shared().outputIOSFile if platform == "ios" else GeneratorConfig.shared().outputAndroidFile
    permission = os.path.exists(filePath) and 'w' or 'x'
    if permission == 'w':
        file = open(filePath, permission)
        file.close()
    file = open(filePath, permission)
    
    print(f'writing file for {platform} localized')
    translatingIndex = 0
    for language in GeneratorConfig.shared().outputLanguages:
        translatingIndex = 0
        file.write(f'//{GGTRANS_LANGUAGE[language]}\n')
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
            result = item.resultContent(language=language, platform=platform)
            file.write(f'{result}\n')
        file.write('\n')
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