from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddEmployeeForm
# , ToggleActiveForm, AddStudentForm)
from app.models import User, Employee
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import and_


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Login for {form.username.data}', 'success')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data):
                form.username.errors.append('This username is already taken. Please choose another')
            if User.query.filter_by(email=form.email.data):
                form.email.errors.append('This email address is already registered. Please choose another')
            flash(f'Registration failed', 'danger')
    return render_template('registration.html', title='Register', form=form)

@app.route('/employeePofile', methods=['GET'])
@login_required
def employeePofile():
    employee = Employee.query.filter_by(employee_id=current_user.user_id).all()
    return render_template('employeePofile.html', title='Employee Pofile', employees=employee)

@app.route('/listAllEmployees', methods=['GET'])
@login_required
def listAllEmployees():
    employees = Employee.query.all()
    return render_template('listAllEmployees.html', title='List All Employees', employees=employees)

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    # employee = Employee.query.filter_by(employee_id=current_user.user_id).all()
    return render_template('admin.html', title='Admin')

@app.route('/addEmployee', methods=['GET', 'POST'])
@login_required
def addEmployee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(
            name=form.name.data,
            email=form.email.data,
            date_of_joining=form.date_of_joining.data,
            current_role=form.current_role.data,
            past_roles=form.past_roles.data,
            skills=form.skills.data,
            experience=float(form.experience.data),
            educational_background=form.educational_background.data
        )
        db.session.add(new_employee)
        try:
            db.session.commit()
            flash(f'New Employee added: {form.name.data}', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add Employee: {str(e)}', 'danger')
            if Employee.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another.')
    return render_template('addEmployee.html', title='Add Employee', form=form)

# def is_valid_email(email):
#     try:
#         validate_email(email, check_deliverability=False)
#     except EmailNotValidError as error:
#         return False
#     return True
#
#
# # Attempt to remove a file but silently cancel any exceptions if anything goes wrong
# def silent_remove(filepath):
#     try:
#         os.remove(filepath)
#     except:
#         pass
#     return

# # 2
# @app.route('/shopping', methods=['GET', 'POST'])
# @login_required
# def shopping():
#     sform = ShoppingForm()
#     tform = BuyForm()
#     tobuy = ToBuy.query.filter_by(user_id=current_user.user_id)
#     bought = Bought.query.filter_by(user_id=current_user.user_id)
#     if sform.validate_on_submit():
#         new_tobuy = ToBuy(item=sform.item.data, user_id=current_user.user_id)
#         db.session.add(new_tobuy)
#         try:
#             db.session.commit()
#             flash(f'New Item {sform.item.data} added to to buy list', 'success')
#             return redirect(url_for('index'))
#         except:
#             db.session.rollback()
#             flash(f'Item not added. Please try again', 'danger')
#     if tform.validate_on_submit():
#         buyitem = request.values.get('buy')
#         new_bought = Bought(item=buyitem, user_id=current_user.user_id)
#         # del_tobuy = ToBuy.query.filter(and_(item=buyitem, user_id=current_user.user_id))
#         db.session.add(new_bought)
#         # db.session.delete(del_tobuy)
#         db.session.commit()
#         return redirect(url_for('shopping'))
#     return render_template('shopping.html', title='Shopping', sform=sform, tform=tform, tobuy=tobuy, bought=bought)


# 4
# @app.route('/upload_tobuylist', methods=['GET', 'POST'])
# @login_required
# def upload_tobuylist():
#     form = UploadItemsForm()
#     if form.validate_on_submit():
#         if form.items_file.data:
#             unique_str = str(uuid4())
#             filename = secure_filename(f'{unique_str}-{form.items_file.data.filename}')
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             form.items_file.data.save(filepath)
#             try:
#                 with (open(filepath, "r") as txtfile):
#                     items = []
#                     for line in txtfile:
#                         line = line.strip()
#                         items.append(line)
#                     for i in items:
#                         new_tobuy = ToBuy(item=i, user_id=current_user.user_id)
#                         db.session.add(new_tobuy)
#                 db.session.commit()
#                 flash(f'To buy list Uploaded', 'success')
#                 return redirect(url_for('index'))
#             except:
#                 flash(f'To buy list upload failed: '
#                       'please try again', 'danger')
#                 db.session.rollback()
#             finally:
#                 silent_remove(filepath)
#     return render_template('upload_tobuylist.html', title='Upload to buy list', form=form)


# Handler for 413 Error: "RequestEntityTooLarge". This error is caused by a file upload
# exceeding its permitted Capacity
# Note, you should add handlers for:
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413
