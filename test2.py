from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
  
  
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
  
    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()
  
  
import sys
sys.excepthook = log_uncaught_exceptions
  
  
def fill_list_widget(lw: QListWidget):
    for i in range(10):
        lw.addItem('Item #{}'.format(i))
  
  
def print_list_widget(lw: QListWidget):
    print('Items ({}):'.format(lw.count()))
  
    for i in range(lw.count()):
        item = lw.item(i)
        print('    {}'.format(item.text()))
  
  
def get_list_from_list_widget(lw: QListWidget) -> list:
    items = []
  
    for i in range(lw.count()):
        item = lw.item(i)
        items.append(item.text())
  
    return items
  
  
if __name__ == '__main__':
    app = QApplication([])
  
    def _on_item_clicked(item: QListWidgetItem):
        print('Item clicked:', item.text())
  
    lw = QListWidget()
    lw.itemClicked.connect(_on_item_clicked)
  
    lw.show()
  
    print_list_widget(lw)
    fill_list_widget(lw)
    print_list_widget(lw)
  
    items = get_list_from_list_widget(lw)
    print('Items:', items)
  
    with open('list_widget.json', mode='w', encoding='utf-8') as f:
        import json
        json.dump(items, f, indent=4, ensure_ascii=False)
  
    app.exec()