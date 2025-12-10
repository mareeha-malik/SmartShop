from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Product, CartItem


def home_view(request):
    context = {
        "welcome_message": "Welcome to ShopSmart, your calm shopping space.",
        "current_year": datetime.now().year,
    }
    return render(request, "home.html", context)


def product_list_view(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
        "current_year": datetime.now().year,
    }
    return render(request, "products.html", context)


@login_required
def cart_view(request):
    product_id = request.GET.get("add")
    if product_id:
        product = Product.objects.filter(id=product_id).first()
        if product and product.stock > 0:
            item, created = CartItem.objects.get_or_create(
                user=request.user, product=product, defaults={"quantity": 1}
            )
            if not created:
                item.quantity += 1
                item.save()
        return redirect("dashboard:cart")

    cart_items = CartItem.objects.filter(user=request.user)

    total_price = 0
    for item in cart_items:
        total_price += item.line_total()

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "current_year": datetime.now().year,
    }
    return render(request, "cart.html", context)


@login_required
def profile_view(request):
    context = {
        "current_year": datetime.now().year,
    }
    return render(request, "profile.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")

    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:home")
        else:
            message = "Invalid username or password."

    context = {
        "message": message,
        "current_year": datetime.now().year,
    }
    return render(request, "login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("dashboard:home")

@login_required
def cart_view(request):
    product_id = request.GET.get("add")
    if product_id:
        product = Product.objects.filter(id=product_id).first()
        if product and product.stock > 0:
            item, created = CartItem.objects.get_or_create(
                user=request.user, product=product, defaults={"quantity": 1}
            )
            if not created:
                item.quantity += 1
                item.save()
        return redirect("dashboard:cart")

    # fake checkout action – for now just redirect with message
    if request.method == "POST" and request.POST.get("action") == "checkout":
        # In a real app you would create an Order here.
        return render(
            request,
            "checkout_success.html",
            {
                "current_year": datetime.now().year,
            },
        )

    cart_items = CartItem.objects.filter(user=request.user)

    total_price = 0
    for item in cart_items:
        total_price += item.line_total()

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "current_year": datetime.now().year,
    }
    return render(request, "cart.html", context)