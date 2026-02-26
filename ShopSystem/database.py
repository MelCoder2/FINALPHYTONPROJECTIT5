import mysql.connector
import bcrypt

# --- CONFIGURATION ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "Computerpartsandservices"
}


def get_connection():
    return mysql.connector.connect(**db_config)


def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    """Verify a password against a hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def initialize_db():
    try:
        conn = mysql.connector.connect(host=db_config["host"], user=db_config["user"], password=db_config["password"])
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        conn.close()

        conn = get_connection()
        cursor = conn.cursor()

        # Users table with email and phone
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'customer',
                full_name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20)
            )
        """)

        # Products table with category and details
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                stock_qty INT NOT NULL,
                category VARCHAR(50) DEFAULT 'General',
                details TEXT,
                is_active TINYINT DEFAULT 1
            )
        """)

        # Sales table (enhanced)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                full_name VARCHAR(255),
                product_id INT,
                quantity INT,
                total_price DECIMAL(10, 2),
                payment_method VARCHAR(50) DEFAULT 'Cash',
                bank_name VARCHAR(100),
                account_number VARCHAR(100),
                sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)

        # Services table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                service_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                full_name VARCHAR(255),
                service_type VARCHAR(100),
                description TEXT,
                price DECIMAL(10, 2) DEFAULT 0.00,
                status VARCHAR(50) DEFAULT 'Pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES users(user_id)
            )
        """)

        # Completed services (kept for historical records / backwards compatibility)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completed_services (
                completed_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                full_name VARCHAR(255),
                service_type VARCHAR(100),
                description TEXT,
                price DECIMAL(10, 2) DEFAULT 0.00,
                started_at DATETIME,
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES users(user_id)
            )
        """)

        # Check and create default manager
        cursor.execute("SELECT * FROM users WHERE username = 'manager'")
        if not cursor.fetchone():
            hashed_pw = hash_password('admin123')
            cursor.execute(
                "INSERT INTO users (username, password, role, full_name, email, phone) VALUES (%s, %s, 'manager', 'Store Manager', 'admin@melcom.com', '09123456789')",
                ('manager', hashed_pw))

        # Check and create default user
        cursor.execute("SELECT * FROM users WHERE username = 'user'")
        if not cursor.fetchone():
            hashed_pw = hash_password('user123')
            cursor.execute(
                "INSERT INTO users (username, password, role, full_name, email, phone) VALUES (%s, %s, 'customer', 'Juan Dela Cruz', 'juan@email.com', '09187654321')",
                ('user', hashed_pw))

        conn.commit()
        print("Database initialized successfully.")

    except Exception as e:
        print(f"DB Init Error: {e}")
    finally:
        try:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
        except:
            pass


# --- USER OPERATIONS ---
def check_login(username, password):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, role, full_name, username, password FROM users WHERE username = %s",
                       (username,))
        user = cursor.fetchone()
        if user and verify_password(password, user[4]):
            return (user[0], user[1], user[2], user[3])
        return None
    except Exception as e:
        print("Login Error:", e)
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()


def register_user(username, password, full_name, email, phone):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Username already taken"

        hashed_pw = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password, full_name, email, phone, role) VALUES (%s, %s, %s, %s, %s, 'customer')",
            (username, hashed_pw, full_name, email, phone))
        conn.commit()
        return True, "Success"
    except Exception as e:
        return False, str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_all_customers():
    """Get all customers (role = 'customer') from users table"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, email, phone FROM users WHERE role = 'customer' ORDER BY full_name")
        return cursor.fetchall() or []
    except Exception as e:
        print("Get All Customers Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


# --- PRODUCT OPERATIONS ---
def get_products(category=None, search=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT product_id, code, name, price, stock_qty, category, details FROM products WHERE is_active = 1"
        params = []

        if category and category != "All":
            query += " AND category = %s"
            params.append(category)

        if search:
            query += " AND (name LIKE %s OR code LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])

        query += " ORDER BY code ASC"

        cursor.execute(query, params)
        return cursor.fetchall() or []
    except Exception as e:
        print("Get Products Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_categories():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products WHERE is_active = 1 ORDER BY category")
        rows = cursor.fetchall()
        return [r[0] for r in rows] if rows else []
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_all_codes():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM products")
        rows = cursor.fetchall()
        return [r[0] for r in rows] if rows else []
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def add_product(code, name, price, stock, category, details):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (code, name, price, stock_qty, category, details, is_active) VALUES (%s, %s, %s, %s, %s, %s, 1)",
            (code, name, price, stock, category, details))
        conn.commit()
    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise Exception(f"Product Code '{code}' is already taken.")
        else:
            raise err
    finally:
        if conn and conn.is_connected():
            conn.close()


def restock_product(product_id, quantity):
    """Add stock to an existing product"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET stock_qty = stock_qty + %s WHERE product_id = %s AND is_active = 1",
            (quantity, product_id))
        conn.commit()

        if cursor.rowcount == 0:
            raise Exception("Product not found or inactive")

    except Exception as e:
        print(f"Restock Error: {e}")
        raise e
    finally:
        if conn and conn.is_connected():
            conn.close()


def delete_product(pid):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET is_active = 0 WHERE product_id = %s", (pid,))
        conn.commit()
    except Exception as e:
        print(f"Delete Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


# --- SALES OPERATIONS ---
def checkout_cart(username, cart_items, payment_method, bank_name=None, account_number=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, full_name FROM users WHERE username = %s", (username,))
        user_row = cursor.fetchone()
        if not user_row:
            raise Exception("User not found")
        user_id, full_name = user_row

        for item in cart_items:
            cursor.execute("SELECT product_id, stock_qty, name FROM products WHERE code = %s", (item['code'],))
            prod_row = cursor.fetchone()
            if not prod_row:
                raise Exception(f"Product {item['code']} not found")
            pid, stock, pname = prod_row
            if stock < item['qty']:
                raise Exception(f"Not enough stock for {pname}")
            cursor.execute("UPDATE products SET stock_qty = stock_qty - %s WHERE product_id = %s", (item['qty'], pid))
            total_price = item['price'] * item['qty']
            cursor.execute(
                "INSERT INTO sales (customer_id, full_name, product_id, quantity, total_price, payment_method, bank_name, account_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (user_id, full_name, pid, item['qty'], total_price, payment_method, bank_name, account_number))
        conn.commit()
        return "Success"
    except Exception as e:
        if conn: conn.rollback()
        return str(e)
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_user_sales(username):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.sale_date, p.name, s.quantity, s.total_price, s.payment_method
            FROM sales s
            JOIN users u ON s.customer_id = u.user_id
            JOIN products p ON s.product_id = p.product_id
            WHERE u.username = %s
            ORDER BY s.sale_date DESC
        """, (username,))
        return cursor.fetchall() or []
    except Exception as e:
        print("User Sales Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_all_sales():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.sale_date, s.full_name, p.name, s.quantity, s.total_price, s.payment_method, s.bank_name
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_date DESC
        """)
        return cursor.fetchall() or []
    except Exception as e:
        print("All Sales Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


# --- STATS ---
def get_stats():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Sales revenue
        cursor.execute("SELECT SUM(total_price) FROM sales")
        sales_rev = cursor.fetchone()[0] or 0

        # Read completed service revenue from services table
        cursor.execute("SELECT SUM(price) FROM services WHERE status = 'Completed'")
        svc_rev = cursor.fetchone()[0] or 0

        total_rev = sales_rev + svc_rev

        # Total orders = product sales count + all services (pending + completed)
        cursor.execute("SELECT COUNT(*) FROM sales")
        sales_cnt = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM services")
        svc_cnt = cursor.fetchone()[0] or 0

        cnt = sales_cnt + svc_cnt

        cursor.execute("SELECT SUM(stock_qty) FROM products WHERE is_active = 1")
        stk = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'customer'")
        custs = cursor.fetchone()[0] or 0

        return total_rev, cnt, stk, custs
    except Exception:
        return 0, 0, 0, 0
    finally:
        if conn and conn.is_connected():
            conn.close()


# --- SERVICE OPERATIONS ---
def book_service(username, service_type, description, price):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, full_name FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row:
            user_id, full_name = row
            cursor.execute(
                "INSERT INTO services (customer_id, full_name, service_type, description, price) VALUES (%s, %s, %s, %s, %s)",
                (user_id, full_name, service_type, description, price))
            conn.commit()
    except Exception as e:
        print("Book Service Error:", e)
        raise e
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_all_services_joined():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT service_id, full_name, service_type, description, status, price FROM services ORDER BY service_id DESC")
        return cursor.fetchall() or []
    except Exception as e:
        print("All Services Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_user_services(username):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.service_id, s.created_at, s.service_type, s.description, s.status, s.price
            FROM services s
            JOIN users u ON s.customer_id = u.user_id
            WHERE u.username = %s
            ORDER BY s.service_id DESC
        """, (username,))
        return cursor.fetchall() or []
    except Exception as e:
        print("User Services Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def delete_service(sid):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE service_id = %s", (sid,))
        conn.commit()
    except Exception:
        pass
    finally:
        if conn and conn.is_connected():
            conn.close()


