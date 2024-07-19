from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Since we named our primary key "user_id", instead of "id", we have to override the
    # get_id() from the UserMixin to return the id, and it has to be returned as a string
    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"user(id='{self.user_id}', '{self.username}', '{self.email}')"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    date_of_joining = db.Column(db.Date, nullable=False)
    current_role = db.Column(db.String(64), nullable=False)
    past_roles = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Numeric(precision=4, scale=1), nullable=False)  # Allows up to 999.9 years of experience
    educational_background = db.Column(db.Text, nullable=False)
    skill_points = db.Column(db.Integer, nullable=True, default=0)
    achievement_badge = db.Column(db.String(64), nullable=True)

    # loans = db.relationship('Loan', backref='employee', lazy='dynamic')  # Adjust if necessary

    def __repr__(self):
        return (f"Employee(id='{self.employee_id}', name='{self.name}', date_of_joining='{self.date_of_joining}', "
                f"current_role='{self.current_role}', past_roles='{self.past_roles}', skills='{self.skills}', "
                f"experience='{self.experience}', educational_background='{self.educational_background}', "
                f"skill_points='{self.skill_points}', achievement_badge='{self.achievement_badge}')")

# class Loan(db.Model):
#     __tablename__ = 'loans'
#     loan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     device_id = db.Column(db.Integer, nullable=False)
#     borrowdatetime = db.Column(db.DateTime, nullable=False)
#     returndatetime = db.Column(db.DateTime, nullable=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
#
#     def __repr__(self):
#         return f"loan(loan_id='{self.loan_id}', device_id='{self.device_id}', borrowdatetime='{self.borrowdatetime}' , returndatetime='{self.returndatetime}', '{self.student}')"
