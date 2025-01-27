import sys
import pyperclip
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy
)

class WorldEditGui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(5, 34, 300, 680)

        main_layout = QVBoxLayout()

        self.buttons_layout = QFormLayout()

        text = QLabel("WorldEdit Pattern generator")
        text.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        add_button = QPushButton("Add Row")
        add_button.clicked.connect(self.addrow)

        gen_button = QPushButton("Generate Pattern")
        gen_button.clicked.connect(self.gen)

        # Header layout for Block and Percentage
        header_layout = QHBoxLayout()

        block_text = QLabel("Block")
        block_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center-align in its half
        percentage_text = QLabel("Percentage")
        percentage_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center-align in its half

        header_layout.addWidget(block_text)
        header_layout.addWidget(percentage_text)

        self.buttons_layout.addRow(text)
        self.buttons_layout.addRow(add_button)
        self.buttons_layout.addRow(gen_button)
        self.buttons_layout.addRow(header_layout)

        # Create a container widget for the scroll area
        self.scroll_widget = QWidget()
        self.pattern_gen_layout = QFormLayout(self.scroll_widget)

        # Set the container widget to the scroll area
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidget(self.scroll_widget)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFixedHeight(220)

        self.block_menu_title = QLabel("Frequent Needs :")
        self.block_menu_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Menu with most used blocks
        self.block_menu_widget = QWidget()
        self.block_menu_layout = QVBoxLayout(self.block_menu_widget)  # Use QVBoxLayout for vertical alignment

        self.block_menu_area = QScrollArea()
        self.block_menu_area.setWidget(self.block_menu_widget)
        self.block_menu_area.setWidgetResizable(True)
        self.block_menu_area.setFixedHeight(220)
        self.block_menu_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show the vertical scrollbar

        # Ensure the block_menu_widget expands to fill the scroll area
        self.block_menu_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        for block in self.get_frequent_list():
            label = QLabel(block)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            label.setCursor(Qt.IBeamCursor)
            self.block_menu_layout.addWidget(label)

        # Empty layout to fill space
        empty_layout = QHBoxLayout()

        # Add every category to the main layout
        main_layout.addLayout(self.buttons_layout)
        main_layout.addWidget(self.scrollarea)
        main_layout.addWidget(self.block_menu_title)
        main_layout.addWidget(self.block_menu_area)
        main_layout.addLayout(empty_layout, stretch=1)

        self.setLayout(main_layout)

    def copy(self):
        pyperclip.copy(self.command)

    def get_frequent_list(self):
        with open("usual.txt", "r") as file:
            liste = file.read().splitlines()

        return liste

    def addrow(self):
        hbox = QHBoxLayout()
        block = QLineEdit("")
        percentage = QLineEdit("")
        hbox.addWidget(block)
        hbox.addWidget(percentage)
        self.pattern_gen_layout.addRow(hbox)

    def gen(self):
        blocks = []
        for row in range(self.pattern_gen_layout.rowCount()):
            # Access the layout (QHBoxLayout) in the FieldRole of each row
            layout = self.pattern_gen_layout.itemAt(row, QFormLayout.FieldRole).layout()
            if layout:  # Ensure the layout exists
                block = layout.itemAt(0).widget().text()  # Get the first QLineEdit (Block)
                percentage = layout.itemAt(1).widget().text()  # Get the second QLineEdit (Percentage)
                blocks.append((block, percentage))

        command = ""
        for blk, pct in blocks:
            if blk and pct:
                command += f"{pct}%{blk},"

        if len(command) > 0 and command[-1] == ",":
            command = command[:-1]

        self.command = command
        self.copy()

app = QApplication(sys.argv)
with open("style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

window = WorldEditGui()
sys.exit(app.exec())