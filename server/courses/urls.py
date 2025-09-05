from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# Topic / Lesson
router.register(r'topics', TopicViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'sublessons', SublessonViewSet)

# Exercises
router.register(r'exercises', ExerciseViewSet)
router.register(r'exercise-hints', ExerciseHintViewSet)

# User Progress
router.register(r'user-exercises', UserExerciseViewSet)
router.register(r'user-sublessons', UserSublessonViewSet)
router.register(r'user-lessons', UserLessonViewSet)

# Review
router.register(r'review-sublessons', ReviewSublessonViewSet)

# Activity & AI
router.register(r'user-activity', UserActivityLogViewSet)
router.register(r'ai-recommendations', AIRecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
