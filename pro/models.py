from django.db import models

# Create your models here.
class Data(models.Model):
    第一大题 = models.IntegerField()
    第二大题 = models.IntegerField()
    第三大题 = models.IntegerField()
    第四大题 = models.IntegerField()
    第五大题 = models.IntegerField()
    总分 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'data'

class History(models.Model):

    path = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    day = models.CharField(max_length=100)

    class Meta:
        db_table = 'history'
