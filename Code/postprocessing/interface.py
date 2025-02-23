from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton, QCheckBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt

class FileInputWidget(QWidget):
    def __init__(self, label_text, key):
        super().__init__()
        self.key = key
        self.layout = QVBoxLayout()
        
        self.headline_label = QLabel(label_text)
        self.headline_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(self.headline_label)
        
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Drag and drop a file or enter a file path")
        self.input_field.setAcceptDrops(True)
        self.layout.addWidget(self.input_field)
        
        self.setLayout(self.layout)
        
        self.input_field.dragEnterEvent = self.dragEnterEvent
        self.input_field.dropEvent = self.dropEvent
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.input_field.setText(file_path)
            
    def get_value(self):
        return {self.key: self.input_field.text()}

    def clear(self):
        self.input_field.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = []  # Store the collected data, this will later be the data part for the program
        self.create_xml = False  # if the user wants to create an XML macro from the imput values or not
        self.xmlpath = ''  # path to the XML file
        self.setWindowTitle("PyQt5 Interface")
        self.setGeometry(100, 100, 1200, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main vertical layout
        self.main_vertical_layout = QVBoxLayout(self.central_widget)
        
        self.main_container = QWidget()
        self.main_container.setFixedHeight(500) 

        # Main horizontal layout for columns
        self.main_layout = QHBoxLayout(self.main_container)
        
        # Transform column
        self.transform_layout = QVBoxLayout()
        self.transform_layout.setAlignment(Qt.AlignTop)
        self.transform_label = QLabel("Transform")
        self.transform_label.setAlignment(Qt.AlignCenter)
        self.transform_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.transform_layout.addWidget(self.transform_label)
        self.add_separator(self.transform_layout)
        
        # Add input fields to Transform column
        self.transform_widgets = [
            FileInputWidget("Transform input path", "Transform_input_file"),
            FileInputWidget("Transform operations file", "Transform_operations_file"),
            FileInputWidget("Transform output file", "Transform_output_file")
        ]
        for widget in self.transform_widgets:
            self.transform_layout.addWidget(widget)
        
        # Math column
        self.math_layout = QVBoxLayout()
        self.math_layout.setAlignment(Qt.AlignTop)
        self.math_label = QLabel("Math")
        self.math_label.setAlignment(Qt.AlignCenter)
        self.math_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.math_layout.addWidget(self.math_label)
        self.add_separator(self.math_layout)
        
        # Add input fields to Math column
        self.math_widgets = [
            FileInputWidget("Math input path", "Math_input_file"),
            FileInputWidget("Math operations file", "Math_operations_file"),
            FileInputWidget("Math output file", "Math_output_file")
        ]
        for widget in self.math_widgets:
            self.math_layout.addWidget(widget)
        
        # Add columns to the main horizontal layout
        self.main_layout.addLayout(self.transform_layout)
        self.main_layout.addLayout(self.math_layout)
       
        # Add the main horizontal layout to the main vertical layout
        self.main_vertical_layout.addWidget(self.main_container)
        
        # Container for create XML toggle and file input
        self.xml_input_container = QWidget()
        self.xml_input_container.setFixedHeight(130)  # Set fixed height for the container
        
        # Vertical layout for XML toggle and input
        self.xml_vertical_layout = QVBoxLayout(self.xml_input_container)
        
        # Add the createXML toggle
        self.create_xml_toggle = QCheckBox("Create XML")
        self.create_xml_toggle.stateChanged.connect(self.toggle_xml_input)
        self.create_xml_toggle.setFixedHeight(20)  # Set fixed height for the create XML checkbox
        self.xml_vertical_layout.addWidget(self.create_xml_toggle)
        
        # Add XML file input (hidden by default)
        self.xml_file_input = FileInputWidget("XML path", "XML_path")
        self.xml_file_input.setFixedHeight(70)  # Set fixed height for the XML file input
        self.xml_file_input.setVisible(False)
        self.xml_vertical_layout.addWidget(self.xml_file_input)
        
        # Add the XML container below the columns
        self.main_vertical_layout.addWidget(self.xml_input_container)
        
        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        
        # Add a submit button to collect the data and close the window
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.buttons_layout.addWidget(self.submit_button)
        
        # Add a clear button to collect the data and clear the fields
        self.clear_button = QPushButton("Clear and Next")
        self.clear_button.clicked.connect(self.collect_and_clear_data)
        self.buttons_layout.addWidget(self.clear_button)
        
        # Add the buttons layout to the bottom of the main vertical layout
        self.main_vertical_layout.addLayout(self.buttons_layout)
    
    # Add a separator line between input fields
    def add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
    
    # Toggle the visibility of the XML file input field
    def toggle_xml_input(self, state):
        self.create_xml = state == Qt.Checked
        self.xml_file_input.setVisible(self.create_xml)
    
    # Collect the data from all input fields
    def collect_data(self):
        transform_data = {widget.key: widget.get_value()[widget.key] for widget in self.transform_widgets}
        math_data = {widget.key: widget.get_value()[widget.key] for widget in self.math_widgets}
        
        collected_data = [transform_data, math_data]
        
        if self.create_xml:
            xml_data = self.xml_file_input.get_value()
            self.xmlpath = xml_data
        
        return collected_data
    
    # Close the window after collecting the data -> final brauch collected
    def submit_data(self):
        self.data.append(self.collect_data())
        self.close()

    # Collect the data and clear all input fields -> new input files of the next branch
    def collect_and_clear_data(self):
        self.data.append(self.collect_data())
        
        # Clear all input fields
        for widget in self.transform_widgets + self.math_widgets:
            widget.clear()

# Function to start the visual interface
def visual_interface():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

    window.xmlpath = window.xmlpath if window.xmlpath else ''
    print({'data': window.data, 'xmlpath': window.xmlpath})
    return {'data': window.data, 'xmlpath': window.xmlpath}

# For testing
if __name__ == "__main__":
    visual_interface()
