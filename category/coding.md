---
layout: page
title: coding
---

<ul style="list-style-type: none;">
  {% for post in site.categories["coding"] %}
    <li>
      <span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
