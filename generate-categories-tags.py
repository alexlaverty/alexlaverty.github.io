import os
import frontmatter
from collections import defaultdict

# Define the paths
posts_folder = '_posts'
categories_folder = 'category'
tags_folder = 'tag'

# Create folders if they don't exist
os.makedirs(categories_folder, exist_ok=True)
os.makedirs(tags_folder, exist_ok=True)

# Dictionaries to hold categories and tags
categories = defaultdict(list)
tags = defaultdict(list)

# Process each Markdown file in the _posts folder
for filename in os.listdir(posts_folder):
    if filename.endswith('.md'):
        filepath = os.path.join(posts_folder, filename)
        
        # Read the front matter and content
        post = frontmatter.load(filepath)
        post_title = post.get('title', 'Untitled')
        post_date = post.get('date', 'Unknown Date')
        post_url = filename.replace('.md', '.html')  # Assuming URL is filename without .md

        # Extract categories and tags
        for category in post.get('categories', []):
            categories[category].append({'date': post_date, 'url': post_url, 'title': post_title})
        
        for tag in post.get('tags', []):
            if isinstance(tag, str):
                tags[tag].append({'date': post_date, 'url': post_url, 'title': post_title})
            elif isinstance(tag, list):
                for t in tag:
                    tags[t].append({'date': post_date, 'url': post_url, 'title': post_title})

# Function to generate Markdown file content
def generate_markdown_content(title, posts_key):
    content = f'''---
layout: page
title: {title}
---

<ul style="list-style-type: none;">
  {{% for post in site.{posts_key} %}}
    <li>
      <h2><span style="font-family: Courier New;">{{{{ post.date | date: "%Y-%m-%d" }}}}</span> <a href="{{{{ post.url }}}}">{{{{ post.title }}}}</a></h2>
    </li>
  {{% endfor %}}
</ul>
'''
    return content

# Write category files
for category in categories:
    category_file = os.path.join(categories_folder, f'{category}.md')
    with open(category_file, 'w') as f:
        f.write(generate_markdown_content(f'{category}', f'categories["{category}"]'))

# Write tag files
for tag in tags:
    tag_file = os.path.join(tags_folder, f'{tag}.md')
    with open(tag_file, 'w') as f:
        f.write(generate_markdown_content(f'{tag}', f'tags["{tag}"]'))

print("Category and tag files have been generated.")
