from wtforms import Form, StringField, PasswordField, SelectField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.Length(
        min=2, max=20, message='Username is invalid!')])
    password = PasswordField('New Password', [validators.Length(
        min=8, max=20, message='Password is invalid!')])


class CommonForm(Form):
    username = StringField('Username', [validators.Length(
        min=2, max=20,
        message='Username must be between 2 and 20 characters long!')])
    email = StringField('Email Address', [validators.Length(
        min=6, max=35,
        message='Email must be between 6 and 35 characters long!'),
        validators.Email('Enter a valid email!')])
    first_name = StringField('First Name', [validators.Length(
        min=2, max=35,
        message='First name must be between 2 and 35 characters long!')])
    last_name = StringField('Last Name', [validators.Length(
        min=2, max=35,
        message='Last name must be between 2 and 35 characters long!')])


class RegistrationForm(CommonForm):
    password = PasswordField('New Password', [validators.Length(
        min=8, max=20,
        message='Password must be between 8 and 20 characters long!')])


class ProfileForm(CommonForm):
    time_zone = SelectField('Time Zone', choices=[
        ('UTC', 'Coordinated Universal Time (UTC)'),
        ('Eastern', 'Eastern -4'),
        ('Central', 'Central -5'),
        ('Mountain', 'Mountain -6'),
        ('Pacific', 'Pacific -7')])
