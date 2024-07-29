import csv
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddEmployeeForm, UploadEmployeesForm, SkillAssessmentForm, \
    GoalSettingForm
from app.models import User, Employee
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
from email_validator import validate_email, EmailNotValidError


def updateBadge():
    employees = Employee.query.all()
    for employee in employees:
        if employee.skill_points > 20:
            employee.achievement_badge = 'Gold'
        elif 10 <= employee.skill_points <= 20:
            employee.achievement_badge = 'Silver'
        elif 5 <= employee.skill_points < 10:
            employee.achievement_badge = 'Bronze'
        else:
            employee.achievement_badge = 'Beginner'
        db.session.commit()


def isValidEmail(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


def silentRemove(filepath):
    try:
        os.remove(filepath)
    except:
        pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data):
                form.username.errors.append('This username is already taken. Please choose another')
            if User.query.filter_by(email=form.email.data):
                form.email.errors.append('This email address is already registered. Please choose another')
            flash(f'Registration failed', 'danger')
    return render_template('0_2_registration.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('0_3_login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
@login_required
def home():
    updateBadge()
    employee = Employee.query.filter_by(employee_id=current_user.user_id).first()
    top_employees = Employee.query.order_by(Employee.skill_points.desc()).limit(5).all()
    return render_template('1_home.html', title='Home', employee=employee, top_employees=top_employees)


@app.route('/')
@app.route('/leaderboard')
@login_required
def leaderboard():
    updateBadge()
    top_employees = Employee.query.order_by(Employee.skill_points.desc()).limit(5).all()
    employee = Employee.query.filter_by(employee_id=current_user.user_id).first()
    return render_template('1_home_1_leaderboard.html', title='Leaderboard', employee=employee,
                           top_employees=top_employees)


@app.route('/employeeProfile', methods=['GET'])
@login_required
def employeeProfile():
    updateBadge()
    employee = Employee.query.filter_by(employee_id=current_user.user_id).first()
    return render_template('1_home_2_employeeProfile.html', title='Employee Pofile', employee=employee)


@app.route('/updateEmployeeProfile', methods=['GET', 'POST'])
@login_required
def updateEmployeeProfile():
    employee = Employee.query.get_or_404(current_user.user_id)
    if request.method == 'POST':
        if request.form['date_of_joining']:
            try:
                employee.date_of_joining = datetime.strptime(request.form['date_of_joining'], '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format for Date of Joining.', 'danger')
                return redirect(url_for('updateEmployeeProfile'))
        if request.form['email']:
            employee.email = request.form['email']
        if request.form['current_role']:
            employee.current_role = request.form['current_role']
        if request.form['past_roles']:
            employee.past_roles = request.form['past_roles']
        if request.form['skills']:
            employee.skills = request.form['skills']
        if request.form['experience']:
            employee.experience = request.form['experience']
        if request.form['educational_background']:
            employee.educational_background = request.form['educational_background']
        if request.form['skill_points']:
            employee.skill_points = request.form['skill_points']
        if request.form['achievement_badge']:
            employee.achievement_badge = request.form['achievement_badge']
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('employeePofile'))
    updateBadge()
    return render_template('1_home_3_updateEmployeeProfile.html', title='Update Profile', employee=employee)


@app.route('/skillAssessment', methods=['GET', 'POST'])
@login_required
def skillAssessment():
    employee = Employee.query.get_or_404(current_user.user_id)
    form = SkillAssessmentForm()
    if form.validate_on_submit():
        if form.self_assessed_skills.data or form.new_competencies.data:
            flash('Employee self-assessment has been saved.', 'success')
        if form.supervisor_assessed_skills.data or form.supervisor_rating.data or form.future_skills.data:
            flash('Supervisor assessment has been saved.', 'success')
        return redirect(url_for('skillAssessment'))
    return render_template('1_home_4_skillAssessment.html', title='Skill Assessment', form=form, employee=employee)


