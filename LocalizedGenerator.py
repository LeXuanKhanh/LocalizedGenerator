from typing import List
from googletrans import Translator
from TranslateContent import LANGUAGES, TranslateContent
import os.path
import time

# ========= MAIN =========
def main():
    start_time = time.perf_counter()
    translator = Translator()
    contents: List[TranslateContent] = []
    iosOutputName = 'output_ios.txt'
    androidOutputName = 'output_android.txt'
    translateLanguages: List[str]= [
        'id', 'th', 'hi', 'vi', 'es', 'tl',
        'bn', 'ur', 'zh-tw'
    ]

    myfile = open('input.txt')
    myfileContent = ''
    for line in myfile:
        item = TranslateContent(line)
        contents.append(item)
        myfileContent = myfileContent + line
    print(myfileContent)
    print()
    contentToTranslateCount = len(list(filter(lambda x: x.isComment == False,contents)))
    
        
    iosMode = os.path.exists(iosOutputName) and 'w' or 'x'
    if iosMode == 'w':
        outputIOSFile = open(iosOutputName, iosMode)
        outputIOSFile.close()
    outputIOSFile = open(iosOutputName, iosMode)

    print('generating for iOS localized')
    translatingIndex = 0
    for language in translateLanguages:
        translatingIndex = 0
        outputIOSFile.write(f'//{LANGUAGES[language]}\n')
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
                print(f'translating {translatingIndex} / {contentToTranslateCount}', end='\r')
            result = item.outputTranslateIOS(language=language)
            outputIOSFile.write(f'{result}\n')
        print(f'translated all into {LANGUAGES[language]}')
        outputIOSFile.write('\n')
    outputIOSFile.close()

    androidMode = os.path.exists(iosOutputName) and 'w' or 'x' 
    if androidMode == 'w':
        outputAndroidFile = open(androidOutputName, androidMode)
        outputAndroidFile.close()
    outputAndroidFile = open(androidOutputName, androidMode)

    print()

    print('generating for Android localized')
    translatingIndex = 0
    for language in translateLanguages:
        translatingIndex = 0
        outputAndroidFile.write(f'//{LANGUAGES[language]}\n')
        for (index, item) in enumerate(contents):
            if (item.isComment != True):
                translatingIndex += 1
                print(f'translating {translatingIndex} / {contentToTranslateCount}', end='\r')
            result = item.outputTranslateAndroid(language=language)
            outputAndroidFile.write(f'{result}\n')
        print(f'translated all into {LANGUAGES[language]}')
        outputAndroidFile.write('\n')
    outputAndroidFile.close()

    end_time = time.perf_counter()
    print(f'executing in {end_time - start_time}s')

if __name__ == '__main__':
    main()