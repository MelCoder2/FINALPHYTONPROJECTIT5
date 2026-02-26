import re
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget,
    QFrame, QDateEdit, QTextEdit, QComboBox, QAbstractItemView, QDialog,
    QSpinBox, QLineEdit, QRadioButton, QButtonGroup, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont, QCursor

from controllers.user_controller import UserController


# === BANK DETAILS DIALOG ===
class BankDetailsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Bank Transfer Details")
        self.setFixedSize(500, 450)
        self.setModal(True)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("""
            QDialog { 
                background-color: #f8fafc;
            }
            QLabel {
                background: transparent;
                border: none;
            }
            QLineEdit {
                background: transparent;
                border: none;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Enter Bank Transfer Details")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)

        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(25, 25, 25, 25)

        bank_label = QLabel("Bank Name:")
        bank_label.setStyleSheet("""
            QLabel {
                font-weight: 700;
                color: #1e293b;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px 0px 6px 0px;
            }
        """)
        form_layout.addWidget(bank_label)

        self.bank_name = QComboBox()
        self.bank_name.addItems([
            "BDO (Banco de Oro)",
            "BPI (Bank of the Philippine Islands)",
            "Metrobank"
        ])
        self.bank_name.setFixedHeight(48)
        self.bank_name.setStyleSheet("""
            QComboBox {
                background: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                padding: 12px;
                padding-right: 30px;
                color: #334155;
                font-size: 14px;
            }
            QComboBox:focus { border: 2px solid #009688; }
            QComboBox:hover { border: 2px solid #94a3b8; }
            QComboBox::drop-down { border: none; padding-right: 10px; }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                selection-background-color: #009688;
                selection-color: white;
                padding: 4px;
                font-size: 14px;
                color: #334155;
            }
        """)
        form_layout.addWidget(self.bank_name)

        form_layout.addSpacing(20)

        account_label = QLabel("Account Number:")
        account_label.setStyleSheet("""
            QLabel {
                font-weight: 700;
                color: #1e293b;
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px 0px 6px 0px;
            }
        """)
        form_layout.addWidget(account_label)

        self.account_num = QLineEdit()
        self.account_num.setPlaceholderText("Your account number")
        self.account_num.setFixedHeight(48)
        self.account_num.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                padding: 12px;
                color: #334155;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #009688;
                background: #ffffff;
            }
            QLineEdit::placeholder { color: #94a3b8; }
        """)
        form_layout.addWidget(self.account_num)

        main_layout.addWidget(form_container)
        main_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(48)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                color: #475569; border-radius: 6px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_submit = QPushButton("Submit")
        btn_submit.setFixedHeight(48)
        btn_submit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_submit.setStyleSheet("""
            QPushButton {
                background: #009688; color: white; border: none;
                border-radius: 6px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background: #00796b; }
        """)
        btn_submit.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_submit)
        main_layout.addLayout(btn_layout)

    def get_bank_details(self):
        return self.bank_name.currentText(), self.account_num.text()


