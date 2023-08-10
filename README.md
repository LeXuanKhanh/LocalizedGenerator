# LocalizedGenerator

Simple Python script to quickly generate localized for Android and iOS

## Features

- Generate localized Android and iOS string in [iOS strings resources format](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html) and [Android xml resource format](developer.android.com/guide/topics/resources/localization)

- Support different translators: Google, Microsoft and Mymemory

- Highly customize via config file (generator_config.json)

- Use timeout between each amount of translate batch to avoid timeout from non-official translator (such as Google)

- Insert new generate localized content into your existing localized files in your project

## Installation

From version 1.2, this script is based on [deep_translator](https://github.com/nidhaloff/deep-translator) because it's still in maintenance and provide many features

```python
pip install -U deep-translator
```

## Basic usage

Create input file with [iOS strings resources format](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html) 

```
/* Comment if need */
"<Key>" = "<Content to transalte>";
/* Example */
"ErrorString_1" = "An unknown error occurred.";
```

In `generator_config.json`:

Set the `"input_file"` with the input file path you just create

Define the `"input_language"` and `"output_languages"` codes. The code is ISO-639, you can get it in [here](https://cloud.google.com/translate/docs/languages)

Defile the `"output_ios_file"` path and `"output_android_file"` path

Run the `LocalizedGenerator.py` file, assuming the `"is_modifying_existing_localized_files_ios"` and `"is_modifying_existing_localized_files_android"` is set to false, it will generate ios output file in ios strings resources format and android output file in xml format in your defined output file paths

## Using different translators

Simple set `"is_enabled": true` in `"google_translator_config"` or `"mymemory_translator"` if you want to use it. Remember to set other translator to `false`, if all translator is set to `true`, most priority translator will use

Priority order:

- Google

- Microsoft

- Mymemory

For `"microsoft_translator_config"` you have to get the region and the key which is generated in the Azure console. That require you to setup the [Microsoft Azure Cognitive Services](https://learn.microsoft.com/en-us/azure/cognitive-services/translator/translator-overview)

```json
"microsoft_translator_config": {
    "is_enabled": true,
    "region": "southeastasia",
    "keys": [
        "example_key"
    ]
},
```

## Insert new localized content into existing localized files

First, set the`"is_modifying_existing_localized_files_ios": true` or `"is_modifying_existing_localized_files_ios": true` in `generator_config.json`

Specify the localized language and file path for each localized file in  `"output_modify_files_ios"` and `"output_modify_files_android"`, for example your project and ios and android support English(en), Japanese(jp) and Vietnamese(vi) the config json would be: 

```json
"output_modify_files_ios": [
    {
        "language": "en",
        "paths": [
            "/Users/macbookpro/Documents/Default/Base.lproj/Localizable.strings",
            "/Users/macbookpro/Documents/Default/en.lproj/Localizable.strings"
        ]
    },
    {
        "language": "ja",
        "paths": ["/Users/macbookpro/Documents/Default/ja-JP.lproj/Localizable.strings"]
    },
    {
        "language": "vi",
        "paths": ["/Users/macbookpro/Documents/Default/vi.lproj/Localizable.strings"]
    }
 ],
"output_modify_files_android": [
    {
        "language": "en",
        "paths": ["/Users/macbookpro/Documents/project-android/src/main/res/values/strings.xml"]
    },
    {
        "language": "ja",
        "paths": ["/Users/macbookpro/Documents/project-android/src/main/res/values-ja/strings.xml"]
    },
    {
        "language": "vi",
        "paths": ["/Users/macbookpro/Documents/project-android/src/main/res/values-vi/strings.xml"]
    }
]
```

**Note:** The amount of the localized language and file path on ios or android which you want to insert must be the same as the languages codes which you define in `"output_languages"`

## Setting the timeout between each amount of translate batch

The `"partition_size"` determine the amount of translate will execute in a workload at the same time, minimum value is 1

The `"sleep_time"` delay time between workload in seconds to avoid timeout, if set to 0 then it will skip the delay. I recommend always to non 0 value to avoid timeout
