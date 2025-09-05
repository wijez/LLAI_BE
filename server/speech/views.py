from io import BytesIO
import uuid
from django.shortcuts import render

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from gtts import gTTS
import whisper
import chromadb
import jiwer
import tempfile
import os

from courses.models import Exercise

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("pronunciation_docs")

# ---------------- Whisper ----------------
whisper_model = whisper.load_model("small")

# ---------------- Text-to-Speech ----------------
class TextToSpeechView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        # Lấy dữ liệu từ request
        text_to_speak = request.data.get("text")        # FE có thể gửi text trực tiếp
        lang = request.data.get("lang")                 # ngôn ngữ nếu gửi
        exercise_id = request.data.get("exercise_id")   # optional: phát từ DB
        word_hint = request.data.get("word")            # optional: từ trong exercise

        # Nếu gửi exercise_id, lấy text từ DB
        if exercise_id:
            try:
                exercise = Exercise.objects.get(id=exercise_id)
            except Exercise.DoesNotExist:
                return Response({"error": "Exercise not found"}, status=404)

            if word_hint:
                hint = exercise.hints.filter(word_in_exercise=word_hint).first()
                if hint:
                    text_to_speak = hint.hint_text
                    lang = hint.language_code
                else:
                    return Response({"error": "Hint not found"}, status=404)
            else:
                text_to_speak = exercise.answer_key
                lang = exercise.language_code if exercise.language_code else "en"

        # Nếu FE không gửi text + không gửi exercise_id
        if not text_to_speak:
            return Response({"error": "Text or exercise_id is required"}, status=400)

        # Tạo audio MP3 trong memory
        mp3_fp = BytesIO()
        tts = gTTS(text=text_to_speak, lang=lang or "en")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Trả về audio
        response = HttpResponse(mp3_fp.read(), content_type="audio/mpeg")
        response["Content-Disposition"] = 'inline; filename="tts.mp3"'
        return response


# ---------------- Transcribe + Semantic Feedback ----------------
class TranscribeAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        exercise_id = request.data.get("exercise_id")
        audio_file = request.FILES.get("file")

        if not audio_file:
            return Response({"error": "No audio uploaded"}, status=400)

        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=404)

        # 1. Lưu audio tạm
        temp_wav = tempfile.mktemp(suffix=".wav")
        with open(temp_wav, "wb") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # 2. Whisper transcribe
        result = whisper_model.transcribe(temp_wav, language="en")
        spoken_text = result["text"].strip()

        # 3. Compare per word
        answer_words = exercise.answer_key.strip().split()
        spoken_words = spoken_text.split()
        word_results = []
        for i, word in enumerate(answer_words):
            if i < len(spoken_words) and word.lower() == spoken_words[i].lower():
                word_results.append({"word": word, "correct": True})
            else:
                word_results.append({"word": word, "correct": False})

        # 4. Calculate WER
        wer = jiwer.wer(exercise.answer_key, spoken_text)
        accuracy = (1 - wer) * 100
        passed = accuracy >= 60

        # 5. Semantic search in ChromaDB for feedback
        # Nếu spoken_text gần giống câu khác trong DB → gợi ý cải thiện
        try:
            # Giả sử collection đã lưu embeddings trước
            query_result = collection.query(query_texts=[spoken_text], n_results=3)
            recommendations = [
                {"text": doc, "score": score}
                for doc, score in zip(query_result["documents"][0], query_result["distances"][0])
            ]
        except Exception:
            recommendations = []

        os.remove(temp_wav)

        return Response({
            "spoken_text": spoken_text,
            "answer_key": exercise.answer_key,
            "word_results": word_results,
            "accuracy": f"{accuracy:.2f}%",
            "passed": passed,
            "recommendations": recommendations
        })


def record_page(request):
    return render(request, "record.html")

def tts_test_page(request):
    return render(request, "tts_test.html")