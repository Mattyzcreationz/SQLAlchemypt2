from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mattyz:password@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

# Root route redirecting to users
@app.route('/')
def root():
    return redirect('/users')

# User index route
@app.route('/users')
def user_index():
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('home.html', users=users)

# New user form route
@app.route('/users/newuser', methods=['GET'])
def new_user_form():
    return render_template('new.html')

# Create new user route
@app.route('/users/newuser', methods=['POST'])
def create_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url']
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# User detail route
@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('display.html', user=user)

# Edit user route
@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

# Update user route
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect('/users')

# Delete user route
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=user_id 
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('display.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
