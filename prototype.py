import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
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
        line = self.scene.addLine(QLineF(block1.sceneBoundingRect().topRight(), block2.sceneBoundingRect().topLeft()), QPen(Qt.black))

    def connect_blocks_dot(self, block1, block2):
        # Create a pen with dash line style
        pen = QPen(Qt.black)
        pen.setStyle(Qt.DashLine)

        line = self.scene.addLine(QLineF(block1.sceneBoundingRect().topRight(), block2.sceneBoundingRect().topLeft()), pen)
def main():
    app = QApplication(sys.argv)
    window = DesignDiagram()
    window.setGeometry(500, 500, 1000, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()