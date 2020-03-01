import pandas as pd
import datetime

from math import pi
from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show #, ColumnDataSource
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from django.utils import timezone
from bokeh.models import DatetimeTickFormatter

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question, ISE2_INFRA
# Create your views here.

#def index(request):
#	return HttpResponse("Hello world. You're at the polls index.")

def ultimos_datos():
		from django.db import connection

		result_list = []
		row_list = []
		with connection.cursor() as cursor:
			cursor.execute("""select * from V_ISE2_INFRA_L2M""")
			for row in cursor.fetchall():
				row_list = [row[0], row[1], row[2], row[3], row[4], row[5]]
				result_list.append(row_list)
		
		return result_list

def homepage(request):
	#Graph X & Y coordinates

	data_list = ultimos_datos()
	frame = pd.DataFrame(data_list)
	frame.columns= ['id','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4','fecha_recepcion']
	#df = pd.DataFrame(list(ISE2_INFRA.objects.all().values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')))
	
	source = ColumnDataSource(frame)
	plot = figure(title = 'Line Graph', x_axis_label = 'X-Axis', y_axis_label = 'Y-Axis', x_axis_type='datetime', plot_width = 1000, plot_height = 400)
	plot.line('fecha_recepcion', 'infrasonido_1', source=source, line_width=3, line_alpha=0.6, line_color="blue")
	plot.line('fecha_recepcion', 'infrasonido_2', source=source, line_width=3, line_alpha=0.3, line_color="red")
	plot.line('fecha_recepcion', 'infrasonido_3', source=source, line_width=3, line_alpha=0.3, line_color="pink")
	plot.line('fecha_recepcion', 'infrasonido_4', source=source, line_width=3, line_alpha=0.3, line_color="green")
	
	#plot.xaxis.formatter=DatetimeTickFormatter(
	#	hours=["%d %B %Y"],
	#	days=["%d %B %Y"],
	#	months=["%d %B %Y"],
	#	years=["%d %B %Y"],
	#)
	plot.xaxis.major_label_orientation = pi/4
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