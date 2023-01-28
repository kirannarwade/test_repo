from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from app.models import Product, Cart, OrderPlaced, Customer
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.forms import CustomerProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# def home(request):  
#    return render(request, 'home.html')

class ProductView(View):
    def get(self, request):
        bottomwears = Product.objects.filter(category='BW')
        topwears = Product.objects.filter(category='TW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        context = {'bottomwears':bottomwears, 'topwears':topwears,'mobiles':mobiles, 'laptops':laptops }
        return render(request, 'home.html', context)

# def product_detail(request):
#     return render(request, 'productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            context = {'product':product}
            return render(request, 'productdetail.html', context)
        except:
            return HttpResponse("Not Found - 404")

class OrderDetailView(View):
    def get(self, request, pk):
        try:
            user = request.user
            op = OrderPlaced.objects.get(pk=pk, user=user)
            context = {'op':op}
            return render(request, 'orderdetail.html', context)
        except:
            return HttpResponse("Not Found")

# Filter Products

# def mobile(request):
#     return render(request, 'mobile.html')

def mobile_filter(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')

    elif data == 'Honor' or data == 'Samsung' or data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    return render(request, 'mobile.html', {'mobiles':mobiles})


def laptop_filter(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')

    elif data == 'HP' or data == 'Acer' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'laptop.html', {'laptops':laptops})

def topwear_filter(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')

    return render(request, 'topwear.html', {'topwears':topwears})

def bottomwear_filter(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')

    return render(request, 'bottomwear.html', {'bottomwears':bottomwears})

# def add_to_cart(request):
#     return render(request, 'addtocart.html')

@login_required(login_url='/login')
def buy_now(request):
    return render(request, 'buynow.html')

# def profile(request):
#     return render(request, 'profile.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        context = {'form':form}
        return render(request, "profile.html", context)


    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile updated!")

        return render(request, "profile.html", {'form':form})
   




def address(request):
    add = Customer.objects.filter(user=request.user)
    context = {'add':add}
    return render(request, 'address.html', context)

def add_to_cart(request):
    if request.user.is_anonymous:
        messages.warning(request, "Please Login to KShop Account")
        return redirect('/login')
    else:
        user = request.user
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        cart = Cart(user=user, product=product)
        cart.save()
        messages.success(request, "Item Cart Successfully!")
        return redirect('/cart')

def show_cart(request):       
    user = request.user
    carts = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    # cart_product = [ p for p in Cart.objects.all() if p.user == user]
    cart_product = [ p for p in Cart.objects.filter(user=user)]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, "addtocart.html", {'carts':carts, 'totalamount':totalamount, 'amount':amount})
    else:
        return render(request, "emptycart.html")

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user) 
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    # cart_product = [ p for p in Cart.objects.all() if p.user == user]
    cart_product = [ p for p in Cart.objects.filter(user=user) ]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'checkout.html', {'add':add, 'cart_items':cart_items, 'totalamount':totalamount})


def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)


    cart = Cart.objects.filter(user=user)
    for c in cart:
        order = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity)
        order.save()
        c.delete()
    messages.success(request, "Thank You For Placing Order")
    return redirect('/orders')

def orders(request):
    user = request.user
    op = OrderPlaced.objects.filter(user=user)
    return render(request, 'orders.html', {'op':op})


def delete_cart(request, pk):
    cart = Cart.objects.get(pk=pk)
    cart.delete()
    messages.success(request, "Item Deleted Successfully")
    return redirect('/cart')
 

# def orders(request):
#     return render(request, 'orders.html')



def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully!")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "login.html")

    return render(request, 'login.html')

def customerregistration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/registration')

        if User.objects.filter(username = username).first():
            messages.warning(request, "Username already exists")
            return redirect('/registration')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, 'Account Registered Successfully!')
        return redirect('/login')
        
    return render(request, 'customerregistration.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect('/login')

# def checkout(request):
#     return render(request, 'checkout.html')


def search(request):
    query = request.GET['query']
    allProductsTitle = Product.objects.filter(title__icontains=query)
    allProductsContent = Product.objects.filter(brand__icontains=query)
    allProducts = allProductsTitle.union(allProductsContent)
      
  
    if allProducts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allProducts' : allProducts, 'query' : query}
    return render(request, "search.html", params)

