from datetime import date

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Employee


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# class AddStudentForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     firstname = StringField('Firstname')
#     lastname = StringField('Lastname', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Add Student')
#
#     def validate_username(self, username):
#         if Student.query.filter_by(username=username.data).first():
#             raise ValidationError('This username is already taken. Please choose another')
#
#     def validate_email(self, email):
#         if Student.query.filter_by(email=email.data).first():
#             raise ValidationError('This email address is already registered. Please choose another')


class AddEmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    # employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_joining = DateField('Date of Joining', validators=[DataRequired()], default=date.today)
    current_role = StringField('Current Role', validators=[DataRequired()])
    past_roles = TextAreaField('Past Roles')
    skills = TextAreaField('Skills')
    experience = DecimalField('Experience', places=1, validators=[DataRequired()])
    educational_background = TextAreaField('Educational Background')
    # skill_points = IntegerField('Skill Points', default=0)
    # achievement_badge = StringField('Achievement Badge')
    submit = SubmitField('Add Employee')

    # def validate_employee_id(self, employee_id):
    #     if Employee.query.filter_by(employee_id=employee_id.data).first():
    #         raise ValidationError('This employee ID is already taken. Please choose another.')

    # def validate_name(self, name):
    #     if Employee.query.filter_by(name=name.data).first():
    #         raise ValidationError('An employee with this name already exists. Please choose another.')

    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')

# class UploadStudentsForm(FlaskForm):
#     student_file = FileField('New Students File', validators=[FileAllowed(['csv'])])
#     submit = SubmitField('Upload')


# class BorrowForm(FlaskForm):
#     student_id = StringField('Student ID', validators=[DataRequired()])
#     device_id = StringField('Device ID', validators=[DataRequired()])
#     submit = SubmitField('Borrow Device')
#
#     def validate_student_id(self, student_id):
#         if not student_id.data.isnumeric():
#             raise ValidationError('This must be a positive integer')
#         student = Student.query.get(student_id.data)
#         if not (student):
#             raise ValidationError('There is no student with this id in the system')
#         if not student.active:
#             raise ValidationError('This student has been dactivated and cannot borrow devices')
#         if Loan.query.filter(
#                     (Loan.student_id == student_id.data)
#                     &
#                     # (Loan.returndatetime.is_(None))
#                     (Loan.returndatetime.is_(None))
#                 ).first():
#             raise ValidationError('This student cannot borrow another item until the previous loan has been returned')
#
#     def validate_device_id(self, device_id):
#         if not device_id.data.isnumeric():
#             raise ValidationError('This must be a positive integer')
#         if Loan.query.filter(
#                     (Loan.device_id == device_id.data)
#                     &
#                     (Loan.returndatetime.is_(None))
#                 ).first():
#             raise ValidationError('This device cannot be borrowed as it is currently on loan')
#
# class DeactivateStudentForm(FlaskForm):
#     student_id = StringField('Student ID', validators=[DataRequired()])
#     submit = SubmitField('Deactivate Student')
#
#     def validate_student_id(self, student_id):
#         if not student_id.data.isnumeric():
#             raise ValidationError('This must be a positive integer')
#         student = Student.query.get(student_id.data)
#         if not student:
#             raise ValidationError('There is no student with this id in the system')
#         if not student.active:
#             raise ValidationError('This student has already been deactivated')
#
# class ToggleActiveForm(FlaskForm):
#     submit = SubmitField('Toggle Active')
