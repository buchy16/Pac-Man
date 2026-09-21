from mlx import Mlx
from typing import Callable
from keysymdef import keysymdef
import time


class Mlx_Engine():
    """High-level engine that wraps MLX window management and the main loop.

    The engine owns the MLX instance, keeps track of created windows, exposes
    a loop timer, and wires the update/draw callbacks into the MLX event loop.
    """

    def __init__(self) -> None:
        """Initialize the MLX engine and prepare the window registry.

        The constructor creates the underlying MLX object, initializes the MLX
        context, builds the X11 keysym lookup table, and records the initial
        timestamp used to compute the frame timer.

        Raises:
            ValueError: If the MLX context cannot be created.
        """
        self.m = Mlx()
        self._mlx_ptr = self.m.mlx_init()
        self._windows: dict[str, int] = {}  # key = Window_name, value = ptr

        if (self._mlx_ptr is None):
            raise (ValueError("Error while creating mlx_ptr"))

        # keysym_X11 dic reference {key_code: kay_name}
        self.KEYNAME = {x[1]: x[0] for x in keysymdef}

        self.last_tick = time.monotonic_ns()
        self._timer = 0.0

    def get_tools(self) -> Mlx:
        """Return the underlying MLX wrapper instance.

        Returns:
            Mlx: The wrapped MLX helper object used by the engine.
        """
        return self.m

    @property
    def mlx_ptr(self) -> int | None:
        """Get the raw MLX context pointer.

        Returns:
            int | None: The MLX context pointer, or ``None`` if initialization
                failed before the engine could be created.
        """
        return self._mlx_ptr

    @property
    def windows(self) -> dict[str, int]:
        """Get the registry of windows managed by the engine.

        Returns:
            dict[str, int]: A mapping of window names to MLX window pointers.
        """
        return self._windows

    @property
    def timer(self) -> float:
        """Get the duration of the last loop iteration in seconds.

        Returns:
            float: The elapsed time, in seconds, computed at the end of the
                most recent main-loop cycle.
        """
        return self._timer

    def new_window(self, w: int, h: int, name: str) -> bool:
        """Create and register a new MLX window.

        Args:
            w: Window width in pixels.
            h: Window height in pixels.
            name: Unique name used to store the window in the registry.

        Returns:
            bool: ``True`` when the window is created and registered
            successfully, otherwise ``False``.
        """
        window = self.m.mlx_new_window(self.mlx_ptr, w, h, name)

        if (window is None):
            print("Error while creating windows")
            return (False)
        self.windows[name] = window
        return (True)

    def _exit(self, keynum, mlx_tools) -> None:
        """Handle exit requests triggered by the MLX key hook.

        Args:
            keynum: Key code received from MLX.
            mlx_tools: Two-item tuple containing the MLX context pointer and
                the window pointer associated with the hook.

        Returns:
            None: This callback only performs side effects.

        Notes:
            Pressing Escape or receiving a zero key code closes the window and
            stops the MLX event loop.
        """
        mlx_ptr, screen = mlx_tools

        if (self.KEYNAME[keynum] == "Escape" or keynum == 0):
            self.m.mlx_destroy_window(mlx_ptr, screen)
            self.m.mlx_loop_exit(mlx_ptr)

    def run(self, update: Callable, draw: Callable) -> None:
        """Start the MLX main loop and execute the game callbacks.

        Args:
            update: Callback executed once per loop iteration before drawing.
            draw: Callback executed once per loop iteration after updating.

        Returns:
            None: The method blocks while the MLX loop is running.

        Notes:
            The engine clears every registered window after each frame and
            updates ``timer`` with the elapsed time since the previous tick.
        """
        def run_app(args: None) -> None:
            """Execute one application frame inside the MLX loop.

            Args:
                args: Unused MLX callback argument.

            Returns:
                None: The callback only drives update, draw, and timing.
            """
            update()
            draw()
            for window in self.windows.values():
                self.m.mlx_clear_window(self.mlx_ptr, window)
            elapsed = (time.monotonic_ns() - self.last_tick) // 1000000
            self._timer = elapsed / 1000

        for window in self.windows.values():
            self.m.mlx_clear_window(self.mlx_ptr, window)
            self.m.mlx_key_hook(window, self._exit, (self.mlx_ptr, window))

        self.m.mlx_loop_hook(self.mlx_ptr, run_app, None)
        self.m.mlx_loop(self.mlx_ptr)


mlx = Mlx_Engine()
