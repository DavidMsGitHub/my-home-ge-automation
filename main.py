from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from scraper import scrape_and_post


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = {}  # Format: {link: {"description": desc, "price": price}}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SAFEHOME")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("SAFEHOME")
        title.setFont(QFont("Helvetica", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Input fields
        input_layout = QVBoxLayout()

        # Link Input
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("ჩაწერეთ ლინკი")
        self.link_input.setFont(QFont("Helvetica", 12))
        input_layout.addWidget(QLabel("ლინკი:"))
        input_layout.addWidget(self.link_input)

        # Description Input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("ჩაწერეთ აღწერა")
        self.description_input.setFont(QFont("Helvetica", 12))
        input_layout.addWidget(QLabel("აღწერა:"))
        input_layout.addWidget(self.description_input)

        # Price Input
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("ჩაწერეთ ფასი (არასავალდებულო)")
        self.price_input.setFont(QFont("Helvetica", 12))
        input_layout.addWidget(QLabel("ფასი:"))
        input_layout.addWidget(self.price_input)

        main_layout.addLayout(input_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("დავალების დამატება")
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        process_button = QPushButton("დავალებების შესრულება")
        process_button.clicked.connect(self.process_tasks)
        button_layout.addWidget(process_button)

        main_layout.addLayout(button_layout)

        # Task Table
        self.task_table = QTableWidget(0, 3)
        self.task_table.setHorizontalHeaderLabels(["ლინკი", "აღწერა", "ფასი"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.task_table)

        # Edit/Delete Buttons
        edit_delete_layout = QHBoxLayout()
        edit_button = QPushButton("რედაქტირება")
        edit_button.clicked.connect(self.edit_task)
        edit_delete_layout.addWidget(edit_button)

        delete_button = QPushButton("წაშლა")
        delete_button.clicked.connect(self.delete_task)
        edit_delete_layout.addWidget(delete_button)

        main_layout.addLayout(edit_delete_layout)

        # Central widget setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

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
