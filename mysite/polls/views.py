import pandas as pd
import datetime
from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show #, ColumnDataSource
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from django.utils import timezone

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question, ISE2_INFRA
# Create your views here.

#def index(request):
#	return HttpResponse("Hello world. You're at the polls index.")

def homepage(request):
	#Graph X & Y coordinates


	df = pd.DataFrame(list(ISE2_INFRA.objects.all().values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')[:10000]))
	#df = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__lte=timezone.now()-datetime.timedelta(seconds=500)).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4'[:5000])))
	source = ColumnDataSource(df)
	plot = figure(title = 'Line Graph', x_axis_label = 'X-Axis', y_axis_label = 'Y-Axis', plot_width = 1000, plot_height = 400)
	plot.line('fecha_recepcion', 'infrasonido_1', source=source, line_width=3, line_alpha=0.6)
	plot.line('fecha_recepcion', 'infrasonido_2', source=source, line_width=3, line_alpha=0.3)
	plot.line('fecha_recepcion', 'infrasonido_3', source=source, line_width=3, line_alpha=0.3)
	plot.line('fecha_recepcion', 'infrasonido_4', source=source, line_width=3, line_alpha=0.3)
	#plot.line(x,y,line_width = 2)
	script, div = components(plot)
    
	return render_to_response('polls/dash.html', {'script': script, 'div': div})

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