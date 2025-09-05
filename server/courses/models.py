from django.db import models
from django.contrib.auth.models import User
from utils.enum_type import SKILL_TYPES, HINT_TYPES, ACTION_TYPES, RECOMMENDATION_TYPES

# ---------------- Topics ----------------
class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    position = models.IntegerField()

class Sublesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sublessons')
    title = models.CharField(max_length=100)
    position = models.IntegerField()

# ---------------- Exercises ----------------
class Exercise(models.Model):
    sublesson = models.ForeignKey(Sublesson, on_delete=models.CASCADE, related_name='exercises')
    content = models.TextField()
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES)
    answer_key = models.TextField()
    xp = models.IntegerField(default=5)
    max_attempts = models.IntegerField(default=3)
    language_code = models.CharField(max_length=10, default='en')

class ExerciseHint(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='hints')
    word_in_exercise = models.CharField(max_length=50)
    hint_text = models.CharField(max_length=255)
    hint_type = models.CharField(max_length=10, choices=HINT_TYPES, default='manual')
    language_code = models.CharField(max_length=10, default='vi')

    class Meta:
        unique_together = ('exercise', 'word_in_exercise', 'language_code')

# ---------------- User Progress ----------------
class UserExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    needs_review = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(auto_now=True)

class UserSublesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sublessons')
    sublesson = models.ForeignKey(Sublesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

# ---------------- Review ----------------
class ReviewSublesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_sublessons')
    review_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

# ---------------- Activity & AI ----------------
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPES)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)
