from .cart import Cart

# Tạo context processors để cart có thể ở tất cả mọi trang
def cart(request):
    # Return the default data from our cart
    return {'cart': Cart(request)}