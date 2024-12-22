from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton

class HistoryWindow(QMainWindow):
    def __init__(self, history):
        super().__init__()
        self.setWindowTitle("История")
        self.setGeometry(200, 200, 400, 300)

        self.history = history  # История посещений
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список истории
        self.history_list = QListWidget()
        self.history_list.addItems(self.history)
        layout.addWidget(self.history_list)

        # Кнопка "Закрыть"
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
