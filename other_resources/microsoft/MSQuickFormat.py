import json
import time

# quickly format microsoft_support_language.json
# ms_sl_result.json:

input = 'other_resources/microsoft/microsoft_support_languages.json'
output = 'other_resources/microsoft/ms_sl_result.json'

def main():
    f = open(input)
    data: dict() = json.load(f)
    #print(json.dumps(data, indent=2))
    f.close()
    
    newJson = dict()
    translationData = data['translation']
    for key in translationData:
        newKey = str(translationData[key]['name']).replace("(", '').replace(')', '').lower()
        newData = str(key).lower()
        # print(f"{translationData[key]}\n")
        newJson[newKey] = newData
        
    with open(output, 'w') as json_file:
        json.dump(newJson, json_file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')