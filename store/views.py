from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .models import Product
from .models import Cart
from .models import Wishlist
from .models import Order



def home(request):

    products=Product.objects.all()

    query=request.GET.get('q')

    if query:

        products=products.filter(
            name__icontains=query
        )

    return render(
        request,
        'home.html',
        {
            'products':products
        }
    )



def product_detail(request,id):

    product=Product.objects.get(
        id=id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product':product
        }
    )


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    item = Cart.objects.filter(product=product).first()

    if item:
        item.quantity += 1
        item.save()
    else:
        Cart.objects.create(
            product=product,
            quantity=1
        )

    cart_count = Cart.objects.count()

    return JsonResponse({
        "success": True,
        "cart_count": cart_count
    })



def cart(request):

    items=Cart.objects.all()

    total=0

    for item in items:

        total+=(
            item.product.price*
            item.quantity
        )

    return render(
        request,
        'cart.html',
        {
            'items':items,
            'total':total
        }
    )



def remove_from_cart(request,id):

    item=Cart.objects.get(
        id=id
    )

    item.delete()

    return redirect(request.META.get("HTTP_REFERER", "home"))



def increase_quantity(request,id):

    item=Cart.objects.get(
        id=id
    )

    item.quantity+=1

    item.save()

    return redirect(request.META.get("HTTP_REFERER", "home"))



def decrease_quantity(request,id):

    item=Cart.objects.get(
        id=id
    )

    if item.quantity>1:

        item.quantity-=1

        item.save()

    return redirect(request.META.get("HTTP_REFERER", "home"))



def add_to_wishlist(request,id):

    product=Product.objects.get(
        id=id
    )

    exists=Wishlist.objects.filter(
        product=product
    ).first()

    if not exists:

        Wishlist.objects.create(
            product=product
        )

    return redirect(request.META.get("HTTP_REFERER", "shop"))



def wishlist(request):

    items=Wishlist.objects.all()

    return render(
        request,
        'wishlist.html',
        {
            'items':items
        }
    )



def signup(request):

    if request.method=="POST":

        username=request.POST['username']

        email=request.POST['email']

        password=request.POST['password']

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'signup.html',
                {
                    'error':
                    'Username exists'
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect(
            'login'
        )

    return render(
        request,
        'signup.html'
    )




def login_user(request):

    if request.method=="POST":

        username=request.POST[
            'username'
        ]

        password=request.POST[
            'password'
        ]

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

    return render(
        request,
        'login.html'
    )



def logout_user(request):

    logout(request)

    return redirect(
        'home'
    )
def checkout(request):

    items = Cart.objects.all()

    total = 0

    product_names = []

    for item in items:

        total += item.product.price * item.quantity

        product_names.append(
            f"{item.product.name} x {item.quantity}"
        )

    products_string = ", ".join(product_names)

    if request.method == "POST":

        name = request.POST.get("name")

        phone = request.POST.get("phone")

        address = request.POST.get("address")

        request.session["name"] = name
        request.session["phone"] = phone
        request.session["address"] = address
        request.session["products"] = products_string
        request.session["total"] = total

        return redirect("payment")

    return render(
        request,
        "checkout.html",
        {
            "total": total
        }
    )
def payment(request):

    if request.method == "POST":

        # Agar Buy Now form se aaye
        if "name" in request.POST:

            request.session["name"] = request.POST.get("name")
            request.session["phone"] = request.POST.get("phone")
            request.session["address"] = request.POST.get("address")

            product = request.POST.get("product")
            price = int(request.POST.get("price"))
            quantity = int(request.POST.get("quantity"))

            request.session["products"] = f"{product} x {quantity}"
            request.session["total"] = price * quantity

            return render(
                request,
                "payment.html",
                {
                    "total": request.session.get("total")
                }
            )

       
        method = request.POST.get("method")

        if method == "cod":

            Order.objects.create(
                name=request.session.get("name"),
                phone=request.session.get("phone"),
                address=request.session.get("address"),
                product=request.session.get("products"),
                total_price=request.session.get("total"),
            )

            Cart.objects.all().delete()
            request.session.clear()

            return redirect("success")

        elif method == "upi":

            return redirect("upi_payment")

        elif method == "card":

            return render(
                request,
                "payment.html",
                {
                    "message": "Card Payment Coming Soon",
                    "total": request.session.get("total")
                }
            )

    return render(
        request,
        "payment.html",
        {
            "total": request.session.get("total")
        }
    )
def success(request):

    return render(
        request,
        "success.html"
    )


def my_orders(request):

    orders = Order.objects.all()

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )

from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )
def shop(request):

    products = Product.objects.all()

    cart_count = Cart.objects.count()  

    return render(
        request,
        "shop.html",
        {
            "products": products,
            "cart_count": cart_count    
        }
    )
def payment_done(request):

    Order.objects.create(

        name=request.session["name"],
        phone=request.session["phone"],
        address=request.session["address"],
        product=request.session["products"],
        total_price=request.session["total"]

    )

    Cart.objects.all().delete()

    request.session.flush()

    return redirect("success")
def upi_payment(request):

    if request.method == "POST":

        Order.objects.create(

            name=request.session.get("name"),
            phone=request.session.get("phone"),
            address=request.session.get("address"),
            product=request.session.get("products"),
            total_price=request.session.get("total")

        )

        Cart.objects.all().delete()

        request.session.clear()

        return redirect("success")

    return render(
        request,
        "upi_payment.html",
        {
            "total":request.session.get("total")
        }
    )
def buy_now(request, id):

    product = Product.objects.get(id=id)

    return render(
        request,
        "order.html",
        {
            "product": product
        }
    )