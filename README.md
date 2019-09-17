# Doxydown - documentation utility
[![Build Status](https://travis-ci.com/ArturBa/doxydown.svg?token=5PNdM7qHNNqDFxDZsBRp&branch=develop)](https://travis-ci.com/ArturBa/doxydown)
[![codecov](https://codecov.io/gh/ArturBa/doxydown/branch/develop/graph/badge.svg)](https://codecov.io/gh/ArturBa/doxydown)

tool to make your source code to Markdown document in few seconds

This tool allows you to transform your source file with doxygen styled comments
    into Markdown document.
    
*Supported languages:*
- C

*Supported comment styles:*
```c 
/**
 * ... text ...
 */
```

```c 
/*!
 * ... text ...
 */
```
In both cases the intermediate *'s are optional, so
```
/*!
 ... text ...
*/
```
is also valid.


## Program running:
```sh
./doxydown.py example/Test.h 
```
Also you can save your output to file
```sh
./doxydown.py example/Test.h -o example/Test.md
```
