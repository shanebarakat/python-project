from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms import PasswordField

from . import db, admin
from .models import User, Category, Product, Order, OrderItem

# --- Custom Admin Views ---

class AuthenticatedModelView(ModelView):
    """Base view for models that require authentication."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        """Redirect non-admins to the home page."""
        if not self.is_accessible():
            return redirect(url_for('main.index', next=request.url))

class UserAdminView(AuthenticatedModelView):
    """Custom view for the User model in the admin panel."""
    # List of columns to display in the list view
    column_list = ('username', 'email', 'is_admin', 'orders')
    
    # Columns that can be searched
    column_searchable_list = ('username', 'email')
    
    # Columns that can be filtered
    column_filters = ('is_admin',)
    
    # Fields to exclude from the create/edit forms
    form_excluded_columns = ('password_hash', 'orders')

    # Use a password field for setting/changing passwords
    form_extra_fields = {
        'new_password': PasswordField('New Password')
    }

    def on_model_change(self, form, model, is_created):
        """Handle password updates."""
        if form.new_password.data:
            model.set_password(form.new_password.data)

class ProductAdminView(AuthenticatedModelView):
    """Custom view for the Product model."""
    column_list = ('name', 'category', 'price', 'stock_quantity')
    column_searchable_list = ('name', 'description')
    column_filters = ('category.name', 'price', 'stock_quantity')
    
    # Use a rich text editor for the description
    form_overrides = {
        'description': 'flask_admin.form.widgets.CKEditorWidget'
    }
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'


class OrderAdminView(AuthenticatedModelView):
    """Custom view for the Order model."""
    column_list = ('id', 'customer', 'order_date', 'status', 'total_price')
    column_searchable_list = ('customer.username', 'status')
    column_filters = ('status', 'order_date')
    
    # Make the view read-only for now to prevent accidental changes
    can_create = False
    can_edit = True # Allow changing status
    can_delete = False
    
    form_columns = ('status',) # Only allow editing the status


class OrderItemAdminView(AuthenticatedModelView):
    """Custom view for OrderItem model."""
    column_list = ('order_id', 'product', 'quantity', 'price_per_item')


# --- Register Admin Views ---
admin.add_view(UserAdminView(User, db.session))
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductAdminView(Product, db.session))
admin.add_view(OrderAdminView(Order, db.session))
admin.add_view(OrderItemAdminView(OrderItem, db.session, name="Order Items")) 