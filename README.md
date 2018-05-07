# Gerrit User Summary

### Get a summary list group by day via gerrit API

Example:

``` bash
python3 main.py -u https://cr.deepin.io/ -a BLumia -c 10
```

Usage:

``` bash
    -h          --help            : Display this help
    -u <url>    --url <url>       : Gerrit API Url
    -a <id>     --account <id>    : Gerrit account id
    -c <count>  --count	<count>   : Commit count fetched from gerrit
    -s <count>  --start	<count>   : Commit start at number <count>
    -o <path>   --output= <path>  : Not implemented...
```
