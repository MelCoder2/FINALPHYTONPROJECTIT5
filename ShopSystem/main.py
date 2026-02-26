import sys
from PyQt6.QtWidgets import QApplication

# --- PROFESSIONAL STYLESHEET ---
STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #f1f5f9;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #1e293b;
    }

    QLabel#Header {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 5px;
    }
    QLabel#SubTitle {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 15px;
    }

    QFrame#Card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
    }

    QLineEdit, QSpinBox, QTextEdit, QDateEdit, QComboBox {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        color: #334155;
        selection-background-color: #009688;
    }
    QLineEdit:focus, QSpinBox:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
        border: 2px solid #009688;
        background-color: #f0fdfa;
    }

    QPushButton {
        background-color: #009688;
        color: white;
        border-radius: 8px;
        padding: 0 20px;
        font-weight: 600;
        font-size: 14px;
        border: none;
        height: 40px;
    }
    QPushButton:hover { background-color: #00796b; margin-top: -1px; }
    QPushButton:pressed { background-color: #004d40; margin-top: 1px; }

    QPushButton#Danger { background-color: #ef4444; }
    QPushButton#Danger:hover { background-color: #dc2626; }

    QPushButton#Secondary { 
        background-color: #ffffff;
        color: #475569; 
        border: 1px solid #cbd5e1; 
    }
    QPushButton#Secondary:hover { background-color: #f8fafc; border-color: #94a3b8; }

    QTabWidget::pane { 
        border: 1px solid #cbd5e1;
        background: #ffffff; 
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        top: -1px; 
    }
    QTabBar::tab {
        background: #e2e8f0;
        color: #64748b;
        padding: 12px 25px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-weight: 600;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        color: #009688;
        border: 1px solid #cbd5e1;
        border-bottom: 1px solid #ffffff;
    }

    QTableWidget {
        background-color: #ffffff;
        alternate-background-color: #ffffff;
        border: none;
        gridline-color: transparent;
    }
    QHeaderView::section {
        background-color: #f1f5f9;
        color: #475569;
        padding: 12px;
        font-weight: 700;
        border: none;
        border-bottom: 2px solid #e2e8f0;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.5px;
    }
    QTableWidget::item {
        padding-left: 10px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }
    QTableWidget::item:selected {
        background-color: #009688;
        color: #ffffff;            
    }
"""

if __name__ == "__main__":
    print("Starting application...")

    try:
        # Initialize database FIRST
        import database

        print("Initializing database...")
        database.initialize_db()
        print("Database initialized successfully!")

        # Create app
        app = QApplication(sys.argv)
        app.setStyleSheet(STYLESHEET)

        # Import and create login window
        print("Loading login window...")
        from views.login_view import LoginView

        window = LoginView()
        print("Login window created!")

        window.show()
        print("Application started successfully!")

        sys.exit(app.exec())

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()