from flask import render_template, redirect, url_for, flash, request, abort, \
    current_app, Response, json, jsonify
from flask_login import current_user, login_required
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous():
        return redirect(url_for('auth.login'))
    else:
        form = PostForm()
        if current_user.can(Permission.WRITE_ARTICLES) and \
                form.validate_on_submit():
            # 'current_user._get_current_object': get the actual user object
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('main.index'))
        # page number to render comes from the request's query string
        # default to the first page when no page is give
        # 'type=int' ensures that if the argument cannot be converted to an int
        # then the default value is returned
        page = request.args.get('page', 1, type=int)
        # paginate() takes the page number and the number of items per page
        # 'error_out=False' will return an empty list for invalid pages
        pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        # the 'pagination' object has many attributes/methods that make it
        # easy to generate page links
        return render_template('index.html', form=form, posts=posts,
                               pagination=pagination)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # change values based on form input
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    # set inital values
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.', 'success')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.', 'success')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.', 'error')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash('You are already following this user.', 'error')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username, 'success')
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.', 'error')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.', 'error')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username, 'success')
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.', 'error')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='main.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
@login_required
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='main.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/company/<int:id>')
@login_required
def company(id):
    # user = User.query.filter_by(username=username).first_or_404()
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('startup.html')


@main.route('/_search')
@login_required
def search():
    query = request.args.get('query', '', type=str).lower()
    results = [
        {'id': 1, 'name': 'Alabama'},
        {'id': 2, 'name': 'Arizona'},
        {'id': 3, 'name': 'Arkansas'},
        {'id': 4, 'name': 'California'},
        {'id': 5, 'name': 'Colorado'},
        {'id': 6, 'name': 'Connecticut'},
        {'id': 7, 'name': 'Delaware'},
        {'id': 8, 'name': 'Florida'},
        {'id': 9, 'name': 'Georgia'},
        {'id': 10, 'name': 'Hawaii'},
        {'id': 11, 'name': 'Idaho'},
        {'id': 12, 'name': 'Illinois'},
        {'id': 13, 'name': 'Indiana'},
        {'id': 14, 'name': 'Iowa'},
        {'id': 15, 'name': 'Kansas'},
        {'id': 16, 'name': 'Kentucky'},
        {'id': 17, 'name': 'Louisiana'},
        {'id': 18, 'name': 'Maine'},
        {'id': 19, 'name': 'Maryland'},
        {'id': 20, 'name': 'Massachusetts'},
        {'id': 21, 'name': 'Michigan'},
        {'id': 22, 'name': 'Minnesota'},
        {'id': 23, 'name': 'Mississippi'},
        {'id': 24, 'name': 'Missouri'},
        {'id': 25, 'name': 'Montana'},
        {'id': 26, 'name': 'Nebraska'},
        {'id': 27, 'name': 'Nevada'},
        {'id': 28, 'name': 'New Hampshire'},
        {'id': 29, 'name': 'New Jersey'},
        {'id': 30, 'name': 'New Mexico'},
        {'id': 31, 'name': 'New York'},
        {'id': 32, 'name': 'North Carolina'},
        {'id': 33, 'name': 'North Dakota'},
        {'id': 34, 'name': 'Ohio'},
        {'id': 35, 'name': 'Oklahoma'},
        {'id': 36, 'name': 'Oregon'},
        {'id': 37, 'name': 'Pennsylvania'},
        {'id': 38, 'name': 'Rhode Island'},
        {'id': 39, 'name': 'South Carolina'},
        {'id': 40, 'name': 'South Dakota'},
        {'id': 41, 'name': 'Tennessee'},
        {'id': 42, 'name': 'Texas'},
        {'id': 43, 'name': 'Utah'},
        {'id': 44, 'name': 'Vermont'},
        {'id': 45, 'name': 'Virginia'},
        {'id': 46, 'name': 'Washington'},
        {'id': 47, 'name': 'West Virginia'},
        {'id': 48, 'name': 'Wisconsin'},
        {'id': 49, 'name': 'Wyoming'},
    ]
    rt_results = [l for l in results if l['name'].lower().startswith(query)]
    return jsonify(results=rt_results)
    # return Response(json.dumps(rt_results), mimetype='application/json')


@main.route('/_search_prefetch')
@login_required
def search_prefetch():
    results = [
        # {'id': 1, 'name': 'Alabama'},
        # {'id': 2, 'name': 'Arizona'},
        # {'id': 3, 'name': 'Arkansas'},
        # {'id': 4, 'name': 'California'},
        # {'id': 5, 'name': 'Colorado'},
        # {'id': 6, 'name': 'Connecticut'},
        # {'id': 7, 'name': 'Delaware'},
        # {'id': 8, 'name': 'Florida'},
        # {'id': 9, 'name': 'Georgia'},
        # {'id': 10, 'name': 'Hawaii'},
        # {'id': 11, 'name': 'Idaho'},
        # {'id': 12, 'name': 'Illinois'},
        # {'id': 13, 'name': 'Indiana'},
        # {'id': 14, 'name': 'Iowa'},
        # {'id': 15, 'name': 'Kansas'},
        # {'id': 16, 'name': 'Kentucky'},
        # {'id': 17, 'name': 'Louisiana'},
        # {'id': 18, 'name': 'Maine'},
        # {'id': 19, 'name': 'Maryland'},
        # {'id': 20, 'name': 'Massachusetts'},
        # {'id': 21, 'name': 'Michigan'},
        # {'id': 22, 'name': 'Minnesota'},
        # {'id': 23, 'name': 'Mississippi'},
        # {'id': 24, 'name': 'Missouri'},
        # {'id': 25, 'name': 'Montana'},
        # {'id': 26, 'name': 'Nebraska'},
        # {'id': 27, 'name': 'Nevada'},
        # {'id': 28, 'name': 'New Hampshire'},
        # {'id': 29, 'name': 'New Jersey'},
        # {'id': 30, 'name': 'New Mexico'},
        # {'id': 31, 'name': 'New York'},
        # {'id': 32, 'name': 'North Carolina'},
        # {'id': 33, 'name': 'North Dakota'},
        # {'id': 34, 'name': 'Ohio'},
        # {'id': 35, 'name': 'Oklahoma'},
        # {'id': 36, 'name': 'Oregon'},
        # {'id': 37, 'name': 'Pennsylvania'},
        # {'id': 38, 'name': 'Rhode Island'},
        # {'id': 39, 'name': 'South Carolina'},
        # {'id': 40, 'name': 'South Dakota'},
        # {'id': 41, 'name': 'Tennessee'},
        # {'id': 42, 'name': 'Texas'},
        # {'id': 43, 'name': 'Utah'},
        # {'id': 44, 'name': 'Vermont'},
        # {'id': 45, 'name': 'Virginia'},
        # {'id': 46, 'name': 'Washington'},
        # {'id': 47, 'name': 'West Virginia'},
        {'id': 48, 'name': 'Wisconsin'},
        {'id': 49, 'name': 'Wyoming'},
    ]
    return jsonify(results=results)
