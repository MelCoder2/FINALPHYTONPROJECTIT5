from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPixmap, QFont, QPainter, QPainterPath, QPen

from controllers.login_controller import LoginController
import database


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = LoginController(self)
        self.setWindowTitle("LOGIN WINDOW")
        self.showMaximized()

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f3f4f6, stop:1 #e2e8f0);
            }
            QLabel { font-family: 'Segoe UI', sans-serif; }
            QLineEdit { font-family: 'Segoe UI', sans-serif; }
            QPushButton { font-family: 'Segoe UI', sans-serif; }
        """)

        database.initialize_db()
        self.mode = 'login'

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # CARD
        self.card = QFrame()
        self.card.setFixedSize(480, 680)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #ffffff;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.card.setGraphicsEffect(shadow)

        self.cl = QVBoxLayout(self.card)
        self.cl.setSpacing(15)  # Reduced from 20
        self.cl.setContentsMargins(40, 40, 40, 40)  # Reduced top/bottom from 50

        # LOGO
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(400, 240)  # Increased from 180 to 240
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo.setStyleSheet("background: transparent; border: none;")
        self.set_rounded_logo("logo.png", 400, 240, 15)
        self.cl.addWidget(self.lbl_logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.cl.addSpacing(10)  # Reduced from 20

        # INPUTS
        input_style = """
            QLineEdit { 
                background-color: #f8fafc; 
                border: 2px solid #e2e8f0; 
                border-radius: 12px; 
                padding: 0px 15px; 
                font-size: 15px; 
                color: #334155; 
            }
            QLineEdit:focus { 
                background-color: white; 
                border: 2px solid #0d9488; 
            }
        """

        self.fn = QLineEdit()
        self.fn.setPlaceholderText("Full Name")
        self.fn.setToolTip("Enter your full name (at least 2 characters)")
        self.fn.setFixedHeight(48)  # Slightly reduced
        self.fn.setStyleSheet(input_style)
        self.fn.returnPressed.connect(self.on_auth_clicked)
        self.fn.hide()
        self.cl.addWidget(self.fn)

        self.em = QLineEdit()
        self.em.setPlaceholderText("Email (user@gmail.com)")
        self.em.setToolTip("Must be a Gmail address (e.g., user@gmail.com)")
        self.em.setFixedHeight(48)
        self.em.setStyleSheet(input_style)
        self.em.returnPressed.connect(self.on_auth_clicked)
        self.em.hide()
        self.cl.addWidget(self.em)

        self.ph = QLineEdit()
        self.ph.setPlaceholderText("Phone (09123456789)")
        self.ph.setToolTip("11-digit Philippine mobile number starting with 09")
        self.ph.setFixedHeight(48)
        self.ph.setStyleSheet(input_style)
        self.ph.returnPressed.connect(self.on_auth_clicked)
        self.ph.hide()
        self.cl.addWidget(self.ph)

        self.u = QLineEdit()
        self.u.setPlaceholderText("Username")
        self.u.setToolTip("3-20 characters, start with letter, letters/numbers/underscores only")
        self.u.setFixedHeight(50)
        self.u.setStyleSheet(input_style)
        self.u.returnPressed.connect(self.on_auth_clicked)
        self.cl.addWidget(self.u)

        self.p = QLineEdit()
        self.p.setPlaceholderText("Password")
        self.p.setToolTip("Min 8 characters: must have uppercase, lowercase, and number")
        self.p.setEchoMode(QLineEdit.EchoMode.Password)
        self.p.setFixedHeight(50)
        self.p.setStyleSheet(input_style)
        self.p.returnPressed.connect(self.on_auth_clicked)
        self.cl.addWidget(self.p)

        self.cl.addSpacing(5)  # Reduced from 10

        # BUTTONS
        self.btn = QPushButton("LOGIN")
        self.btn.setFixedHeight(55)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0d9488, stop:1 #0f766e);
                color: white; 
                font-weight: bold; 
                font-size: 16px; 
                border-radius: 12px; 
                border: none; 
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #14b8a6, stop:1 #0d9488);
            }
            QPushButton:pressed { 
                background-color: #0f172a; 
                margin-top: 2px;
            }
        """)
        self.btn.clicked.connect(self.on_auth_clicked)
        self.cl.addWidget(self.btn)

        self.toggle_btn = QPushButton("Don't have an account? Create one")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                color: #64748b; 
                font-weight: 600; 
                border: none; 
                font-size: 14px;
            }
            QPushButton:hover { 
                color: #0d9488; 
                text-decoration: underline; 
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        self.cl.addWidget(self.toggle_btn)

        self.cl.addStretch()
        layout.addWidget(self.card)

    def set_rounded_logo(self, path, width, height, radius):
        canvas = QPixmap(width, height)
        canvas.fill(Qt.GlobalColor.transparent)
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        path_rect = QRectF(0, 0, width, height)
        path_obj = QPainterPath()
        path_obj.addRoundedRect(path_rect, radius, radius)
        painter.setClipPath(path_obj)
        src_pix = QPixmap(path)
        if not src_pix.isNull():
            # Scale to fill the container while maintaining aspect ratio
            scaled_pix = src_pix.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                        Qt.TransformationMode.SmoothTransformation)
            # Center the scaled image
            x_offset = (width - scaled_pix.width()) // 2
            y_offset = (height - scaled_pix.height()) // 2
            painter.drawPixmap(x_offset, y_offset, scaled_pix)
        else:
            painter.fillRect(path_rect, QColor("#f8fafc"))
            painter.setPen(QColor("#94a3b8"))
            font = QFont("Segoe UI", 20, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(path_rect, Qt.AlignmentFlag.AlignCenter, "LOGO")
        painter.setClipping(False)
        pen = QPen(QColor("#cbd5e1"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(1, 1, width - 2, height - 2), radius, radius)
        painter.end()
        self.lbl_logo.setPixmap(canvas)

    def toggle_mode(self):
        self.u.clear()
        self.p.clear()
        self.fn.clear()
        self.em.clear()
        self.ph.clear()

        if self.mode == 'login':
            self.mode = 'register'
            self.fn.show()
            self.em.show()
            self.ph.show()
            self.btn.setText("REGISTER")
            self.toggle_btn.setText("Already have an account? Login")
            self.fn.setFocus()
            # Increase card height for register mode with smooth animation
            self.animate_card_height(780)  # Adjusted for better fit
        else:
            self.mode = 'login'
            self.fn.hide()
            self.em.hide()
            self.ph.hide()
            self.btn.setText("LOGIN")
            self.toggle_btn.setText("Don't have an account? Create one")
            self.u.setFocus()
            # Restore original height for login mode
            self.animate_card_height(680)

    def animate_card_height(self, target_height):
        """Smoothly animate the card height change"""
        self.animation = QPropertyAnimation(self.card, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.card.height())
        self.animation.setEndValue(target_height)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Also animate minimum height
        self.animation2 = QPropertyAnimation(self.card, b"minimumHeight")
        self.animation2.setDuration(300)
        self.animation2.setStartValue(self.card.height())
        self.animation2.setEndValue(target_height)
        self.animation2.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.animation.start()
        self.animation2.start()

    def on_auth_clicked(self):
        u_text = self.u.text().strip()
        p_text = self.p.text().strip()
        fn_text = self.fn.text().strip()
        em_text = self.em.text().strip()
        ph_text = self.ph.text().strip()

        if self.mode == 'login':
            success, user_data = self.controller.handle_login(u_text, p_text)
            if success:
                user_id, role, full_name, username = user_data

                # Import here to avoid circular dependency
                if role == "manager":
                    from views.manager_view import ManagerView
                    self.next_window = ManagerView()
                else:
                    from views.user_view import UserView
                    self.next_window = UserView(user_id, username, full_name)

                self.next_window.show()
                self.close()
            else:
                self.show_custom_error("Incorrect Username or Password", is_error=True)
        else:
            success, msg = self.controller.handle_register(u_text, p_text, fn_text, em_text, ph_text)
            if success:
                self.show_custom_error("Account Created! Please Login.", is_error=False)
                self.toggle_mode()
            else:
                self.show_custom_error(msg, is_error=True)

    def show_custom_error(self, message, is_error=True):
        dlg = QDialog(self)
        dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setFixedSize(400, 60)

        bg_color = "#fef2f2" if is_error else "#f0fdf4"
        border_color = "#ef4444" if is_error else "#22c55e"
        text_color = "#b91c1c" if is_error else "#15803d"
        icon_char = "✕" if is_error else "✓"

        frame.setStyleSheet(f"""
            QFrame {{ 
                background-color: {bg_color}; 
                border: 1px solid {border_color}; 
                border-radius: 12px; 
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        frame.setGraphicsEffect(shadow)

        fl = QHBoxLayout(frame)
        fl.setContentsMargins(20, 0, 20, 0)

        icon = QLabel(icon_char)
        icon.setStyleSheet(f"color: {border_color}; font-size: 20px; font-weight: 900; border: none;")

        text = QLabel(message)
        text.setStyleSheet(f"color: {text_color}; font-weight: 600; font-size: 14px; border: none;")
        text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        fl.addWidget(icon)
        fl.addSpacing(10)
        fl.addWidget(text)
        fl.addStretch()

        layout.addWidget(frame)
        QTimer.singleShot(2000, dlg.accept)
        dlg.exec()