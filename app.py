from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import datetime
import re
import os
import urllib.parse
import markdown  # Import markdown library
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'assets/images'
VIDEO_FOLDER = 'assets/videos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4'}  # Only MP4 now

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size for videos

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def extract_youtube_id(url):
    """Extract YouTube video ID from various YouTube URL formats"""
    parsed_url = urllib.parse.urlparse(url)
    
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path.lstrip('/')
    
    if parsed_url.netloc in ['www.youtube.com', 'youtube.com']:
        query = urllib.parse.parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    
    return None

def process_content(content):
    """Process content to convert YouTube links to embed format"""
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
    """Format date as 'Monday the 18th of August 2025'"""
    day_name = date_obj.strftime('%A')
    day = date_obj.day
    month_name = date_obj.strftime('%B')
    year = date_obj.year
    
    # Add ordinal suffix to day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    return f"{day_name} the {day}{suffix} of {month_name} {year}"

@app.route('/', methods=['GET'])
def index():
    # Get today's date
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    posts_dir = '_posts'
    filename = f"{today}-*.md"  # Match today's Markdown file

    # Find the Markdown file for today
    matching_files = [f for f in os.listdir(posts_dir) if re.match(rf"{today}-.*\.md", f)]

    if matching_files:
        filepath = os.path.join(posts_dir, matching_files[0])
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract content after frontmatter
        _, content = content.split('---', 2)[-1], content.split('---', 2)[-1]

        # Convert Markdown to HTML
        html_content = markdown.markdown(content)
    else:
        html_content = "<p>No content available for today.</p>"

    return render_template('index.html', preview_html=html_content)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image file', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Return markdown image syntax
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
        # Only accept MP4 files
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext != 'mp4':
            return 'Only MP4 video files are supported', 400
            
        unique_filename = f"{uuid.uuid4().hex}.mp4"
        
        # Ensure upload directory exists
        os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
        
        # Save the file
        filepath = os.path.join(app.config['VIDEO_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Return Jekyll include syntax for video (MP4 only)
        return f'{{% include video.html src="/assets/videos/{unique_filename}" %}}'
    
    return 'Invalid video file type. Only MP4 files are supported.', 400

@app.route('/assets/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/assets/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)

@app.route('/save', methods=['POST'])
def save():
    now = datetime.datetime.now()
    title = format_date_title(now)  # Use the new formatted title
    content = request.form['content']
    
    processed_content = process_content(content)
    
    posts_dir = os.path.join('_posts')
    os.makedirs(posts_dir, exist_ok=True)
    
    filepath = os.path.join(posts_dir, create_filename(title))
    
    if os.path.exists(filepath):
        with open(filepath, 'a') as f:
            f.write('\n\n')
            f.write(processed_content)
    else:
        with open(filepath, 'w') as f:
            f.write(create_frontmatter(title))
            f.write(processed_content)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=7000)