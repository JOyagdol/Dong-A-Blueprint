import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DraggableBlock(QGraphicsRectItem):
    def __init__(self, x, y, width, height, label):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setPen(QPen(Qt.black))
        self.setBrush(QBrush(Qt.lightGray))

        # Create a text item and set its parent to the block
        text = QGraphicsTextItem(label)
        text.setParentItem(self)
        text.setDefaultTextColor(Qt.black)  # Set text color
        text.setPos(x + 10, y + 10)  # Adjust text position inside the block

class DraggableLine(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, line_style=Qt.SolidLine):
        super().__init__(x1, y1, x2, y2)
        self.setFlag(QGraphicsLineItem.ItemIsMovable)
        self.setPen(QPen(Qt.black, 4, line_style))

    def update_line(self, pos):
        self.setLine(self.line().x1(), self.line().y1(), pos.x(), pos.y())

def create_block(x, y, label):
    block = DraggableBlock(x, y, 100, 50, label)
    return block

def create_line(x1, y1, x2, y2, line_style=Qt.SolidLine):
    line = DraggableLine(x1, y1, x2, y2, line_style)
    return line

class DesignDiagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.view = QGraphicsView(self)
        self.setCentralWidget(self.view)
        self.view.setWindowTitle('Design Diagram')

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Add user input for object name
        self.object_name_input = QLineEdit(self)
        self.object_name_input.setGeometry(85, 50, 150, 30)
        self.object_name_input.setPlaceholderText("Enter object name")

        # Add button to create object
        create_object_button = QPushButton("Create Object", self)
        create_object_button.setGeometry(85, 90, 150, 30)
        create_object_button.clicked.connect(self.create_object)

        # Add button to delete object(마지막으로 생성된 순으로 제거)
        delete_object_button = QPushButton("Delete Object", self)
        delete_object_button.setGeometry(85, 130, 150, 30)
        delete_object_button.clicked.connect(self.delete_object)

        # Add button to create solid line
        create_solid_line_button = QPushButton("Solid Line", self)
        create_solid_line_button.setGeometry(85, 170, 150, 30)
        create_solid_line_button.clicked.connect(lambda: self.create_line(Qt.SolidLine))

        # Add button to create dashed line
        create_dashed_line_button = QPushButton("Dot Line", self)
        create_dashed_line_button.setGeometry(85, 210, 150, 30)
        create_dashed_line_button.clicked.connect(lambda: self.create_line(Qt.DashLine))

        delete_line_button = QPushButton("Delete Line", self)
        delete_line_button.setGeometry(85, 250, 150, 30)
        delete_line_button.clicked.connect(self.delete_line)

        self.current_line = None

    def create_object(self):
        # Get object name from user input
        object_name = self.object_name_input.text()

        # Create a block with the entered object name
        new_block = create_block(x=500, y=50, label=object_name)
        self.scene.addItem(new_block)

    def delete_object(self):
        # Remove the last item added to the scene
        items = self.scene.items()
        if items:
            last_item = items[-1]
            self.scene.removeItem(last_item)

    def create_line(self, line_style):
        # Set up the current line
        pos = self.view.mapFromGlobal(self.view.cursor().pos())
        self.current_line = create_line(pos.x(), pos.y(), pos.x(), pos.y(), line_style)
        self.scene.addItem(self.current_line)

    def delete_line(self):
        lines = self.scene.items()
        if lines:
            last_line = lines[-1]
            self.scene.removeItem(last_line)

    def mouseMoveEvent(self, event):
        # Update the current line's end point while dragging
        if self.current_line:
            pos = self.view.mapToScene(event.pos())
            self.current_line.update_line(pos)

    def mouseReleaseEvent(self, event):
        # Reset the current line after dragging is finished
        if self.current_line:
            self.current_line = None

def main():
    app = QApplication(sys.argv)
    window = DesignDiagram()
    window.setGeometry(500, 500, 1000, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()