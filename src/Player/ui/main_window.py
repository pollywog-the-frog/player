from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QStackedWidget, QPushButton
from Player.ui.pages.HomePage import HomePage
from Player.ui.pages.YtSearchPage import YTSearchPage
from Player.ui.pages.DirectUrlPage import DirectURLPage
from Player.ui.pages.PlayerPage import PlayerPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player")
        self.resize(800, 600)
        
        # Define core widget arrangement
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Define the layout
        v_layout = QVBoxLayout(central_widget)

        # Add the stack
        self.stack = QStackedWidget()

        # Define pages
        self.home_page = HomePage(stack=self.stack, main_window=self)
        self.ytsearch_page = YTSearchPage(stack=self.stack, main_window=self)
        self.direct_url_page = DirectURLPage(stack=self.stack, main_window=self)
        self.player_page = PlayerPage(stack=self.stack, main_window=self)

        # Add pages to stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.ytsearch_page)
        self.stack.addWidget(self.direct_url_page)
        self.stack.addWidget(self.player_page)
        
        # Add stack to v_layout
        v_layout.addWidget(self.stack)

        # Set stack to home_page
        self.stack.setCurrentWidget(self.home_page)