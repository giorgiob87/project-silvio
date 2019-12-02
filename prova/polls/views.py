from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone
from django.test import TestCase

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset ( self ):
        """
        Excludes any questions that aren't published yet.
        """
        return Question . objects . filter ( pub_date__lte = timezone . now ())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
       
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



class QuestionDetailViewTests ( TestCase ):
    def test_future_question ( self ):
 
        future_question = create_question ( question_text = 'Future question.' , days = 5 )
        url = reverse ( 'polls:detail' , args = ( future_question . id ,))
        response = self . client . get ( url )
        self . assertEqual ( response . status_code , 404 )

    def test_past_question ( self ):

        past_question = create_question ( question_text = 'Past Question.' , days =- 5 )
        url = reverse ( 'polls:detail' , args = ( past_question . id ,))
        response = self . client . get ( url )
        self . assertContains ( response , past_question . question_text )





