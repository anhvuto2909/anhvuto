from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session 
        # Get request
        self.request = request
        # Get the current session key if it exist
        cart = self.session.get('session_key')

        # If the user is new, no session key, create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} 

        # Make sure care is available on all page of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # Deal with log in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart= str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True

        # Deal with log in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart= str(carty))

    def cart_total(self):
        # Get product ids
        product_ids = self.cart.keys()
        # Lookup those key in our products db models
        products = Product.objects.filter(id__in=product_ids)
        # Get quantity
        quantities = self.cart
        # Counting 
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:  
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in db model
        products = Product.objects.filter(id__in = product_ids)

        # Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

		# Get cart
        ourcart = self.cart
		# Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        

        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart= str(carty))

        thing = self.cart
        return thing
    
    def delete(self, product):
        {'4':1, '2':1}
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True    

        # Deal with log in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart= str(carty))

        
        
