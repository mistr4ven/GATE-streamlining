from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton, QCheckBox
from PyQt5.QtCore import Qt

class FileInputWidget(QWidget):
    def __init__(self, label_text, key, placeholder_text):
        super().__init__()
        self.key = key
        self.init_ui(label_text, placeholder_text)
    
    def init_ui(self, label_text, placeholder_text):
        # Create layout
        layout = QVBoxLayout()
        
        # Set up the label
        headline_label = QLabel(label_text)
        headline_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(headline_label)
        
        # Set up the input field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText(placeholder_text)
        layout.addWidget(self.input_field)
        
        # Enable drag and drop for the input field
        self.input_field.setAcceptDrops(True)
        
        # Set layout
        self.setLayout(layout)
    
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
        self.create_xml = False  # if the user wants to create an XML macro from the input values or not
        self.xmlpath = ''  # path to the XML file

        self.setWindowTitle("Visual Mode")
        self.setGeometry(100, 100, 1200, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main vertical layout
        self.main_vertical_layout = QVBoxLayout(self.central_widget)
        
        self.file_container = QWidget()
        # Removed fixed height for dynamic layout management
        self.file_layout = QVBoxLayout()
        self.file_layout.setAlignment(Qt.AlignTop)
        
        self.file_label = QLabel("File Parameters")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.file_layout.addWidget(self.file_label)
        self.add_separator(self.file_layout)

        self.file_widgets = [
            FileInputWidget("Dummy macro file", "dummy_macro_file", "drag and drop a file or enter a file path"),
            FileInputWidget(".seed file (leave empty for random seeds)", "seed_file", "drag and drop a file or enter a file path"),
            FileInputWidget("Location of output folders", "output_location", "drag and drop a location or enter a path")
        ]
        for widget in self.file_widgets:
            self.file_layout.addWidget(widget)
        
        self.file_container.setLayout(self.file_layout)

        # Add the file container to the main vertical layout
        self.main_vertical_layout.addWidget(self.file_container)

        self.main_container = QWidget()

        # Main horizontal layout for columns
        self.main_layout = QHBoxLayout(self.main_container)
        
        # Split column
        self.splitting_layout = QVBoxLayout()
        self.splitting_layout.setAlignment(Qt.AlignTop)
        self.splitting_label = QLabel("Splits")
        self.splitting_label.setAlignment(Qt.AlignCenter)
        self.splitting_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.splitting_layout.addWidget(self.splitting_label)
        self.add_separator(self.splitting_layout)
        
        # Add input fields to Split column
        self.split_widgets = [
            FileInputWidget("Amount of splits", "split_amount", "input the amount of split-files that should be created"),
            FileInputWidget("Amount of particles per split", "particle_amount", "input the amount of particles per split-file as a NUMBER (i.e. 100000)")
        ]
        for widget in self.split_widgets:
            self.splitting_layout.addWidget(widget)
        
        # Hardware column
        self.hardware_layout = QVBoxLayout()
        self.hardware_layout.setAlignment(Qt.AlignTop)
        self.hardware_label = QLabel("Hardware")
        self.hardware_label.setAlignment(Qt.AlignCenter)
        self.hardware_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.hardware_layout.addWidget(self.hardware_label)
        self.add_separator(self.hardware_layout)
        
        # Add input fields to hardware column
        self.hardware_widgets = [
            FileInputWidget("Amount of cores to use", "cores", "input the amount of cores that should be used for the simulation = max amount of parallel processes"),
            FileInputWidget("Amount of memory in MB", "ram", "input the amount of memory that should be used for the simulation IN MB (i.e. 64000MB)")
        ]
        for widget in self.hardware_widgets:
            self.hardware_layout.addWidget(widget)
        
        # Add columns to the main horizontal layout
        self.main_layout.addLayout(self.splitting_layout)
        self.main_layout.addLayout(self.hardware_layout)
       
        # Add the main horizontal layout to the main vertical layout
        self.main_vertical_layout.addWidget(self.main_container)
        
        self.post_container = QWidget()

        # Main horizontal layout for columns
        self.post_layout = QHBoxLayout(self.post_container)
        
        # Dimension column
        self.dimension_layout = QVBoxLayout()
        self.dimension_layout.setAlignment(Qt.AlignTop)
        self.dimension_label = QLabel("Dimensions")
        self.dimension_label.setAlignment(Qt.AlignCenter)
        self.dimension_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.dimension_layout.addWidget(self.dimension_label)
        self.add_separator(self.dimension_layout)
        
        # Add input fields to Dimension column
        self.dimension_widgets = [
            FileInputWidget("Voxels X", "dim_x", "input the amount of voxels in x-direction"),
            FileInputWidget("Voxels Y", "dim_y", "input the amount of voxels in y-direction"),
            FileInputWidget("Voxels Z", "dim_z", "input the amount of voxels in z-direction")
        ]
        for widget in self.dimension_widgets:
            self.dimension_layout.addWidget(widget)
        
        # Hardware column
        self.size_layout = QVBoxLayout()
        self.size_layout.setAlignment(Qt.AlignTop)
        self.size_label = QLabel("Voxel Size")
        self.size_label.setAlignment(Qt.AlignCenter)
        self.size_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.size_layout.addWidget(self.size_label)
        self.add_separator(self.size_layout)
        
        # Add input fields to hardware column
        self.size_widgets = [
            FileInputWidget("Voxel Size X", "size_x", "input the size of a voxel in x-direction in mm"),
            FileInputWidget("Voxel Size Y", "size_y", "input the size of a voxel in y-direction in mm"),
            FileInputWidget("Voxel Size Z", "size_z", "input the size of a voxel in z-direction in mm")
        ]
        for widget in self.size_widgets:
            self.size_layout.addWidget(widget)
        
        # Add columns to the main horizontal layout
        self.post_layout.addLayout(self.dimension_layout)
        self.post_layout.addLayout(self.size_layout)
       
        # Add the main horizontal layout to the main vertical layout
        self.main_vertical_layout.addWidget(self.post_container)

        # Container for create XML toggle and file input
        self.xml_input_container = QWidget()
        self.xml_input_container.setFixedHeight(130)  # Set fixed height for the container

        # Vertical layout for XML toggle and input
        self.xml_vertical_layout = QVBoxLayout(self.xml_input_container)
        
        # Add the createXML toggle
        self.create_xml_toggle = QCheckBox("Create XML")
        self.create_xml_toggle.stateChanged.connect(self.toggle_xml_input)
        self.xml_vertical_layout.addWidget(self.create_xml_toggle)
        
        # Add XML file input (hidden by default)
        self.xml_file_input = FileInputWidget("XML path", "XML_path", "drag and drop a file or enter a file path for the macro file to be created")
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
        file_data = {widget.key: widget.get_value()[widget.key] for widget in self.file_widgets}
        split_data = {widget.key: widget.get_value()[widget.key] for widget in self.split_widgets}
        hardware_data = {widget.key: widget.get_value()[widget.key] for widget in self.hardware_widgets}
        dimension_data = {widget.key: widget.get_value()[widget.key] for widget in self.dimension_widgets}
        size_data = {widget.key: widget.get_value()[widget.key] for widget in self.size_widgets}
        
        self.data = [file_data, split_data, hardware_data, dimension_data, size_data]
        
        if self.create_xml:
            xml_data = self.xml_file_input.get_value()
            self.xmlpath = xml_data['XML_path']
        
    
    # Close the window after collecting the data -> submit button
    def submit_data(self):
        self.collect_data()
        self.close()

# Function to start the visual interface
def visual_interface():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

    window.xmlpath = window.xmlpath if window.xmlpath else ''
    print({'data': window.data, 'xmlpath': window.xmlpath})
    return {'data': window.data, 'xmlpath': window.xmlpath}

# For testing purposes
if __name__ == "__main__":
    visual_interface()
