# base.py
from deta import Deta
from pydantic import BaseModel
from core.config import settings


# Initialize Deta with your project key
deta = Deta(settings.deta_app_key)

# Create a Deta Base instance for products
products_db = deta.Base("ecommerce_products")

# Define a Pydantic model for the Product entity
class Product(BaseModel):
    # Use key as the primary identifier
    key: str
    name: str
    description: str
    price: float
    image: str

    # Define a string representation of the model
    def __repr__(self):
        return f"<Product(key={self.key}, name={self.name}, description={self.description}, price={self.price}, image={self.image})>"

# Create a Deta Base instance for users
users_db = deta.Base("ecommerce_users")

# Define a Pydantic model for the User entity
class User(BaseModel):
    # Use key as the primary identifier
    key: str
    username: str
    email: str
    hashed_password: str
    is_active: bool
    is_admin: bool

    # Define a string representation of the model
    def __repr__(self):
        return f"<User(key={self.key}, username={self.username}, email={self.email}, hashed_password={self.hashed_password}, is_active={self.is_active}, is_admin={self.is_admin})>"

# Create a Deta Base instance for carts
carts_db = deta.Base("carts")

# Define a Pydantic model for the CartItem entity
class CartItem(BaseModel):
    # Use key as the primary identifier (composed of user_key and product_key)
    key: str
    user_key: str
    product_key: str
    quantity: int

    # Define a string representation of the model
    def __repr__(self):
        return f"<CartItem(key={self.key}, user_key={self.user_key}, product_key={self.product_key}, quantity={self.quantity})>"

# Create a Deta Base instance for orders
orders_db = deta.Base("ecommerce_orders")

# Define a Pydantic model for the Order entity
class Order(BaseModel):
    # Use key as the primary identifier (composed of user_key and order_id)
    key: str
    user_key: str
    order_id: str
    items: list # list of CartItem instances
    total: float
    status: str # one of "pending", "paid", "shipped", "delivered", "cancelled"

    # Define a string representation of the model
    def __repr__(self):
        return f"<Order(key={self.key}, user_key={self.user_key}, order_id={self.order_id}, items={self.items}, total={self.total}, status={self.status})>"
