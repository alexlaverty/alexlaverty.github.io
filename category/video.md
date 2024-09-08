---
layout: page
title: video
---

<ul style="list-style-type: none;">
  {% for post in site.categories["video"] %}
    <li>
      <span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
