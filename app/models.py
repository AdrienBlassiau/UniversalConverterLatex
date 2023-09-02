import datetime

from django.db import models
from django.utils import timezone


CONTENT_FORMAT_CHOICES = (
    ('arc', 'Arc'),
    ('arr', 'Arrow'),
    ('cir', 'Circle'),
    ('dia', 'Diamond'), #Losange ...
    ('ell', 'Ellipse'),
    ('gra', 'Graph'),
    ('lin', 'Line'),
    ('mol', 'Molecule'),
    ('par', 'Parallelogram'),
    ('pol', 'Polygon'),
    ('rec', 'Rectangle'),
    ('sta', 'Star'),
    ('tra', 'Trapeze'),
    ('tre', 'Tree'),
)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class LatexDoc(models.Model):
    name = models.CharField(default='',max_length=200)
    content = models.TextField(default='')
    creat_date = models.DateTimeField('date creation')
    latex_type = models.CharField(choices=CONTENT_FORMAT_CHOICES, max_length=50)

    def __str__(self):
        return self.name


class Molecule(models.Model):
    name = models.CharField(default='',max_length=200)
    content = models.TextField(default='')
    creat_date = models.DateTimeField('date creation')

    def __str__(self):
        return self.name