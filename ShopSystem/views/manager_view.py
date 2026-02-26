import re
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget,
    QFrame, QLineEdit, QGridLayout, QAbstractItemView, QFileDialog,
    QComboBox, QTextEdit, QDialog, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QCursor
from controllers.manager_controller import ManagerController


class RestockDialog(QDialog):
    def __init__(self, parent, product_code, product_name, current_stock):
        super().__init__(parent)
        self.setWindowTitle("Restock Product")
        self.setFixedSize(450, 350)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(f"Restock: {product_name}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #0f172a; background: transparent; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        info_container = QWidget()
        info_container.setStyleSheet("QWidget { background: white; border: 1px solid #e2e8f0; border-radius: 12px; }")
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(15)
        info_layout.setContentsMargins(25, 25, 25, 25)

        current_label = QLabel(f"Current Stock: {current_stock} units")
        current_label.setStyleSheet("font-size: 14px; color: #64748b; background: transparent; border: none;")
        info_layout.addWidget(current_label)

        qty_label = QLabel("Add Quantity:")
        qty_label.setStyleSheet("font-weight: 700; color: #1e293b; font-size: 14px; background: transparent; border: none;")
        info_layout.addWidget(qty_label)

        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(10000)
        self.qty_input.setValue(10)
        self.qty_input.setFixedHeight(48)
        self.qty_input.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.qty_input.setStyleSheet("""
            QSpinBox {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 6px;
                padding-left: 12px;
                color: #334155;
                font-size: 16px;
                font-weight: bold;
            }
            QSpinBox:focus { border: 2px solid #009688; }
        """)
        info_layout.addWidget(self.qty_input)
        main_layout.addWidget(info_container)
        main_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(48)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton { background: white; border: 1px solid #cbd5e1; color: #475569; border-radius: 6px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background: #f1f5f9; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_confirm = QPushButton("Confirm Restock")
        btn_confirm.setFixedHeight(48)
        btn_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_confirm.setStyleSheet("""
            QPushButton { background: #009688; color: white; border: none; border-radius: 6px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background: #00796b; }
        """)
        btn_confirm.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        main_layout.addLayout(btn_layout)

    def get_quantity(self):
        return self.qty_input.value()


class StatDetailDialog(QDialog):
    def __init__(self, parent, title, content_widget):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QLabel(title)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        layout.addWidget(header)

        layout.addWidget(content_widget)

        btn_close = QPushButton("Close")
        btn_close.setFixedWidth(120)
        btn_close.setFixedHeight(40)
        btn_close.setStyleSheet("""
            QPushButton { background: #009688; color: white; border-radius: 6px; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background: #00796b; }
        """)
        btn_close.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)


class ManagerView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = ManagerController(self)
        self.setWindowTitle("Manager Window")
        self.resize(1200, 800)

        # Pagination state for Sales
        self.current_sales_page = 0
        self.sales_per_page = 10

        # Pagination state for Pending Services
        self.current_services_page = 0
        self.services_per_page = 10

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("QWidget#centralWidget { background-color: #f8fafc; }")
        central.setObjectName("centralWidget")
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # HEADER
        top = QHBoxLayout()
        tl = QVBoxLayout()
        t = QLabel("Manager Dashboard")
        t.setStyleSheet("font-size: 30px; font-weight: bold; color: #1e293b; background: none;")
        s = QLabel("Manage inventory & services.")
        s.setStyleSheet("color: #64748b; font-size: 20px; background: none;")
        tl.addWidget(t)
        tl.addWidget(s)

        self.btn_profile = QPushButton(" 👤 Store Manager")
        self.btn_profile.setStyleSheet("""
            QPushButton { background: transparent; border: none; color: #334155; font-size: 15px; font-weight: bold; }
        """)

        logout = QPushButton("➥🚪 Sign Out")
        logout.setFixedWidth(140)
        logout.setFixedHeight(40)
        logout.setStyleSheet("""
            QPushButton { background: #fee2e2; border: 1px solid #fecaca; border-radius: 6px; padding: 8px; color: #b91c1c; font-weight: bold; font-size: 14px; }
            QPushButton:hover { background: #fca5a5; color: #7f1d1d; border-color: #fca5a5; }
        """)
        logout.clicked.connect(self.on_logout_clicked)

        top.addLayout(tl)
        top.addStretch()
        top.addWidget(self.btn_profile)
        top.addWidget(logout)
        main_layout.addLayout(top)

        # CLICKABLE STATS
        stats = QHBoxLayout()
        stats.setSpacing(20)

        self.c1, self.l1 = self.stat_card("💰 Total Revenue", "#10b981", self.show_revenue_details)
        self.c2, self.l2 = self.stat_card("🧾 Total Orders", "#3b82f6", self.show_orders_details)
        self.c3, self.l3 = self.stat_card("📦 Stock Count", "#f59e0b", self.show_stock_details)
        self.c4, self.l4 = self.stat_card("👥 Customers", "#8b5cf6", self.show_customers_details)

        stats.addWidget(self.c1)
        stats.addWidget(self.c2)
        stats.addWidget(self.c3)
        stats.addWidget(self.c4)
        main_layout.addLayout(stats)

        # TABS
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #e2e8f0; background: white; border-radius: 8px; }
            QTabBar::tab { background: #e2e8f0; padding: 10px 20px; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; font-weight: bold; color: #64748b; }
            QTabBar::tab:selected { background: white; color: #0f172a; border-bottom: none; }
            QTabWidget > QWidget { background-color: #f8fafc; }
        """)
        main_layout.addWidget(self.tabs)

        self.init_inventory_tab()
        self.init_services_tab()
        self.init_history_tab()
        self.init_sales_tab()

        QTimer.singleShot(100, self.refresh_all)

    def stat_card(self, title, color, click_handler):
        f = QFrame()
        f.setStyleSheet(f"""
            QFrame {{ background-color: white; border-radius: 12px; border: 1px solid #cbd5e1; border-left: 5px solid {color}; }}
            QFrame:hover {{ background-color: #f8fafc; border: 1px solid #94a3b8; border-left: 5px solid {color}; }}
        """)
        f.setFixedHeight(100)
        f.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        f.mousePressEvent = lambda event: click_handler()

        l = QVBoxLayout(f)
        l.setContentsMargins(20, 15, 20, 15)

        t = QLabel(title)
        t.setStyleSheet("color: #64748b; font-weight: bold; border:none; background:transparent;")

        v = QLabel("0")
        v.setStyleSheet("color: #1e293b; font-size: 28px; font-weight: 900; border:none; background:transparent;")

        l.addWidget(t)
        l.addWidget(v)

        return f, v

    def _make_stat_table(self, headers, color="#009688"):
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setShowGrid(False)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                outline: none;
                gridline-color: transparent;
            }
            QTableWidget::item { border: none; padding: 10px; }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                color: #1e293b;
            }
        """)
        return table

    def _make_search_bar(self, placeholder="🔍 Search..."):
        search_input = QLineEdit()
        search_input.setPlaceholderText(placeholder)
        search_input.setFixedHeight(40)
        search_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #009688; outline: none; }
        """)
        return search_input

    def _make_page_controls(self, lbl_attr, prev_slot, next_slot, export_slot=None, export_label="📄 Export PDF"):
        """Helper to build a reusable pagination + optional export button row."""
        btn_style = """
            QPushButton { background: white; border: 1px solid #cbd5e1; border-radius: 6px; color: #475569; font-weight: bold; }
            QPushButton:hover { background: #f1f5f9; }
            QPushButton:disabled { background: #f8fafc; color: #cbd5e1; }
        """
        layout = QHBoxLayout()

        btn_prev = QPushButton("◀ Previous")
        btn_prev.setFixedWidth(120)
        btn_prev.setFixedHeight(40)
        btn_prev.setStyleSheet(btn_style)
        btn_prev.clicked.connect(prev_slot)

        lbl = QLabel("Page 1 of 1")
        lbl.setStyleSheet("font-weight: bold; color: #334155; border: none;")
        setattr(self, lbl_attr, lbl)

        btn_next = QPushButton("Next ▶")
        btn_next.setFixedWidth(120)
        btn_next.setFixedHeight(40)
        btn_next.setStyleSheet(btn_style)
        btn_next.clicked.connect(next_slot)

        layout.addWidget(btn_prev)
        layout.addWidget(lbl)
        layout.addWidget(btn_next)
        layout.addStretch()

        if export_slot:
            bp = QPushButton(export_label)
            bp.setFixedWidth(150)
            bp.setFixedHeight(40)
            bp.setStyleSheet("""
                QPushButton { background: #009688; color: white; border-radius: 6px; font-weight: bold; }
                QPushButton:hover { background: #00796b; }
            """)
            bp.clicked.connect(export_slot)
            layout.addWidget(bp)

        return layout, btn_prev, btn_next

    # ------------------------------------------------------------------ #
    #  STAT DETAIL DIALOGS
    # ------------------------------------------------------------------ #

    def show_revenue_details(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        summary = QLabel("Revenue Breakdown")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        table = self._make_stat_table(["Source", "Amount", "Percentage"])
        breakdown = self.controller.get_revenue_breakdown()
        total_revenue = sum(amount for _, amount in breakdown)

        for source, amount in breakdown:
            row = table.rowCount()
            table.insertRow(row)
            table.setRowHeight(row, 50)
            percentage = (amount / total_revenue * 100) if total_revenue > 0 else 0
            for col, val in enumerate([source, f"₱{amount:,.2f}", f"{percentage:.1f}%"]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)

        layout.addWidget(table)
        total_label = QLabel(f"Total Revenue: ₱{total_revenue:,.2f}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #10b981; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "💰 Revenue Details", content)
        dialog.exec()

    def show_orders_details(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        summary = QLabel("Orders Overview")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        table = self._make_stat_table(["Category", "Count", "Percentage"])
        breakdown = self.controller.get_orders_breakdown()
        total_orders = sum(count for _, count in breakdown)

        for category, count in breakdown:
            row = table.rowCount()
            table.insertRow(row)
            table.setRowHeight(row, 50)
            percentage = (count / total_orders * 100) if total_orders > 0 else 0
            for col, val in enumerate([category, str(count), f"{percentage:.1f}%"]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)

        layout.addWidget(table)
        total_label = QLabel(f"Total Orders: {total_orders}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3b82f6; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "🧾 Orders Details", content)
        dialog.exec()

    def show_stock_details(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        summary = QLabel("Inventory Status - All Products")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        search_input = self._make_search_bar("🔍 Search products...")
        layout.addWidget(search_input)

        table = self._make_stat_table(["Category", "Product Name", "Code", "Stock"])
        products = self.controller.get_all_products()
        all_product_data = [(p[5], p[2], p[1], p[4]) for p in products]

        def populate_table(search_text=""):
            table.setRowCount(0)
            filtered = [
                (cat, name, code, stock) for cat, name, code, stock in all_product_data
                if search_text.lower() in name.lower()
                or search_text.lower() in code.lower()
                or search_text.lower() in cat.lower()
            ]
            filtered.sort(key=lambda x: (x[0], x[1]))
            for cat, name, code, stock in filtered:
                row = table.rowCount()
                table.insertRow(row)
                table.setRowHeight(row, 50)
                cat_item = QTableWidgetItem(cat)
                cat_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, 0, cat_item)
                for col, val in enumerate([name, code], start=1):
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, col, item)
                stock_item = QTableWidgetItem(str(stock))
                stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if stock <= 5:
                    stock_item.setForeground(QColor("#ef4444"))
                    stock_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                else:
                    stock_item.setForeground(QColor("#10b981"))
                table.setItem(row, 3, stock_item)

        search_input.textChanged.connect(populate_table)
        populate_table()
        layout.addWidget(table)

        total_stock = sum([p[4] for p in products])
        low_stock_count = len([p for p in products if p[4] <= 5])
        total_label = QLabel(f"Total Stock Units: {total_stock} | Low Stock Items: {low_stock_count}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f59e0b; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "📦 Stock Details", content)
        dialog.exec()

    def show_customers_details(self):
        content = QWidget()
        layout = QVBoxLayout(content)

        summary = QLabel("Customer Activity")
        summary.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(summary)

        search_input = self._make_search_bar("🔍 Search customers...")
        layout.addWidget(search_input)

        table = self._make_stat_table(["Customer", "Total Orders", "Total Spent"])

        all_registered = self.controller.get_all_customers()
        customers = {}
        for customer_data in all_registered:
            full_name = customer_data[0]
            customers[full_name] = {"orders": 0, "spent": 0}

        for sale in self.controller.get_all_sales():
            date, cust, item, qty, total, payment, bank = sale
            if cust not in customers:
                customers[cust] = {"orders": 0, "spent": 0}
            customers[cust]["orders"] += 1
            customers[cust]["spent"] += total

        import database
        all_services = database.get_all_services_joined()
        for service in all_services:
            sid, cust, svc_type, desc, status, price = service
            if status == "Completed":
                if cust not in customers:
                    customers[cust] = {"orders": 0, "spent": 0}
                customers[cust]["orders"] += 1
                customers[cust]["spent"] += price

        all_customer_data = sorted(customers.items(), key=lambda x: (-x[1]["spent"], x[0]))

        def populate_table(search_text=""):
            table.setRowCount(0)
            filtered = [
                (customer, data) for customer, data in all_customer_data
                if search_text.lower() in customer.lower()
            ]
            for customer, data in filtered:
                row = table.rowCount()
                table.insertRow(row)
                table.setRowHeight(row, 50)
                for col, val in enumerate([customer, str(data["orders"]), f"₱{data['spent']:,.2f}"]):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, col, item)

        search_input.textChanged.connect(populate_table)
        populate_table()
        layout.addWidget(table)

        total_label = QLabel(f"Total Unique Customers: {len(customers)}")
        total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #8b5cf6; margin-top: 20px;")
        layout.addWidget(total_label)

        dialog = StatDetailDialog(self, "👥 Customer Details", content)
        dialog.exec()

    def on_logout_clicked(self):
        from views.login_view import LoginView
        self.login_window = LoginView()
        self.login_window.show()
        self.close()

    # ------------------------------------------------------------------ #
    #  INVENTORY TAB
    # ------------------------------------------------------------------ #

    def init_inventory_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)
        l.setSpacing(20)

        c = QFrame()
        c.setStyleSheet("QFrame { background: white; border: 1px solid #cbd5e1; border-radius: 12px; }")
        cl = QVBoxLayout(c)
        cl.setContentsMargins(20, 20, 20, 20)

        g = QGridLayout()
        g.setVerticalSpacing(15)
        g.setHorizontalSpacing(20)

        self.ic = QLineEdit()
        self.ic.setPlaceholderText("Auto")
        self.ic.setReadOnly(True)
        self.ic.setStyleSheet("""
            QLineEdit {
                background-color: #e0f2f1; color: #00796b; border: 0px;
                border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px;
            }
            QLineEdit:focus { border: 0px; outline: none; }
        """)

        self.inm = QLineEdit(placeholderText="Name")
        self.ip = QLineEdit(placeholderText="0.00")

        self.is_ = QSpinBox()
        self.is_.setMinimum(1)
        self.is_.setMaximum(10000)
        self.is_.setValue(1)
        self.is_.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.is_.setStyleSheet("""
            QSpinBox {
                background-color: white; border: 1px solid #e2e8f0;
                border-radius: 6px; padding-left: 10px; color: #334155; font-size: 14px;
            }
            QSpinBox:focus { background-color: white; border: 2px solid #009688; outline: none; }
        """)

        self.icat = QComboBox()
        self.icat.addItems(["CPU", "GPU", "RAM", "Storage", "Motherboard", "PSU", "Case", "Cooling", "Peripherals", "Other"])
        self.icat.setStyleSheet("""
            QComboBox {
                background-color: white; border: 1px solid #e2e8f0;
                border-radius: 6px; padding: 10px; padding-right: 30px; color: #334155; font-size: 14px;
            }
            QComboBox:hover { border: 1px solid #cbd5e1; }
            QComboBox:focus { background-color: white; border: 2px solid #009688; outline: none; }
        """)

        input_style = """
            QLineEdit {
                background-color: white; border: 1px solid #e2e8f0;
                border-radius: 6px; padding: 10px; color: #334155; font-size: 14px;
            }
            QLineEdit:focus { background-color: white; border: 2px solid #009688; outline: none; }
        """

        for w in [self.inm, self.ip]:
            w.setFixedHeight(45)
            w.setStyleSheet(input_style)

        self.icat.setFixedHeight(45)
        self.icat.setFixedWidth(200)
        self.ic.setFixedHeight(45)
        self.is_.setFixedHeight(45)

        lbl_style = "background-color: transparent; font-weight: bold; color: #1e293b; border: none;"

        g.addWidget(QLabel("Code:", styleSheet=lbl_style), 0, 0)
        g.addWidget(self.ic, 1, 0)
        g.addWidget(QLabel("Name:", styleSheet=lbl_style), 0, 1)
        g.addWidget(self.inm, 1, 1)
        g.addWidget(QLabel("Price:", styleSheet=lbl_style), 0, 2)
        g.addWidget(self.ip, 1, 2)
        g.addWidget(QLabel("Stock:", styleSheet=lbl_style), 0, 3)
        g.addWidget(self.is_, 1, 3)
        g.addWidget(QLabel("Category:", styleSheet=lbl_style), 0, 4)
        g.addWidget(self.icat, 1, 4)

        btn = QPushButton("➕ Add Product", cursor=Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(40)
        btn.setFixedWidth(150)
        btn.setStyleSheet("background-color: #009688; color: white; border-radius: 6px; font-weight: bold; font-size: 14px; border: none;")
        btn.clicked.connect(self.on_add_product_clicked)
        g.addWidget(btn, 1, 5)

        cl.addLayout(g)
        l.addWidget(c)

        # FILTER BAR
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(15)
        filter_bar.addWidget(QLabel("Filter:", styleSheet="font-weight: bold; color: #334155; font-size: 14px; border: none;"))

        self.filter_cat = QComboBox()
        self.filter_cat.addItem("All Categories")
        self.filter_cat.setFixedHeight(45)
        self.filter_cat.setStyleSheet("""
            QComboBox {
                background: white; border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 10px; padding-right: 30px; min-width: 180px; font-size: 14px; color: #334155;
            }
            QComboBox:hover { border: 1px solid #cbd5e1; }
            QComboBox:focus { border: 2px solid #009688; outline: none; }
        """)
        self.filter_cat.currentTextChanged.connect(self.refresh_inventory)
        filter_bar.addWidget(self.filter_cat)

        self.filter_search = QLineEdit()
        self.filter_search.setPlaceholderText("🔍 Search products...")
        self.filter_search.setFixedWidth(350)
        self.filter_search.setFixedHeight(45)
        self.filter_search.setStyleSheet("""
            QLineEdit {
                background: white; border: 1px solid #e2e8f0;
                border-radius: 6px; padding: 10px; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #009688; outline: none; }
        """)
        self.filter_search.textChanged.connect(self.refresh_inventory)
        filter_bar.addWidget(self.filter_search)
        filter_bar.addStretch()
        l.addLayout(filter_bar)

        self.inv_t = QTableWidget(0, 6)
        self.inv_t.setHorizontalHeaderLabels(["CODE", "NAME", "PRICE", "STOCK", "CATEGORY", "ACTION"])
        self.inv_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inv_t.setAlternatingRowColors(True)
        self.inv_t.verticalHeader().setVisible(False)
        self.inv_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inv_t.setShowGrid(False)
        self.inv_t.setFrameShape(QFrame.Shape.NoFrame)
        self.inv_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.inv_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.inv_t.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 8px; outline: none; gridline-color: transparent; background-color: white; }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b; }
            QLabel { border: none; outline: none; }
        """)
        l.addWidget(self.inv_t)
        self.tabs.addTab(tab, " 📦 Inventory ")

    def on_add_product_clicked(self):
        next_code = self.controller.get_next_product_code()
        if self.ic.text() and self.ic.text() != "Auto":
            next_code = self.ic.text()

        success, msg = self.controller.add_product(
            next_code, self.inm.text(), self.ip.text(),
            str(self.is_.value()), self.icat.currentText(), ""
        )

        if success:
            self.inm.clear()
            self.ip.clear()
            self.is_.setValue(1)
            self.refresh_all()
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.warning(self, "Error", msg)

    # ------------------------------------------------------------------ #
    #  PENDING SERVICES TAB
    # ------------------------------------------------------------------ #

    def init_services_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)
        l.setSpacing(15)

        self.srv_t = QTableWidget(0, 7)
        self.srv_t.setHorizontalHeaderLabels(["CUSTOMER", "SERVICE TYPE", "DETAILS", "TOTAL", "STATUS", "", ""])
        self.srv_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.srv_t.setAlternatingRowColors(True)
        self.srv_t.verticalHeader().setVisible(False)
        self.srv_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.srv_t.setWordWrap(True)
        self.srv_t.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.srv_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.srv_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.srv_t.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 8px; outline: none; gridline-color: transparent; background-color: white; }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b; }
        """)
        l.addWidget(self.srv_t, stretch=1)

        # Pagination + Refresh
        page_layout, self.srv_btn_prev, self.srv_btn_next = self._make_page_controls(
            "lbl_srv_page",
            self.prev_services_page,
            self.next_services_page
        )

        br = QPushButton("🔁 Refresh")
        br.setFixedWidth(150)
        br.setFixedHeight(40)
        br.setStyleSheet("""
            QPushButton { background: white; border: 1px solid #cbd5e1; border-radius: 6px; color: #475569; font-weight: bold; }
            QPushButton:hover { background: #f1f5f9; }
        """)
        br.clicked.connect(self.refresh_all)
        page_layout.addWidget(br)

        l.addLayout(page_layout)
        self.tabs.addTab(tab, " 🛠️ Pending Services ")

    def prev_services_page(self):
        if self.current_services_page > 0:
            self.current_services_page -= 1
            self.refresh_services()

    def next_services_page(self):
        total_pages = self._get_total_services_pages()
        if self.current_services_page < total_pages - 1:
            self.current_services_page += 1
            self.refresh_services()

    def _get_total_services_pages(self):
        all_services = self.controller.get_all_services()
        pending = [s for s in all_services if s[4] != "Completed"]
        total = len(pending)
        return max(1, (total + self.services_per_page - 1) // self.services_per_page)

    # ------------------------------------------------------------------ #
    #  COMPLETED SERVICES (HISTORY) TAB
    # ------------------------------------------------------------------ #

    def init_history_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)
        l.setSpacing(15)

        self.hist_t = QTableWidget(0, 6)
        self.hist_t.setHorizontalHeaderLabels(["COMPLETED", "CUSTOMER", "SERVICE", "STATUS", "TOTAL", "STARTED"])
        self.hist_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.hist_t.setAlternatingRowColors(True)
        self.hist_t.verticalHeader().setVisible(False)
        self.hist_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.hist_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.hist_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.hist_t.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 8px; outline: none; gridline-color: transparent; background-color: white; }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b; }
        """)
        self.hist_t.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.hist_t.verticalHeader().setDefaultSectionSize(50)
        l.addWidget(self.hist_t, stretch=1)

        page_layout, self.btn_prev, self.btn_next = self._make_page_controls(
            "lbl_page",
            self.prev_page,
            self.next_page,
            export_slot=self.on_export_history_clicked
        )
        l.addLayout(page_layout)
        self.tabs.addTab(tab, " 📜 Completed Services ")

    def prev_page(self):
        if self.controller.current_history_page > 0:
            self.controller.current_history_page -= 1
            self.refresh_history()

    def next_page(self):
        total_pages = self.controller.get_total_history_pages()
        if self.controller.current_history_page < total_pages - 1:
            self.controller.current_history_page += 1
            self.refresh_history()

    # ------------------------------------------------------------------ #
    #  SALES REPORT TAB
    # ------------------------------------------------------------------ #

    def init_sales_tab(self):
        tab = QWidget()
        l = QVBoxLayout(tab)
        l.setContentsMargins(30, 30, 30, 30)
        l.setSpacing(15)

        self.sal_t = QTableWidget(0, 7)
        self.sal_t.setHorizontalHeaderLabels(["DATE", "CUSTOMER", "ITEM", "QTY", "TOTAL", "PAYMENT", "BANK"])
        self.sal_t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sal_t.setAlternatingRowColors(True)
        self.sal_t.verticalHeader().setVisible(False)
        self.sal_t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sal_t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.sal_t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sal_t.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.sal_t.verticalHeader().setDefaultSectionSize(50)
        self.sal_t.setStyleSheet("""
            QTableWidget { border: 1px solid #e2e8f0; border-radius: 8px; outline: none; gridline-color: transparent; background-color: white; }
            QTableWidget::item { border: none; outline: none; padding: 8px; }
            QHeaderView::section { background-color: #f8fafc; padding: 12px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #1e293b; }
        """)
        l.addWidget(self.sal_t, stretch=1)

        page_layout, self.sal_btn_prev, self.sal_btn_next = self._make_page_controls(
            "lbl_sal_page",
            self.prev_sales_page,
            self.next_sales_page,
            export_slot=self.on_export_sales_clicked
        )
        l.addLayout(page_layout)
        self.tabs.addTab(tab, " 💰 Sales Report ")

    def prev_sales_page(self):
        if self.current_sales_page > 0:
            self.current_sales_page -= 1
            self.refresh_sales()

    def next_sales_page(self):
        total_pages = self._get_total_sales_pages()
        if self.current_sales_page < total_pages - 1:
            self.current_sales_page += 1
            self.refresh_sales()

    def _get_total_sales_pages(self):
        total = len(self.controller.get_all_sales())
        return max(1, (total + self.sales_per_page - 1) // self.sales_per_page)

    # ------------------------------------------------------------------ #
    #  ACTION HANDLERS
    # ------------------------------------------------------------------ #

    def on_restock_product_clicked(self, pid):
        products = self.controller.get_all_products()
        product = next((p for p in products if p[0] == pid), None)
        if not product:
            QMessageBox.warning(self, "Error", "Product not found")
            return

        _, code, name, price, current_stock, cat, details = product
        dialog = RestockDialog(self, code, name, current_stock)

        if dialog.exec():
            qty = dialog.get_quantity()
            success, msg = self.controller.restock_product(pid, qty)
            if success:
                self.refresh_all()
                QMessageBox.information(self, "Success", f"Added {qty} units to {name}")
            else:
                QMessageBox.warning(self, "Error", msg)

    def on_delete_product_clicked(self, pid):
        if QMessageBox.question(self, "Confirm", "Delete this product?") == QMessageBox.StandardButton.Yes:
            self.controller.delete_product(pid)
            self.refresh_all()

    def on_mark_complete_clicked(self, sid):
        if QMessageBox.question(self, "Confirm", "Mark as Completed?") == QMessageBox.StandardButton.Yes:
            self.controller.mark_service_complete(sid)
            self.refresh_all()

    def on_delete_service_clicked(self, sid):
        if QMessageBox.question(self, "Confirm", "Delete this record?") == QMessageBox.StandardButton.Yes:
            self.controller.delete_service(sid)
            self.refresh_all()

    def on_export_sales_clicked(self):
        try:
            headers = ["Date", "Customer", "Item", "Qty", "Total", "Payment", "Bank"]
            data = self.controller.get_all_sales()
            fn, _ = QFileDialog.getSaveFileName(self, "Export", "Sales_Report.pdf", "PDF (*.pdf)")
            if fn:
                success, msg = self.controller.export_to_pdf("Sales Report", headers, data, fn)
                if success:
                    QMessageBox.information(self, "Saved", msg)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def on_export_history_clicked(self):
        try:
            raw_data = self.controller.get_completed_services()
            formatted_data = [[row[5], row[1], row[2], "Completed", f"₱{row[6]:,.2f}", row[4]] for row in raw_data]
            headers = ["Date Completed", "Customer", "Service", "Status", "Total", "Date Started"]
            fn, _ = QFileDialog.getSaveFileName(self, "Export", "History.pdf", "PDF (*.pdf)")
            if fn:
                success, msg = self.controller.export_to_pdf("Service History", headers, formatted_data, fn)
                if success:
                    QMessageBox.information(self, "Saved", msg)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ------------------------------------------------------------------ #
    #  REFRESH METHODS
    # ------------------------------------------------------------------ #

    def refresh_all(self):
        self.refresh_stats()
        self.refresh_inventory()
        self.refresh_services()
        self.refresh_history()
        self.refresh_sales()

        categories = self.controller.get_categories()
        current_text = self.filter_cat.currentText()
        self.filter_cat.blockSignals(True)
        self.filter_cat.clear()
        self.filter_cat.addItem("All Categories")
        self.filter_cat.addItems(categories)
        if current_text in categories or current_text == "All Categories":
            self.filter_cat.setCurrentText(current_text)
        self.filter_cat.blockSignals(False)

    def refresh_stats(self):
        try:
            rev, orders, stk, custs = self.controller.get_stats()
            self.l1.setText(f"₱{rev:,.2f}")
            self.l2.setText(str(orders))
            self.l3.setText(str(stk))
            self.l4.setText(str(custs))
            self.ic.setText(self.controller.get_next_product_code())
        except Exception as e:
            print("Stats Error:", e)

    def refresh_inventory(self):
        try:
            category = None if self.filter_cat.currentText() == "All Categories" else self.filter_cat.currentText()
            search = self.filter_search.text() if self.filter_search.text() else None
            products = self.controller.get_all_products(category, search)
            self.inv_t.setRowCount(0)

            for row_data in products:
                pid, code, name, price, stock, cat, details = row_data
                r = self.inv_t.rowCount()
                self.inv_t.insertRow(r)
                self.inv_t.setRowHeight(r, 70)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.inv_t.setItem(r, 0, make_item(code))
                self.inv_t.setItem(r, 1, make_item(name))
                self.inv_t.setItem(r, 2, make_item(f"₱{price:,.2f}"))

                st = make_item(str(stock))
                st.setForeground(QColor("#ef4444") if stock == 0 else QColor("#10b981"))
                st.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                self.inv_t.setItem(r, 3, st)
                self.inv_t.setItem(r, 4, make_item(cat))

                action_widget = QWidget()
                action_widget.setStyleSheet("background: transparent;")
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(5, 0, 5, 0)
                action_layout.setSpacing(5)
                action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                btn_restock = QPushButton("Restock")
                btn_restock.setFixedSize(110, 34)
                btn_restock.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_restock.setStyleSheet("""
                    QPushButton { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; border-radius: 6px; font-weight: bold; font-size: 13px; }
                    QPushButton:hover { background: #a7f3d0; color: #064e3b; }
                """)
                btn_restock.clicked.connect(lambda _, x=pid: self.on_restock_product_clicked(x))
                action_layout.addWidget(btn_restock)

                bd = QPushButton("Delete")
                bd.setFixedSize(110, 34)
                bd.setCursor(Qt.CursorShape.PointingHandCursor)
                bd.setStyleSheet("""
                    QPushButton { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 6px; font-weight: bold; font-size: 13px; }
                    QPushButton:hover { background: #fca5a5; color: #7f1d1d; }
                """)
                bd.clicked.connect(lambda _, x=pid: self.on_delete_product_clicked(x))
                action_layout.addWidget(bd)

                self.inv_t.setCellWidget(r, 5, action_widget)

        except Exception as e:
            print(f"Inventory Error: {e}")
            import traceback
            traceback.print_exc()

    def refresh_services(self):
        try:
            all_services = self.controller.get_all_services()
            pending = [s for s in all_services if s[4] != "Completed"]

            total_pages = self._get_total_services_pages()
            self.lbl_srv_page.setText(f"Page {self.current_services_page + 1} of {total_pages}")
            self.srv_btn_prev.setEnabled(self.current_services_page > 0)
            self.srv_btn_next.setEnabled(self.current_services_page < total_pages - 1)

            # Slice for current page
            start = self.current_services_page * self.services_per_page
            end = start + self.services_per_page
            page_services = pending[start:end]

            self.srv_t.setRowCount(0)

            for row_data in page_services:
                sid, cust, svc_type, raw_desc, status, price = row_data
                r = self.srv_t.rowCount()
                self.srv_t.insertRow(r)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    return it

                self.srv_t.setItem(r, 0, make_item(cust))
                self.srv_t.setItem(r, 1, make_item(svc_type))

                details_item = QTableWidgetItem(raw_desc)
                details_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                details_item.setFlags(details_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.srv_t.setItem(r, 2, details_item)
                self.srv_t.setItem(r, 3, make_item(f"₱{price:,.2f}"))

                status_container = QWidget()
                status_container.setStyleSheet("background: transparent;")
                status_layout = QHBoxLayout(status_container)
                status_layout.setContentsMargins(0, 0, 0, 0)
                status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_status = QLabel(status)
                lbl_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                lbl_status.setStyleSheet("QLabel { color: #f97316; background: transparent; border: none; }")
                status_layout.addWidget(lbl_status)
                self.srv_t.setCellWidget(r, 4, status_container)

                b = QPushButton("Complete")
                b.setFixedSize(110, 34)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setStyleSheet("""
                    QPushButton { background-color: #d1fae5; color: #047857; border: 1px solid #a7f3d0; border-radius: 6px; font-weight: bold; font-size: 13px; }
                    QPushButton:hover { background-color: #a7f3d0; color: #065f46; }
                """)
                b.clicked.connect(lambda _, x=sid: self.on_mark_complete_clicked(x))
                w = QWidget()
                wl = QHBoxLayout(w)
                wl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                wl.setContentsMargins(0, 0, 0, 0)
                wl.addWidget(b)
                w.setStyleSheet("background:transparent;")
                self.srv_t.setCellWidget(r, 5, w)

                bd = QPushButton("Delete")
                bd.setFixedSize(110, 34)
                bd.setCursor(Qt.CursorShape.PointingHandCursor)
                bd.setStyleSheet("""
                    QPushButton { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 6px; font-weight: bold; font-size: 13px; }
                    QPushButton:hover { background: #fca5a5; color: #7f1d1d; }
                """)
                bd.clicked.connect(lambda _, x=sid: self.on_delete_service_clicked(x))
                w2 = QWidget()
                l2 = QHBoxLayout(w2)
                l2.setAlignment(Qt.AlignmentFlag.AlignCenter)
                l2.setContentsMargins(0, 0, 0, 0)
                l2.addWidget(bd)
                w2.setStyleSheet("background:transparent;")
                self.srv_t.setCellWidget(r, 6, w2)

        except Exception as e:
            print("Services Error:", e)

    def refresh_sales(self):
        try:
            all_sales = self.controller.get_all_sales()
            total_pages = self._get_total_sales_pages()

            self.lbl_sal_page.setText(f"Page {self.current_sales_page + 1} of {total_pages}")
            self.sal_btn_prev.setEnabled(self.current_sales_page > 0)
            self.sal_btn_next.setEnabled(self.current_sales_page < total_pages - 1)

            # Slice for current page
            start = self.current_sales_page * self.sales_per_page
            end = start + self.sales_per_page
            page_sales = all_sales[start:end]

            self.sal_t.setRowCount(0)

            for row_data in page_sales:
                date, cust, item, qty, total, payment, bank = row_data
                r = self.sal_t.rowCount()
                self.sal_t.insertRow(r)

                def make_item(text):
                    it = QTableWidgetItem(str(text) if text else "N/A")
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.sal_t.setItem(r, 0, make_item(str(date)))
                self.sal_t.setItem(r, 1, make_item(cust))
                self.sal_t.setItem(r, 2, make_item(item))
                self.sal_t.setItem(r, 3, make_item(str(qty)))
                self.sal_t.setItem(r, 4, make_item(f"₱{total:,.2f}"))
                self.sal_t.setItem(r, 5, make_item(payment))
                self.sal_t.setItem(r, 6, make_item(bank if bank else "N/A"))

        except Exception as e:
            print("Sales Error:", e)

    def refresh_history(self):
        try:
            history = self.controller.get_completed_services(self.controller.current_history_page)
            total_pages = self.controller.get_total_history_pages()
            self.lbl_page.setText(f"Page {self.controller.current_history_page + 1} of {total_pages}")
            self.btn_prev.setEnabled(self.controller.current_history_page > 0)
            self.btn_next.setEnabled(self.controller.current_history_page < total_pages - 1)

            self.hist_t.setRowCount(0)

            for row in history:
                sid, cname, svc_type, desc, start, end, price = row
                r = self.hist_t.rowCount()
                self.hist_t.insertRow(r)
                self.hist_t.setRowHeight(r, 50)

                def make_item(text):
                    it = QTableWidgetItem(str(text))
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    return it

                self.hist_t.setItem(r, 0, make_item(str(end)))
                self.hist_t.setItem(r, 1, make_item(cname))
                self.hist_t.setItem(r, 2, make_item(svc_type))

                container = QWidget()
                container.setStyleSheet("background: transparent;")
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_status = QLabel("Completed")
                lbl_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                lbl_status.setStyleSheet("QLabel { color: #059669; background: transparent; border: none; }")
                layout.addWidget(lbl_status)
                self.hist_t.setCellWidget(r, 3, container)

                self.hist_t.setItem(r, 4, make_item(f"₱{price:,.2f}"))
                self.hist_t.setItem(r, 5, make_item(str(start)))

        except Exception as e:
            print("History Error:", e)