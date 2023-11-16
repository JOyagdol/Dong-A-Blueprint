import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QLineEdit, QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QLineF, QPointF


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
        self.object_name_input.setGeometry(350, 50, 150, 30)
        self.object_name_input.setPlaceholderText("Enter object name")

        # Add button to create object
        create_object_button = QPushButton("Create Object", self)
        create_object_button.setGeometry(350, 90, 150, 30)
        create_object_button.clicked.connect(self.create_object)

    def create_block(self, x, y, label):
        block = DraggableBlock(x, y, 100, 50, label)
        return block

    def create_object(self):
        # Get object name from user input
        object_name = self.object_name_input.text()

        # Create a block with the entered object name
        new_block = self.create_block(x=500, y=50, label=object_name)
        self.scene.addItem(new_block)


def main():
    app = QApplication(sys.argv)
    window = DesignDiagram()
    window.setGeometry(500, 500, 1000, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
