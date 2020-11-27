from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QTreeWidget
app = QApplication([])
window = QWidget()
layout = QHBoxLayout()
layout.addWidget(QTreeWidget())
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec_()
