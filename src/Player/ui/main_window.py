from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt, Slot, QRect, QPoint
from PySide6.QtGui import QResizeEvent

from Player.ui.pages.home_page import HomePage
from Player.ui.pages.ytsearch_page import YTSearchPage
from Player.ui.pages.direct_url_page import DirectURLPage
from Player.ui.components.nav_bar import NavBar
from Player.ui.components.display_frame import DisplayFrame
from Player.core.mpv_widgets import MpvDisplay
from Player.core.mpv_widgets import MpvControls
from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus

from mpv import MPV

import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player")
        self.resize(800, 600)

        # import locale
        import locale

        # Set locale for MPV
        locale.setlocale(locale.LC_NUMERIC, 'C')

        # Initialize _player
        self._player = MPV(
            ytdl=True,
            log_handler=print,
            loglevel='debug',
            hwdec='auto-safe',
            vo='libmpv',
        )
        
        # Define controls
        self.controls = MpvControls(mpv_instance=self._player)
        
        # Define status objects
        self.status = MpvStatus(instance=self._player)
        self.qtstatus = QtMpvStatus(mpv_instance=self._player, parent=self)
        
        # Define core widget arrangement
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Define the v_layout
        self.v_layout = QVBoxLayout(central_widget)

        # Add the stack
        self.stack = QStackedWidget()

        # Define the NavBar
        self.nav_bar = NavBar(stack=self.stack, main_window=self, parent=self)

        # Connect buttonClicked to _cycle_display_fullwindow
        self.nav_bar.buttonClicked.connect(self._cycle_display_fullwindow)

        # Define pages
        self.home_page = HomePage(stack=self.stack, main_window=self)
        self.ytsearch_page = YTSearchPage(stack=self.stack, main_window=self)
        self.direct_url_page = DirectURLPage(stack=self.stack, main_window=self)

        # Define display_frame
        self.display_frame = DisplayFrame(self, parent=self)

        # Define display
        self.display = MpvDisplay(mpv_instance=self._player, parent=self.display_frame, main_window=self)
        self.display_frame.layout().addWidget(self.display)
        # Connect display.doubleClicked to _handle_display_double_clicked
        self.display_frame.doubleClicked.connect(self._handle_display_double_clicked)

        self.qtstatus.file_loadedChanged.connect(self.cycle_display_show)

        # Add pages to stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.ytsearch_page)
        self.stack.addWidget(self.direct_url_page)
        
        # Add widgets to v_layout
        self.v_layout.addWidget(self.stack)

        # Hide the display
        self.display_frame.hide()

        # Set stack to home_page
        self.stack.setCurrentWidget(self.home_page)

        # Throw nav_bar on top 
        self.nav_bar.raise_()
    
    @Slot()
    def _cycle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @Slot(bool)
    def cycle_display_show(self, val):
        if val:
            if self.display_frame.isHidden():
                self.display_frame.setGeometry(self.rect())
                self.display_frame.show()
                self.nav_bar.raise_()
            elif self.display_frame.isVisible():
                pass
        else:
            self.display_frame.hide()

    @Slot()
    def _cycle_display_fullwindow(self):
        if self.display_frame.rect() == self.rect():
            self.display_frame.setGeometry(
                self.width() - self.display_frame.minimumWidth() - 7,
                self.height() - self.display_frame.minimumHeight() -7,
                self.display_frame.minimumWidth(),
                self.display_frame.minimumHeight(),
            )
        else:
            self.display_frame.setGeometry(self.rect())
            self.nav_bar.raise_()

    @Slot()
    def _handle_display_double_clicked(self) -> None:
        if not self.display_frame.rect() == self.rect():
            self._cycle_display_fullwindow()
        elif self.display_frame.rect() == self.rect() and not self.isFullScreen():
            self.showFullScreen()
        elif self.display_frame.rect() == self.rect() and self.isFullScreen():
            self.showNormal()

    def displayIsFullWindow(self) -> bool:
        return self.rect() == self.display_frame.rect()

    def keyPressEvent(self, event):
        if self.isFullScreen():
            if event.key() == Qt.Key_Escape:
                self._cycle_fullscreen()
        elif not self.isFullScreen() and self.display_frame.rect() == self.rect():
            if event.key() == Qt.Key_F:
                self._cycle_fullscreen()

        if event.key() == Qt.Key_Space:
            self._controls.cycle_pause()
        else:
            return super().keyPressEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        rect = QRect(QPoint(0, 0), event.oldSize())
        print("\033[96m\nresizeEvent was called", f"{self.rect()}\n\033[0m")
        if self.display_frame.rect() == rect:
            print("\033[96m\nresizeEvent passed first condition\n\033[0m")
            self.display_frame.setGeometry(self.rect())
        elif not self.display_frame.rect() == rect:
            print("\033[96m\nresizeEvent passed second condition\n\033[0m")
            self.display.setGeometry(
                self.width() - self.display_frame.minimumWidth() - 7,
                self.height() - self.display_frame.minimumHeight() -7,
                self.display_frame.minimumWidth(),
                self.display_frame.minimumHeight(),
            )
        return super().resizeEvent(event)