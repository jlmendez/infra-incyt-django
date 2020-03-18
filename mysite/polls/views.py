import pandas as pd
from datetime import datetime, timedelta 

from math import pi
from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show #, ColumnDataSource
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from django.utils import timezone
from bokeh.models import DatetimeTickFormatter

from django.views.decorators.clickjacking import xframe_options_exempt

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import E1MS1, ISE1_INFRA, ISE2_INFRA
# Create your views here.



def ultimos_datos():
    from django.db import connection
    result_list = []
    row_list = []
    with connection.cursor() as cursor:
        cursor.execute("""select  fecha_sistema,  mpu_gxe, mpu_gye, mpu_gze, mpu_axe, mpu_aye, mpu_aze from e1ms1 where fecha_sistema > (current_timestamp - (1 * interval '1 minute')) """)
        for row in cursor.fetchall():
                row_list = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                result_list.append(row_list)
        return result_list

def homepage(request):

#Graph X & Y coordinates
    d= datetime.now() - timedelta(minutes=2)

#	data_list = ultimos_datos()
#	frame = pd.DataFrame(data_list)
#	frame.columns= ['fecha_sistema','gxe','gye','gze','axe','aye','aze']
    df = pd.DataFrame(list(ISE2_INFRA.objects.filter(fecha_recepcion__range=(d,datetime.now())).values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')))
#    df = pd.DataFrame(list(ISE2_INFRA.objects.all().values('fecha_recepcion','infrasonido_1','infrasonido_2','infrasonido_3','infrasonido_4')))
	
    source = ColumnDataSource(df)
    plot = figure(title = 'Line Graph', x_axis_label = 'X-Axis', y_axis_label = 'Y-Axis', x_axis_type='linear', plot_width = 1000, plot_height = 400)
    plot.line('fecha_sistema', 'gxe', source=source, line_width=3, line_alpha=1, line_color="blue")
    plot.line('fecha_sistema', 'gye', source=source, line_width=3, line_alpha=1, line_color="red")
    plot.line('fecha_sistema', 'gze', source=source, line_width=3, line_alpha=1, line_color="green")
#	plot.line('id', 'infrasonido_4', source=source, line_width=3, line_alpha=0.3, line_color="green")
	
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
        

