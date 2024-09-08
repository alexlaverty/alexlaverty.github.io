---
layout: page
title: deadmans
---

<ul style="list-style-type: none;">
  {% for post in site.tags["deadmans"] %}
    <li>
      <span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
