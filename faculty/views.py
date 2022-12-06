import csv
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from login.models import Team,Admin,Class,Student,Faculty,Calender,Course,Attendance,Timetable,Teache,College
from django.contrib import messages

# Create your views here.
fac=""
dep=""
cla=""
cou=""
colg=""

def initial(fact,dept,college):
    global fac,dep,colg
    fac=fact
    dep=dept
    colg=college
    return

def tial(clat,cout):
    global cla,cou
    cla=clat
    cou=cout
    return

def faclogin(request):
    if request.method=="POST":
        u,p=request.POST.get('email'),request.POST.get('password')
        faco=Faculty.objects.filter(fac_id=u)
        if faco.exists():
            if faco.get().f_password==p:
                d=faco.get().team_id.team_id
                c=faco.get().college_id.college_id
                initial(u,d,c)
                return updatedindex(request)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('index')
        else:
            messages.error(request, 'No such User exists')
            return redirect('index')
    else:
        messages.error(request, 'Enter Credentials')
        return redirect('index')

def updatedprofile(request):
    if request.method=="POST":
        try:
            fact=Faculty.objects.filter(fac_id=fac)
            fn=request.POST.get('fn')
            ln=request.POST.get('ln')
            pa=request.POST.get('pass')
            if fn != "":
                Faculty.objects.filter(fac_id=fac).update(f_name=fn)
            if ln !="" :
                Faculty.objects.filter(fac_id=fac).update(l_name=ln)
            if pa !="" :
                Faculty.objects.filter(fac_id=fac).update(f_password=pa)
            di=fact.get().team_id.team_id
        except:
            messages.error(request, 'Oops something went wrong!')
            return redirect('updatedadd')
    faco=Faculty.objects.filter(fac_id=fac)
    dept=Team.objects.filter(team_id=dep)
    teach=Teache.objects.filter(fac_id=fac)
    clas=[]
    for i in teach:
        clas.append([i.class_id.class_id,i.course_id.course_id])
    return render(request,'updatedprofile.html',{'clas':clas,'fac':faco.get(),'dept':dept.get()})

def editatt(request):
    dept=Team.objects.filter(team_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    teach=Teache.objects.filter(fac_id=fac)
    clao=Class.objects.filter(class_id=cla)
    couo=Course.objects.filter(course_id=cou)
    stud=Student.objects.all().filter(class_id=cla)
    atte=Attendance.objects.all().filter(course_id=cou,fac_id=fac).order_by('-date')
    if request.method=="POST":
        dict=request.POST
        for stud1 in stud:
            if stud1.stud_id in dict.keys():
                if dict.get('bate'):
                    try:
                        a=Attendance.objects.filter(stud_id=stud1,fac_id=faco.get(),course_id=couo.get(),date=dict.get('bate')).get()
                        if a.presence:
                            p=0
                        else:
                            p=1
                        Attendance.objects.filter(stud_id=stud1,fac_id=faco.get(),course_id=couo.get(),date=dict.get('bate')).update(presence=p)
                        messages.success(request, 'Attendance Edited.')
                    except:
                        # print(dict.get('bate').exists())
                        messages.error(request, 'Value does not Exist')
                        return redirect('updatedadd')
    return redirect('updatedadd')

def updatedindex(request):
    dept=Team.objects.filter(team_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    teach=Teache.objects.filter(fac_id=fac)
    clas=[]
    for i in teach:
        # print(i.class_id,'acalss')
        clas.append([i.class_id.class_id,i.course_id.course_id])

    # print(clas,'Class Data1')

    team = 0

    for i in dept:
        # print(i.team_id,'team')
        team = i.team_id
    # print(team,'Team data')    

    return render(request,'updatedindex.html',{'clas':clas,'teach':teach,'team':team})

def updatedadd(request):
    dept=Team.objects.filter(team_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    teach=Teache.objects.filter(fac_id=fac)
    college = College.objects.filter(college_id=colg)
    clas=[]
    for i in teach:
        clas.append([i.class_id.class_id,i.course_id.course_id])

    # print(clas,'Class Data2')

    team = 0
    for i in dept:
        # print(i.team_id,'team')
        team = i.team_id
    print(colg,'Team data')     
    clao=Class.objects.filter(class_id=cla)
    couo=Course.objects.filter(course_id=cou)
    stud=Student.objects.all().filter(class_id=cla,team_id=dep)
    atte=Attendance.objects.all().filter(course_id=cou,fac_id=fac).order_by('-date')
    if request.method=="POST":
        n=request.POST.get('classg')
        if n is not None:
            n,p=n[:n.find('$')],n[n.find('$')+1:]
            tial(n,p)
        dict=request.POST
        # print(dict.keys(),'Dict keys')
        for stud1 in stud:
            # print(stud1.stud_id,'student id')

            if stud1.stud_id in dict.keys():
                p=0
            else:
                p=1
            if dict.get('bate'):
                try:    
                    a=Attendance(stud_id=stud1,fac_id=faco.get(),course_id=couo.get(),date=dict.get('bate'),periods=1,team_id=dept.get(),college_id=college.get(),presence=p)
                    # print(dict.get('bate'),'date is ')
                    a.save()
                    messages.success(request, 'Attendance Added.')
                except:
                    messages.error(request, 'Value already Exists')
                    return redirect('updatedadd')
    clao=Class.objects.filter(class_id=cla)
    couo=Course.objects.filter(course_id=cou)
    stud=Student.objects.all().filter(class_id=cla,team_id=dep)
    # stud=Student.objects.all().filter(,) 

    dept=Team.objects.filter(team_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    teach=Teache.objects.filter(fac_id=fac)
    if stud.exists():
        dept=stud.first().team_id
    else:
        dept=dept.get()
    atte=Attendance.objects.all().filter(course_id=cou,fac_id=fac).order_by('-date')
    return render(request,'updatedadd.html',{'stud' : stud,'fac':faco.get(),'clat':clao.get(),'cout':couo.get(),'dept':dept,'atte':atte,'clas':clas,'team':team})

def fac_report(request):
    if request.method=="POST":
        dict=request.POST
        for i in dict.keys():
            if i!='csrfmiddlewaretoken':
                j=i
                break
        n,p=j[:j.find('$')],j[j.find('$')+1:]
        tial(n,p)
    a=[1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    stud=Student.objects.all().filter(class_id=cla)
    atte=Attendance.objects.all().filter(course_id=cou,fac_id=fac).order_by('stud_id','date')
    writer = csv.writer(response)

    writer.writerow(['Stud-Id','Class-Id','Dept','Course-Id','Date','Status'])
    for i in atte:
        if i.stud_id in stud:
            if i.presence:
                writer.writerow([i.stud_id.stud_id,cla,dep,cou,i.date,'Present'])
            else:
                writer.writerow([i.stud_id.stud_id,cla,dep,cou,i.date,'Absent'])
    return response
