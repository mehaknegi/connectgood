"""
Forms for ConnectGood
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

SKILLS_CHOICES = [
    'Teaching',
    'Technology/Coding',
    'Marketing',
    'Event Planning',
    'Healthcare',
    'Legal Advice',
    'Writing/Content',
    'Design',
    'Fundraising',
    'Manual Labor'
]

class SignupForm(FlaskForm):
    """User signup form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('I am a', choices=[('volunteer', 'Volunteer'), ('ngo', 'NGO')], validators=[DataRequired()])

class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

class VolunteerProfileForm(FlaskForm):
    """Volunteer profile form"""
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    skills = SelectMultipleField('Skills', choices=[(s, s) for s in SKILLS_CHOICES], validators=[DataRequired()])
    interests = TextAreaField('Causes You Care About', validators=[DataRequired()])
    availability = SelectField('Availability', choices=[
        ('weekends', 'Weekends only'),
        ('weekdays', 'Weekday evenings'),
        ('flexible', 'Flexible schedule'),
        ('one-time', 'One-time events'),
        ('ongoing', 'Ongoing commitment')
    ], validators=[DataRequired()])
    hours_per_week = IntegerField('Hours per Week', validators=[DataRequired()])

class NGOProfileForm(FlaskForm):
    """NGO profile form"""
    organization_name = StringField('Organization Name', validators=[DataRequired(), Length(max=200)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    cause_area = SelectField('Cause Area', choices=[
        ('education', 'Education'),
        ('environment', 'Environment'),
        ('health', 'Healthcare'),
        ('poverty', 'Poverty Alleviation'),
        ('rights', 'Human Rights'),
        ('animals', 'Animal Welfare'),
        ('arts', 'Arts & Culture'),
        ('elderly', 'Elderly Care')
    ], validators=[DataRequired()])
    description = TextAreaField('What Help Do You Need?', validators=[DataRequired()])
    skills_required = SelectMultipleField('Skills Required', choices=[(s, s) for s in SKILLS_CHOICES], validators=[DataRequired()])
    commitment_type = SelectField('Time Commitment', choices=[
        ('one-time', 'One-time project'),
        ('short-term', 'Short-term (1-3 months)'),
        ('ongoing', 'Ongoing volunteer needed'),
        ('flexible', 'Flexible arrangement')
    ], validators=[DataRequired()])
