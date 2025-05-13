from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QHBoxLayout, QWidget, QMessageBox, QCheckBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from scraper import scrape_and_post
from funqciebi import check_for_ip, login, check_for_update


login()

from PyQt5.QtCore import QThread, pyqtSignal


class TaskWorker(QThread):
    task_completed = pyqtSignal(str, str)  # Signal to indicate task completion (link, result)

    def __init__(self, link, price, area, agency_id, agentname, to_myhome, to_ssge):
        super().__init__()
        self.link = link
        self.price = price
        self.area = area
        self.agency_id = agency_id
        self.agentname = agentname
        self.to_myhome = to_myhome
        self.to_ssge = to_ssge

    def run(self):

        try:
            print(
                f"Executing scrape_and_post - ID: {self.link}, MyHome: {self.to_myhome}, SS.GE: {self.to_ssge}")  # Debugging

            result = scrape_and_post(
                self.link,
                self.price,
                self.area,
                self.agency_id,
                self.agentname,
                self.to_myhome,
                self.to_ssge
            )
        except Exception as e:
            result = f"შეცდომა: {e}"

        # Emit completion signal
        self.task_completed.emit(self.link, result)


from PyQt5.QtCore import QMutex

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = {}
        self.workers = []
        self.concurrent_tasks = 1  # Number of simultaneous tasks
        self.mutex = QMutex()  # Mutex for thread safety
        self.init_ui()
        self.tasks_queue = []


    def init_ui(self):
        self.setWindowTitle("EverBroker")
        self.setGeometry(100, 100, 800, 600)

        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("EverBroker ავტომატიზაცია")
        title.setFont(QFont("Helvetica", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #BE3144;")
        main_layout.addWidget(title)

        # Input fields layout
        input_layout = QVBoxLayout()

        # Link Input
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("ჩაწერეთ პოსტის აიდი")
        self.link_input.setFont(QFont("Helvetica", 15))
        self.link_input.setStyleSheet("background-color: #09122C; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("პოსტის აიდი:"))
        input_layout.addWidget(self.link_input)


        # Price Input
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("ჩაწერეთ ფასი (არასავალდებულო)")
        self.price_input.setFont(QFont("Helvetica", 15))
        self.price_input.setStyleSheet("background-color: #09122C; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("ფასი:"))
        input_layout.addWidget(self.price_input)

        # Price Input
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText("ჩაწერეთ კვადრატულობა (არასავალდებულო)")
        self.area_input.setFont(QFont("Helvetica", 15))
        self.area_input.setStyleSheet("background-color: #09122C; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("კვადრატულობა:"))
        input_layout.addWidget(self.area_input)

        # Link Input
        self.agencyid_input = QLineEdit()
        self.agencyid_input.setPlaceholderText("ჩაწერეთ საიდენტიფიკაციო ნომერი")
        self.agencyid_input.setFont(QFont("Helvetica", 15))
        self.agencyid_input.setStyleSheet("background-color: #09122C; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("საიდენტიფიკაციო ნომერი სააგენტოსთვის:"))
        input_layout.addWidget(self.agencyid_input)

        self.agentname_input = QLineEdit()
        self.agentname_input.setPlaceholderText("ჩაწერეთ აგენტის სახელი")
        self.agentname_input.setFont(QFont("Helvetica", 15))
        self.agentname_input.setStyleSheet(
            "background-color: #09122C; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(QLabel("აგენტის სახელი:"))
        input_layout.addWidget(self.agentname_input)

        main_layout.addLayout(input_layout)

        # Buttons layout with animation
        button_layout = QHBoxLayout()

        add_button = QPushButton("დავალების დამატება")
        add_button.setStyleSheet("background-color: #BE3144; color: white; border-radius: 5px; padding: 10px; font-size: 20px;")
        add_button.setFixedHeight(45)
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        delete_button = QPushButton("დავალების წაშლა")
        delete_button.setStyleSheet(
            "background-color: #BE3144; color: white; border-radius: 5px; padding: 10px; font-size: 20px;")
        delete_button.setFixedHeight(45)
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        main_layout.addLayout(button_layout)

        import_button = QPushButton("ფაილიდან დაიმპორტება")
        import_button.setStyleSheet(
            "background-color: #BE3144; color: white; border-radius: 5px; padding: 10px; font-size: 20px;")
        import_button.setFixedHeight(45)
        import_button.clicked.connect(self.import_tasks)
        button_layout.addWidget(import_button)

        # Create a horizontal layout for checkboxes
        checkbox_layout = QHBoxLayout()

        # MyHome Checkbox
        self.upload_myhome_checkbox = QCheckBox("Upload to MyHome")
        self.upload_myhome_checkbox.setStyleSheet(
            "QCheckBox { color: white; font-size: 15px; padding: 5px; }"
            "QCheckBox::indicator { width: 20px; height: 20px; }"
            "QCheckBox::indicator:checked { background-color: #BE3144; border-radius: 5px; }"
        )

        # SS.GE Checkbox
        self.upload_ssge_checkbox = QCheckBox("Upload to SS.GE")
        self.upload_ssge_checkbox.setStyleSheet(
            "QCheckBox { color: white; font-size: 15px; padding: 5px; }"
            "QCheckBox::indicator { width: 20px; height: 20px; }"
            "QCheckBox::indicator:checked { background-color: #BE3144; border-radius: 5px; }"
        )

        # Add checkboxes to the horizontal layout
        checkbox_layout.addWidget(self.upload_myhome_checkbox)
        checkbox_layout.addWidget(self.upload_ssge_checkbox)

        # Add the checkbox layout to the main input layout
        input_layout.addLayout(checkbox_layout)

        # Edit/Delete Buttons
        edit_delete_layout = QHBoxLayout()

        process_button = QPushButton("დავალებების შესრულება")
        process_button.setStyleSheet(
            "background-color: #BE3144; color: white; border-radius: 5px; padding: 10px; font-size: 25px;")
        process_button.setFixedHeight(50)
        process_button.clicked.connect(self.process_tasks)
        edit_delete_layout.addWidget(process_button)

        main_layout.addLayout(edit_delete_layout)

        # Central widget setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Set initial mode to light
        self.apply_light_mode()

        # Task Table for pending tasks
        self.task_table = QTableWidget(0, 4)  # 4 columns: ID, price, area, agency ID
        self.task_table.setHorizontalHeaderLabels(["პოსტის აიდი", "ფასი", "კვადრატულობა", "აიდი"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setStyleSheet(
            "QTableWidget {background-color: #872341;} QTableWidget::item {padding: 10px;} QHeaderView::section {background-color: #BE3144; color: white; font-weight: bold;}")
        main_layout.addWidget(self.task_table)

        # Completed Tasks Table (below the main task table)
        completed_task_layout = QVBoxLayout()

        # Title for completed tasks
        completed_title = QLabel("დასრულებულები")
        completed_title.setFont(QFont("Helvetica", 20, QFont.Bold))
        completed_title.setAlignment(Qt.AlignCenter)
        completed_task_layout.addWidget(completed_title)

        # Table for completed tasks (only containing IDs)
        self.completed_task_table = QTableWidget(0, 1)  # 1 column for task IDs
        self.completed_task_table.setHorizontalHeaderLabels(["პოსტის აიდი"])
        self.completed_task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.completed_task_table.setStyleSheet(
            "QTableWidget {background-color: #872341;} QTableWidget::item {padding: 10px;} QHeaderView::section {background-color: #BE3144; color: white; font-weight: bold;}")
        completed_task_layout.addWidget(self.completed_task_table)

        # Add the completed tasks layout below the task table
        main_layout.addLayout(completed_task_layout)

    def toggle_mode(self):
        if self.is_dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()
        self.is_dark_mode = not self.is_dark_mode

    def apply_light_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:2, y2:2, stop:0 #09122C, stop:1 #872341);
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QLabel {
                color: #BE3144;
            }
            QLineEdit, QTextEdit {
                background-color: #F1F8E9;
                color: #BE3144;
            }
            QTableWidget {
                background-color: #E17564;
            }
            QHeaderView::section {
                background-color: #E17564;
                color: white;
                font-weight: bold;
            }
        """)


    def import_tasks(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Task File", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)

        if not file_path:
            return  # User canceled

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            for line in lines:
                parts = line.strip().split(" ", 1)
                if not parts:
                    continue

                link = parts[0]  # ID
                task_type = parts[1] if len(parts) > 1 else ""  # Type of post (optional)

                price = 1500 if task_type == "იყიდება" else 0.0  # Set price if "იყიდება"

                self.tasks[link] = {
                    "price": price,
                    "area": 0.0,  # Default area to 0
                    "agencyid": "",
                    "agentname": "",
                    "to_myhome": True,
                    "to_ssge": False
                }

            self.update_task_table()
            QMessageBox.information(self, "Import Successful", "Tasks imported successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import tasks: {e}")

    def add_task(self):
        link = self.link_input.text().strip()
        price = self.price_input.text().strip()
        area = self.area_input.text().strip()
        agencyid = self.agencyid_input.text().strip()
        agentname = self.agentname_input.text().strip()

        # Ensure the checkbox values are correctly retrieved
        to_myhome = self.upload_myhome_checkbox.isChecked()
        to_ssge = self.upload_ssge_checkbox.isChecked()

        # Check if link is empty
        if not link:
            QMessageBox.warning(self, "შეცდომა", "პოსტის აიდი აუცილებელია.")
            return

        try:
            price = float(price) if price else 0.0
        except ValueError:
            QMessageBox.warning(self, "შეცდომა", "ფასი უნდა იყოს რიცხვი.")
            return

        try:
            area = float(area) if area else 0.0
        except ValueError:
            QMessageBox.warning(self, "შეცდომა", "კვადრატულობა უნდა იყოს რიცხვი.")
            return

        # Debugging prints
        print(f"Checkbox States - MyHome: {to_myhome}, SS.GE: {to_ssge}")  # Check values

        # Add task to the dictionary
        self.tasks[link] = {
            "price": price,
            "area": area,
            "agencyid": agencyid,
            "agentname": agentname,
            "to_myhome": to_myhome,
            "to_ssge": to_ssge
        }

        self.update_task_table()

        # Clear inputs
        self.link_input.clear()
        self.price_input.clear()
        self.area_input.clear()
        self.agencyid_input.clear()
        self.agentname_input.clear()

    def update_task_table(self):
        # Remove all existing rows
        while self.task_table.rowCount() > 0:
            self.task_table.removeRow(0)

        # Add new rows from tasks dictionary
        for link, task in self.tasks.items():
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(link))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(str(task["price"])))
            self.task_table.setItem(row_position, 2, QTableWidgetItem(str(task["area"])))
            self.task_table.setItem(row_position, 3, QTableWidgetItem(str(task["agencyid"])))
            self.task_table.setItem(row_position, 4, QTableWidgetItem("sruldeba.."))  # Default status

    def edit_task(self):
        selected_row = self.task_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "არჩევა", "გთხოვთ აირჩიეთ დავალება შესაცვლელად.")
            return

        link = self.task_table.item(selected_row, 0).text()
        task = self.tasks.pop(link)

        self.link_input.setText(link)
        self.price_input.setText(str(task["price"]))
        self.area_input.setText(str(task["area"]))
        self.agencyid_input.setText(str(task["agencyid"]))
        self.agentname_input.setText(str(task["agentname"]))
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
        """Starts processing tasks with up to `self.concurrent_tasks` workers running at the same time."""
        if not self.tasks:
            QMessageBox.warning(self, "არ არის დავალებები", "გთხოვთ დაამატოთ დავალებები.")
            return

        self.tasks_queue = list(self.tasks.items())  # Convert tasks dict to a queue
        self.active_workers = []  # Track active workers

        # Start initial tasks (up to self.concurrent_tasks)
        for _ in range(min(self.concurrent_tasks, len(self.tasks_queue))):
            self.start_next_task()

    def start_next_task(self):
        """Starts a new task if there is available space for concurrent execution."""
        if not self.tasks_queue or len(self.active_workers) >= self.concurrent_tasks:
            return  # No more tasks or max workers reached

        link, task = self.tasks_queue.pop(0)  # Get next task

        print(f"Starting Task - ID: {link}, MyHome: {task['to_myhome']}, SS.GE: {task['to_ssge']}")  # Debugging

        worker = TaskWorker(
            link,
            task["price"],
            task["area"],
            task.get("agencyid", "0"),  # Default to "0"
            task.get("agentname", "EverBroker"),  # Default to "SafeHome"
            task.get("to_myhome", True),
            task.get("to_ssge", False)
        )

        worker.task_completed.connect(self.handle_task_completion)
        self.active_workers.append(worker)  # Track active workers
        worker.start()

    def handle_task_completion(self, link, result):
        """Handles task completion and starts the next one if available."""

        print(f"Task Completed - ID: {link}, Result: {result}")  # Debugging

        # Remove completed task from the list
        if link in self.tasks:
            del self.tasks[link]

        # Update the task table without blocking execution
        self.update_task_table()

        # Remove worker from the active list
        self.active_workers = [worker for worker in self.active_workers if worker.link != link]

        # Add the completed task ID to the completed tasks table
        row_position = self.completed_task_table.rowCount()
        self.completed_task_table.insertRow(row_position)
        self.completed_task_table.setItem(row_position, 0, QTableWidgetItem(link))

        # Start the next task if there are pending tasks
        self.start_next_task()

    def get_row_for_link(self, link):
        # Find the row index of the task with the given link
        for row in range(self.task_table.rowCount()):
            if self.task_table.item(row, 0).text() == link:
                return row
        return -1  # Return -1 if not found


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern style
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())