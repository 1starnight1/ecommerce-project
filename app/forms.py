from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    TextAreaField, FloatField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError, NumberRange
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('电话', validators=[DataRequired(), Length(min=11, max=20)])
    address = TextAreaField('地址', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册')


class ProductForm(FlaskForm):
    name = StringField('商品名称', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('商品描述', validators=[DataRequired()])
    price = FloatField('价格', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('库存', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('分类', coerce=int, validators=[DataRequired()])
    submit = SubmitField('保存')


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('分类描述')
    submit = SubmitField('保存')


class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('收货地址', validators=[DataRequired()])
    phone = StringField('联系电话', validators=[DataRequired(), Length(min=11, max=20)])
    notes = TextAreaField('备注')
    submit = SubmitField('提交订单')


class ReviewForm(FlaskForm):
    rating = SelectField('评分', choices=[(5, '5星'), (4, '4星'), (3, '3星'), (2, '2星'), (1, '1星')], coerce=int)
    comment = TextAreaField('评论')
    submit = SubmitField('提交评价')