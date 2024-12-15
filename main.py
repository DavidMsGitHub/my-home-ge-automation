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
        self.tasks = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MyHome პოსტის ავტომატიზაცია")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("MyHome პოსტის ავტომატიზაცია")
        title.setFont(QFont("Helvetica", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Input fields
        input_layout = QVBoxLayout()
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("ჩაწერეთ ლინკი")
        self.link_input.setFont(QFont("Helvetica", 12))
        input_layout.addWidget(QLabel("ლინკი:"))
        input_layout.addWidget(self.link_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("ჩაწერეთ აღწერა")
        self.description_input.setFont(QFont("Helvetica", 12))
        input_layout.addWidget(QLabel("აღწერა:"))
        input_layout.addWidget(self.description_input)

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
        self.task_table = QTableWidget(0, 2)
        self.task_table.setHorizontalHeaderLabels(["ლინკი", "აღწერა"])
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

        if not link or not description:
            QMessageBox.warning(self, "შეცდომა", "გთხოვთ შეიყვანეთ ლინკი და აღწერა.")
            return

        self.tasks[link] = description
        self.update_task_table()
        self.link_input.clear()
        self.description_input.clear()
        QMessageBox.information(self, "დამატებულია", "დავალება წარმატებით დაემატა!")

    def update_task_table(self):
        self.task_table.setRowCount(0)
        for link, description in self.tasks.items():
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(link))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(description))

    def edit_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "არჩევა", "გთხოვთ აირჩიეთ დავალება შესაცვლელად.")
            return

        link = self.task_table.item(selected_row, 0).text()
        description = self.task_table.item(selected_row, 1).text()

        self.link_input.setText(link)
        self.description_input.setPlainText(description)
        del self.tasks[link]
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
        for link, description in self.tasks.items():
            result = scrape_and_post(link, description)
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
