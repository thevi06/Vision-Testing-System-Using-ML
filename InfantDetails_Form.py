import os
import re
import datetime
import mysql.connector
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QCheckBox, \
    QPushButton, QDateEdit, QFormLayout, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from Infants_Database import MyWidget

class MyPage(QWidget):

    start_signal = pyqtSignal()
    close_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.connect_to_db = False
        # Create the database and table
        self.create_database_and_table()
        self.database = MyWidget()

        # Set the window size as a percentage of the screen size
        screen_size = QApplication.primaryScreen().availableGeometry()
        width_percent = 0.5
        height_percent = 0.6
        self.setGeometry(
            int((1 - width_percent) * screen_size.width() / 2),
            int((1 - height_percent) * screen_size.height() / 2),
            int(width_percent * screen_size.width()),
            int(height_percent * screen_size.height())
        )

        # Set the background color to blue
        self.setStyleSheet("background-color: #D0DAFF;")

        self.setWindowTitle("ECTA")

        # Create a white container in the middle of the page
        container = QWidget(self)
        container.setStyleSheet("background-color: white;")

        container_layout = QVBoxLayout()

        # Create the heading label and add it to the container layout
        heading_label = QLabel("Infants Details Form", self)
        heading_label.setFont(QFont("Inter", 15, QFont.Weight.Bold))
        heading_label.setStyleSheet("color: #3136AF;")  # Set the text color to blue

        # Set up the blue underline
        underline = QLabel()
        underline.setStyleSheet("background-color: #869EF4;")
        underline.setFixedHeight(2)

        # Get the width of the text and add padding of 20 pixels on each side
        text_width = heading_label.fontMetrics().boundingRect(heading_label.text()).width() + 2
        underline.setFixedWidth(text_width)

        # Create a layout to hold the heading and underline
        heading_layout = QVBoxLayout()
        heading_layout.addWidget(heading_label)
        heading_layout.addWidget(underline)

        # Add the heading layout to the container layout
        container_layout.addLayout(heading_layout)

        # Create the icon widget and add it to the container layout
        icon = QLabel(self)
        pixmap = QPixmap('ECTALogo.png').scaledToHeight(90)  # Set the height of the pixmap to 50 pixels
        pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2)
        icon.setPixmap(pixmap)
        icon.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align the icon to the top

        # Create a vertical spacer item to push the form elements to the top of the container
        vspacer = QWidget(self)
        vspacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a horizontal layout to add the vertical spacer, icon and spacer to the container layout
        hbox = QHBoxLayout()
        hbox.addWidget(heading_label)
        hbox.addWidget(vspacer)
        hbox.addWidget(icon)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        # Add the horizontal layout to the container layout
        container_layout.addLayout(hbox)

        # Add a vertical spacer to push the form elements to the top of the container
        container_layout.addStretch(1)

        # Set the layout of the container
        container.setLayout(container_layout)

        # Create the form layout
        form_layout = QFormLayout()

        # Create form elements
        name_label = QLabel("Name*")
        self.first_name_input = QLineEdit()
        self.first_name_input.setFixedSize(200, 30)
        self.first_name_input.setFont(QFont())
        self.first_name_input.setPlaceholderText("First Name")
        self.surname_input = QLineEdit()
        self.surname_input.setFixedSize(200, 30)
        self.surname_input.setFont(QFont())
        self.surname_input.setPlaceholderText("Surname")
        gender_label = QLabel("Gender*")
        self.gender_input = QLineEdit()
        self.gender_input.setFixedSize(200, 30)
        self.gender_input.setFont(QFont())
        self.gender_input.setPlaceholderText("Male/Female")
        dob_label = QLabel("Date of Birth*")
        self.dob_input = QLineEdit()
        self.dob_input.setFixedSize(200, 30)
        self.dob_input.setFont(QFont())
        self.dob_input.setPlaceholderText("DD/MM/YYYY")
        test_id_label = QLabel("Test ID*")
        self.test_id_input = QLineEdit()
        self.test_id_input.setFixedSize(200, 30)
        self.test_id_input.setFont(QFont())
        self.test_id_input.setPlaceholderText("123456")
        parent_type_label = QLabel("Parent Type*")
        self.parent_type_input = QLineEdit()
        self.parent_type_input.setFixedSize(200, 30)
        self.parent_type_input.setFont(QFont())
        self.parent_type_input.setPlaceholderText("Mother/Father")
        parent_name_label = QLabel("Parent's Full Name*")
        self.parent_name_input = QLineEdit()
        self.parent_name_input.setFixedSize(200, 30)
        self.parent_name_input.setFont(QFont())
        self.parent_name_input.setPlaceholderText("Enter parent full name")
        nic_number_label = QLabel("NIC Number*")
        self.nic_number_input = QLineEdit()
        self.nic_number_input.setFixedSize(200, 30)
        self.nic_number_input.setFont(QFont())
        self.nic_number_input.setPlaceholderText("Enter NIC number")
        contact_number_label = QLabel("Contact Number*")
        self.contact_number_input = QLineEdit()
        self.contact_number_input.setFixedSize(200, 30)
        self.contact_number_input.setFont(QFont())
        self.contact_number_input.setPlaceholderText("+94 77 266 8000")
        email_label = QLabel("Email Address*")
        self.email_input = QLineEdit()
        self.email_input.setFixedSize(200, 30)
        self.email_input.setFont(QFont())
        self.email_input.setPlaceholderText("abcd@gmail.com")

        # Create buttons
        self.login_button = QPushButton("Return to LOGINPAGE")
        self.submit_button = QPushButton("Submit & start Testing")
        self.db_button = QPushButton("Select from existing database")

        # Connect button to function
        self.submit_button.clicked.connect(self.submit_data)
        self.login_button.clicked.connect(self.return_to_login)

        self.db_button.clicked.connect(self.getDetails)

        # Change the color of the login button
        self.login_button.setStyleSheet("background-color: #235FF9; color: white;")

        # Change the color of the submit button
        self.submit_button.setStyleSheet("background-color: #235FF9; color: white;")

        # Change the color of the db button
        self.db_button.setStyleSheet("background-color: #65C8FF; color: white;")

        # Add form elements and buttons to form container
        form_layout = QGridLayout()
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.first_name_input, 0, 1)
        form_layout.addWidget(self.surname_input, 0, 2)
        form_layout.addWidget(gender_label, 1, 0)
        form_layout.addWidget(self.gender_input, 1, 1)
        form_layout.addWidget(dob_label, 2, 0)
        form_layout.addWidget(self.dob_input, 2, 1)
        form_layout.addWidget(test_id_label, 3, 0)
        form_layout.addWidget(self.test_id_input, 3, 1)
        form_layout.addWidget(parent_type_label, 4, 0)
        form_layout.addWidget(self.parent_type_input, 4, 1)
        form_layout.addWidget(parent_name_label, 5, 0)
        form_layout.addWidget(self.parent_name_input, 5, 1)
        form_layout.addWidget(nic_number_label, 6, 0)
        form_layout.addWidget(self.nic_number_input, 6, 1)
        form_layout.addWidget(contact_number_label, 7, 0)
        form_layout.addWidget(self.contact_number_input, 7, 1)
        form_layout.addWidget(email_label, 8, 0)
        form_layout.addWidget(self.email_input, 8, 1)

        # Add buttons to form container
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.db_button)
        form_layout.addLayout(button_layout, 9, 1, 1, 2)

        # Add the form layout to the container layout
        container_layout.addLayout(form_layout)

        # Set the layout of the container
        container.setLayout(container_layout)

        # Add the container to the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(container)

        # Set the main layout of the page
        self.setLayout(main_layout)

    def getDetails(self):
        self.database.show()

    def return_to_login(self):
        self.close_signal.emit(True)
        self.close()

    def create_database_and_table(self):
        # Connect to MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Check if the database exists
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [x[0] for x in cursor]

            if "infantsdatabase" not in databases:
                # Create the database
                cursor.execute("CREATE DATABASE InfantsDatabase")
                print("Database created")

                # Use the database
                conn.database = "InfantsDatabase"

                # Check if the table exists
                cursor.execute("SHOW TABLES")
                tables = [x[0] for x in cursor]
                if "InfantsTable" not in tables:
                    # Create the table
                    cursor.execute("""
                                CREATE TABLE InfantsTable (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255) NOT NULL,
                                    gender VARCHAR(255) NOT NULL,
                                    dob VARCHAR(255) NOT NULL,
                                    test_id VARCHAR(255) NOT NULL,
                                    parent_type VARCHAR(255) NOT NULL,
                                    parent_name VARCHAR(255) NOT NULL,
                                    nic_number VARCHAR(255) NOT NULL,
                                    contact_number VARCHAR(255) NOT NULL,
                                    email VARCHAR(255) NOT NULL
                                )
                            """)
                    print("Table created")
                    # Close the connection
                    cursor.close()
                    conn.close()

        except Exception as E:
            QMessageBox.critical(self, "Error", str(E))

    def submit_data(self):
        name = self.first_name_input.text() + " " + self.surname_input.text()
        gender = self.gender_input.text()
        dob = self.dob_input.text()
        test_id = self.test_id_input.text()
        parent_type = self.parent_type_input.text()
        parent_name = self.parent_name_input.text()
        nic_number = self.nic_number_input.text()
        contact_number = self.contact_number_input.text()
        email = self.email_input.text()

        # Check for empty fields
        if not all([name, gender, dob, test_id, parent_type, parent_name, nic_number, contact_number, email]):
            QMessageBox.critical(self, "Error", "Please fill all the fields!")
            return

        # Validate name
        if not re.match(r"^[A-Za-z\s]+$", name):
            QMessageBox.critical(self, "Error", "Name can only contain letters and spaces!")
            return

        # Validate gender
        if gender.lower() not in ["male", "female", "other"]:
            QMessageBox.critical(self, "Error", "Gender can only be Male, Female, or Other!")
            return

            # Validate dob
            try:
                datetime.datetime.strptime(dob, '%d/%m/%Y')
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid date format. Date should be in DD/MM/YYYY format!")
                return

            # Validate test_id
            if not re.match(r"^[A-Za-z0-9]+$", test_id):
                QMessageBox.critical(self, "Error", "Test ID can only contain letters and numbers!")
                return

            # Validate parent_type
            if parent_type.lower() not in ["father", "mother", "guardian"]:
                QMessageBox.critical(self, "Error", "Parent Type can only be Father, Mother, or Guardian!")
                return