# === PAYMENT DIALOG ===
class PaymentDialog(QDialog):
    def __init__(self, parent, total_amount):
        super().__init__(parent)
        self.setWindowTitle("Payment Method")
        self.setFixedSize(520, 380)
        self.setModal(True)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("""
            QDialog { background-color: #f8fafc; }
            QLabel { background: transparent; border: none; }
            QRadioButton { background: transparent; border: none; }
        """)

        self.bank_name_val = None
        self.account_num_val = None

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(35, 35, 35, 35)

        lbl_title = QLabel("Select Payment Method")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_title)

        lbl_total = QLabel(f"Total Amount: ₱{total_amount:,.2f}")
        lbl_total.setStyleSheet("font-size: 18px; color: #009688; font-weight: bold;")
        lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lbl_total)

        options_container = QWidget()
        options_container.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)
        options_layout = QVBoxLayout(options_container)
        options_layout.setContentsMargins(30, 25, 30, 25)
        options_layout.setSpacing(18)

        self.btn_group = QButtonGroup(self)

        self.rb_cash = QRadioButton("💵 Cash on Pickup")
        self.rb_cash.setStyleSheet("""
            QRadioButton {
                font-size: 16px; font-weight: 600; color: #334155;
                spacing: 10px; background: transparent; border: none; outline: none;
            }
            QRadioButton::indicator { width: 20px; height: 20px; }
            QRadioButton:focus { outline: none; }
        """)
        self.rb_cash.setChecked(True)
        self.btn_group.addButton(self.rb_cash)
        options_layout.addWidget(self.rb_cash)

        self.rb_bank = QRadioButton("🏦 Bank Transfer")
        self.rb_bank.setStyleSheet("""
            QRadioButton {
                font-size: 16px; font-weight: 600; color: #334155;
                spacing: 10px; background: transparent; border: none; outline: none;
            }
            QRadioButton::indicator { width: 20px; height: 20px; }
            QRadioButton:focus { outline: none; }
        """)
        self.btn_group.addButton(self.rb_bank)
        options_layout.addWidget(self.rb_bank)

        main_layout.addWidget(options_container)
        main_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(48)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                color: #475569; border-radius: 6px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("Confirm Payment")
        btn_confirm.setFixedHeight(48)
        btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_confirm.setStyleSheet("""
            QPushButton {
                background: #009688; color: white; border: none;
                border-radius: 6px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background: #00796b; }
        """)
        btn_confirm.clicked.connect(self.on_confirm_clicked)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        main_layout.addLayout(btn_layout)

    def on_confirm_clicked(self):
        if self.rb_bank.isChecked():
            bank_dlg = BankDetailsDialog(self)
            if bank_dlg.exec():
                self.bank_name_val, self.account_num_val = bank_dlg.get_bank_details()
                if not self.bank_name_val or not self.account_num_val:
                    QMessageBox.warning(self, "Missing Info", "Please enter both bank name and account number")
                    return
                self.accept()
        else:
            self.accept()

    def get_payment_info(self):
        if self.rb_cash.isChecked():
            return "Cash on Pickup", None, None
        else:
            return "Bank Transfer", self.bank_name_val, self.account_num_val


