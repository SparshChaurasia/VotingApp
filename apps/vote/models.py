from datetime import datetime

from django.db import models


class Classes(models.TextChoices):
    _9A = "9A"
    _9B = "9B"
    _10A = "10A"
    _10B = "10B"
    _11A = "11A"
    _11B = "11B"
    _11C = "11C"
    _12A = "12A"
    _12B = "12B"

class Event(models.Model):
    EventID = models.AutoField(primary_key=True)
    Date = models.DateField()
    EventName = models.TextField() 

    def __str__(self):
        return self.EventName
    

class Category(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    CategoryName = models.TextField()
 
    def __str__(self):
        return self.CategoryName   

class Option(models.Model):
    OptionID = models.AutoField(primary_key=True)
    OptionEvent = models.ForeignKey(Event, on_delete=models.CASCADE)
    OpitonCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    OptionName = models.TextField()
    Votes = models.IntegerField(default=0)

    def vote(self):
        self.Votes += 1

    def __str__(self):
        return self.OptionName

class Student(models.Model):
    StudentID = models.CharField(max_length=8)
    Name = models.TextField() 
    Class = models.CharField(max_length=3, choices=Classes.choices)
    Voted = models.TextField(default="{}")

    def voted(self, event_id):
        v = eval(self.Voted())
        v[event_id] = str(datetime.now())
        self.Voted = str(v)

    def has_voted(self, event_id):
        v = eval(self.Voted())
        return True if v.get(event_id) else False

    def __str__(self):
        return self.Name
