from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
import uuid
from decimal import Decimal
from .helpers import get_timer
from mutagen.mp4 import MP4,MP4StreamInfoError
from django.utils import timezone
from django.core.validators import validate_image_file_extension
from .validators import validate_is_video
from apps.category.models import Category
# from apps.questions.models import Question


def course_directory_path(instance, filename):
    return 'courses/{0}/{1}'.format(instance.title, filename)

def sector_directory_path(instance, filename):
    return 'courses/sector/{0}/{1}'.format(instance.title, filename)

def chapter_directory_path(instance, filename):
    return 'courses/{0}/{1}/{2}'.format(instance.course, instance.title, filename)

def lesson_directory_path(instance, filename):
    return 'courses/{0}/{1}/Lesson #{2}: {3}/{4}'.format(instance.course, instance.chapter, instance.lesson_number,instance.title, filename)


VOTES_CHOICES = (
	('U', 'Up Vote'),
	('D', 'Down Vote'),
)



class Course(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    dedic = (
        ('starter', 'Starter'),
        ('hobbyist', 'Hobbyist'),
        ('freelancer', 'Freelancer'),
        ('entrepreneur', 'Entrepreneur'),
    )
    
    payment = (
        ('paid', 'Paid'),
        ('free', 'Free'),
    )

    id =                models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    author =            models.UUIDField(blank=True, null=True)

    title =             models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(max_length=125, blank=True, null=True)
    description =       models.TextField(blank=True, null=True)
    thumbnail =         models.ImageField(upload_to=course_directory_path, blank=True, null=True) 
    sales_video =       models.FileField(upload_to=course_directory_path, blank=True, null=True)
    
    category =          models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    date_created =      models.DateTimeField(auto_now_add=True)

    keywords =          models.CharField(max_length=255, blank=True, null=True)
    slug =              models.SlugField(unique=True, default=uuid.uuid4)

    published =         models.DateTimeField(default=timezone.now)
    updated =           models.DateTimeField(auto_now=True)

    rating =            models.ManyToManyField('Rate',blank=True, related_name='rating_from_course')
    student_rating =    models.IntegerField(default=0, blank=True, null=True)

    slug_changes =      models.IntegerField(default=1, blank=True, null=True)
    
    language =          models.CharField(max_length=50, blank=True, null=True)
    level =             models.CharField(max_length=50, blank=True, null=True)
    taught =            models.CharField(max_length=120, blank=True, null=True)

    welcome_message =   models.CharField(max_length=1200, blank=True, null=True)
    congrats_message =  models.CharField(max_length=1200, blank=True, null=True)

    course_length =     models.CharField(default=0,max_length=20, blank=True, null=True)

    payment =           models.CharField(max_length=100, default='Paid', blank=True, null=True)

    price =             models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    compare_price =     models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # tiers =             models.ManyToManyField(Tier, blank=True)

    sold =              models.IntegerField(default=0, blank=True)
    students =          models.IntegerField(default=0, blank=True)
    views =             models.IntegerField(default=0, blank=True)
    best_seller =       models.BooleanField(default=False)

    goals =             models.BooleanField(default=False)
    course_structure =  models.BooleanField(default=False)
    setup =             models.BooleanField(default=False)
    film =              models.BooleanField(default=False)
    curriculum =        models.BooleanField(default=False)
    captions =          models.BooleanField(default=False)
    accessibility =     models.BooleanField(default=False)
    landing_page =      models.BooleanField(default=False)
    pricing =           models.BooleanField(default=False)
    promotions =        models.BooleanField(default=False)
    allow_messages =    models.BooleanField(default=False)

    sections =          models.ManyToManyField('Section', blank=True, related_name='section_from_course')
    what_learnt =       models.ManyToManyField('WhatLearnt', blank=True, related_name='whatlearnt_from_course')
    requisites =         models.ManyToManyField('Requisite', blank=True, related_name='requisite_from_course')
    who_is_for =        models.ManyToManyField('WhoIsFor', blank=True, related_name='whoisfor_from_course')
    resources =         models.ManyToManyField('Resource', blank=True, related_name='resources_from_course')

    status =            models.CharField(max_length=10, choices=options, default='draft')
    dedication =        models.CharField(max_length=100)

    objects =           models.Manager()  # default manager
    postobjects =       PostObjects()  # custom manager

    def __str__(self):
        return self.title

    def get_video(self):
        if self.thumbnail:
            return self.sales_video.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    def get_rating(self):
        ratings=self.rating.all()
        rate=0
        for rating in ratings:
            rate+=rating.rate_number
        try:
            rate/=len(ratings)
        except ZeroDivisionError:
            rate=0
        return rate

    def get_no_rating(self):
        return len(self.rating.all())

    def get_whatlearnt(self):
        return WhatLearnt.objects.filter(course=self)[:4]
    
    def get_requisites(self):
        return len(self.requisite.all())

    def get_brief_description(self):
        return self.description[:100]

    def get_total_lectures(self):
        lectures=0
        for section in self.course_section.all():
            lectures+=len(section.episodes.all())
        return lectures

    def total_course_length(self):
        length=Decimal(0.00)
        for section in self.course_section.all():
            for episode in section.episodes.all():
                length +=episode.length
        return get_timer(length)

    def get_price(self):
        price = 0
        if(self.price):
            price = self.price / 100
        return price
    
    def get_category_name(self):
        if(self.category):
            name = self.category.name
            return name
        else:
            return

    def get_view_count(self):
        game_views = ViewCount.objects.filter(post=self).count()
        return game_views

    class Meta:
        ordering = ('date_created',)


class ViewCount(models.Model):
    course = models.ForeignKey(Course, related_name='course_view_count', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"


class Rate(models.Model):
    rate_number=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    user =                  models.UUIDField(blank=True, null=True)
    course =                models.ForeignKey(Course, on_delete=models.CASCADE, related_name='rate_belongs_to_course', blank=True, null=True)


class Requisite(models.Model):
    position_id =             models.IntegerField(null=True, blank=True)
    title =             models.CharField(max_length=255)
    user =              models.UUIDField(blank=True, null=True)
    course =              models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requisite_belongs_to_course', blank=True, null=True)

    def __str__(self):
        return self.title

class WhatLearnt(models.Model):
    position_id =             models.IntegerField(null=True, blank=True)
    title =             models.CharField(max_length=255)
    user =              models.UUIDField(blank=True, null=True)
    course =              models.ForeignKey(Course, on_delete=models.CASCADE, related_name='whatlearnt_belongs_to_course', blank=True, null=True)

    def __str__(self):
        return self.title

class WhoIsFor(models.Model):
    position_id =             models.IntegerField(null=True, blank=True)
    title =             models.CharField(max_length=255)
    user =              models.UUIDField(blank=True, null=True)
    course =              models.ForeignKey(Course, on_delete=models.CASCADE, related_name='whoisfor_belongs_to_course', blank=True, null=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    id =                    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title =                 models.CharField(max_length=255, blank=True, null=True)
    learning_objective =    models.CharField(max_length=1200, blank=True, null=True)
    number =                models.IntegerField(blank=True, null=True)
    episodes =              models.ManyToManyField('Episode', blank=True)
    user =                  models.UUIDField(blank=True, null=True)
    published =             models.BooleanField(default=False)
    course =                models.ForeignKey(Course, on_delete=models.CASCADE, related_name='section_belongs_to_course', blank=True, null=True)

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return self.title

    def total_length(self):
        total=Decimal(0.00)
        for episode in self.episodes.all():
            total+=episode.length
        return get_timer(total,type='min')


class Episode(models.Model):
    id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title =             models.CharField(max_length=255)
    file =              models.FileField(upload_to='episodes', blank=True, null=True)
    filename =          models.CharField(max_length=1200, blank=True, null=True)
    content =           models.TextField(blank=True, null=True)
    description =       models.CharField(max_length=1200, blank=True, null=True)
    length =            models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    free =              models.BooleanField(default=False, blank=True, null=True)
    resources =         models.ManyToManyField('Resource', blank=True)
    questions =         models.ManyToManyField('Question', blank=True, related_name='episode_questions')
    episode_number =    models.IntegerField(blank=True, null=True)
    user =              models.UUIDField(blank=True, null=True)
    course =            models.ForeignKey(Course, on_delete=models.CASCADE, related_name='episode_belongs_to_course', blank=True, null=True)
    section_uuid =      models.CharField(max_length=1200, blank=True, null=True)
    date =              models.DateTimeField(auto_now=True, blank=True, null=True)
    published =         models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ('episode_number',)

    def __str__(self):
        return self.title

    def get_video_length(self):
        if(self.file):
            try:
                video=MP4(self.file)
                return video.info.length
                
            except MP4StreamInfoError:
                return 0.0
        else:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)
    
    def get_absolute_url(self):
        if(self.file):
            return self.file.url

    def save(self,*args, **kwargs):
        self.length=self.get_video_length()
        return super().save(*args, **kwargs)


class Resource(models.Model):
    title =             models.CharField(max_length=255)
    file =              models.FileField(upload_to=course_directory_path, blank=True, null=True)
    url =               models.URLField(blank=True, null=True)
    user =              models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.UUIDField(blank=True, null=True)
    title = models.CharField(max_length=120)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    episode = models.ForeignKey('Episode', on_delete=models.CASCADE, related_name='episode_belongs_to_question', blank=True, null=True)
    correct_answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='correct_answer',null=True)
    update_date = models.DateTimeField(auto_now_add=True)
    has_accepted_answer = models.BooleanField(default=False)
    question_uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    likes = models.ManyToManyField('Like', blank=True, related_name='question_likes')
    dislikes = models.ManyToManyField('Like', blank=True, related_name='question_dislikes')

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def liked_by_user(self):
        is_like = False
        for like in self.likes.all():
            if like.user == self.user:
                is_like = True
        return is_like
    
    def disliked_by_user(self):
        is_dislike = False
        for dislike in self.dislikes.all():
            if dislike.user == self.user:
                is_dislike = True
        return is_dislike

    def likes_count(self):
        likes_count = self.likes.count()
        return likes_count

    def dislikes_count(self):
        dislikes_count = self.dislikes.count()
        return dislikes_count

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_answers(self):
        return Answer.objects.filter(question=self)


class Answer(models.Model):
    answer_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.UUIDField(blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    is_accepted_answer = models.BooleanField(default=False)
    likes = models.ManyToManyField('Like', blank=True, related_name='answer_likes')
    dislikes = models.ManyToManyField('Like', blank=True, related_name='answer_dislikes')

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.question.title

    def liked_by_user(self):
        is_like = False
        for like in self.likes.all():
            if like == self.user:
                is_like = True
        return is_like

    def disliked_by_user(self):
        is_dislike = False
        for dislike in self.dislikes.all():
            if dislike.user == self.user:
                is_dislike = True
        return is_dislike
    
    def likes_count(self):
        likes_count = self.likes.count()
        return likes_count

    def dislikes_count(self):
        dislikes_count = self.dislikes.count()
        return dislikes_count


class Like(models.Model):
    user =      models.UUIDField(blank=True, null=True)


class Dislike(models.Model):
    user =      models.UUIDField(blank=True, null=True)




class ViewedCoursesLibrary(models.Model):
    user =                models.UUIDField(blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)

    class Meta:
        verbose_name_plural="Viewed Courses"
    
    def __str__(self):
        return self.user