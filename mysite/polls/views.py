from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    #가장 최근 질문 5개 보여줌
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #요청에 맞는 id를 가진 질문이 없을때 
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # 투표 폼을 다시 보여줌
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # 항상 POST데이터를 성공적으로 다루었을때는
        # HttpResponseRedirect를 반환하여 리다이렉션 처리함
        # 이렇게 하면 사용자가 뒤로가기 버튼을 눌러 데이터 두번 전송하는 걸 막음
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))