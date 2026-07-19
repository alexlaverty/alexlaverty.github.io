from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import datetime
import re
import os
import urllib.parse
import markdown
from werkzeug.utils import secure_filename
import uuid
import glob

app = Flask(__name__)

# --- Your existing configuration and helper functions remain the same ---

# Configure upload settings
UPLOAD_FOLDER = 'assets/images'
VIDEO_FOLDER = 'assets/videos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def extract_youtube_id(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path.lstrip('/')
    if parsed_url.netloc in ['www.youtube.com', 'youtube.com']:
        query = urllib.parse.parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None

def process_content(content):
    youtube_pattern = r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[^\s]+)'
    def replace_with_embed(match):
        url = match.group(0)
        video_id = extract_youtube_id(url)
        if video_id:
            return f'{{% include youtube.html id=\'{video_id}\' %}}'
        return url
    return re.sub(youtube_pattern, replace_with_embed, content)

def create_filename(title):
    filename = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    filename = re.sub(r'[\s]+', '-', filename)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return f"{date}-{filename}.md"

def create_frontmatter(title):
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S %z')
    return f"""---
layout: post
title: "{title}"
date: {date} +1100
categories: blog
---
"""

def format_date_title(date_obj):
    day_name = date_obj.strftime('%A')
    day = date_obj.day
    month_name = date_obj.strftime('%B')
    year = date_obj.year
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return f"{day_name} the {day}{suffix} of {month_name} {year}"

# --- Route modifications start here ---

@app.route('/', methods=['GET'])
def index():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    posts_dir = '_posts'
    
    # Use glob to find today's markdown file
    matching_files = glob.glob(os.path.join(posts_dir, f"{today}-*.md"))
    
    html_content = "<p>No content for today. Start writing!</p>"
    raw_content = ""

    if matching_files:
        filepath = matching_files[0]
        with open(filepath, 'r', encoding='utf-8') as f:
            full_file_content = f.read()

        # Separate frontmatter from the main content
        parts = full_file_content.split('---', 2)
        if len(parts) == 3:
            # The actual markdown content for editing is after the second '---'
            raw_content = parts[2].strip()
        else:
            # Fallback for malformed files
            raw_content = full_file_content
        
        # Generate HTML preview from the raw content
        html_content = markdown.markdown(raw_content)
    
    # Pass both the preview and the raw content to the template
    return render_template('index.html', preview_html=html_content, existing_content=raw_content)

@app.route('/save', methods=['POST'])
def save():
    now = datetime.datetime.now()
    title = format_date_title(now)
    # This is the new, edited content from the form
    content = request.form['content']
    
    processed_content = process_content(content)
    
    posts_dir = os.path.join('_posts')
    os.makedirs(posts_dir, exist_ok=True)
    
    filepath = os.path.join(posts_dir, create_filename(title))
    
    frontmatter = ""
    # Check if the file already exists to preserve its frontmatter
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            full_file_content = f.read()
        
        parts = full_file_content.split('---', 2)
        if len(parts) == 3:
            # Reconstruct the frontmatter block
            frontmatter = f"---{parts[1]}---"
        else:
            # If frontmatter is missing or malformed, create a new one
            frontmatter = create_frontmatter(title)
    else:
        # If the file is new, create the frontmatter
        frontmatter = create_frontmatter(title)

    # Write the file in 'w' mode (overwrite) with the frontmatter and new content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write('\n') # Ensure there's a newline after the frontmatter
        f.write(processed_content)
    
    return redirect(url_for('index'))

# --- Your other routes remain the same ---
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image file', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return f"![](/assets/images/{unique_filename})"
    return 'Invalid file type', 400

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No video file', 400
    file = request.files['video']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_video_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext != 'mp4':
            return 'Only MP4 video files are supported', 400
        unique_filename = f"{uuid.uuid4().hex}.mp4"
        os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['VIDEO_FOLDER'], unique_filename)
        file.save(filepath)
        return f'{{% include video.html src="/assets/videos/{unique_filename}" %}}'
    return 'Invalid video file type. Only MP4 files are supported.', 400

@app.route('/assets/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/assets/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=7000)