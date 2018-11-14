from django.shortcuts import render , redirect
from .models import Product,Items,Category,Users
from datetime import datetime
from django.utils.text import slugify
from django.db import transaction
from .forms import UserForm
from .tools.randimg import ValidCodeImg
from django.http import HttpResponse
from django.views.generic import View
import json
from django.core import serializers



def getExtend(str):
    return str[str.rfind('.'):]


def category_list_view(request):
    context = {}
    context['categorys'] = Category.objects.all()
    return render(request, "category/list.html", context)


def category_addedit_view(request,id=None):
    context = {}
    if request.method == "POST":
        name = request.POST['name'].strip()
        slug = slugify(name)
        obj = Category()
        if id:
            obj = Category.objects.get(id=id)
        obj.name=name
        obj.slug=slug
        obj.save()
        return redirect('category_list')
    if id:
        obj = Category.objects.get(id=id)
        context['category'] = obj
    return render(request, "category/addedit.html", context)







def is_login(request):
    try:
        user = Users.objects.get(id=request.session['userobj'])
    except (KeyError, Users.DoesNotExist):
        user = None
    return user


def shop_list_view(request,category_id=None):
    user=is_login(request)
    if user is None:
        return redirect("login")

    print( request.session['userobj'] )
    context = {'user':user}
    if category_id is None :
        products = Product.objects.all()
    else :
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    context['products'] = products
    return render(request, "product/list.html", context)


@transaction.atomic
def save_product(request,id=None):
    name = request.POST['name'].strip()
    content = request.POST['content'].strip()
    available = int(request.POST['available'])
    category_id = int(request.POST['category_id'])

    item_name = request.POST.getlist('item_name')
    item_price = request.POST.getlist('item_price')
    item_stock = request.POST.getlist('item_stock')

    imageurl = ''
    image = request.FILES.get("image", None)
    if image:
        ext = getExtend(image.name)
        filename = datetime.now().strftime('%Y%m%d%H%M%S')
        imageurl = f'media/upload/{filename}{ext}'
        with open(imageurl, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

    product = Product()
    if id:
        product = Product.objects.get(id=id)
        for item in product.items.all() :
            item.delete()

    product.category = Category.objects.get(id=category_id)
    product.name = name
    product.slug = slugify(name)
    product.content = content
    product.available = available
    if id and imageurl != '':
        product.image = imageurl
    product.save()

    for i in range(len(item_name)):
        item = Items()
        item.name = item_name[i]
        item.price = item_price[i]
        item.stock = item_stock[i]
        item.product = product
        item.save()


def shop_edit_view(request,id=None):
    if request.method == "POST":
        try:
            save_product(request,id)
        except ValueError:
            print("error")
        return redirect('shop_list')
    context = {}
    context['categorys'] = Category.objects.all()
    context['product'] = Product.objects.get(id=id)
    return render(request, "product/edit.html",context)


def shop_add_view(request):
    if request.method == "POST":
        save_product(request)
        return redirect('shop_list')
    context = {}
    context['categorys'] = Category.objects.all()
    return render(request, "product/add.html",context)


def shop_del_view(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('shop_list')





def user_list_view(request):
    context = {}
    users = Users.objects.all()
    context['users'] = users
    return render(request, "user/list.html", context)


def user_add_view(request,id=None):
    message=''
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data['name']
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            obj=Users()
            if id:
                obj = Users.objects.get(id=id)
            obj.name=name
            obj.username=username
            obj.password=password
            obj.save()
            return redirect('user_list')
        else:
            message="Error"

    context = {}
    if id and request.method!="POST" :
        obj = Users.objects.get(id=id)
        initial={'id':id,'name':obj.name,'username':obj.username,'password':obj.password}
        userform = UserForm(initial=initial)
    else :
        userform = UserForm(request.POST,initial={'id':id})

    context['userform'] = userform
    context['message'] = message
    return render(request, "user/add.html", context)


def user_del_view(request,id):
    user = Users.objects.get(id=id)
    user.delete()
    return redirect('user_list')


def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        checkcode = request.POST['checkcode'].strip()

        if checkcode.upper() != request.session['checkcode'] :
            context['message'] = '驗證碼錯誤'
            return render(request, "system/login.html", context)

        if len(username)<5 or len(password)<5 :
            context['message'] = '帳號密碼錯誤'
            return render(request, "system/login.html",context)
        else :
            user=Users.objects.get(username=username)
            if user is None:
                context['message'] = '查無此帳號'
                return render(request, "system/login.html", context)

            if user.password != password:
                context['message'] = '密碼錯誤'
                return render(request, "system/login.html", context)
            else :
                request.session['userobj'] = user.id
                return redirect('shop_list')

    return render(request, "system/login.html")


def logout_view(request):
    request.session.clear()
    return render(request, "system/login.html")



class GetValidImg(View):
    def get(self,request):
        obj = ValidCodeImg()
        img_data,valid_code = obj.getValidCodeImg()
        request.session['checkcode'] = valid_code.upper()
        return HttpResponse(img_data)



