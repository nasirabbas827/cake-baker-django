from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Cake, Cart , CakeCategory , CustomizationRequest, Order , OrderItem , Transaction
from .forms import ProfileForm , CustomizationRequestForm , TransactionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered and logged in.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def index(request):
    # Fetching all cakes for display
    cakes = Cake.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    size_filter = request.GET.get('size', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        cakes = cakes.filter(Q(cake_name__icontains=search_query) | Q(description__icontains=search_query))

    if size_filter:
        cakes = cakes.filter(size=size_filter)

    if category_filter:
        cakes = cakes.filter(category__category_name=category_filter)

    categories = CakeCategory.objects.all()  # Fetching categories for the filter

    return render(request, 'index.html', {'cakes': cakes, 'categories': categories, 'search_query': search_query})

@login_required
def dashboard(request):
    # Fetching all cakes for display
    cakes = Cake.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    size_filter = request.GET.get('size', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        cakes = cakes.filter(Q(cake_name__icontains=search_query) | Q(description__icontains=search_query))

    if size_filter:
        cakes = cakes.filter(size=size_filter)

    if category_filter:
        cakes = cakes.filter(category__category_name=category_filter)

    categories = CakeCategory.objects.all()  # Fetching categories for the filter
    return render(request, 'dashboard.html', {'cakes': cakes, 'categories': categories, 'search_query': search_query})

@login_required
def add_to_cart(request, cake_id):
    cake = Cake.objects.get(cake_id=cake_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, cake=cake)
    
    if not created:
        cart_item.quantity += 1  # Increase quantity if already in the cart
        cart_item.save()
    
    return redirect('dashboard')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Fetch cart items for the logged-in user
    total_price = sum(item.cake.price * item.quantity for item in cart_items)  # Calculate total price

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity and new_quantity.isdigit() and int(new_quantity) > 0:
            item.quantity = int(new_quantity)
            item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            messages.error(request, 'Please enter a valid quantity.')
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart successfully.')
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.cake.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def make_order(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.cake.price * item.quantity for item in cart_items)

        if cart_items:
            # Create Order
            order = Order.objects.create(
                user=request.user,
                address=request.POST.get('address'),
                total_amount=total_price,
                payment_method=request.POST.get('payment_method'),
                order_status='Pending',
                payment_status='Pending'
            )

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    cake=item.cake,
                    quantity=item.quantity,
                    price=item.cake.price
                )
            # Clear Cart after placing order
            cart_items.delete()

            return redirect('order_success')
    return render(request, 'make_order.html')

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'view_orders.html', {'orders': orders})
@login_required
def view_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, order_status='Pending', payment_method='Cash on Delivery')
    order.delete()
    return redirect('view_orders')


@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, payment_status='Pending')
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new transaction
            transaction = form.save(commit=False)
            transaction.order = order
            transaction.transaction_date = timezone.now()
            transaction.amount = order.total_amount
            transaction.save()
            
            # Update the order payment status to 'Paid'
            order.payment_status = 'Paid'
            order.save()
            
            return redirect('view_order_details', order_id=order.id)
    else:
        form = TransactionForm()

    return render(request, 'pay_order.html', {'order': order, 'form': form})


@login_required
def customization_request(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, payment_status='Paid')
    
    # Get existing customization requests for this order
    customization_requests = CustomizationRequest.objects.filter(order=order)

    if request.method == 'POST':
        form = CustomizationRequestForm(request.POST)
        if form.is_valid():
            customization_request = form.save(commit=False)
            customization_request.order = order
            customization_request.created_at = timezone.now()
            customization_request.save()
            return redirect('customization_request', order_id=order.id)
    else:
        form = CustomizationRequestForm()

    return render(request, 'customization_request.html', {
        'order': order,
        'form': form,
        'customization_requests': customization_requests
    })

@login_required
def update_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def view_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')
