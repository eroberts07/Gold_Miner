import random
from django.shortcuts import  redirect, render
from time import gmtime, strftime
date = strftime("%A, %B %d, %Y", gmtime())
time = strftime("%I:%M %p", gmtime())

def index(request):
    if 'moves' not in request.session:
        request.session['moves']=0
    else:
        request.session['moves']+= 1
    if 'user_gold' not in request.session:
        request.session['user_gold'] = 0
        request.session['activities']= []
        request.session['gold']={
            'farm':0,
            'cave':0,
            'house':0,
            'casino':0
        }
    context={
        'gold':request.session['gold']
    }
    return render(request,'index.html',context)

def process_money(request):
    request.session['gold']={
    'farm':random.randint(10,20),
    'cave':random.randint(5,10),
    'house':random.randint(2,5),
    'casino':random.randint(-50,50),
    }
    earned_money=0
    current_area='area'
    if request.method == 'POST':
        if request.POST['area'] == 'farm':
            earned_money = request.session['gold']['farm']
            current_area=request.POST['area']
        if request.POST['area'] == 'cave':
            earned_money = request.session['gold']['cave']
            current_area=request.POST['area']
        if request.POST['area'] == 'house':
            earned_money = request.session['gold']['house']
            current_area=request.POST['area']
        if request.POST['area'] == 'casino':
            earned_money = request.session['gold']['casino']
            current_area=request.POST['area']
    request.session['user_gold']+= earned_money
    gold= request.session['user_gold']
    if earned_money<0:
        activity=f'You lost {earned_money} at {current_area} ({date} {time})'
    else:
        activity=f'You found {earned_money} at {current_area} ({date} {time})'
    if request.session['moves']==9:
        if request.session['user_gold']>=100:
            activity=f'You Win! You finished the game with {gold}'
        else:
            activity=f'You Lost! Try to get more than 100 gold!'
    request.session['activities'].append(activity)
    return redirect('/')


def reset(request):
    request.session.flush()
    return redirect('/')
# Create your views here.
