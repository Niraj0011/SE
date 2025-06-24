from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage (loaded once on startup)
articles = []
comments = []

class Article:
    def __init__(self, articleID, title, content, author, pubDate):
        self.articleID = articleID
        self.title = title
        self.content = content
        self.author = author
        self.pubDate = pubDate

    def getInfo(self):
        return f"Article ID: {self.articleID}, Title: {self.title}, Author: {self.author}, Published: {self.pubDate.strftime('%Y-%m-%d %H:%M')}"

class Comment:
    def __init__(self, commentID, articleID, user, text, postDate):
        self.commentID = commentID
        self.articleID = articleID
        self.user = user
        self.text = text
        self.postDate = postDate

# Load data once on startup
def load_data():
    global articles, comments
    file_path_articles = 'c:/Users/ACER/OneDrive/Desktop/SE/articles.csv'
    file_path_comments = 'c:/Users/ACER/OneDrive/Desktop/SE/comments.csv'
    try:
        if os.path.exists(file_path_articles):
            with open(file_path_articles, 'r') as file:
                reader = csv.DictReader(file)
                articles = [
                    Article(
                        int(row['articleID']),
                        row['title'],
                        row['content'],
                        row['author'],
                        datetime.fromisoformat(row['pubDate'])
                    ) for row in reader if all(k in row for k in ['articleID', 'title', 'content', 'author', 'pubDate'])
                ]
                print(f"Loaded {len(articles)} articles from {file_path_articles}")
        else:
            print(f"Articles CSV not found at {file_path_articles}, initializing empty")
            articles = []
        if os.path.exists(file_path_comments):
            with open(file_path_comments, 'r') as file:
                reader = csv.DictReader(file)
                comments = [
                    Comment(
                        int(row['commentID']),
                        int(row['articleID']),
                        row['user'],
                        row['text'],
                        datetime.fromisoformat(row['postDate'])
                    ) for row in reader if all(k in row for k in ['commentID', 'articleID', 'user', 'text', 'postDate'])
                ]
                print(f"Loaded {len(comments)} comments from {file_path_comments}")
        else:
            print(f"Comments CSV not found at {file_path_comments}, initializing empty")
            comments = []
    except Exception as e:
        print(f"Error loading data: {e}")
        articles = []
        comments = []

# Save data to CSV
def save_data():
    file_path_articles = 'c:/Users/ACER/OneDrive/Desktop/SE/articles.csv'
    file_path_comments = 'c:/Users/ACER/OneDrive/Desktop/SE/comments.csv'
    try:
        with open(file_path_articles, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['articleID', 'title', 'content', 'author', 'pubDate'])
            writer.writeheader()
            for a in articles:
                writer.writerow({
                    'articleID': a.articleID,
                    'title': a.title,
                    'content': a.content,
                    'author': a.author,
                    'pubDate': a.pubDate.isoformat()
                })
            file.flush()
            os.fsync(file.fileno())  # Ensure data is written to disk
            print(f"Saved {len(articles)} articles to {file_path_articles}")
        with open(file_path_comments, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['commentID', 'articleID', 'user', 'text', 'postDate'])
            writer.writeheader()
            for c in comments:
                writer.writerow({
                    'commentID': c.commentID,
                    'articleID': c.articleID,
                    'user': c.user,
                    'text': c.text,
                    'postDate': c.postDate.isoformat()
                })
            file.flush()
            os.fsync(file.fileno())
            print(f"Saved {len(comments)} comments to {file_path_comments}")
    except PermissionError as e:
        print(f"Permission error saving data: {e}")
    except Exception as e:
        print(f"Error saving data: {e}")

# Load data on startup
load_data()

# Routes
@app.route('/')
def index():
    print(f"Rendering index with {len(articles)} articles")
    return render_template('index.html', articles=articles)

@app.route('/article/<int:articleID>')
def view_article(articleID):
    print(f"Rendering article {articleID}")
    article = next((a for a in articles if a.articleID == articleID), None)
    article_comments = [c for c in comments if c.articleID == articleID]
    return render_template('article.html', article=article, comments=article_comments)

@app.route('/add_comment/<int:articleID>', methods=['POST'])
def add_comment(articleID):
    print(f"Adding comment to article {articleID}")
    user = request.form['user']
    text = request.form['text']
    commentID = max((c.commentID for c in comments), default=0) + 1
    comment = Comment(commentID, articleID, user, text, datetime.now())
    comments.append(comment)
    save_data()
    return redirect(url_for('view_article', articleID=articleID))

@app.route('/admin/add_article', methods=['GET', 'POST'])
def add_article():
    print(f"Handling add_article request, method: {request.method}")
    if request.method == 'POST':
        articleID = max((a.articleID for a in articles), default=0) + 1
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        if not any(a.title == title for a in articles):
            article = Article(articleID, title, content, author, datetime.now())
            articles.append(article)
            save_data()
            return redirect(url_for('index'))
        return "Article already exists!", 400
    return render_template('add_article.html')

if __name__ == '__main__':
    print("Starting app at", datetime.now())
    # My first web app! - Updated on June 23, 2025 at 02:53 AM
    app.run(debug=True, host='0.0.0.0', port=5001)
