# Getchu Anime Face Dataset

## Requirements:

    # Tools: curl, parallel, python 3, wget, awk
    sudo apt install parallel

    # macOS
    brew install parallel

    # python library: animeface, cv2
    pip install animeface opencv-python


## Link to online images

`./img_link_.txt`

## Download Getchu dataset

### Query SQL 

Run the following query:

```
SELECT g.id, g.gamename, g.sellday,
'www.getchu.com/soft.phtml?id=' || g.comike as links
FROM gamelist g
WHERE g.comike is NOT NULL
ORDER BY g.sellday
```

at http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_form.php

Otherwise, we can use `curl` to do the same thing:

```
curl 'http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_form.php' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: http://erogamescape.dyndns.org' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_form.php' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: vi,en-US;q=0.9,en;q=0.8' --data 'sql=SELECT+g.id%2C+g.gamename%2C+g.sellday%2C%0D%0A%27www.getchu.com%2Fsoft.phtml%3Fid%3D%27+%7C%7C+g.comike+as+links%0D%0AFROM+gamelist+g%0D%0AWHERE+g.comike+is+NOT+NULL%0D%0AORDER+BY+g.sellday%0D%0A' --compressed --output getchu.html
```

The output is stored at `getchu.html`

### Extract Link and Date information

```
cat getchu.html | grep -Ehro "www.getchu.com/soft.phtml\?id=[0-9]+" > links.txt
cat getchu.html | grep -Ehro         "[0-9]+-[0-9][0-9]-[0-9][0-9]" > dates.txt
```

Append some magic, to bypass the warning

```
awk '{print $0"&gc=gc"}' links.txt > links_.txt
```

### Create a new directory and download web pages 

```
mkdir getchu
cd getchu
cat ../links_.txt | parallel -j 32 wget -q -O {#}.html {}
cd ..
```

### Extract image links

```
cat getchu/* | grep -Ehro "./brandnew/[0-9]+/c[0-9]+chara[0-9]+.jpg" > img_links.txt
awk '{print "www.getchu.com/"substr($0,3)}' img_links.txt > img_links_.txt
```

### Download images

```
mkdir imgs
cd imgs && cat ../img_links_.txt | parallel -j 32 wget -q -O {#}.jpg {}
cd ..
```


## Extract Faces


```
find ./imgs | parallel -j 8 python detect.py {}
```


List of all faces

```
find ./imgs | grep cropped > faces.txt
```