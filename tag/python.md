---
layout: page
title: python
---

<ul style="list-style-type: none;">
  {% for post in site.tags["python"] %}
    <li>
      <span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
