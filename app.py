from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class BookPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Unknown Author')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Book post ' + str(self.id)

# Search function
@app.route('/book-posts/result', methods=['GET'])
def search():
    search = request.args.get('search')

    if search:
        posts = BookPost.query.filter(BookPost.title.contains(search) | 
        BookPost.author.contains(search) | BookPost.synopsis.contains(search))
        return render_template('result.html', posts=posts)
    else:
        all_posts = BookPost.query.all()
        return render_template('book-post.html', posts=all_posts)

# GET and POST Book posts
@app.route('/book-posts', methods=['GET', 'POST'])
def posts():
    
    if request.method == 'POST':
        post_title = request.form['title']
        post_synopsis = request.form['synopsis']
        post_author = request.form['author']
        new_post = BookPost(title=post_title, synopsis=post_synopsis, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/book-posts')
    else:
        all_posts = BookPost.query.order_by(BookPost.date_posted.desc()).all()
        return render_template('book-posts.html', posts=all_posts)

# Delete Book posts
@app.route('/book-posts/delete/<int:id>')
def delete(id):
    post = BookPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/book-posts')

# Edit Book posts
@app.route('/book-posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BookPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.synopsis = request.form['synopsis']
        db.session.commit()
        return redirect('/book-posts')
    else:
        return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)