---
layout: post
title:  "Syncing Photos with Python and browsing them with Immich"
date:   2024-09-15 09:00:00
categories: [coding]
tags: [photo-sync, python]
description: Python script to sync and organise photos into a date based folder structure and browsing them with Immich.
image : /images/2024-09-15/2024-09-15_04.png
---

Goals for today :
* Organise my photos

I have thousands of personal photos and videos from 2000 through to 2024 currently totalling 1.5TB.

![alt text](/images/2024-09-15/2024-09-15_01.png)

I've tried to stick to a naming convention over the years but overtime it has become pretty messy. From changing the filename format from YYYYMMDD to YYYY-MM-DD, using different photo capturing devices with different filenames, to importing photos from iphones multiple times creating lots of duplicates, I have been meaning to getting around to writing a script to tidy this all up.

I wrote a Python script to help me automate this process, I have uploaded into a github repository here

<https://github.com/alexlaverty/photo-sync>


I launch the script like this :

```
python photo-sync.py --source-directory "F:\Pictures" --destination-directory "Z:\Pictures"
```

This script recursively scans through the source photo directory, it reads the EXIF date from the images if available.

![alt text](/images/2024-09-15/2024-09-15_02.png)

The script will copy across files that are included in the `file_extensions` array, it will attempt to read dates from EXIF data for files in the `image_extensions` array otherwise it falls back to using the oldest date in the files creation or modified date.

```
file_extensions = ('.jpg', '.jpeg', '.heic', '.cr2', '.mov', '.mp4', '.png', '.avi')
image_extensions = ('.jpg', '.jpeg', '.heic', '.cr2')
```

It will then copy the photo to the destination path in date based folder structure, for example :

```
Z:\Pictures\YYYY\YYYY-MM-DD\YYYYMMDD_HHMMSS.jpg
Z:\Pictures\2023\2023-01-17\20230117_194402.jpg
```

This is my preferred naming standard for storing photos and videos. If the script is unable to retrieve the metadata from EXIF on the file it falls back to reading the file creation and modified date, previously I would just specify creation date, but found that when copying files around on windows it won't preserve the original dates so sometimes creation date is newer than the modified date, so this script will read in creation and modified date and choose the older of the two.

Also I added a feature where if the destination photo exists it will check if the source file is larger and if so overwrite it, this was in case I had small thumbnail or cache images that somehow were copied across i would rather take the larger size image.

I left the script to run overnight and woke up to all my photos copied across to the Z drive all nicely organised.

To view the images I decided to use <https://immich.app/> an open source photo organising project, seems to be very popular at the moment, especially in the self-hosted community.

I ran up Immich in a docker container on my computer launching it with a docker-compose.yml file :

```
name: immich

services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    # extends:
    #   file: hwaccel.transcoding.yml
    #   service: cpu # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    volumes:
      # Do not edit the next line. If you want to change the media storage location on your system, edit the value of UPLOAD_LOCATION in the .env file
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
      - /data/Pictures:/pictures
    env_file:
      - .env
    ports:
      - 2283:3001
    depends_on:
      - redis
      - database
    restart: always
    healthcheck:
      disable: false

  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, openvino] to the image tag.
    # Example tag: ${IMMICH_VERSION:-release}-cuda
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    # extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/ml-hardware-acceleration
    #   file: hwaccel.ml.yml
    #   service: cpu # set to one of [armnn, cuda, openvino, openvino-wsl] for accelerated inference - use the `-wsl` version for WSL2 where applicable
    volumes:
      - model-cache:/cache
    env_file:
      - .env
    restart: always
    healthcheck:
      disable: false

  redis:
    container_name: immich_redis
    image: docker.io/redis:6.2-alpine@sha256:2d1463258f2764328496376f5d965f20c6a67f66ea2b06dc42af351f75248792
    healthcheck:
      test: redis-cli ping || exit 1
    restart: always

  database:
    container_name: immich_postgres
    image: docker.io/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:90724186f0a3517cf6914295b5ab410db9ce23190a2d9d0b9dd6463e3fa298f0
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
      POSTGRES_INITDB_ARGS: '--data-checksums'
    volumes:
      # Do not edit the next line. If you want to change the database storage location on your system, edit the value of DB_DATA_LOCATION in the .env file
      - ${DB_DATA_LOCATION}:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready --dbname='${DB_DATABASE_NAME}' --username='${DB_USERNAME}' || exit 1; Chksum="$$(psql --dbname='${DB_DATABASE_NAME}' --username='${DB_USERNAME}' --tuples-only --no-align --command='SELECT COALESCE(SUM(checksum_failures), 0) FROM pg_stat_database')"; echo "checksum failure count is $$Chksum"; [ "$$Chksum" = '0' ] || exit 1
      interval: 5m
      start_interval: 30s
      start_period: 5m
    command: ["postgres", "-c", "shared_preload_libraries=vectors.so", "-c", 'search_path="$$user", public, vectors', "-c", "logging_collector=on", "-c", "max_wal_size=2GB", "-c", "shared_buffers=512MB", "-c", "wal_compression=on"]
    restart: always

volumes:
  model-cache:
```

The only change I made was adding an additional volume to mount my photos into the image container :

```
- /data/Pictures:/pictures
```

When logging into immich I added the `/pictures` path as an external library

![alt text](/images/2024-09-15/2024-09-15_03.png)

Immich was then able to detect the images and import them, after a while it was organising and sorting them

![alt text](/images/2024-09-15/2024-09-15_04.png)

Feel like I'm back on top now with my photo album and have everything organised and in the correct folder and naming structure!