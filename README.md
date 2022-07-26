# LocalizedGenerator

Simple Python script to quickly generate localized for Android and iOS, based on [googletrans](https://github.com/ssut/py-googletrans)

## Usage

Since it's based on [googletrans](https://github.com/ssut/py-googletrans), you have to install the library first to use the script, this was based on googletrans 4.0.0rc1 when i first write, if you have issue involved with this library, please install the differrent version

```
pip install googletrans==4.0.0rc1
```

Create input.txt with [iOS strings resources format](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html) 

```
/* Comment if need */
"<Key>" = "<Content to transalte>";
/* Example */
"ErrorString_1" = "An unknown error occurred.";
```

Run the script, it will generate output_ios.txt in strings resources format and output_android.txt in xml format