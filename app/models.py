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

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    loans = db.relationship('Loan', backref='student', lazy='dynamic')

    def __repr__(self):
        return f"student(id='{self.student_id}', '{self.username}', '{self.lastname}', '{self.firstname}' , '{self.email}', active='{self.active}')"


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    device_id = db.Column(db.Integer, nullable=False)
    borrowdatetime = db.Column(db.DateTime, nullable=False)
    returndatetime = db.Column(db.DateTime, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    def __repr__(self):
        return f"loan(loan_id='{self.loan_id}', device_id='{self.device_id}', borrowdatetime='{self.borrowdatetime}' , returndatetime='{self.returndatetime}', '{self.student}')"


