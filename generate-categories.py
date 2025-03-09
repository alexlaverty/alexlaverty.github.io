#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path
import sys

def extract_categories_from_posts():
    """
    Extract all categories from posts in the _posts directory
    Returns a set of all unique categories
    """
    all_categories = set()
    posts_dir = Path("_posts")

    if not posts_dir.exists():
        print("Error: _posts directory not found")
        sys.exit(1)

    # Create categories directory if it doesn't exist
    Path("categories").mkdir(exist_ok=True)

    # Process each markdown file in _posts (supporting both .md and .markdown extensions)
    for markdown_file in posts_dir.glob("*.[md]*"):
        if markdown_file.suffix not in ['.md', '.markdown']:
            continue

        with open(markdown_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find the YAML front matter
        front_matter_match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            try:
                # Parse the YAML front matter
                front_matter = yaml.safe_load(front_matter_match.group(1))

                # Extract categories
                if 'categories' in front_matter:
                    categories = front_matter['categories']

                    # Handle both string and list formats
                    if isinstance(categories, str):
                        all_categories.add(categories)
                    elif isinstance(categories, list):
                        all_categories.update(categories)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {markdown_file}: {e}")

    return all_categories

def generate_category_pages(categories):
    """
    Generate a markdown file for each category in the categories directory
    """
    for category in categories:
        # Create a markdown file for the category
        category_file = Path(f"categories/{category}.md")

        # Write the content
        with open(category_file, "w", encoding="utf-8") as f:
            f.write(f"---\nlayout: categories\ncategory: {category}\n---\n")

        print(f"Generated category page: {category_file}")

def main():
    print("Extracting categories from posts...")
    categories = extract_categories_from_posts()

    if not categories:
        print("No categories found in posts")
        return

    print(f"Found {len(categories)} unique categories")
    generate_category_pages(categories)
    print("Category pages generation complete!")

if __name__ == "__main__":
    main()