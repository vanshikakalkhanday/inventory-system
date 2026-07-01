from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal, InvalidOperation
import re
 
# SHOW ALL PRODUCTS

def product_list(request):
    query = request.GET.get('search')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    selected_category = None
    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()

    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

   
 
# SHOW PRODUCT BY ID
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'inventory/product_detail.html', {'product': product})

# SHOW PRODUCTS BY CATEGORY
def product_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })


# add category
@staff_member_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(
                request,
                "Category name is required."
            )
            return redirect("add_category")

        if not re.match(r"^[A-Za-z ]+$", name):
            messages.error(
                request,
                "Category name should contain only letters and spaces."
            )
            return redirect("add_category")

        Category.objects.create(
            name=name
        )
        messages.success(
            request,
            "Category added successfully."
        )
        return redirect("add_category")   # keep same page

    return render(
        request,
        "inventory/add_category.html"
    )
 

# ADD NEW PRODUCT (CREATE)
@staff_member_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price_raw = request.POST.get("price")
        quantity_raw = request.POST.get("quantity")
        category_id = request.POST.get("category")

        # Name validation
        if not name:
            messages.error(request, "Product name is required.")
            return redirect("add_product")
        if not re.match(r"^[A-Za-z ]+$", name):
            messages.error(
                request,
                "Product name should contain only letters and spaces."
            )
            return redirect("add_product")

        # Category validation
        if not category_id:
            messages.error(request, "Please select a category.")
            return redirect("add_product")
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect("add_product")

        # Price validation
        try:
            price = Decimal(price_raw)
            if price <= 0:
                messages.error(
                    request,
                    "Price must be greater than 0."
                )
                return redirect("add_product")
        except (InvalidOperation, TypeError):
            messages.error(request, "Enter a valid price.")
            return redirect("add_product")

        # Quantity validation
        try:
            quantity = int(quantity_raw)
            if quantity <= 0:
                messages.error(
                    request,
                    "Quantity must be greater than 0."
                )
                return redirect("add_product")
        except (ValueError, TypeError):
            messages.error(request, "Enter a valid quantity.")
            return redirect("add_product")
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category
        )
        messages.success(
            request,
            "Product added successfully."
        )
        return redirect("product_list")

    categories = Category.objects.all()
    return render(
        request,
        "inventory/add_product.html",
        {"categories": categories}
    )
 
# EDIT PRODUCT (UPDATE)
@staff_member_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            description = request.POST.get("description")
            price = Decimal(request.POST.get("price"))
            quantity = int(request.POST.get("quantity"))
            category = Category.objects.get(id=request.POST.get("category"))

            if not name or not description:
                raise ValueError

            if price < 0 or quantity < 0:
                raise ValueError

            product.name = name
            product.description = description
            product.price = price
            product.quantity = quantity
            product.category = category
            product.save()

            messages.success(request, "Product updated successfully.")
            return redirect("product_list")

        except:
            messages.error(request, "Invalid data provided.")
            return redirect("edit_product", id=id)

    categories = Category.objects.all()
    return render(request, "inventory/edit_product.html", {
        "product": product,
        "categories": categories
    })


# DELETE PRODUCT
@staff_member_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')
# Delete category
@staff_member_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('product_list')
# add to cart 
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    current_qty = cart.get(str(product.id), 0)
    if current_qty >= product.quantity:
        messages.error(
            request,
            f"Only {product.quantity} item(s) available in stock!"
        )
        return redirect('product_list')
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session['cart'] = cart
    messages.success(request, "Product added to cart successfully!")
    return redirect('product_list')
 
# view
def view_cart(request):
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    products = []
    total = 0

    for id, qty in cart.items():
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            continue

        product.qty = qty
        product.subtotal = product.price * qty
        total += product.subtotal
        products.append(product)

    return render(request, 'inventory/cart.html', {
        'products': products,
        'total': total
    })

# update cart quantity
def update_cart(request, id):
   product = get_object_or_404(Product, id=id)
   qty = int(request.POST.get('qty'))
   if qty > product.quantity:
       messages.error(
           request,
           f"Only {product.quantity} items available in stock"
       )
       return redirect('view_cart')
   if qty <= 0:
       messages.error(request, "Quantity must be greater than 0")
       return redirect('view_cart')

   cart = request.session.get('cart', {})
   cart[str(id)] = qty
   request.session['cart'] = cart

   messages.success(request, "Cart updated")
   return redirect('view_cart')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('view_cart') 