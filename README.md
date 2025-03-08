# <u>README</u>:

## ABOUT

`cc_fetch.py` is a python script design to assist downloading web archive files (*.warc) from the [Common Crawl](https://commoncrawl.org/) without the need to use AWS. Its main functions are to estimate the size of a download and to compile a list of file locations. Currently the reccomended download method is to use [curl](https://curl.se/docs/). Archives can be downloaded directly with cc_fetch, but this is an experimental feature.

The only external external library `cc_fetch.py` uses is [tqdm](https://tqdm.github.io/). It's only used for direct downloading and can be easily edited out if you're unable/unwilling to  install tqdm.

`cc_fetch.py` is offered under the MIT License.

## USAGE

To use `cc_fetch.py` you can `git clone https://github.com/ioncurve/cc_fetch.git` or copy/paste the 'cc_fetch.py' file in this repo. `cc_fetch.py` was tested in a Conda virtual environment using Python 3.10.

### Example Run:
```
$python cc_fetch.py
Welcome to cc_fetch!

By default cc_fetch will create text files with links to web archives of the domains you specify.
If curl is installed on your sytem, you can use it to download the archives.

See Terms of Use for Common Crawl data here: https://commoncrawl.org/terms-of-use

Use [TAB] for command completion.
Type "help" or "?" for a list of commands.
Using crawl: CC-MAIN-2025-05-index
Chunk size: 1024

ccf:\>domains
Create a list of domains to search for.
Enter an empty line or type exit to return to the main program.
add domain:epa.gov
add domain:fda.gov
add domain:cdc.gov
add domain:
Domain list complete.
ccf:\>dl

To download with curl use the command "curl -LOC - -K [domain-urls.txt]"
For more options use "man curl" or "curl -h"


Url file written as epa_gov-urls.txt
Downloading the archive epa.gov will require 5.83Gb

Url file written as fda_gov-urls.txt
Downloading the archive fda.gov will require 11.58Gb

Url file written as cdc_gov-urls.txt
Downloading the archive cdc.gov will require 15.02Gb

Total download size 32.43Gb

ccf:\>q
$curl -LOC - -K epa_gov-urls.txt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  3 1111M    3 43.1M    0     0  9909k      0  0:01:54  0:00:04  0:01:50 9913k
...

```

### Commands:
<blockquote>
  
- `chunk`

    Short: `ch`<br>
    If downloading with cc_fetch, the downloads are broken into chunks. This option allows you to change the chunk size.

- `crawl`

    Choose which crawl to use.

- `domains`

    Short: `d`<br>
    Create a list of domains to seach the for in the crawl. This will overwite the existing list.

- `download`

    Short: `dl`<br>
    This command searches the selected crawl for archives of the domains in the domain list. When using the default settings,
    no files will be downloaded. Instead, files containing urls of the archives will be written. The archives can then easily 
    be downloaded with curl. Regardless of using curl, cc_fetch attempts to provide an estimate of the size of the download(s).

- `list_domains`

    Short: `lsd`<br>
    Show the list of domains.

- `no_curl`

    Don't save list of files for use with curl. This option will force cc_fetch to attempt the download.

- `quit`

    Short: `q`<br>
    Exits the program.

  </blockquote>


  ### Web Archive Format:

  In order to use the files after you download them, you'll need software that lets you browse or  extract the data from the *.warc files. You can find a list of tools [here](https://webrecorder.net/developer-tools/).


  My prefered method at present is to use [pywb](https://github.com/webrecorder/pywb/tree/main).


  ### TODO:

  - [ ] Auto resume for direct downloads
  - [ ] Auto update list of Crawls
  - [ ] Add domain list from file
  - [ ] GUI or frontend
  - [ ] Option to convert to *.zim files (easier to browse than *.warc imo)

  
