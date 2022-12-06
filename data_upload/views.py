from django.shortcuts import render
from django.http import HttpResponse
from .forms import CsvModelForm
from .models import Csv
import csv
from login.models import Team, Faculty, Student, Class, Teache, Course, College
# Create your views here.



def upload_file_view(request):
    form  = CsvModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i==0:
                    pass
                else:
                    # print("Team object({})".format(row[8]))

                    # team = row[7]
                    # id = int(row[0])+1
                    # Team.objects.create(
                    #     team_name = row[1],
                    #     team_id = int(row[0])+1,
                    #     college_id = College.objects.get(college_id='ADC-KKD')
                    # )

                    # Faculty.objects.create(
                    #     fac_id = row[4],
                    #     f_password = row[8],
                    #     f_name = row[2],
                    #     l_name = row[3],
                    #     team_id = Team.objects.get(team_id=row[7]),    #"Team object({})".format(row[7])
                    #     college_id = College.objects.get(college_id='ADC-KKD')
                    # )


                    # Student.objects.create(
                    #     stud_id = row[1],
                    #     s_password = row[6],
                    #     in_out ='Yes',
                    #     f_name = row[2],
                    #     l_name = row[5],
                    #     team_id = Team.objects.get(team_id=row[7]) ,   #"Team object({})".format(row[7])
                    #     class_id = Class.objects.get(class_id=row[8]),
                    #     college_id = College.objects.get(college_id='ADC-KKD')
                    # )

                    # print(row[5],'row - 8 ->',row[3])

                    Teache.objects.create(
                        fac_id = Faculty.objects.get(fac_id = row[5],),
                        course_id = Course.objects.get(course_id=1),
                        class_id = Class.objects.get(class_id=row[3])
                    )




            obj.activated=True
            obj.save()        

    return render(request, 'upload.html', {'form':form})