def move_service_to_completed(service_id):
    """Kept for backwards compatibility only. Not called by update_service_status."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT customer_id, full_name, service_type, description, created_at, price FROM services WHERE service_id = %s",
            (service_id,))
        row = cursor.fetchone()
        if row:
            cust_id, full_name, svc_type, desc, start_date, price = row
            cursor.execute(
                "INSERT INTO completed_services (customer_id, full_name, service_type, description, started_at, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (cust_id, full_name, svc_type, desc, start_date, price))
            cursor.execute("DELETE FROM services WHERE service_id = %s", (service_id,))
            conn.commit()
            return True
        return False
    except Exception as e:
        print(f"Error moving service: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()


def update_service_status(sid, status):
    """Updates status in-place in the services table."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE services SET status = %s WHERE service_id = %s", (status, sid))
        conn.commit()
    except Exception as e:
        print("Update Status Error:", e)
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_completed_services_from_services(limit=None, offset=None):
    """
    Gets completed services from the services table (status = 'Completed').
    Returns: (service_id, full_name, service_type, description, created_at, created_at, price)
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT service_id, full_name, service_type, description, created_at, created_at, price
            FROM services
            WHERE status = 'Completed'
            ORDER BY created_at DESC
        """

        if limit is not None and offset is not None:
            query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query)
        return cursor.fetchall() or []
    except Exception as e:
        print("Completed Services (services table) Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_completed_services_count_from_services():
    """Count of completed services in services table."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM services WHERE status = 'Completed'")
        return cursor.fetchone()[0] or 0
    except Exception:
        return 0
    finally:
        if conn and conn.is_connected():
            conn.close()


# Keep old functions for backwards compatibility
def get_completed_services(limit=None, offset=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT completed_id, full_name, service_type, description, started_at, completed_at, price
            FROM completed_services
            ORDER BY completed_at DESC
        """

        if limit is not None and offset is not None:
            query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query)
        return cursor.fetchall() or []
    except Exception as e:
        print("Completed Services Error:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()


def get_completed_services_count():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM completed_services")
        return cursor.fetchone()[0] or 0
    except Exception:
        return 0
    finally:
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    initialize_db()