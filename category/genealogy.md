---
layout: page
title: genealogy
---

<ul style="list-style-type: none;">
  {% for post in site.categories["genealogy"] %}
    <li>
      <h2><span style="font-family: Courier New;">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url }}">{{ post.title }}</a></h2>
    </li>
  {% endfor %}
</ul>
