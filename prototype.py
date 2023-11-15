import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QLineEdit, QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QLineF


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

        # Create a block with text
        block1 = self.create_block(x=50, y=50, label="Block 1")
        self.scene.addItem(block1)

        # Create another block with text
        block2 = self.create_block(x=200, y=50, label="Block 2")
        self.scene.addItem(block2)

        # Connect the blocks
        self.connect_blocks_line(block1, block2)

        # Add user input for object name
        self.object_name_input = QLineEdit(self)
        self.object_name_input.setGeometry(350, 50, 150, 30)
        self.object_name_input.setPlaceholderText("객체 이름을 넣으시요")

        # Add button to create object
        create_object_button = QPushButton("객체 생성", self)
        create_object_button.setGeometry(350, 90, 150, 30)
        create_object_button.clicked.connect(self.create_object)

    def create_block(self, x, y, label):
        block = QGraphicsRectItem(x, y, 100, 50)
        block.setPen(QPen(Qt.black))
        block.setBrush(QBrush(Qt.lightGray))

        # Create a text item and set its parent to the block
        text = QGraphicsTextItem(label)
        text.setParentItem(block)
        text.setDefaultTextColor(Qt.black)  # 텍스트 색상 설정
        text.setPos(x + 10, y + 10)  # 텍스트의 위치를 블록 내부로 조정

        return block

    def connect_blocks_line(self, block1, block2):
        line = self.scene.addLine(QLineF(block1.sceneBoundingRect(
        ).center(), block2.sceneBoundingRect().center()), QPen(Qt.black))

    def connect_blocks_dot(self, block1, block2):
        # Create a pen with dash line style
        pen = QPen(Qt.black)
        pen.setStyle(Qt.DashLine)

        line = self.scene.addLine(QLineF(block1.sceneBoundingRect(
        ).center(), block2.sceneBoundingRect().center()), pen)

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
