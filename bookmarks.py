from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton

class BookmarksWindow(QMainWindow):
    def __init__(self, bookmarks):
        super().__init__()
        self.setWindowTitle("Закладки")
        self.setGeometry(200, 200, 400, 300)

        self.bookmarks = bookmarks  # Закладки
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список закладок
        self.bookmarks_list = QListWidget()
        self.bookmarks_list.addItems(self.bookmarks)
        layout.addWidget(self.bookmarks_list)

        # Кнопка "Закрыть"
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
