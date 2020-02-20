#from django.shortcuts import render
from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
# Create your views here.

#def index(request):
#	return HttpResponse("Hello world. You're at the polls index.")

def homepage(request):
	#Graph X & Y coordinates
	x=[1,2,3,4,5,6]
	y=[1,2,3,4,5,6]

	plot = figure(title = 'Line Graph', x_axis_label = 'X-Axis', y_axis_label = 'Y-Axis', plot_width = 400, plot_height = 400)

	plot.line(x,y,line_width = 2)

	script, div = components(plot)

	return render_to_response('pages/index.html', {'script': script, 'div': div})

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)
#    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request,'polls/index.html',context)
#    return HttpResponse(template.render(context, request))
	
def detail(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'polls/detail.html', {'question': question})
#	return HttpResponse("You're looking at question_id %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'polls/detail.html',{
			'question':question, 
			'error_message':"You didn't select a choice.",
		})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))