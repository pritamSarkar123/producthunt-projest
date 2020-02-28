from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

# Create your views here.
def home(request):
    products=Product.objects
    return render(request,'products/home.html',{'products':products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method=='POST':
        #user already put info
        #now check all fields are filled or not
        if request.POST.get('title') and request.POST.get('body') and request.POST.get('url') and request.FILES['icon'] and request.FILES['image'] :
            product=Product()
            product.title=request.POST.get('title')
            product.body=request.POST.get('body')
            if request.POST.get('url').startswith('http://') or request.POST.get('url').startswith('https://') :
                product.url=request.POST.get('url')
            else:
                product.url='http://'+request.POST.get('url')
            product.icon=request.FILES['icon']
            product.image=request.FILES['image']
            product.pub_date=timezone.datetime.now()
            #product.votes_total=1 #already set to one
            product.hunter=request.user
            product.save()
            return redirect('/products/'+str(product.pk))
        else:
            return render(request,'products/create.html',{'error':'All the fields are required!'})
    else:
        #not yeat given info
        return render(request,'products/create.html')


def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request,product_id):
    if request.method=="POST":
        #already clicks to the button
        product=get_object_or_404(Product,pk=product_id)
        product.votes_total+=1
        product.save()
        return redirect('/products/'+str(product_id))