@app.route('/goalSetting', methods=['GET', 'POST'])
@login_required
def goalSetting():
    employee = Employee.query.get_or_404(current_user.user_id)
    form = GoalSettingForm()
    if form.validate_on_submit():
        flash('Goals and KPIs have been submitted successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to a relevant page
    return render_template('1_home_5_goalSetting.html', form=form, title='Goal Setting', employee=employee)


class DevelopmentPlanForm:
    pass


@app.route('/developmentPlan', methods=['GET', 'POST'])
@login_required
def developmentPlan():
    employee = Employee.query.get_or_404(current_user.user_id)
    plan = """
1. Development Goals

Goal 1: Enhance Leadership Skills

Objective: Prepare Manju for potential leadership roles within the data science team.

Actions:
- Enroll in a Leadership Training Program.
- Attend workshops or seminars on management and team leadership.
- Mentor junior data scientists and lead internal projects.

Timeline: 6 months

Measurement: Successful completion of training programs and positive feedback from team members.

Goal 2: Advance Expertise in Machine Learning and AI

Objective: Deepen knowledge and skills in machine learning and artificial intelligence.

Actions:
- Complete advanced courses in machine learning and AI (e.g., deep learning, reinforcement learning).
- Work on complex AI projects and case studies.
- Contribute to research papers or industry publications.

Timeline: 1 year

Measurement: Certification in advanced machine learning courses and successful delivery of AI projects.
    """
    return render_template('1_home_6_developmentPlan.html', title='Development Plan', employee=employee, plan=plan)


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    # employee = Employee.query.filter_by(employee_id=current_user.user_id).all()
    return render_template('2_admin.html', title='Admin')


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
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add Employee: {str(e)}', 'danger')
            if Employee.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another.')
    return render_template('2_admin_1_addEmployee.html', title='Add Employee', form=form)


@app.route('/bulkAddEmployee', methods=['GET', 'POST'])
@login_required
def bulkAddEmployee():
    form = UploadEmployeesForm()
    if form.validate_on_submit():
        if form.employee_file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.employee_file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.employee_file.data.save(filepath)
            try:
                with open(filepath, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    error_count = 0
                    row = next(reader)
                    if row != ['Name', 'Email', 'Date of Joining', 'Current Role', 'Past Roles', 'Skills', 'Experience',
                               'Educational Background', 'Skill Points', 'Achievement Badge']:
                        form.employee_file.errors.append(
                            'First row of file must be a Header row containing "Name, Email, Date of Joining, Current Role, Past Roles, Skills, Experience, Educational Background, Skill Points, Achievement Badge"')
                        raise ValueError()
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.employee_file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 10:
                            form.employee_file.errors.append(f'Row {row_num} does not have precisely 10 fields')
                            error_count += 1
                        if Employee.query.filter_by(email=row[1]).first():
                            form.employee_file.errors.append(
                                f'Row {row_num} has email {row[1]}, which is already in use')
                            error_count += 1
                        if not isValidEmail(row[1]):
                            form.employee_file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                            error_count += 1
                        try:
                            date_of_joining = datetime.strptime(row[2], '%Y-%m-%d').date()
                            experience = float(row[6])
                        except ValueError as e:
                            form.employee_file.errors.append(f'Row {row_num} has invalid data: {e}')
                            error_count += 1
                            continue

                        if error_count == 0:
                            employee = Employee(
                                name=row[0],
                                email=row[1],
                                date_of_joining=date_of_joining,
                                current_role=row[3],
                                past_roles=row[4],
                                skills=row[5],
                                experience=experience,
                                educational_background=row[7],
                                skill_points=int(row[8]),
                                achievement_badge=row[9]
                            )
                            db.session.add(employee)
                if error_count > 0:
                    raise ValueError
                db.session.commit()
                flash(f'New Employees Uploaded', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                flash(f'New employees upload failed: {e}', 'danger')
                db.session.rollback()
            finally:
                silentRemove(filepath)
    return render_template('2_admin_2_bulkAddEmployee.html', title='Bulk Add Employee', form=form)


@app.route('/listAllEmployees', methods=['GET'])
def listAllEmployees():
    employees = Employee.query.all()
    return render_template('test_listAllEmployees.html', title='List All Employees', employees=employees)


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
#             return redirect(url_for('home'))
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
#                 return redirect(url_for('home'))
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
