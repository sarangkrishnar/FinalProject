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

    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError('This email address is already registered. Please choose another')


class UploadEmployeesForm(FlaskForm):
    employee_file = FileField('Upload the csv file with employee data', validators=[
        DataRequired(), FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload')


class SkillAssessmentForm(FlaskForm):
    # Self-Assessment Fields
    self_assessed_skills = TextAreaField('Self-Assessed Skills', validators=[DataRequired()])
    self_assessment_rating = IntegerField('Self-Assessment Rating (1-10)', validators=[DataRequired()])
    new_competencies = TextAreaField('New Competencies of Interest')

    # Supervisor Assessment Fields
    supervisor_assessed_skills = TextAreaField('Skills Assessed by Supervisor', validators=[DataRequired()])
    supervisor_rating = IntegerField('Supervisor Rating (1-10)', validators=[DataRequired()])
    future_skills = TextAreaField('Skills Suggested for Future Development')

    submit = SubmitField('Submit Assessment')

    def validate_self_assessment_rating(self, self_assessment_rating):
        if self_assessment_rating.data < 1 or self_assessment_rating.data > 10:
            raise ValidationError('Self-Assessment Rating must be between 1 and 10.')

    def validate_supervisor_rating(self, supervisor_rating):
        if supervisor_rating.data < 1 or supervisor_rating.data > 10:
            raise ValidationError('Supervisor Rating must be between 1 and 10.')


class GoalSettingForm(FlaskForm):
    # Fields for Employee Goal Setting
    goals = TextAreaField('Goals', validators=[DataRequired()])
    kpis = TextAreaField('Key Performance Indicators (KPIs)', validators=[DataRequired()])

    # Field for Manager Feedback
    feedback = TextAreaField('Feedback on KPIs')

    submit = SubmitField('Submit')