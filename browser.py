from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from history import HistoryWindow  # Импортируем окно История
from bookmarks import BookmarksWindow  # Импортируем окно Закладки

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Браузер с меню")
        self.setGeometry(100, 100, 1024, 768)

        # Основной стек виджетов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # История и закладки
        self.history = []
        self.bookmarks = []
        self.previous_url = None  # Для отслеживания предыдущего URL

        # Создаём страницы
        self.create_browser_page()

        # Добавляем меню
        self.create_menu()

        self.stacked_widget.setCurrentWidget(self.browser_page)  # Открываем браузер

    def create_browser_page(self):
        """Главная страница браузера."""
        self.browser_page = QWidget()
        layout = QVBoxLayout()

        # Браузер
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.add_to_history)

        # Ввод адреса
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL...")
        self.url_input.returnPressed.connect(self.load_url)
        layout.addWidget(self.url_input)

        layout.addWidget(self.browser)

        # Кнопка "На главную"
        self.home_button = QPushButton("На главную")
        self.home_button.clicked.connect(self.go_to_home)
        layout.addWidget(self.home_button)

        self.browser_page.setLayout(layout)
        self.stacked_widget.addWidget(self.browser_page)

    def create_menu(self):
        """Создаёт главное меню."""
        menu_bar = self.menuBar()

        # Меню "Настройки"
        settings_menu = menu_bar.addMenu("Настройки")
        refresh_action = QAction("Обновить", self)
        refresh_action.triggered.connect(self.refresh_page)
        settings_menu.addAction(refresh_action)

        close_action = QAction("Закрыть", self)
        close_action.triggered.connect(self.close)
        settings_menu.addAction(close_action)

        # Меню "Переход"
        navigate_menu = menu_bar.addMenu("Переход")
        home_action = QAction("На главную", self)
        home_action.triggered.connect(self.go_to_home)
        navigate_menu.addAction(home_action)

        # Меню "История"
        history_menu = menu_bar.addMenu("История")
        history_action = QAction("Посмотреть историю", self)
        history_action.triggered.connect(self.show_history)
        history_menu.addAction(history_action)

        # Меню "Закладки"
        bookmarks_menu = menu_bar.addMenu("Закладки")
        bookmarks_action = QAction("Посмотреть закладки", self)
        bookmarks_action.triggered.connect(self.show_bookmarks)
        bookmarks_menu.addAction(bookmarks_action)

    def refresh_page(self):
        """Обновляет текущую страницу."""
        self.browser.reload()

    def go_to_home(self):
        """Возвращает на главную страницу."""
        self.browser.setUrl(QUrl("https://www.google.com"))

    def load_url(self):
        """Загружает введённый URL."""
        url = self.url_input.text()
        self.browser.setUrl(QUrl(url))

    def add_to_history(self, url):
        """Добавляет посещённую страницу в историю."""
        if url.toString() not in self.history:
            self.history.append(url.toString())

    def show_history(self):
        """Показывает окно истории в новом окне."""
        self.history_window = HistoryWindow(self.history)
        self.history_window.show()

    def show_bookmarks(self):
        """Показывает окно закладок в новом окне."""
        self.bookmarks_window = BookmarksWindow(self.bookmarks)
        self.bookmarks_window.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Browser()
    window.show()
    app.exec()
