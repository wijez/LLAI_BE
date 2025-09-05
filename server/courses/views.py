from django.shortcuts import render

from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import *
from .serializers import *

# ---------------- Topic / Lesson ----------------
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class SublessonViewSet(viewsets.ModelViewSet):
    queryset = Sublesson.objects.all()
    serializer_class = SublessonSerializer

# ---------------- Exercises ----------------
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseHintViewSet(viewsets.ModelViewSet):
    queryset = ExerciseHint.objects.all()
    serializer_class = ExerciseHintSerializer

# ---------------- User Progress ----------------
class UserExerciseViewSet(viewsets.ModelViewSet):
    queryset = UserExercise.objects.all()
    serializer_class = UserExerciseSerializer

class UserSublessonViewSet(viewsets.ModelViewSet):
    queryset = UserSublesson.objects.all()
    serializer_class = UserSublessonSerializer

class UserLessonViewSet(viewsets.ModelViewSet):
    queryset = UserLesson.objects.all()
    serializer_class = UserLessonSerializer

# ---------------- Review ----------------
class ReviewSublessonViewSet(viewsets.ModelViewSet):
    queryset = ReviewSublesson.objects.all()
    serializer_class = ReviewSublessonSerializer

# ---------------- Activity & AI ----------------
class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer

class AIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AIRecommendation.objects.all()
    serializer_class = AIRecommendationSerializer

