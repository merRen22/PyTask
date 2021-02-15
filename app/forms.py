from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Start')


class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('✏ Create')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('🗑 Delete')


class UpdateTodoForm(FlaskForm):
    submit = SubmitField('❗ Update')
