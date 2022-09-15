from typing import List
from TranslateContent import LANGUAGES, TranslateContent
import os.path
import time
import asyncio

contents: List[TranslateContent] = []
iosOutputName = 'output_ios.txt'
androidOutputName = 'output_android.txt'
translateLanguages: List[str]= [
    'id', 'th', 'hi', 'vi', 'es', 'tl',
    'bn', 'ur', 'zh-tw', 'ja'
]
 
totalContentToTranslate = 0
translatedContentCount = 0
    
# ========= MAIN =========
async def main():
    myfile = open('input.txt')
    myfileContent = ''
    for line in myfile:
        if not line.strip():
            continue
        item = TranslateContent(line)
        contents.append(item)
        myfileContent = myfileContent + line
    print(myfileContent)
    print()

    await beginTranslate()
    writeFile('ios')
    writeFile('android')

async def beginTranslate():
    global totalContentToTranslate
    global translatedContentCount
    
    print(f'generating localized')
    totalContentToTranslate = len(list(filter(lambda x: x.isComment == False,contents))) * len(translateLanguages)
    translatedContentCount = 0
    
    asyncWorks = []
    translatingIndex = 0
    for language in translateLanguages:
        translatingIndex = 0
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
            asyncWorks.append(beginTranslateItem(item=item, language=language))
    await asyncio.gather(*asyncWorks)
    print()
        
async def beginTranslateItem(item: TranslateContent, language: str):
    global translatedContentCount
    await item.translateAsync(language=language)
    if (item.isComment != True):
        translatedContentCount += 1
        print(f"translated {translatedContentCount}/{totalContentToTranslate}", end='\r')
    
def writeFile(platform: str):
    filePath = iosOutputName if platform == "ios" else androidOutputName
    permission = os.path.exists(filePath) and 'w' or 'x'
    if permission == 'w':
        file = open(filePath, permission)
        file.close()
    file = open(filePath, permission)
    
    print(f'writing file for {platform} localized')
    translatingIndex = 0
    for language in translateLanguages:
        translatingIndex = 0
        file.write(f'//{LANGUAGES[language]}\n')
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
            result = item.resultContent(language=language, platform=platform)
            file.write(f'{result}\n')
        file.write('\n')
    file.close()
        
if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')