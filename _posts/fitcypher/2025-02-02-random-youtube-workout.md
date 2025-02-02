---
title:  "Random Bodyweight Workout with Video!"
date:   2025-02-02 3:34:00
layout: post
categories: ["fitcypher"]
image: /assets/images/fitcypher/20250202/screenshot004.png
---

I have added a new workout page, this one will read a list of youtube videos from a json file, for example :

```
/src/fitcypher$ cat ui/data/darebee.json 
[
  {
    "id": "4XcGTvcSRxY",
    "title": "hop heel clicks",
    "duration": 8
  },
  {
    "id": "wqfRvXc7BHY",
    "title": "half squat walk",
    "duration": 19
  },
  {
    "id": "HAQvQXovwuo",
    "title": "side splits",
    "duration": 83
  }
]
```

and then will play a random youtube video for the user with a counter of the elapsed time :

![alt text](/assets/images/fitcypher/20250202/screenshot004.png)

Once the user has done the exercise for as long as they want, they click the Complete button, this will save the exercise and duration to the database.

If an exercise video comes up that you don't like click the skip button and it will go to the next video and will not save the exercise to the database.

Checkout the FitCypher Workouts here :

<https://alexlaverty.pythonanywhere.com/workouts>

![alt text](/assets/images/fitcypher/20250202/screenshot005.png)

Or git clone the FitCypher github repo and run it locally :

<https://github.com/alexlaverty/fitcypher>