from app import app, db, login
from flask import session
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddTodoForm, EditTodoForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Todo
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
import os


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.now(timezone.utc)
        db.session.commit()
        
@app.before_request
def check_inactivity():
    session.permanent = True
    session.modified = True  # This keeps the session active when the user is interacting

    # Check if user is logged in
    if 'last_activity' in session:
        now = datetime.now()
        last_activity = session['last_activity']

        # If the time since the last activity is more than 5 minutes
        if (now - last_activity).total_seconds() > 300:  # 300 seconds = 5 minutes
            return redirect(url_for('logout_inactive'))

    # Update last_activity for every new request
    session['last_activity'] = datetime.now()
        
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user,todos=Todo.query.filter_by(user_id=current_user.id).all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.files['image']:
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.jpg'
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, phone=form.phone.data, address=form.address.data, zipcode=form.zipcode.data, image=filename)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    image = None
    if form.validate_on_submit():
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # remove current image file if user uploads a new image
            current_image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.image)
            if current_user.image != 'default.jpg' and os.path.exists(current_image_path):
                os.remove(current_image_path)
            current_user.image = filename
        current_user.firstname=form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.address = form.address.data
        current_user.zipcode = form.zipcode.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.image.data = current_user.image
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        form.zipcode.data = current_user.zipcode
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/add_todo', methods=['GET', 'POST'])
@login_required
def add_todo():
    form = AddTodoForm()
    if form.validate_on_submit():
        todo = Todo(title=form.title.data, description=form.description.data, status=form.status.data, user_id=current_user.id, date_todo=form.date_todo.data)
        db.session.add(todo)
        db.session.commit()
        flash('Your todo has been added.')
        return redirect(url_for('index'))
    return render_template('add_todo.html', title='Add Todo', form=form)

@app.route('/edit_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    form = EditTodoForm()
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.status = form.status.data
        todo.date_todo = form.date_todo.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = todo.title
        form.description.data = todo.description
        form.status.data = todo.status
        form.date_todo.data = todo.date_todo
    return render_template('edit_todo.html', title='Edit Todo', form=form)

@app.route('/delete_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Your todo has been deleted.')
    return redirect(url_for('index'))   


# logout user after 5 minutes of inactivity
@app.route('/logout_inactive')
def logout_inactive():
    logout_user()
    session.pop('last_activity', None)  # Remove last_activity from session
    return redirect(url_for('index'))

