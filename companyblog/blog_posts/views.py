# puppycompanyblog/blog_posts/views.py
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from companyblog import db
from companyblog.models import BlogPost
from companyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)

########### CRUD ############
# CREATE
@blog_posts.route('/create', methods = ['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(user_id = current_user.id, title = form.title.data, text = form.text.data)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

# Read (viewing a blog post)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title = blog_post.title, text = blog_post.text, date = blog_post.date, post = blog_post)

# Update
@blog_posts.route('/<int:blog_post_id>/update', methods = ['GET', 'POST'])
@login_required
def update(blog_post_id):
    # we will get the blog post from the database
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # if the person opened the blog post to update is not the one who posted it, he cannot post it
    if blog_post.author != current_user:
        abort(403)

    # if the persion opened opened the post to edit is the one who posted it, he can edit
    form = BlogPostForm()
    # when he clicks submit, all the details will be updated
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id = blog_post_id))

    # before clicking update, he will see the old data prefilled in the input areas
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title = 'Updating', form = form)

# Delete
# @blog_posts.route('/<int:blog_post_id>/delete', methods = ['POST']) # didn't use methods = ['GET', 'POST']
# @login_required
# def delete_post(blog_post_id):
#     blog_post = BlogPost.query.get_or_404(blog_post_id)
#     if blog_post.author != current_user:
#         abort(403)
#     db.session.delete(blog_post)
#     db.session.commit()
#     flash('Blog Post Deleted')
#     return redirect(url_for('core.index'))

@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
