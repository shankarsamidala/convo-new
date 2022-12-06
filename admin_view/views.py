from django.shortcuts import render
from login import models
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import GDFileter,DayFileter
import itertools
# Create your views here.

day_of = timezone.localtime(timezone.now()).day

def StudentCount(request):
    student_count = models.Student.objects.all().count()
    faculty_count = models.Faculty.objects.all().count()
    team_count = models.Team.objects.all().count()
    college_count = models.College.objects.all().count()
    attendence = models.Attendance.objects.all().count()
    colg = models.College.objects.all()


    # Total Teams and students in Each Colleges
    college_all = models.College.objects.all()
    college_name_list = []
    team_count_list = []
    student_count_list_in_college = []

    for college in college_all:
        teams = models.Team.objects.filter(college_id=college.college_id).count()
        students = models.Student.objects.filter(college_id=college.college_id).count()
        college_name_list.append(college.college_id)
        team_count_list.append(teams)
        student_count_list_in_college.append(students)


    college_studnet_count = {
        college_name_list[i]:student_count_list_in_college[i] for i in range(len(college_name_list))
    }


    college_team_count = {
        college_name_list[i]:team_count_list[i] for i in range(len(college_name_list))
    }



    # Total GD Report , Past Day in Each Colleges

    attendence_latest_list = []
    college_name_list2 = []

    for college in college_all:
        attendence_latest_p = models.Attendance.objects.filter(college_id=college.college_id,date__day=day_of,presence=1).count()
        attendence_latest_a = models.Attendance.objects.filter(college_id=college.college_id,date__day=day_of,presence=0).count()

        attendence_latest_list.append([attendence_latest_p,attendence_latest_a])
        college_name_list2.append(college.college_id)


    attendence_all = models.Attendance.objects.all().count

    college_att_lt_count = {
        college_name_list2[i]:attendence_latest_list[i] for i in range(len(college_name_list2))
    }


    print(attendence_latest_list)

    # Total GD Report , Past Day in Each Colleges
    page = request.GET.get('page', 1)
    student_list = models.Attendance.objects.all().order_by('-date')

    myfilter = GDFileter(request.GET,queryset=student_list)


    student_list = myfilter.qs


    paginator = Paginator(student_list,10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)






    # All Days Count of Absent and Present

    all_day_data = models.Attendance.objects.all().order_by('-date')


    myfilter2 = DayFileter(request.GET,queryset=all_day_data)


    all_day_data = myfilter2.qs

    # print(all_day_data)
    # print(myfilter2.qs[20].date)


    attendence_all_list = []
    college_name_list3 = []


    for i in all_day_data:
        # print(i.date)
        present_count = models.Attendance.objects.filter(date=i.date,presence=1).count()
        absent_count = models.Attendance.objects.filter(date=i.date,presence=0).count()
        # college_name = models.Attendance.objects.filter(college_id=i.college,date=i.date)
        attendence_all_list.append([present_count,absent_count,i.college_id,i.date])
        college_name_list3.append(i.date)

    new_num = list(num for num,_ in itertools.groupby(attendence_all_list))



    context = {
        'students':student_count,
        'faculty':faculty_count,
        'teams':team_count,
        'colleges':college_count,
        'attendance':attendence,
        'colle_std':colg,
        'student_count_list_in_college':college_studnet_count,
        'college_name_list':college_name_list,
        'college_team_count':college_team_count,
        'attendence_all':attendence_all,
        'clg_att_day':college_att_lt_count,
        'date': timezone.localtime(timezone.now()).date,
        'all_students':users,
        'all_day_data':new_num,
        'filter':myfilter,
        'filter2':myfilter2

    }

 

    # for i in college_count:
    #     print(i.college_id)

    # return HttpResponse('Students ->{} Faculties -> {} Teams ->{} Colleges -> {}'.format(student_count,faculty_count,team_count,college_count))
    return render(request, 'admin23/hod_template/home_content.html',context)