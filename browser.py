from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QListWidget, QWidget, QStackedWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sqlite3  # Для работы с базой данных


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Браузер с историей и закладками")
        self.setGeometry(100, 100, 1024, 768)

        # Настраиваем базу данных
        self.setup_database()

        # Основной стек виджетов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Создаём страницы
        self.create_browser_page()
        self.create_history_page()
        self.create_bookmarks_page()

        self.stacked_widget.setCurrentWidget(self.browser_page)  # Открываем браузер

    def setup_database(self):
        """Создаём базу данных и таблицы, если их нет."""
        self.conn = sqlite3.connect("browser_data.db")
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_browser_page(self):
        """Главная страница браузера."""
        self.browser_page = QWidget()
        layout = QVBoxLayout()

        # Поле для ввода URL и кнопки управления
        url_layout = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите URL...")
        self.url_bar.returnPressed.connect(self.load_url)
        url_layout.addWidget(self.url_bar)

        # Кнопка "Обновить"
        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.refresh_page)
        url_layout.addWidget(refresh_button)

        # Кнопка "Добавить в закладки"
        bookmark_button = QPushButton("В закладки")
        bookmark_button.clicked.connect(self.add_to_bookmarks)
        url_layout.addWidget(bookmark_button)

        layout.addLayout(url_layout)

        # Браузер
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.urlChanged.connect(self.update_url)
        self.browser.urlChanged.connect(self.save_to_history)  # Сохраняем URL в историю
        layout.addWidget(self.browser)

        self.browser_page.setLayout(layout)
        self.stacked_widget.addWidget(self.browser_page)

    def create_history_page(self):
        """Страница истории."""
        self.history_page = QWidget()
        layout = QVBoxLayout()

        # Список истории
        self.history_list = QListWidget()
        self.load_history()
        self.history_list.itemClicked.connect(self.open_from_history)
        layout.addWidget(self.history_list)

        # Кнопка "На главную"
        home_button = QPushButton("На главную")
        home_button.clicked.connect(self.go_to_browser)
        layout.addWidget(home_button)

        self.history_page.setLayout(layout)
        self.stacked_widget.addWidget(self.history_page)

    def create_bookmarks_page(self):
        """Страница закладок."""
        self.bookmarks_page = QWidget()
        layout = QVBoxLayout()

        # Список закладок
        self.bookmarks_list = QListWidget()
        self.load_bookmarks()
        self.bookmarks_list.itemClicked.connect(self.open_from_bookmarks)
        layout.addWidget(self.bookmarks_list)

        # Кнопка "На главную"
        home_button = QPushButton("На главную")
        home_button.clicked.connect(self.go_to_browser)
        layout.addWidget(home_button)

        self.bookmarks_page.setLayout(layout)
        self.stacked_widget.addWidget(self.bookmarks_page)

    def load_url(self):
        """Загружает URL из строки."""
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, url):
        """Обновляет строку URL при переходе."""
        self.url_bar.setText(url.toString())

    def save_to_history(self, url):
        """Сохраняет URL в историю."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO history (url) VALUES (?)", (url.toString(),))
        self.conn.commit()

    def load_history(self):
        """Загружает историю в список."""
        self.history_list.clear()
        cursor = self.conn.cursor()
        cursor.execute("SELECT url FROM history ORDER BY id DESC")
        for row in cursor.fetchall():
            self.history_list.addItem(row[0])

    def load_bookmarks(self):
        """Загружает закладки в список."""
        self.bookmarks_list.clear()
        cursor = self.conn.cursor()
        cursor.execute("SELECT url FROM bookmarks ORDER BY id DESC")
        for row in cursor.fetchall():
            self.bookmarks_list.addItem(row[0])

    def open_from_history(self, item):
        """Открывает URL из истории."""
        self.browser.setUrl(QUrl(item.text()))
        self.stacked_widget.setCurrentWidget(self.browser_page)

    def open_from_bookmarks(self, item):
        """Открывает URL из закладок."""
        self.browser.setUrl(QUrl(item.text()))
        self.stacked_widget.setCurrentWidget(self.browser_page)

    def add_to_bookmarks(self):
        """Добавляет текущий URL в закладки."""
        current_url = self.browser.url().toString()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO bookmarks (url) VALUES (?)", (current_url,))
        self.conn.commit()
        self.load_bookmarks()

    def refresh_page(self):
        """Обновляет текущую страницу."""
        self.browser.reload()

    def go_to_browser(self):
        """Возвращает на главную страницу браузера."""
        self.stacked_widget.setCurrentWidget(self.browser_page)


if __name__ == "__main__":
    app = QApplication([])
    window = Browser()
    window.show()
    app.exec()
