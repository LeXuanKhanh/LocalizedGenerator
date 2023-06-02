import json
import time

# quickly format google_support_languages.json
# gg_sl_result.json:

input = 'other_resources/google/google_support_languages.json'
output = 'other_resources/google/gg_sl_result.json'

def main():
    f = open(input)
    data: dict() = json.load(f)
    #print(json.dumps(data, indent=2))
    f.close()
    
    newJson = dict()
    translationData = data
    for key in translationData:
        newKey = str(key)
        # print(f"{translationData[key]}\n")
        newJson[translationData[key]] = newKey
        
    with open(output, 'w') as json_file:
        json.dump(newJson, json_file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print(f'executed in {end_time - start_time}s')