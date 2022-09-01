import imp
from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
    # checking existed user --
        existing_user = User.query.filter((User.email == email) | (User.username == username)).all()
        if existing_user:
            flash("Username or Email is Token !!", 'danger')
            return redirect(url_for('signup'))
    # ------------------------
        User(email=email, username=username, password=password)
        flash("The new user has been created","success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/createpost', methods=["GET","POST"])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        print("hello !!")
        title = form.title.data
        body = form.body.data
        Post(title=title, body=body, user_id=current_user.id)
        flash(f"{title} has been created", 'secondary')
        return redirect(url_for('index'))
    return render_template('createpost.html', form=form)
    

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Hi {user.username}","success")
            return redirect(url_for('index'))
        else:
            flash("Incorrect credential","danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successfully","info")
    return redirect(url_for('index'))


@app.route('/posts/<post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<post_id>/edit', methods=["GET","POST"])
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    if post_to_edit.author != current_user:
        flash("You don't have permission to edit this post","danger")
        return redirect(url_for('view_post',post_id=post_id))
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        post_to_edit.update(title=title, body=body)
        flash(f'{post_to_edit.title} has been updated', 'success')
        return redirect(url_for('view_post',post_id=post_id))

    return render_template('editpost.html', post=post_to_edit, form=form)


@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash("You don't have permission to delete this post","danger")
        return redirect(url_for('index'))
    post_to_delete.delete()
    flash(f'{post_to_delete.title} has been deleted','info')
    return redirect(url_for('index'))    
