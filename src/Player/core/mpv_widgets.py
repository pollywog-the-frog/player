from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot, Signal, Property
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QMouseEvent, QKeyEvent

from Player.core.mediastream import MediaStream
from Player.core.mpvstatus import MpvStatus
from Player.core.qtmpvstatus import QtMpvStatus
from Player.ui.components.vid_controls import VideoControls

from OpenGL import GL, EGL

from mpv import MPV, MpvRenderContext, MpvGlGetProcAddressFn

import ctypes

def get_process_address(_, name):
    address = EGL.eglGetProcAddress(name.decode('utf-8'))
    return ctypes.cast(address, ctypes.c_void_p).value

class MpvDisplay(QOpenGLWidget):

    doubleClicked = Signal()

    def __init__(self, mpv_instance: MPV, main_window: QMainWindow, **kwargs):
        super().__init__(**kwargs)

        # Define main_window
        self.main_window = main_window

        # Define self._controls
        self._controls: MpvControls = self.main_window.controls

        # Define function to get process address
        self._proc_addr_wrapper = MpvGlGetProcAddressFn(get_process_address)

        # Initialize render context to None
        self.ctx: MpvRenderContext = None

        # Initialize _player
        self._player = mpv_instance

        # Set mouse tracking
        self.setMouseTracking(True)

        # Set Focus policy
        self.setFocusPolicy(Qt.StrongFocus)

        # Set update behavior
        self.setUpdateBehavior(QOpenGLWidget.NoPartialUpdate)

        # Define video controls
        self.video_controls = VideoControls(main_window=self.main_window, parent=self, status=self.main_window.qtstatus)

        # Hide video_controls
        self.video_controls.hide()

        # Define timer
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.video_controls.hide)
        self.timer.timeout.connect(self.main_window.nav_bar.conditionalHide)

        # Setup other signals
        #self.qtstatus.file_loadedChanged.connect(self._cycle_show)

    def initializeGL(self) -> None:
        print('\033[91minitializeGL called\033[0m')
        self.makeCurrent()
        if self.ctx is not None:
            self.ctx.update_cb = None
            self.ctx.free()
            self.ctx = None
        self.ctx = MpvRenderContext(self._player, 'opengl',
                                    opengl_init_params={'get_proc_address': self._proc_addr_wrapper})
        self.ctx.update_cb = self.on_update
        self.doneCurrent()

    def paintGL(self) -> bool:
        print('\033[91mpaintGL called\033[0m')
        if self.ctx:
            factor = self.devicePixelRatioF()
            rect = self.rect()

            width = rect.width() * factor
            height = rect.height() * factor

            fbo = self.defaultFramebufferObject()
            self.ctx.render(flip_y=True, opengl_fbo={'w': int(width), 'h': int(height), 'fbo': fbo})
            return True
        return False
    
    @Slot()
    def maybe_update(self) -> None:
        if self.main_window.isMinimized():
            self.makeCurrent()
            self.paintGL()
            self.context().swapBuffers(self.context().surface())
            self.swapped()
            self.doneCurrent()
        else:
            self.update()

    def on_update(self, ctx=None) -> None:
        # maybe_update method should run on the thread that creates the OpenGLContext,
        # which in general is the main thread. QMetaObject.invokeMethod can
        # do this trick.
        QMetaObject.invokeMethod(self, 'maybe_update', Qt.ConnectionType.QueuedConnection)

    def on_update_fake(self, ctx=None) -> None:
        pass

    def swapped(self) -> None:
        if self.ctx:
            self.ctx.render()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.video_controls.show()
        self.main_window.nav_bar.show()
        if self.main_window.status.playing:
            self.timer.start()
        return super().mouseMoveEvent(event)
    
    # def mousePressEvent(self, event: QMouseEvent):
    #     self._controls.cycle_pause()
    #     return super().mousePressEvent(event)
    
    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     self.doubleClicked.emit()
    #     return super().mouseDoubleClickEvent(event)
    
    # def keyPressEvent(self, event: QKeyEvent):
    #     if event.key() == Qt.Key_Space:
    #         self._controls.cycle_pause()
    #     else:
    #         return super().keyPressEvent(event)
        
    def resizeEvent(self, e):
        self.video_controls.setGeometry(self.rect())
        return super().resizeEvent(e)

    def closeEvent(self, event) -> None:
        self.makeCurrent()
        if self.ctx:
            self.ctx.free()
        self._controls.terminate()

    @Slot(bool)
    def _cycle_show(self, val):
        print('\033[96m', f'loaded: {self.main_window.status.file_loaded}', f'hidden: {self.isHidden()}', f'playing: {self.main_window.status.playing}', '\033[0m', sep="\t")
        if val:
            if self.isHidden():
                self.show()
            elif self.isVisible():
                pass
        else:
            self.hide()

    def initalize_media(self, stream: MediaStream) -> None:
        self.video_controls.control_bar.initializeMetaData(stream)

class MpvControls():
    def __init__(self, mpv_instance: MPV):
        self._player = mpv_instance
        self.stream: MediaStream = None

    def play_all(self) -> None:
        try:
            self._player.play(self.stream.video_url)
            self._player.wait_until_playing()
            self._player.audio_add(self.stream.audio_url)
        except AttributeError:
            self._player.play(self.stream.video_url)
        except AttributeError:
            pass
    
    def play_video(self) -> None:
        try:
            self._player.play(self.stream.video_url)
        except AttributeError:
            pass

    def play_audio(self) -> None:
        try:
            self._player.play(self.stream.audio_url)
        except AttributeError:
            pass

    def cycle_pause(self):
        self._player.command('cycle', 'pause')
    
    def stop(self) -> None:
        self._player.stop()

    def seek(self, val) -> None:
        self._player.command('seek', val, 'absolute-percent')
    
    def terminate(self) -> None:
        self._controls.terminate()

    def initalize_media(self, stream: MediaStream) -> None:
        self.stop()
        self.stream = stream