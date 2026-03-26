def cart_total_items(request):
    cart = request.session.get('cart', {})
    total = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_total_items': total}
