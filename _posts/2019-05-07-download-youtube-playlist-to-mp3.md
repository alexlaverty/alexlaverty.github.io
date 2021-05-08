---
title: Download Youtube Playlist to MP3
author: Alex Laverty
date: 2019-06-04 10:32:00
categories: [Tech]
tags: [youtube, music]
---

Add music to a youtube playlist :

<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PLH8Xx-s33Emo7637FEP4bFnLK3S51vYew" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


Install youtube-dl

```
pip install youtube-dl
```

Run the following command to download the videos and convert them to MP3's, a downloaded.txt file will be created to remember which have all ready been downloaded, next time command is run it will skip already downloaded videos.

```
youtube-dl -xwic --audio-format mp3 --download-archive downloaded.txt https://www.youtube.com/playlist?list=PLH8Xx-s33Emo7637FEP4bFnLK3S51vYew

[youtube:tab] PLH8Xx-s33Emo7637FEP4bFnLK3S51vYew: Downloading webpage
[download] Downloading playlist: Music
[youtube:tab] playlist Music: Downloading 1 videos
[download] Downloading video 1 of 1
[youtube] BZHAjDHHAR4: Downloading webpage
[youtube] BZHAjDHHAR4: Downloading player 838cc154
[download] Destination: Bring Me The Horizon - Can You Feel My Heart (Lyrics) [TikTok Song]-BZHAjDHHAR4.m4a
[download] 100% of 3.51MiB in 00:02
[ffmpeg] Correcting container in "Bring Me The Horizon - Can You Feel My Heart (Lyrics) [TikTok Song]-BZHAjDHHAR4.m4a"
[ffmpeg] Destination: Bring Me The Horizon - Can You Feel My Heart (Lyrics) [TikTok Song]-BZHAjDHHAR4.mp3
Deleting original file Bring Me The Horizon - Can You Feel My Heart (Lyrics) [TikTok Song]-BZHAjDHHAR4.m4a (pass -k to keep)
[download] Finished downloading playlist: Music

➜  Music ls
Bring Me The Horizon - Can You Feel My Heart (Lyrics) [TikTok Song]-BZHAjDHHAR4.mp3
```