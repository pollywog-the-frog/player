from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QMouseEvent

from Player.core.mediastream import MediaStream
from Player.core.MpvStatus import MpvStatus
from Player.ui.components.VideoControls import VideoControls

from OpenGL import GL, EGL

from mpv import MPV, MpvRenderContext, MpvGlGetProcAddressFn

import ctypes

def get_process_address(_, name):
    address = EGL.eglGetProcAddress(name.decode('utf-8'))
    return ctypes.cast(address, ctypes.c_void_p).value

class MpvWidget(QOpenGLWidget):
    def __init__(self, stream: MediaStream | None, parent: QWidget | None = None):
        super().__init__(parent=parent)

        # Set mouse tracking
        self.setMouseTracking(True)

        # Set update behavior
        self.setUpdateBehavior(QOpenGLWidget.NoPartialUpdate)

        # Define function to get process address
        self._proc_addr_wrapper = MpvGlGetProcAddressFn(get_process_address)

        # Initialize render context to None
        self.ctx: MpvRenderContext | None = None
        
        # import locale
        import locale

        # Set locale for MPV
        locale.setlocale(locale.LC_NUMERIC, 'C')

        # Initialize _player
        self._player: MPV = MPV(
            ytdl=True,
            log_handler=print,
            loglevel='info',
            hwdec='no',
            vo='libmpv',
        )
        
        # Define status object
        self.status = MpvStatus(self._player)

        # Define layout for video controls
        v_layout = QVBoxLayout(self)

        self.video_controls = VideoControls(self, mpv_instance=self._player, status=self.status, stream=stream)

        # Add video controls to v_layout
        v_layout.addWidget(self.video_controls)

        # Hide video_controls
        self.video_controls.hide()

        # Define timer
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.video_controls.hide)

    def initializeGL(self) -> None:
        print('\033[91minitializeGL called\033[0m')
        self.makeCurrent()
        self.ctx = MpvRenderContext(self._player, 'opengl',
                                    opengl_init_params={'get_proc_address': self._proc_addr_wrapper})
        self.ctx.update_cb = self.on_update

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
        if self.window().isMinimized():
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
        self.video_controls.showFullScreen()
        if self.status.playing:
            self.timer.start()
        return super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        self._player.command('cycle', 'pause')
        return super().mousePressEvent(event)

    def closeEvent(self, event) -> None:
        self.makeCurrent()
        if self.ctx:
            self.ctx.free()
        self._player.terminate()

    def play_all(self, video_url: str, audio_url: str) -> None:
        self._player.play(video_url)
        self._player.wait_until_playing()
        self._player.audio_add(audio_url)
    
    def play_video(self, video_url: str) -> None:
        self._player.play(video_url)

    def play_audio(self, audio_url: str) -> None:
        self._player.play(audio_url)

    def stop(self) -> None:
        self._player.stop()