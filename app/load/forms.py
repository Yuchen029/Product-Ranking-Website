from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


# Form for upload product
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 32)])
    description = StringField('Description', validators=[DataRequired(), Length(1, 32)])
    price = FloatField('Price', validators=[DataRequired()])
    # image = FileField('Image', validators=[FileRequired(), FileAllowed('jpg', 'Images only!')])
    category = SelectField(label='category', validators=[DataRequired()], choices=[('food', 'Food'),
                                                                                   ('clothes', 'Clothes'),
                                                                                   ('electronics', 'Electronics'),
                                                                                   ('sports', 'Sports'),
                                                                                   ('books', 'Books'),
                                                                                   ('medicine', 'Medicine'),
                                                                                   ('life', 'Life'),
                                                                                   ('others', 'Others')])
    submit = SubmitField('Upload')


# Form for search price
class PriceForm(FlaskForm):
    lowPrice = FloatField('lowPrice', validators=[DataRequired()])
    highPrice = FloatField('highPrice', validators=[DataRequired()])
    submit = SubmitField('Search')


# Form for search product
class SearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('Search')


# Form for add comment
class CommentForm(FlaskForm):
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(1, 140)])
    star = SelectField("Star", validators=[DataRequired()], choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5)
    submit = SubmitField('Submit')