# === RECEIPT WINDOW ===
class ReceiptWindow(QDialog):
    def __init__(self, parent, receipt_text):
        super().__init__(parent)
        self.setWindowTitle("Official Receipt")
        self.setFixedSize(450, 650)

        self.setStyleSheet("QDialog { background-color: #f8fafc; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        lbl = QLabel("✅ Transaction Complete")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("""
            QLabel {
                color: #059669; font-size: 20px; font-weight: bold;
                background: transparent; border: none;
            }
        """)
        layout.addWidget(lbl)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setText(receipt_text)
        font = QFont("Courier New", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_area.setFont(font)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 15px;
                color: #334155;
            }
        """)
        layout.addWidget(self.text_area)

        btn_close = QPushButton("Close")
        btn_close.setFixedHeight(48)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #009688; color: white; border-radius: 6px;
                font-weight: bold; border: none; font-size: 14px;
            }
            QPushButton:hover { background-color: #00796b; }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


# === MAIN USER WINDOW ===
class UserView(QMainWindow):
    def __init__(self, user_id, username, full_name):
        super().__init__()
        self.controller = UserController(self, user_id, username, full_name)

        self.setWindowTitle("Customer Window")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("QWidget#centralWidget { background-color: #f8fafc; }")
        central.setObjectName("centralWidget")

        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # HEADER
        top = QHBoxLayout()
        t_layout = QVBoxLayout()

        title = QLabel("Customer Dashboard")
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: #1e293b; background: none;")

        sub = QLabel("Purchase Premium Computer Parts & Professional Services")
        sub.setStyleSheet("font-size: 16px; color: #64748b; background: none;")

        contact = QLabel("📧 melcomshopandservices@gmail.com   |   📞 (0912) 345-6789")
        contact.setStyleSheet("font-size: 14px; color: #009688; font-weight: bold; background: none;")

        t_layout.addWidget(title)
        t_layout.addWidget(sub)
        t_layout.addWidget(contact)

        self.prof_btn = QPushButton(f"  👤 {full_name}")
        self.prof_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; border: none; color: #334155; 
                font-size: 15px; font-weight: bold; 
            }
        """)

        logout = QPushButton("➥🚪 Sign Out")
        logout.setFixedWidth(140)
        logout.setFixedHeight(40)
        logout.setCursor(Qt.CursorShape.PointingHandCursor)
        logout.setStyleSheet("""
            QPushButton { 
                background: #fee2e2; border: 1px solid #fecaca;
                border-radius: 6px; padding: 8px; color: #b91c1c;
                font-weight: bold; font-size: 14px;
            }
            QPushButton:hover {
                background: #fca5a5; color: #7f1d1d; border-color: #fca5a5;
            }
        """)
        logout.clicked.connect(self.on_logout_clicked)

        top.addLayout(t_layout)
        top.addStretch()
        top.addWidget(self.prof_btn)
        top.addWidget(logout)
        layout.addLayout(top)

        # TABS
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #e2e8f0; background: white; border-radius: 8px; 
            }
            QTabBar::tab { 
                background: #e2e8f0; padding: 10px 20px; margin-right: 4px; 
                border-top-left-radius: 6px; border-top-right-radius: 6px; 
                font-weight: bold; color: #64748b; 
            }
            QTabBar::tab:selected { 
                background: white; color: #0f172a; border-bottom: none; 
            }
            QTabWidget > QWidget { background-color: #f8fafc; }
        """)
        layout.addWidget(self.tabs)

        self.init_shop_tab()
        self.init_cart_tab()
        self.init_orders_tab()
        self.init_booking_tab()
        self.init_my_bookings_tab()

    def on_logout_clicked(self):
        from views.login_view import LoginView
        self.login_window = LoginView()
        self.login_window.show()
        self.close()

    # === SHOP TAB ===
    def init_shop_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(15)
        filter_bar.addWidget(
            QLabel("Filter:", styleSheet="font-weight: bold; color: #334155; font-size: 14px; border: none;"))

        self.shop_cat_filter = QComboBox()
        self.shop_cat_filter.addItem("All Categories")
        self.shop_cat_filter.setFixedHeight(45)
        self.shop_cat_filter.setStyleSheet("""
            QComboBox {
                background: white; border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 10px; padding-right: 30px; min-width: 180px;
                font-size: 14px; color: #334155;
            }
            QComboBox:hover { border: 1px solid #cbd5e1; }
            QComboBox:focus { border: 2px solid #009688; outline: none; }
        """)
        self.shop_cat_filter.currentTextChanged.connect(self.refresh_shop)
        filter_bar.addWidget(self.shop_cat_filter)

        self.shop_search = QLineEdit()
        self.shop_search.setPlaceholderText("🔍 Search products...")
        self.shop_search.setFixedWidth(350)
        self.shop_search.setFixedHeight(45)
        self.shop_search.setStyleSheet("""
            QLineEdit {
                background: white; border: 1px solid #e2e8f0;
                border-radius: 6px; padding: 10px; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #009688; outline: none; }
        """)
        self.shop_search.textChanged.connect(self.refresh_shop)
        filter_bar.addWidget(self.shop_search)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        self.shop_table = QTableWidget(0, 6)
        self.shop_table.setHorizontalHeaderLabels(["CODE", "NAME", "PRICE", "STOCK", "CATEGORY", "QTY"])

        header = self.shop_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.shop_table.setColumnWidth(5, 200)

        self.shop_table.setAlternatingRowColors(True)
        self.shop_table.verticalHeader().setVisible(False)
        self.shop_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.shop_table.setShowGrid(False)
        self.shop_table.setFrameShape(QFrame.Shape.NoFrame)
        self.shop_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.shop_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.shop_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.shop_table.verticalHeader().setDefaultSectionSize(60)
        self.shop_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0; border-radius: 8px; outline: none;
                gridline-color: transparent; background-color: white;
            }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section {
                background-color: #f8fafc; padding: 12px; border: none;
                border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b;
            }
            QLabel { border: none; outline: none; }
        """)
        layout.addWidget(self.shop_table, stretch=1)

        btn = QPushButton("🔁 Refresh")
        btn.setFixedWidth(150)
        btn.setFixedHeight(40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn.clicked.connect(self.refresh_shop)

        bl = QHBoxLayout()
        bl.addStretch()
        bl.addWidget(btn)
        layout.addLayout(bl)

        self.tabs.addTab(tab, "  🛒 Shop Products  ")

        try:
            self.refresh_shop()
        except Exception as e:
            print(f"Error loading shop: {e}")

    # === CART TAB ===
    def init_cart_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.cart_table = QTableWidget(0, 5)
        self.cart_table.setHorizontalHeaderLabels(["PRODUCT", "PRICE", "QTY", "TOTAL", "ACTION"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cart_table.setShowGrid(False)
        self.cart_table.setFrameShape(QFrame.Shape.NoFrame)
        self.cart_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.cart_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cart_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.cart_table.verticalHeader().setDefaultSectionSize(50)
        self.cart_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0; border-radius: 8px; outline: none;
                gridline-color: transparent; background-color: white;
            }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section {
                background-color: #f8fafc; padding: 12px; border: none;
                border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b;
            }
        """)
        layout.addWidget(self.cart_table, stretch=1)

        bottom_box = QHBoxLayout()

        btn_clear = QPushButton("🗑️ Clear Cart")
        btn_clear.setFixedWidth(150)
        btn_clear.setFixedHeight(45)
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton { 
                background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; 
                border-radius: 6px; font-weight: bold; 
            }
            QPushButton:hover { background-color: #fca5a5; }
        """)
        btn_clear.clicked.connect(self.on_clear_cart_clicked)

        self.lbl_total = QLabel("Total: ₱0.00")
        self.lbl_total.setStyleSheet("font-size: 26px; font-weight: 900; color: #1e293b; border: none;")

        btn_checkout = QPushButton("💳 Checkout")
        btn_checkout.setFixedWidth(150)
        btn_checkout.setFixedHeight(45)
        btn_checkout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_checkout.setStyleSheet("""
            QPushButton {
                background: #009688; color: white; border: none;
                border-radius: 6px; font-weight: bold; font-size: 15px;
            }
            QPushButton:hover { background: #00796b; }
        """)
        btn_checkout.clicked.connect(self.on_checkout_clicked)

        bottom_box.addWidget(btn_clear)
        bottom_box.addStretch()
        bottom_box.addWidget(self.lbl_total)
        bottom_box.addWidget(btn_checkout)

        layout.addLayout(bottom_box)
        self.tabs.addTab(tab, "  🛍️ My Cart  ")

    # === ORDERS TAB ===
    def init_orders_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.orders_table = QTableWidget(0, 5)
        self.orders_table.setHorizontalHeaderLabels(["DATE", "PRODUCT", "QTY", "TOTAL", "PAYMENT"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.verticalHeader().setVisible(False)
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.orders_table.setShowGrid(False)
        self.orders_table.setFrameShape(QFrame.Shape.NoFrame)
        self.orders_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.orders_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.orders_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.orders_table.verticalHeader().setDefaultSectionSize(50)
        self.orders_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0; border-radius: 8px; outline: none;
                gridline-color: transparent; background-color: white;
            }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section {
                background-color: #f8fafc; padding: 12px; border: none;
                border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b;
            }
        """)
        layout.addWidget(self.orders_table, stretch=1)

        # Pagination bar
        page_bar = QHBoxLayout()
        page_bar.setSpacing(10)

        self.orders_btn_prev = QPushButton("◀ Previous")
        self.orders_btn_prev.setFixedWidth(110)
        self.orders_btn_prev.setFixedHeight(40)
        self.orders_btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        self.orders_btn_prev.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
            QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }
        """)
        self.orders_btn_prev.clicked.connect(self._orders_prev_page)

        self.orders_lbl_page = QLabel("Page 1 of 1")
        self.orders_lbl_page.setFixedWidth(100)
        self.orders_lbl_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orders_lbl_page.setStyleSheet("font-weight: bold; color: #334155; border: none; background: transparent;")

        self.orders_btn_next = QPushButton("Next ▶")
        self.orders_btn_next.setFixedWidth(110)
        self.orders_btn_next.setFixedHeight(40)
        self.orders_btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.orders_btn_next.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
            QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }
        """)
        self.orders_btn_next.clicked.connect(self._orders_next_page)

        btn_refresh_orders = QPushButton("🔁 Refresh")
        btn_refresh_orders.setFixedWidth(110)
        btn_refresh_orders.setFixedHeight(40)
        btn_refresh_orders.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh_orders.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_refresh_orders.clicked.connect(self.refresh_orders)

        page_bar.addWidget(self.orders_btn_prev)
        page_bar.addWidget(self.orders_lbl_page)
        page_bar.addWidget(self.orders_btn_next)
        page_bar.addStretch()
        page_bar.addWidget(btn_refresh_orders)
        layout.addLayout(page_bar)

        self.tabs.addTab(tab, "  📦 My Orders  ")
        self.refresh_orders()

    # === BOOKING TAB ===
    def init_booking_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        card = QFrame()
        card.setFixedWidth(550)
        card.setStyleSheet("QFrame { background: white; border: 1px solid #cbd5e1; border-radius: 12px; }")
        cl = QVBoxLayout(card)
        cl.setSpacing(15)
        cl.setContentsMargins(40, 40, 40, 40)

        cl.addWidget(QLabel("📅 Book Service Appointment",
                            styleSheet="font-size: 20px; font-weight: bold; color: #1e293b; border:none;"))

        cl.addWidget(QLabel("Service Type:", styleSheet="border:none; font-weight:bold; color: #334155;"))
        self.service_combo = QComboBox()
        self.service_combo.setFixedHeight(45)
        self.service_combo.setStyleSheet("""
            QComboBox {
                background: white; border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 10px; padding-right: 30px; color: #334155; font-size: 14px;
            }
            QComboBox:hover { border: 1px solid #cbd5e1; }
            QComboBox:focus { border: 2px solid #009688; outline: none; }
        """)

        services = [
            "System Reformat",
            "Deep Cleaning / Dust Removal",
            "Hardware Installation",
            "Troubleshooting / Diagnostics",
            "Thermal Paste Repasting",
            "Software Installation",
            "Others (Custom Request)"
        ]
        self.service_combo.addItems(services)
        cl.addWidget(self.service_combo)

        cl.addWidget(QLabel("Preferred Date:", styleSheet="border:none; font-weight:bold; color: #334155;"))
        self.bk_date = QDateEdit()
        self.bk_date.setDate(QDate.currentDate())
        self.bk_date.setCalendarPopup(True)
        self.bk_date.setDisplayFormat("yyyy-MM-dd")
        self.bk_date.setFixedHeight(45)
        self.bk_date.setStyleSheet("""
            QDateEdit {
                background: white; border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 10px; color: #334155; font-size: 14px;
            }
            QDateEdit:focus { border: 2px solid #009688; outline: none; }
        """)
        cl.addWidget(self.bk_date)

        cl.addWidget(QLabel("Description / Notes:", styleSheet="border:none; font-weight:bold; color: #334155;"))
        self.bk_detail = QTextEdit()
        self.bk_detail.setPlaceholderText("Describe the issue or request in detail...")
        self.bk_detail.setFixedHeight(100)
        self.bk_detail.setStyleSheet("""
            QTextEdit {
                background: white; border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 10px; color: #334155; font-size: 14px;
            }
            QTextEdit:focus { border: 2px solid #009688; outline: none; }
        """)
        cl.addWidget(self.bk_detail)

        btn = QPushButton("Submit Booking")
        btn.setFixedHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #009688; color: white; border-radius: 6px;
                font-weight: bold; border: none;
            }
            QPushButton:hover { background: #00796b; }
        """)
        btn.clicked.connect(self.on_submit_booking_clicked)
        cl.addWidget(btn)

        layout.addWidget(card)
        self.tabs.addTab(tab, "  📅 Request Service  ")

    # === MY BOOKINGS TAB ===
    def init_my_bookings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.bookings_table = QTableWidget(0, 6)
        self.bookings_table.setHorizontalHeaderLabels(["SERVICE", "SCHEDULED", "DETAILS", "PRICE", "STATUS", "ACTION"])
        self.bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bookings_table.verticalHeader().setVisible(False)
        self.bookings_table.setAlternatingRowColors(True)
        self.bookings_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.bookings_table.setShowGrid(False)
        self.bookings_table.setFrameShape(QFrame.Shape.NoFrame)
        self.bookings_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.bookings_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bookings_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.bookings_table.verticalHeader().setDefaultSectionSize(60)
        self.bookings_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0; border-radius: 8px; outline: none;
                gridline-color: transparent; background-color: white;
            }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section {
                background-color: #f8fafc; padding: 12px; border: none;
                border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b;
            }
        """)
        layout.addWidget(self.bookings_table, stretch=1)

        # Pagination bar
        page_bar = QHBoxLayout()
        page_bar.setSpacing(10)

        self.bookings_btn_prev = QPushButton("◀ Previous")
        self.bookings_btn_prev.setFixedWidth(110)
        self.bookings_btn_prev.setFixedHeight(40)
        self.bookings_btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bookings_btn_prev.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
            QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }
        """)
        self.bookings_btn_prev.clicked.connect(self._bookings_prev_page)

        self.bookings_lbl_page = QLabel("Page 1 of 1")
        self.bookings_lbl_page.setFixedWidth(100)
        self.bookings_lbl_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bookings_lbl_page.setStyleSheet("font-weight: bold; color: #334155; border: none; background: transparent;")

        self.bookings_btn_next = QPushButton("Next ▶")
        self.bookings_btn_next.setFixedWidth(110)
        self.bookings_btn_next.setFixedHeight(40)
        self.bookings_btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bookings_btn_next.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
            QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }
        """)
        self.bookings_btn_next.clicked.connect(self._bookings_next_page)

        btn_refresh_bookings = QPushButton("🔁 Refresh")
        btn_refresh_bookings.setFixedWidth(110)
        btn_refresh_bookings.setFixedHeight(40)
        btn_refresh_bookings.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh_bookings.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #cbd5e1;
                border-radius: 6px; color: #475569; font-weight: bold;
            }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_refresh_bookings.clicked.connect(self.refresh_my_bookings)

        page_bar.addWidget(self.bookings_btn_prev)
        page_bar.addWidget(self.bookings_lbl_page)
        page_bar.addWidget(self.bookings_btn_next)
        page_bar.addStretch()
        page_bar.addWidget(btn_refresh_bookings)
        layout.addLayout(page_bar)

        self.tabs.addTab(tab, "  📂 My Bookings  ")
        self.refresh_my_bookings()

    # === PAGINATION HANDLERS ===
    def _orders_prev_page(self):
        if self.controller.orders_page > 0:
            self.controller.orders_page -= 1
            self.refresh_orders()

    def _orders_next_page(self):
        if self.controller.orders_page < self.controller.get_total_order_pages() - 1:
            self.controller.orders_page += 1
            self.refresh_orders()

    def _bookings_prev_page(self):
        if self.controller.bookings_page > 0:
            self.controller.bookings_page -= 1
            self.refresh_my_bookings()

    def _bookings_next_page(self):
        if self.controller.bookings_page < self.controller.get_total_bookings_pages() - 1:
            self.controller.bookings_page += 1
            self.refresh_my_bookings()

    # === ACTIONS ===
    def refresh_shop(self):
        try:
            self.shop_table.setRowCount(0)

            categories = self.controller.get_categories()
            current = self.shop_cat_filter.currentText()

            self.shop_cat_filter.blockSignals(True)
            self.shop_cat_filter.clear()
            self.shop_cat_filter.addItem("All Categories")
            self.shop_cat_filter.addItems(categories)
            if current in categories or current == "All Categories":
                self.shop_cat_filter.setCurrentText(current)
            self.shop_cat_filter.blockSignals(False)

            category = None if self.shop_cat_filter.currentText() == "All Categories" else self.shop_cat_filter.currentText()
            search = self.shop_search.text() if self.shop_search.text() else None

            products = self.controller.get_all_products(category, search)

            for row_data in products:
                pid, code, name, price, stock, cat, details = row_data
                r = self.shop_table.rowCount()
                self.shop_table.insertRow(r)
                self.shop_table.setRowHeight(r, 60)

                def make_item(val):
                    i = QTableWidgetItem(str(val))
                    i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return i

                self.shop_table.setItem(r, 0, make_item(code))
                self.shop_table.setItem(r, 1, make_item(name))
                self.shop_table.setItem(r, 2, make_item(f"₱{price:,.2f}"))

                s_text = f"{stock} available" if stock > 0 else "OUT OF STOCK"
                s_color = QColor("#10b981") if stock > 0 else QColor("#ef4444")
                s_item = QTableWidgetItem(s_text)
                s_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                s_item.setForeground(s_color)
                s_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                self.shop_table.setItem(r, 3, s_item)

                self.shop_table.setItem(r, 4, make_item(cat))

                if stock > 0:
                    qty_widget = QWidget()
                    qty_widget.setStyleSheet("background: transparent;")
                    qty_layout = QHBoxLayout(qty_widget)
                    qty_layout.setContentsMargins(5, 3, 5, 3)
                    qty_layout.setSpacing(8)
                    qty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    spin = QSpinBox()
                    spin.setRange(0, stock)
                    spin.setValue(0)
                    spin.setFixedWidth(60)
                    spin.setFixedHeight(34)
                    spin.setStyleSheet("""
                        QSpinBox {
                            background: white; border: 1px solid #cbd5e1;
                            border-radius: 5px; padding: 4px; color: #334155;
                            font-weight: bold; font-size: 13px;
                        }
                        QSpinBox:focus { border: 2px solid #009688; }
                    """)

                    btn_add = QPushButton("➕ Add to Cart")
                    btn_add.setFixedWidth(110)
                    btn_add.setFixedHeight(34)
                    btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
                    btn_add.setStyleSheet("""
                        QPushButton {
                            background: #009688; color: white; border: none;
                            border-radius: 5px; font-weight: 700; font-size: 11px; padding: 4px 6px;
                        }
                        QPushButton:hover { background: #00796b; }
                    """)
                    btn_add.clicked.connect(
                        lambda _, c=code, n=name, p=price, s=stock, sp=spin: self.add_to_cart_inline(c, n, p, s, sp))

                    qty_layout.addWidget(spin)
                    qty_layout.addWidget(btn_add)
                    self.shop_table.setCellWidget(r, 5, qty_widget)
                else:
                    label = QLabel("N/A")
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("color: #94a3b8; background: transparent; border: none;")
                    self.shop_table.setCellWidget(r, 5, label)
        except Exception as e:
            print(f"Error in refresh_shop: {e}")
            import traceback
            traceback.print_exc()

    def add_to_cart_inline(self, code, name, price, max_stock, spinner):
        qty = spinner.value()
        if qty <= 0:
            QMessageBox.warning(self, "Invalid", "Please select a quantity")
            return

        success, msg = self.controller.add_to_cart(code, name, price, max_stock, qty)
        if success:
            spinner.setValue(0)
            self.refresh_cart()
            QMessageBox.information(self, "Cart", msg)
        else:
            QMessageBox.warning(self, "Error", msg)

    def refresh_cart(self):
        self.cart_table.setRowCount(0)
        cart_items = self.controller.get_cart_items()

        for item in cart_items:
            r = self.cart_table.rowCount()
            self.cart_table.insertRow(r)
            self.cart_table.setRowHeight(r, 50)

            def make_item(val):
                i = QTableWidgetItem(str(val))
                i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                return i

            self.cart_table.setItem(r, 0, make_item(item['name']))
            self.cart_table.setItem(r, 1, make_item(f"₱{item['price']:,.2f}"))
            self.cart_table.setItem(r, 2, make_item(str(item['qty'])))
            self.cart_table.setItem(r, 3, make_item(f"₱{item['total']:,.2f}"))

            btn_remove = QPushButton("Remove")
            btn_remove.setFixedSize(90, 34)
            btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_remove.setStyleSheet("""
                QPushButton {
                    background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca;
                    border-radius: 6px; font-weight: bold; font-size: 13px;
                }
                QPushButton:hover { background: #fca5a5; color: #7f1d1d; }
            """)
            btn_remove.clicked.connect(lambda _, c=item['code']: self.remove_from_cart(c))

            w = QWidget()
            w.setStyleSheet("background: transparent;")
            l = QHBoxLayout(w)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l.setContentsMargins(0, 0, 0, 0)
            l.addWidget(btn_remove)
            self.cart_table.setCellWidget(r, 4, w)

        total_val = self.controller.get_cart_total()
        self.lbl_total.setText(f"Total: ₱{total_val:,.2f}")

    def remove_from_cart(self, code):
        self.controller.remove_from_cart(code)
        self.refresh_cart()

    def on_clear_cart_clicked(self):
        self.controller.clear_cart()
        self.refresh_cart()

    def on_checkout_clicked(self):
        if not self.controller.get_cart_items():
            QMessageBox.warning(self, "Empty Cart", "Your cart is empty")
            return

        total = self.controller.get_cart_total()
        dlg = PaymentDialog(self, total)

        if dlg.exec():
            payment_method, bank_name, account_number = dlg.get_payment_info()
            success, msg, receipt_text = self.controller.process_checkout(payment_method, bank_name, account_number)

            if success:
                receipt_dlg = ReceiptWindow(self, receipt_text)
                receipt_dlg.exec()
                self.refresh_cart()
                self.refresh_shop()
                self.refresh_orders()
            else:
                QMessageBox.critical(self, "Error", msg)

    def refresh_orders(self):
        self.orders_table.setRowCount(0)

        sales = self.controller.get_order_history_page()
        total_pages = self.controller.get_total_order_pages()
        current_page = self.controller.orders_page

        self.orders_lbl_page.setText(f"Page {current_page + 1} of {total_pages}")
        self.orders_btn_prev.setEnabled(current_page > 0)
        self.orders_btn_next.setEnabled(current_page < total_pages - 1)

        for row in sales:
            d, prod_name, qty, sub, payment = row
            r = self.orders_table.rowCount()
            self.orders_table.insertRow(r)
            self.orders_table.setRowHeight(r, 50)

            def make_item(val):
                i = QTableWidgetItem(str(val))
                i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                return i

            self.orders_table.setItem(r, 0, make_item(str(d)))
            self.orders_table.setItem(r, 1, make_item(prod_name))
            self.orders_table.setItem(r, 2, make_item(str(qty)))
            self.orders_table.setItem(r, 3, make_item(f"₱{sub:,.2f}"))
            self.orders_table.setItem(r, 4, make_item(payment))

    def on_submit_booking_clicked(self):
        service_type = self.service_combo.currentText()
        pref_date = self.bk_date.date().toString("yyyy-MM-dd")
        description = self.bk_detail.toPlainText()

        if not description:
            QMessageBox.warning(self, "Missing Info", "Please provide details about your service request")
            return

        success, msg = self.controller.book_service(service_type, pref_date, description)

        if success:
            QMessageBox.information(self, "Success", msg)
            self.bk_detail.clear()
            self.refresh_my_bookings()
        else:
            QMessageBox.critical(self, "Error", msg)

    def refresh_my_bookings(self):
        self.bookings_table.setRowCount(0)

        rows = self.controller.get_my_bookings_page()
        total_pages = self.controller.get_total_bookings_pages()
        current_page = self.controller.bookings_page

        self.bookings_lbl_page.setText(f"Page {current_page + 1} of {total_pages}")
        self.bookings_btn_prev.setEnabled(current_page > 0)
        self.bookings_btn_next.setEnabled(current_page < total_pages - 1)

        for row in rows:
            sid, submitted_date, svc_type, raw_desc, status, price = row

            scheduled_display = "TBD"
            date_match = re.search(r'\[Scheduled: (.*?)\]', raw_desc)
            if date_match:
                scheduled_display = date_match.group(1)
                raw_desc = raw_desc.replace(date_match.group(0), "").strip()

            r = self.bookings_table.rowCount()
            self.bookings_table.insertRow(r)
            self.bookings_table.setRowHeight(r, 60)

            def make_item(val):
                i = QTableWidgetItem(str(val))
                i.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                return i

            self.bookings_table.setItem(r, 0, make_item(svc_type))
            self.bookings_table.setItem(r, 1, make_item(scheduled_display))
            self.bookings_table.setItem(r, 2, make_item(raw_desc))
            self.bookings_table.setItem(r, 3, make_item(f"₱{price:,.2f}" if price > 0 else "TBD"))

            container = QWidget()
            container.setStyleSheet("background: transparent;")
            clayout = QHBoxLayout(container)
            clayout.setContentsMargins(0, 0, 0, 0)
            clayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_status = QLabel(status)
            lbl_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

            if status == "Pending":
                lbl_status.setStyleSheet("color: #f97316; background: transparent; border: none;")
            elif status == "Completed":
                lbl_status.setStyleSheet("color: #059669; background: transparent; border: none;")
            else:
                lbl_status.setStyleSheet("color: #64748b; background: transparent; border: none;")

            clayout.addWidget(lbl_status)
            self.bookings_table.setCellWidget(r, 4, container)

            if status == "Pending":
                btn = QPushButton("Cancel")
                btn.setFixedSize(90, 34)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("""
                    QPushButton {
                        background: #fee2e2; border: 1px solid #fecaca;
                        color: #b91c1c; border-radius: 6px; font-weight: bold; font-size: 13px;
                    }
                    QPushButton:hover { background: #fca5a5; color: #7f1d1d; }
                """)
                btn.clicked.connect(lambda _, x=sid: self.on_cancel_booking_clicked(x))

                w = QWidget()
                w.setStyleSheet("background: transparent;")
                wl = QHBoxLayout(w)
                wl.setContentsMargins(0, 0, 0, 0)
                wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                wl.addWidget(btn)
                self.bookings_table.setCellWidget(r, 5, w)
            else:
                dash = QWidget()
                dash.setStyleSheet("background: transparent;")
                dl = QHBoxLayout(dash)
                dl.setContentsMargins(0, 0, 0, 0)
                dl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_dash = QLabel("—")
                lbl_dash.setStyleSheet("color: #94a3b8; background: transparent; border: none;")
                dl.addWidget(lbl_dash)
                self.bookings_table.setCellWidget(r, 5, dash)

    def on_cancel_booking_clicked(self, sid):
        if QMessageBox.question(self, "Cancel", "Cancel this appointment?") == QMessageBox.StandardButton.Yes:
            self.controller.cancel_booking(sid)
            self.refresh_my_bookings()