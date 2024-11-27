from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Choice, Question
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

class IndexView(View):
    def get(self, request):
        question = get_object_or_404(Question)
        dict_obj = model_to_dict(question)
        response = json.dumps(dict_obj, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type='application/json')

class DetailView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question.objects.prefetch_related('choice_set'), pk=pk)
        choices = list(question.choice_set.all().values('id', 'choice_text'))
        question_obj = model_to_dict(question)
        question_obj['polls_choice'] = choices
        response = json.dumps(question_obj, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type='application/json')
    #     return JsonResponse({
    # "id": 1,
    # "question_text": "클라우드를 배우고 싶으신가요?",
    # "pub_date": "2024-11-27",
    # "polls_choice": [
    #     {
    #         "id": 1,
    #         "choice_text": "네 배우고 싶어요"
    #     },
    #     {
    #         "id": 2,
    #         "choice_text": "아니요 별로"
    #     },
    #     {
    #         "id": 3,
    #         "choice_text": "생각중이예요"
    #     }
    # ]
    # })

class ResultsView(View):
    def get(self, request, pk):
        question = get_object_or_404(Question.objects.prefetch_related('choice_set'), pk=pk)
        choices = list(question.choice_set.all().values())
        question_obj = model_to_dict(question)
        question_obj['polls_choice'] = choices
        response = json.dumps(question_obj, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type='application/json')
#         return JsonResponse({
#     "id": 1,
#     "question_text": "클라우드를 배우고 싶으신가요?",
#     "pub_date": "2024-11-27",
#     "polls_choice": [
#         {
#             "id": 1,
#             "choice_text": "네 배우고 싶어요",
#             "votes": 10
#         },
#         {
#             "id": 2,
#             "choice_text": "아니요 별로",
#             "votes": 4
#         },
#         {
#             "id": 3,
#             "choice_text": "생각중이예요",
#             "votes": 2
#         }
#     ]
# })

@csrf_exempt
def vote(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        try:
            data = json.loads(request.body)
            selected_choice = question.choice_set.get(pk=data["choice_id"])
        except (KeyError, Choice.DoesNotExist, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid choice"}, status=400)
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            return JsonResponse({"message": "voted"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
