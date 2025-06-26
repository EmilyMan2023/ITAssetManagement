from flask import abort
from flask_login import current_user
from functools import wraps

# custom decorator to restrict route access to admin users only
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
         # check if user is not authenticated OR doesn't have admin role
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # forbidden
        # user is allowed - proceed to the original view function
        return f(*args, **kwargs)
    return decorated_function
