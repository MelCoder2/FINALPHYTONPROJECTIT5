import re
import database


class LoginController:
    def __init__(self, view):
        self.view = view

    def validate_username(self, username):
        """
        Validate username:
        - 3-20 characters
        - Alphanumeric and underscores only
        - Must start with a letter
        """
        if not username:
            return False, "Username is required"

        if len(username) < 3:
            return False, "Username must be at least 3 characters long"

        if len(username) > 20:
            return False, "Username must not exceed 20 characters"

        if not username[0].isalpha():
            return False, "Username must start with a letter"

        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
            return False, "Username can only contain letters, numbers, and underscores"

        return True, "Valid"

    def validate_password(self, password):
        """
        Validate password:
        - Minimum 8 characters
        - Must contain at least one uppercase letter
        - Must contain at least one lowercase letter
        - Must contain at least one number
        """
        if not password:
            return False, "Password is required"

        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"

        return True, "Valid"

    def validate_email(self, email):
        """
        Validate email:
        - Must contain @gmail.com
        - Basic email format validation
        """
        if not email:
            return False, "Email is required"

        if not '@gmail.com' in email.lower():
            return False, "Email must be a Gmail address (@gmail.com)"

        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        if not re.match(email_pattern, email, re.IGNORECASE):
            return False, "Invalid email format (example: user@gmail.com)"

        return True, "Valid"

    def validate_phone(self, phone):
        """
        Validate phone number:
        - Must be exactly 11 digits (Philippine mobile number format)
        - Must contain only numbers
        - Should start with 09
        """
        if not phone:
            return False, "Phone number is required"

        # Remove any spaces or dashes
        phone_clean = phone.replace(" ", "").replace("-", "")

        if not phone_clean.isdigit():
            return False, "Phone number must contain only numbers"

        if len(phone_clean) != 11:
            return False, "Phone number must be exactly 11 digits"

        if not phone_clean.startswith('09'):
            return False, "Philippine mobile number must start with 09"

        return True, "Valid"

    def validate_full_name(self, full_name):
        """Validate full name"""
        if not full_name:
            return False, "Full name is required"

        if len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters long"

        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", full_name):
            return False, "Full name can only contain letters, spaces, hyphens, and apostrophes"

        return True, "Valid"

    def handle_login(self, username, password):
        """Handle user login"""
        if not username or not password:
            return False, None

        user_data = database.check_login(username, password)
        if user_data:
            return True, user_data
        else:
            return False, None

    def handle_register(self, username, password, full_name, email, phone):
        """Handle user registration with comprehensive validation"""

        # Validate username
        valid, msg = self.validate_username(username)
        if not valid:
            return False, msg

        # Validate password
        valid, msg = self.validate_password(password)
        if not valid:
            return False, msg

        # Validate full name
        valid, msg = self.validate_full_name(full_name)
        if not valid:
            return False, msg

        # Validate email
        valid, msg = self.validate_email(email)
        if not valid:
            return False, msg

        # Validate phone
        valid, msg = self.validate_phone(phone)
        if not valid:
            return False, msg

        # If all validations pass, attempt to register
        success, db_msg = database.register_user(username, password, full_name, email, phone)

        return success, db_msg