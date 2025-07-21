import csv

from apps.vote.models import Student

with open("./static/data/StudentsList.csv", mode="r") as f:
    csv_file = csv.reader(f)

    for line in csv_file:
        student = Student.objects.create(StudentID=line[0], Class=line[1], Name=line[2])
        print(line[0], line[1], line[2],"...Done")