# crud.py
from . import base, schemas
from uuid import uuid4
from typing import Optional




# Update the create_product function to include a category field
def create_product(product: schemas.ProductCreate):
    key = f"product_{uuid4().hex}"
    # get category from productcreate and convert to category instance and add key for categories
    category_dict = product.category.dict()
    category_dict['key'] = f"category_{uuid4().hex}"
    category_ = base.Category(**category_dict)
    product = base.Product(
        key=key,
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image,
        category=category_  # new field
    )
    base.products_db.put(product.dict())
    base.categories_db.put(category_.dict())
    return product

def get_products(category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = {}
    if category:
        query["category.name?contains"] = category
    if min_price is not None:
        query["price?gte"] = min_price
    if max_price is not None:
        query["price?lte"] = max_price
    products = base.products_db.fetch(query).items
    products = [base.Product(**product) for product in products]
    return products

# Get a product by key from the database 
def get_product(key: str): 
    # Get the product from the database by key as a dictionary or None if not found 
    product = base.products_db.get(key) 
    # If the product is found, convert it to a Product instance 
    if product: 
        product = base.Product(**product) 
    # Return the product or None 
    return product

# Update a product by key in the database
def update_product(key: str, product: schemas.ProductUpdate):
    # Get the product from the database by key as a dictionary or None if not found
    product = base.products_db.get(key)
    # If the product is not found, return None
    if product is None:
        return None
    # Update the product attributes with the schema data
    for key, value in product.dict().items():
        setattr(product, key, value)
    # Put the updated product in the database
    base.products_db.put(product.dict())
    # Return the updated product
    return product

# Delete a product by key from the database
def delete_product(key: str):
    # Get the product from the database by key as a dictionary or None if not found
    product = base.products_db.get(key)
    # If the product is not found, return None
    if product is None:
        return None
    # Delete the product from the database by key
    base.products_db.delete(key)
    # Return the deleted product as a Product instance
    return base.Product(**product)

# Create a new user in the database
def create_user(user: schemas.UserCreate):
    # Generate a unique key for the user
    key = f"user_{uuid4().hex}"
    # Create a User instance from the schema data and the key
    user = base.User(
        key=key,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )
    # Put the user in the database
    base.users_db.put(user.dict())
    # Return the user
    return user

# Get all users from the database
def get_users():
     # Fetch all users from the database as a list of dictionaries 
     users = base.users_db.fetch().items
    
     # Convert each dictionary to a User instance 
     users = [base.User(**user) for user in users]
    
     # Return the users 
     return users

# Get a user by key from the database 
def get_user(key: str): 
     # Get the user from the database by key as a dictionary or None if not found 
     user = base.users_db.get(key) 
     # If the user is found, convert it to a User instance 
     if user: 
         user = base.User(**user) 
     # Return the user or None 
     return user

# Get a user by username from the database 
def get_user_by_username(username: str): 
     # Fetch all users from the database that match the username as a list of dictionaries (or empty list if not found) 
     users = base.users_db.fetch({"username": username}).items
    
     # If there is at least one user, convert the first one to a User instance (assume usernames are unique) 
     if users: 
         user = base.User(**users[0]) 
    
     else: 
         # Otherwise, set user to None 
         user = None
    
     # Return the user or None 
     return user

# Get a user by email from the database 
def get_user_by_email(email: str): 
    # Fetch match in the database else return None
    users = base.users_db.fetch({"email": email}).items

    if users:
        user = base.User(**users[0])

    else:
        user = None

    return user
    

    

# Update a user by key in the database
def update_user(key: str, user_update: schemas.UserUpdate):
    # Get the user from the database by key as a dictionary or None if not found
    user_dict = base.users_db.get(key)
    # If the user is not found, return None
    if user_dict is None:
        return None
    # Create a User object from the dictionary
    user = base.User(**user_dict)
    # Update the user attributes with the schema data
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    # Put the updated user in the database
    base.users_db.put(user.dict())
    # Return the updated user
    return user

# Delete a user by key from the database
def delete_user(key: str):
    # Get the user from the database by key as a dictionary or None if not found
    user = base.users_db.get(key)
    # If the user is not found, return None
    if user is None:
        return None
    # Delete the user from the database by key
    base.users_db.delete(key)
    # Return the deleted user as a User instance
    return base.User(**user)