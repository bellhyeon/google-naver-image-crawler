<div align="center">
    
# Google, Naver Image Crawler

</div>

## Supported Sites
* Google
* Naver
***
## Requirements
***
To run this repository, must meet these requirements. You can download chromedriver at [here](https://chromedriver.chromium.org/downloads)
```
urllib
selenium
os
time
tqdm
argparse
chromedriver
```
***
## Arguments
- `--site`: site name to crawling images (supports "google", "naver", "구글", and "네이버")
- `--keyword`: keyword to crawling images
- `--CCL`: if True, crawl images in commercial license only else crawl all images
- `--wait`: time to wait (recommend time: google=1.5, naver=3.0)
***

## Getting Started
***
### Run
Examples for Google and Naver
```shell
python crawler.py --site "google" --keyword "doraemon" --CCL "True" --wait 1.5
```
```shell
python crawler.py --site "네이버" --keyword "도라에몽" --CCL "False" --wait 3.0
```

### Result
The folder will be created automatically, with a name like {site}_{keyword}.<br>
The log file contains original source url of images.
***
```
repo
  |——crawler.py
  |——translation.py
  |——{site}_{keyword}
        |——1.jpg
        |——2.jpg
        |——...
        |——log.txt
```

## Licence
***
```
MIT license

Copyright (c) 2023-present JongHyeon Kim.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

```