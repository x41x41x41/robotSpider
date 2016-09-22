# robotSpider
A simple python script that will collect and analyze the robots.txt file of websites.

![terminal](https://cloud.githubusercontent.com/assets/5831119/18748093/a9a3438e-80c8-11e6-82ad-f5c62f467aff.jpg)

## Use
1. Create a text file list of domains you wish to search `top-100.txt` is included as an example, larger lists can be found in the [Top-Site-Lists](https://github.com/stolenbikes88/Top-Site-Lists) repo

2. Run the command `./robotSpider.py -i YOURINPUTFILE` for example `./robotSpider.py -i top-100.txt`

3. The files will be output into the current directory, prefixed with the name of your input file
