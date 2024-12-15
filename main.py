from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = {}  # Format: {link: {"description": desc, "price": price}}
        self.is_dark_mode = False  # Variable to track the mode
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SAFEHOME")
        self.setGeometry(100, 100, 800, 600)

        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("SAFEHOME")
        title.setFont(QFont("Helvetica", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title)

        # Input fields layout
        input_layout = QVBoxLayout()

        # Link Input
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("ჩაწერეთ ლინკი")
        self.link_input.setFont(QFont("Helvetica", 12))
        self.link_input.setStyleSheet("background-color: #F1F8E9; color: #333333; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("ლინკი:"))
        input_layout.addWidget(self.link_input)

        # Description Input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("ჩაწერეთ აღწერა")
        self.description_input.setFont(QFont("Helvetica", 12))
        self.description_input.setStyleSheet("background-color: #F1F8E9; color: #333333; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("აღწერა:"))
        input_layout.addWidget(self.description_input)

        # Price Input
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("ჩაწერეთ ფასი (არასავალდებულო)")
        self.price_input.setFont(QFont("Helvetica", 12))
        self.price_input.setStyleSheet("background-color: #F1F8E9; color: #333333; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("ფასი:"))
        input_layout.addWidget(self.price_input)

        main_layout.addLayout(input_layout)

        # Buttons layout with animation
        button_layout = QHBoxLayout()

        add_button = QPushButton("დავალების დამატება")
        add_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        add_button.setFixedHeight(40)
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        process_button = QPushButton("დავალებების შესრულება")
        process_button.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        process_button.setFixedHeight(40)
        process_button.clicked.connect(self.process_tasks)
        button_layout.addWidget(process_button)

        # Dark/Light mode toggle button
        toggle_button = QPushButton("ბნელი/ნათელი რეჟიმი")
        toggle_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 20px; padding: 10px; font-size: 14px;")
        toggle_button.setFixedHeight(40)
        toggle_button.clicked.connect(self.toggle_mode)
        button_layout.addWidget(toggle_button)

        main_layout.addLayout(button_layout)

        # Task Table
        self.task_table = QTableWidget(0, 3)
        self.task_table.setHorizontalHeaderLabels(["ლინკი", "აღწერა", "ფასი"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setStyleSheet("QTableWidget {background-color: #355F2E;} QTableWidget::item {padding: 10px;} QHeaderView::section {background-color: #4CAF50; color: white; font-weight: bold;}")
        main_layout.addWidget(self.task_table)

        # Edit/Delete Buttons
        edit_delete_layout = QHBoxLayout()

        edit_button = QPushButton("რედაქტირება")
        edit_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        edit_button.setFixedHeight(40)
        edit_button.clicked.connect(self.edit_task)
        edit_delete_layout.addWidget(edit_button)

        delete_button = QPushButton("წაშლა")
        delete_button.setStyleSheet("background-color: #F44336; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        delete_button.setFixedHeight(40)
        delete_button.clicked.connect(self.delete_task)
        edit_delete_layout.addWidget(delete_button)

        main_layout.addLayout(edit_delete_layout)

        # Central widget setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Set initial mode to light
        self.apply_light_mode()

    def toggle_mode(self):
        if self.is_dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
        self.is_dark_mode = not self.is_dark_mode

    def apply_light_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #A5D6A7, stop:1 #FFEB3B);
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit, QTextEdit {
                background-color: #F1F8E9;
                color: #333333;
            }
            QTableWidget {
                background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C2C2C, stop:1 #1C1C1C);
            }
            QPushButton {
                background-color: #333333;
                color: white;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit, QTextEdit {
                background-color: #444444;
                color: #FFFFFF;
            }
            QTableWidget {
                background-color: #333333;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)

    def add_task(self):
        link = self.link_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.text().strip()

        if not link or not description:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ შეიყვანეთ ლინკი და აღწერა.")
            return

        try:
            price = float(price) if price else 0.0
        except ValueError:
            QMessageBox.warning(self, "შეცდომა", "ფასი უნდა იყოს რიცხვი.")
            return

        self.tasks[link] = {"description": description, "price": price}
        self.update_task_table()
        self.link_input.clear()
        self.description_input.clear()
        self.price_input.clear()
        QMessageBox.information(self, "დამატებულია", "დავალება წარმატებით დაემატა!")

    def update_task_table(self):
        self.task_table.setRowCount(0)
        for link, task in self.tasks.items():
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(link))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(task["description"]))
            self.task_table.setItem(row_position, 2, QTableWidgetItem(str(task["price"])))

    def edit_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "არჩევა", "გთხოვთ აირჩიეთ დავალება შესაცვლელად.")
            return

        link = self.task_table.item(selected_row, 0).text()
        task = self.tasks.pop(link)

        self.link_input.setText(link)
        self.description_input.setPlainText(task["description"])
        self.price_input.setText(str(task["price"]))
        self.update_task_table()

    def delete_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "არჩევა", "გთხოვთ აირჩიეთ დავალება წასაშლელად.")
            return

        link = self.task_table.item(selected_row, 0).text()
        del self.tasks[link]
        self.update_task_table()
        QMessageBox.information(self, "წაშლილია", "დავალება წარმატებით წაიშალა!")

    def process_tasks(self):
        if not self.tasks:
            QMessageBox.warning(self, "არ არის დავალებები", "გთხოვთ დაამატოთ დავალებები.")
            return

        results = []
        for link, task in self.tasks.items():
            result = scrape_and_post(link, task["description"], task["price"])
            results.append(f"ლინკი: {link}\nშედეგი: {result}")

        QMessageBox.information(self, "შედეგები", "\n\n".join(results))
        self.tasks.clear()
        self.update_task_table()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern style
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
