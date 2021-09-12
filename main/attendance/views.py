from django.shortcuts import render, redirect
from .models import Employee, Record, User, EmpLeaveRequests, Notification, Tickets
from django.http import HttpResponse
import datetime
import csv
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import EmpLeaveAppForm, NotificationForm, TicketForm
from django.http import HttpResponseRedirect

global stat
stat=''

global selected
selected=None

@login_required
def sendticket(request):
    data=[]
    emp = Tickets.objects.filter(temp = request.user.employee)
    for datas in emp:
        data.append(datas)
    data.reverse()

    form = TicketForm(request.POST)
    if form.is_valid():
        event =form.save(commit=False)
        event.temp = request.user.employee
        event.save()
    context = {'form':form, 'data':data}
    return render(request, 'attendance/empticket.html', context) 

@login_required
def notice_view(request):
    data=[]
    noticerecords = Notification.objects.all()
    for nr in noticerecords:
        data.append(nr)
    data.reverse()
    context = {'data':data}
    return render(request, 'attendance/notice_view.html', context)

@login_required
def notification(request):
    # data=[]
    # emp = Tickets.objects.filter(temp = request.user.employee)
    # for datas in emp:
    #     data.append(datas)
    # data.reverse()

    form = NotificationForm(request.POST)
    
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
    
    context = {'form': form}
    return render (request, 'attendance/notification.html',context)

@login_required
def tickets(request):
    tics = []
    ticketrecords = Tickets.objects.all()
    app = Tickets.objects.filter(id = request.POST.get('answer')).all()
    for items in app:
        items.status = request.POST.get('status')
        items.save()
    
    for tc in ticketrecords:
        tics.append(tc)
    tics.reverse()
    data = {'tics':tics}
    return render(request, 'attendance/ticketview.html', data)

@login_required
def leaves(request):
    recs= []
    leaverecords = EmpLeaveRequests.objects.all()
    app = EmpLeaveRequests.objects.filter(id = request.POST.get('answer')).all()
    for items in app:
        items.status = request.POST.get('status')
        items.save()
        
    for lc in leaverecords:
        recs.append(lc)
    recs.reverse()
    data = {'recs':recs}
    return render(request, 'attendance/leaves.html', data)

@login_required
def EmpLeaveApp(request):
    data = []
    emp = EmpLeaveRequests.objects.filter(remp = request.user.employee)
    for datas in emp:
        data.append(datas)
    data.reverse()
    
    form = EmpLeaveAppForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.remp = request.user.employee
        event.save()
    
    context = {'form': form, 'data':data}
    return render (request, 'attendance/empApp.html',context)

@login_required
def userlogin(request):
    if request.user.is_employee:
        data = []
        udata = Record.objects.filter(name=request.user)
        sub = Record.objects.filter(name=request.user).count()
        # rejected = EmpLeaveRequests.objects.filter(remp= request.user.employee, status = 'reject').count()
        # accepted = EmpLeaveRequests.objects.filter(remp = request.user.employee, status = 'accept').count()
        present = Record.objects.filter(name=request.user).count()
        absent =  sub - present
        leave = EmpLeaveRequests.objects.filter(remp = request.user.employee).count()
        tickets = Tickets.objects.filter(temp = request.user.employee, status='clear').count()

        for datas in udata:
            data.append(datas)
        data.reverse()
        dataset ={'datau':data, 'absent': absent, 'present':present, 'leave':leave, 'tickets':tickets}
        return render(request, 'attendance/staffview.html', dataset)
    else:
        staffs= Employee.objects.count()
        recd = Record.objects.filter(date = datetime.date.today())
        tickets = Tickets.objects.filter( status='pend').count()
        records = recd.count()
        absents = staffs - records
        data = {'staffs': staffs, 'records': records, 'absents':absents, 'tickets':tickets}
        return render(request, 'attendance/index.html',data)
    return render(request, 'attendance/logout.html')

@login_required
def index1(request):
    recordf = []
    records = Record.objects.all()
    staffs = Employee.objects.count()

    for record in records:
        if record.date == datetime.date.today() :
            recordf.append(record)
    recordf.reverse()
    dataset = {'record': recordf, 'staffs': staffs}
    return render(request, 'attendance/attendance.html', dataset)

@login_required
def index(request):
    staffs= Employee.objects.count()
    recd = Record.objects.filter(date = datetime.date.today())
    tickets = Tickets.objects.filter( status ='pend').count()
    records1 = Record.objects.all()
    records = recd.count()
    absents = staffs - records
    recordf = []
    
    for record in records1:
        recordf.append(record)
    recordf.reverse()
    
    data = {'staffs': staffs, 'records': records, 'absents':absents, 'tickets':tickets, 'recordf':recordf}
    return render(request, 'attendance/index.html', data)

