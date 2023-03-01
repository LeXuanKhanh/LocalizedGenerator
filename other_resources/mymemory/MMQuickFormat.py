import json
import time

# quickly format microsoft_support_language.json
# ms_sl_result.json:

input = 'other_resources/mymemory/mymemory_support_languages.json'
output = 'other_resources/mymemory/mm_sl_result.json'

def main():
    f = open(input)
    data: dict() = json.load(f)
    #print(json.dumps(data, indent=2))
    f.close()
    
    newJson = dict()
    translationData = data
    for key in translationData:
        newKey = str(key).replace("(", '').replace(')', '').lower()
        # print(f"{translationData[key]}\n")
        newJson[newKey] = translationData[key]
        
    with open(output, 'w') as json_file:
        json.dump(newJson, json_file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')