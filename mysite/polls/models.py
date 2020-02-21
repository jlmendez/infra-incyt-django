import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		return self.question_text

class Choice(models.Model):
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes= models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

class ISE2_INFRA(models.Model):
	ISE2_INFRA_id = models.IntegerField(default=0)
	infrasonido_1 = models.FloatField(default=0)
	infrasonido_2 = models.FloatField(default=0)
	infrasonido_3 = models.FloatField(default=0)
	infrasonido_4 = models.FloatField(default=0)
	infrasonido_5 = models.FloatField(default=0)
	posicion = models.CharField(max_length=200)
	fecha_recepcion = models.DateTimeField('fecha_captura')

	def __str__(self):
		return self.fecha_recepcion	
	
	def published_recently(self):
		return self.fecha_recepcion >= timezone.now() - datetime.timedelta(minutes=1)


class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                select * from v_ise2_infr_Zdat""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
        return result_list