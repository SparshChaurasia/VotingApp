import csv

from django.contrib.auth.models import User

with open("./StaffList.csv", mode="r") as f:
    csv_file = csv.reader(f)

    for line in csv_file:
        user = User.objects.create_user(username=line[0], password=line[1])
        print(line[0], line[1], "...Done")
