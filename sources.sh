#!/bin/bash
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/ratings.list.gz | gunzip > ratings.txt
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/countries.list.gz | gunzip > countries.txt
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/genres.list.gz | gunzip > genres.txt
curl ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz | gunzip > running-times.txt
