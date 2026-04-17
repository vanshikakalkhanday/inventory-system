from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal, InvalidOperation
 
# SHOW ALL PRODUCTS

def product_list(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    if query:
        products = Product.objects.filter(name__icontains=query)
    categories = Category.objects.all()
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories
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
        'categories': categories
    })

# ADD NEW PRODUCT (CREATE)
@staff_member_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price_raw = request.POST.get("price")
        quantity_raw = request.POST.get("quantity")
        category_id = request.POST.get("category")
        if not category_id:
            messages.error(request, "Please select a category.")
            return redirect("add_product")
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect("add_product")
        if not price_raw:
            messages.error(request, "Price is required.")
            return redirect("add_product")
        try:
            price = Decimal(price_raw)
            if price < 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, "Please enter a valid price.")
            return redirect("add_product")
        if not quantity_raw:
            messages.error(request, "Quantity is required.")
            return redirect("add_product")
        try:
            quantity = int(quantity_raw)
            if quantity < 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Please enter a valid quantity.")
            return redirect("add_product")
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
        )
        messages.success(request, "Product added successfully.")
        return redirect("product_list")
    categories = Category.objects.all()
    return render(request, "inventory/add_product.html", {"categories": categories})


# EDIT PRODUCT (UPDATE)
@staff_member_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.category = Category.objects.get(id=request.POST['category'])
        product.save()
        return redirect('product_list')
    categories = Category.objects.all()
    return render(request, 'inventory/edit_product.html', {
        'product': product,
        'categories': categories
    })

# DELETE PRODUCT
@staff_member_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')
# add to cart 
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', {})
    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1
    request.session['cart'] = cart
    messages.success(request, "Product added to cart successfully!")
    return redirect('product_list') 

def view_cart(request):

    cart = request.session.get('cart', {})   
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart
    products = []
    total = 0
    for id, qty in cart.items():
        product = Product.objects.get(id=id)
        product.qty = qty
        product.subtotal = product.price * qty
        total += product.subtotal
        products.append(product)
    return render(request, 'inventory/cart.html', {
        'products': products,
        'total': total
    })
   
def update_cart(request, id):
    if request.method == "POST":
        qty = int(request.POST['qty'])
        cart = request.session.get('cart', {})
        if str(id) in cart:
            cart[str(id)] = qty
        request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('view_cart')
  

 