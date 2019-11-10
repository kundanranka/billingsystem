from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm
import cx_Oracle


# Create your views here.

def register(request):
	if request.method == 'POST':
		dsn_tns = cx_Oracle.makedsn('LAPTOP-AIT9NR87', '1521', service_name='XE') 
		conn = cx_Oracle.connect(user='SYSTEM', password='toor', dsn=dsn_tns) 
		c = conn.cursor()
		form = UserRegisterForm(request.POST)	
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			emailid=form.cleaned_data.get('email')
			password=form.cleaned_data.get('password1')
			c.prepare("insert into users values(:username,:emailid,:password1)")
			c.execute(None,{'username':username,'emailid':emailid,'password1':password})
			conn.commit()
			messages.success(request,f'Account created for {username}!')
			return redirect('Bill-home')
	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form' : form})
	conn.close()


def login(request):
	if request.method=='POST':
		dsn_tns = cx_Oracle.makedsn('LAPTOP-AIT9NR87', '1521', service_name='XE') 
		conn = cx_Oracle.connect(user='SYSTEM', password='toor', dsn=dsn_tns) 
		cx = conn.cursor()
		username=request.POST.get('username')
		password=request.POST.get('password')
		cx.prepare("select password from users where username = :usr")
		cx.execute(None,{'usr':username})
		flag=0
		for i in cx:
			if password==i[0]:
				flag=1
		if flag==1:
			messages.success(request,f'Login Success {username}!')
			return redirect('Bill-home')
		else:
			messages.error(request,f'Login denied!')
			return redirect('Bill-home')	
		conn.close()	
	return render(request,'users/login.html')