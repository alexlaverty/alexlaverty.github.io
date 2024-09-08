---
layout: page
title: laverty-family-history
---

<ul style="list-style-type: none;">
  {% for post in site.tags["laverty-family-history"] %}
    <li>
      <span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
