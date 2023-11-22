import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, \
    QGraphicsTextItem, QGraphicsLineItem, QPushButton, QLineEdit
from PyQt5.QtGui import QPen, QBrush, QPainter
from PyQt5.QtCore import Qt, QRectF

class DraggableBlock(QGraphicsRectItem):

    def __init__(self, x, y, width, height, label, line_style=Qt.SolidLine):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setPen(QPen(Qt.black,4,line_style))
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
        
class DraggableGod(QGraphicsEllipseItem):
    def __init__(self,x,y,width,height):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setPen(QPen(Qt.black,3))
        
        text = QGraphicsTextItem("God")
        text.setParentItem(self)
        text.setDefaultTextColor(Qt.black)
        text.setPos(x,y+5)

class DraggableText(QGraphicsTextItem):
    def __init__(self,text):
        super().__init__(text)
        self.setFlag(QGraphicsTextItem.ItemIsMovable)
        self.setFlag(QGraphicsTextItem.ItemIsSelectable)
        
        self.setDefaultTextColor(Qt.black)
    

def create_block(x, y, label, line_style=Qt.SolidLine):
    block = DraggableBlock(x, y, 100, 50, label, line_style)
    return block

def create_line(x1, y1, x2, y2, line_style=Qt.SolidLine):
    line = DraggableLine(x1, y1, x2, y2, line_style)
    return line

def create_god_block(x,y):
    block = DraggableGod(x,y,30,30)
    return block

def text_block(text):
    block = DraggableText(text)
    return block


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
        self.object_name_input.setGeometry(55, 50, 150, 30)
        self.object_name_input.setPlaceholderText("Enter object name")

        # Add button to create object
        create_object_button = QPushButton("Create Object", self)
        create_object_button.setGeometry(55, 170, 150, 30)
        create_object_button.clicked.connect(lambda: self.create_object(Qt.SolidLine))

        # Add button to delete object(마지막으로 생성된 순으로 제거)
        delete_object_button = QPushButton("Delete Object", self)
        delete_object_button.setGeometry(55, 210, 150, 30)
        delete_object_button.clicked.connect(self.delete_object)

        # Add button to create solid line
        create_solid_line_button = QPushButton("Solid Line", self)
        create_solid_line_button.setGeometry(55, 250, 150, 30)
        create_solid_line_button.clicked.connect(lambda: self.create_line(Qt.SolidLine))

        # Add button to create dashed line
        create_dashed_line_button = QPushButton("Dot Line", self)
        create_dashed_line_button.setGeometry(55, 290, 150, 30)
        create_dashed_line_button.clicked.connect(lambda: self.create_line(Qt.DashLine))
        
        create_start_object_button = QPushButton("Create Start Object", self)
        create_start_object_button.setGeometry(55, 90, 150, 30)
        create_start_object_button.clicked.connect(lambda: self.create_object(Qt.DashLine))
        
        create_god_button = QPushButton("God", self)
        create_god_button.setGeometry(55, 130, 150, 30)
        create_god_button.clicked.connect(self.create_god)

        create_text_button = QPushButton("Text", self)
        create_text_button.setGeometry(55, 330, 150, 30)
        create_text_button.clicked.connect(self.create_text_box)


        self.current_line = None
    def create_text_box(self):
        text = self.object_name_input.text()
        
        new_block = text_block(text=text)
        self.scene.addItem(new_block)
        

        
    def create_god(self):
        god = create_god_block(x=100,y=50)
        self.scene.addItem(god)

    def create_object(self, line_style):
        # Get object name from user input
        object_name = self.object_name_input.text()

        # Define UI area
        ui_area = QRectF(0, 0, 300, 250)  # Adjust the dimensions as needed

        # Generate random positions for x and y, avoiding UI area
        random_x = random.uniform(0, self.scene.width() - 100)  # Adjust the range according to the object size
        random_y = random.uniform(0, self.scene.height() - 50)

        # Check if the random position overlaps with the UI area and adjust if needed
        if ui_area.contains(random_x, random_y):
            random_x += 200  # Adjust the offset as needed
            random_y += 100

        # Create a block with the entered object name
        new_block = create_block(x=random_x, y=random_y, label=object_name, line_style=line_style)
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
    
