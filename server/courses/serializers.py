from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Topic, Lesson, Sublesson,
    Exercise, ExerciseHint,
    UserExercise, UserSublesson, UserLesson,
    ReviewSublesson, UserActivityLog, AIRecommendation
)

# ---------------- Topics / Lessons ----------------
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class SublessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sublesson
        fields = '__all__'

# ---------------- Exercises ----------------
class ExerciseHintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseHint
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    hints = ExerciseHintSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = '__all__'

    def create(self, validated_data):
        exercise = Exercise.objects.create(**validated_data)

        # Tách từ không trùng lặp từ answer_key
        words = set(exercise.answer_key.split())  # set loại bỏ từ trùng nhau

        hints = []
        for word in words:
            hints.append(ExerciseHint(
                exercise=exercise,
                word_in_exercise=word,
                hint_text=word,  # lúc này có thể dùng AI để tạo phiên âm, dịch
                hint_type='manual',
                language_code='vi'  # hoặc lấy từ frontend nếu muốn dịch sang ngôn ngữ khác
            ))
        ExerciseHint.objects.bulk_create(hints)
        return exercise

# ---------------- User Progress ----------------
class UserExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExercise
        fields = '__all__'

class UserSublessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSublesson
        fields = '__all__'

class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'

# ---------------- Review ----------------
class ReviewSublessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSublesson
        fields = '__all__'

# ---------------- Activity & AI ----------------
class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = '__all__'

class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = '__all__'
