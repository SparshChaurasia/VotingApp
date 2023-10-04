from datetime import datetime

from django.db import models


class Classes(models.TextChoices):
    _AA = "AA"
    _BB = "BB"
    _6A = "6A"
    _6B = "6B"
    _7A = "7A"
    _7B = "7B"
    _8A = "8A"
    _8B = "8B"
    _9A = "9A"
    _9B = "9B"
    _10A = "10A"
    _10B = "10B"
    _11A = "11A"
    _11B = "11B"
    _12A = "12A"
    _12B = "12B"
    _12C = "12C"

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
        self.save()

    def __str__(self):
        return self.OptionName

class Student(models.Model):
    StudentID = models.CharField(max_length=8)
    Name = models.TextField() 
    Class = models.CharField(max_length=3, choices=Classes.choices)
    Voted = models.TextField(default="{}")

    def __str__(self):
        return self.Name

    def voted(self, event_id, options):
        v = eval(self.Voted)
        v[event_id] = [datetime.now().strftime("%m-%d-%Y_%H:%M:%S"), options]
        self.Voted = str(v)
        self.save()

    def has_voted(self, event_id):
        v = eval(self.Voted)
        if event_id in v.keys():
            return True 
        else: 
            return False

# class Voted(models.Model):
#     StudentVote = models.ForeignKey(Student, models.CASCADE)
#     EventVote = models.ForeignKey(Event, models.CASCADE)
#     DateTime = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.Name
