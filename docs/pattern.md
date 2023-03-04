# All pattern

## Match Java Code

### Method

Java Method defination syntax
```
[accessSpecifier] [static] [abstract] [final] [native] [synchronized] returnType methodName ([paramlist]) [throws exceptionsList]
```

`accessSpecifier`: `private/protected/public/package`

`static/abstract/final/native/synchronized`: are keywords

returnType: must

methodName: identifier ::= <b> "a..z,\$,\_" \{ "a..z,$,_,0..9,unicode character over 00C0" } </b>

Difference between Method and Variable Declaration: ([paramlist]) [throws exceptionsList] in Method vs <b>=</b> in Variable

## Extracting Infomation

Target: log statement

First step: find 'Logger' in slf4j

Where to find log statement: all log statements must be in method.

Which infomation is useful in log statement: according to [slf4j](https://www.slf4j.org/faq.html#logging_performance), log templates can be classfied into three types: plain text, string +, parameterized messages

Which infomation is useful to better understand log: comments on method and log statement, log text, log parameter and method.