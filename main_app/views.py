from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import LoginForm, ProductCreationForm, ProductUpdateForm, SignUpForm
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

def home(request):
    # product = Product.objects.all()
    product = "hi"
    user = request.user
    context = {
        'product':product,
    }
    return render(request, 'home.html', {'context': context})


class Products_Index(TemplateView):
    template_name = 'products.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user=user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Womens(TemplateView):
    template_name = 'product_womens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Mens(TemplateView):
    template_name = 'product_mens.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

class Products_Accessories(TemplateView):
    template_name = 'product_accessories.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('title')
        print(title)
        user = self.request.user
        products = Product.objects.filter(user= user.id)
        if title != None:
            context['products'] = products.filter(name__icontains=title)
        else:
            context['products'] = products
        return context

def product_create(request):
    product = Product.objects.all()
    user = request.user
    form_class = ProductCreationForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return HttpResponseRedirect ('/')
    else:
        form = form_class
    context = {
        'form':form
    }
    return render (request, 'product_create.html', context)    

def product_show(request, product_id):
    # products = get_object_or_404(Product, id=id) 
    product = Product.objects.get(id=product_id)
    return render(request, 'product_show.html', {'product':product})

class Product_Update(UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = '/products'
    # def get_success_url(self):
        # return reverse('product_show', kwargs={'id': self.object.id})
        # return HttpResponseRedirect('/products') 

class Product_Delete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = '/products'


#### AUTHENTICATION
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            e = form.cleaned_data['email']
            p = form.cleaned_data['password']
            user = authenticate(email=e, password=p)
            if user is not None: 
                login(request, user)
                return HttpResponseRedirect('/home')
            else: 
                print('The account has been disabled')
                return HttpResponseRedirect('/login')
        else:
            messages.sucess(request, 'The username and/or password is incorrect')
            return HttpResponseRedirect('login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Hi', user.username)
            return HttpResponseRedirect('/user/'+str(user.username))
        else:
            return render(request, 'signup.html', {'form':form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')