def process(request):
    card=request.GET.get('card_id', 'Cannot find the card')
    users=Employee.objects.all()
    for user in users:
        if user.card_id== int(card):
            res = attend(user)
            return HttpResponse(res)
    #new_user=Employee(card_id=int(card))
    #new_user.save()
    
    return HttpResponse("Not registered")

def attend(user):
    if user.name==None:
        curr= 'The profile is not registered'
        return curr
    records = Record.objects.all()
    for record in records:
        if record.card_id == int(user.card_id):
            if str(record.date) == str(datetime.datetime.now())[:10]:
                if record.time_out==None:
                    record.time_out=datetime.datetime.now()
                    record.save()
                    curr='logout'
                    return curr
                else:
                    curr='Walkout now'
                    return curr
    status = 'present'
    '''user_id =user.user_id,'''
    new_record=Record( ids=user.id, card_id=user.card_id, name=user.name, department=user.department, date=timezone.now(), time_in=datetime.datetime.now(), status='')
    new_record.save()
    curr='auth'
    return curr

@login_required
def click_add(request):
    users=Employee.objects.all()
    usid = request.POST.get('usid')
    user = request.POST.get('user')
    name=request.POST.get('name')
    phone=request.POST.get('phone')
    department=request.POST.get('department')
    email=request.POST.get('email')
    address=request.POST.get('address')
    card_id=request.POST.get('card_id')
    
    try:
        new_staff=Employee(user_id =usid, card_id=card_id, name=name, phone=phone, department=department, email=email, address=address)
        new_staff.save()
        return redirect('/users')
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def details1(request):
    users=Employee.objects.all()
    us=[]
    for user in users:
        us.append(user)
    us.reverse()
    userset={'users': us}
    return render(request, 'attendance/userdetails.html', userset)

@login_required
def details(request):
    return render(request, 'attendance/details.html')

@login_required
def manage1(request):
    users=Employee.objects.all()
    us=[]
    for user in users:
        us.append(user)
    us.reverse()
    global stat
    userset={'users': us}
    stat=''
    return render(request, 'attendance/allusers.html', userset)

@login_required
def manage(request):
    global stat
    status={'cardstatus': stat}
    return render(request, 'attendance/manage.html', status)


def card(request):
    users=Employee.objects.all()
    global stat
    global selected
    if request.method == 'POST':
        if request.POST.get("sel"):
            id_s=request.POST.get('idsearch', 'Cannot find the id')
            for user in users:
                if user.id==int(id_s):
                    stat='Card is Selected'
                    selected=user
                    break
                else:
                    stat='Card not found'
            return redirect('/manage')
        else:
            id_s=request.POST.get('idsearch')
            if Employee.objects.filter(id=int(id_s)).exists():
                Employee.objects.filter(id=int(id_s)).update(
                    name=None, phone=None, department=None, email=None, address=None)
                stat = 'Deleted Successfully'
            else:
                stat = 'Card not found'
            return redirect('/manage')


@login_required
def edit(request):
    i = 0
    users=Employee.objects.all()
    global selected
    global stat
    if selected == None:
        stat = 'No Card was Selected'
        return redirect('/manage')
    else:
        try:
            name=request.POST.get('name')
            phone=request.POST.get('phone')
            department=request.POST.get('department')
            email=request.POST.get('email')
            address=request.POST.get('address')
            new = [name, phone, department, email, address]
            for user in users:
                if user.card_id == selected.card_id:
                    old = [user.name, user.department, user.phone, user.email, user.address]
                    for item in new:
                        if item == '' or item is None:
                            new[i] = old[i]
                        i = i + 1
                    user.name = new[0]
                    user.phone = new[1]
                    user.department = new[2]
                    user.email = new[3]
                    user.address = new[4]
                    user.save()
                    stat = 'Profile Updated'
            selected = None
            return redirect('/manage')
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def search(request):
    sel_user = ''
    users = Employee.objects.all()
    records = Record.objects.all()
    path = request.get_full_path()
    id = request.POST.get('search')
    if (id):
        recordf = []
        for user in users:
            if str(user.id) == str(id):
                sel_user = user
        for record in records:
            if str(record.date)[5:7] == str(datetime.datetime.now())[5:7] and str(record.ids) == str(id):
                recordf.append(record)
        recordf.reverse()
        dataset = {'use': sel_user, 'recoqrd': recordf}
        return render(request, 'attendance/search.html', dataset)
    else:
        return redirect(request.META['HTTP_REFERER'])


@login_required
def add_staff(request):
    return render(request,'attendance/add_staff.html')
    
@login_required
def exportcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "Record.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ids', 'card_id', 'name', 'department', 'date', 'time_in', 'time_out'])
    
    users = Record.objects.all().values_list('ids', 'card_id', 'name', 'department', 'date', 'time_in', 'time_out')
    
    for user in users:
        writer.writerow(user)
    
    return response


        
