from .models import Order

def cart_items(request):
    cartItems = 0
    if request.user.is_authenticated and request.user.customer:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items()
    return {'cartItems': cartItems}
