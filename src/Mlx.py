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

        # key = Window_name, value = list of key_hook_functions
        self.key_hook_functions: dict[str, list[Callable]] = {}
        # key = Window_name, value = list of mouse_hook_functions
        self.mouse_hook_functions: dict[str, list[Callable]] = {}

        self._start_time = time.monotonic_ns()
        self._timer = 0.0
        self.last_tick = self.timer

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

    def add_key_hook_function(self, function: Callable,
                              window_name: str):
        """Link a function with the window's keys events specified in args

        Args:
            function (Callable): function to link with a specified window
            window_name (str): name of the window
        """
        self.key_hook_functions[window_name].append(function)

    def rm_key_hook_function(self, function: Callable,
                             window_name: str) -> bool:
        """Unlink a function with the window's keys events specified in args

        Args:
            function (Callable): function to unlink with a specified window
            window_name (str): name of the window

        Returns:
            bool: True if the function was unlinked successfuly otherwise Else
        """
        try:
            self.key_hook_functions[window_name].remove(function)
        except (ValueError):
            print("Warning, you are trying to remove a function that is not \
linked to this window ")
            return (False)
        return (True)

    def add_mouse_hook_function(self, function: Callable,
                                window_name: str):
        """Link a function with the window's mouse events specified in args

        Args:
            function (Callable): function to link with a specified window
            window_name (str): name of the window
        """
        self.mouse_hook_functions[window_name].append(function)

    def rm_mouse_hook_function(self, function: Callable,
                               window_name: str) -> bool:
        """Unlink a function with the window's mouse events specified in args

        Args:
            function (Callable): function to unlink with a specified window
            window_name (str): name of the window

        Returns:
            bool: True if the function was unlinked successfuly otherwise Else
        """
        try:
            self.mouse_hook_functions[window_name].remove(function)
        except (ValueError):
            print("Warning, you are trying to remove a function that is not \
linked to this window ")
            return (False)
        return (True)

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
        self.key_hook_functions[name] = []
        self.mouse_hook_functions[name] = []

        self.m.mlx_key_hook(window, self._do_key_functions, name)
        self.m.mlx_mouse_hook(window, self._do_mouse_functions, name)
        return (True)

    def close_window(self, window_name: str) -> None:
        self.key_hook_functions = {key: item for key, item in
                                   self.key_hook_functions.items()
                                   if key != window_name}
        self.mouse_hook_functions = {key: item for key, item in
                                     self.mouse_hook_functions.items()
                                     if key != window_name}
        self.m.mlx_destroy_window(self.mlx_ptr, self.windows[window_name])
        del self.windows[window_name]

    def _do_key_functions(self, keynum: int, window_name: str) -> None:
        """Listen for key action and pass them to all function linked
        with their windows

        Args:
            keynum (int): Value of the key catched (keysym_X11)
            window_name (str): name of the window
        """
        if (keynum == 0 or self.KEYNAME[keynum] == "Escape"):
            self.m.mlx_destroy_window(self.mlx_ptr, self.windows[window_name])
            self.m.mlx_loop_exit(self.mlx_ptr)

        for function in self.key_hook_functions[window_name]:
            function(keynum)

    def _do_mouse_functions(self, button: int, mouse_x: int,
                            mouse_y: int, window_name: str) -> None:
        """Listen for mouse action and pass them to all function linked
        with their windows

        Args:
            keynum (int): ?
            window_name (str): name of the window
        """
        for function in self.mouse_hook_functions[window_name]:
            function(button, mouse_x, mouse_y)

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

            if (self.timer - self.last_tick >= 0.016):
                update()
                for window in self.windows.values():
                    self.m.mlx_clear_window(self.mlx_ptr, window)
                draw()
                self.last_tick = self.timer
                self.get_tools().mlx_do_sync(self.mlx_ptr)

            elapsed = (time.monotonic_ns() - self._start_time) // 1000000
            self._timer = elapsed / 1000

            # print("Mouse", self.mouse_hook_functions)
            # print("Keys", self.key_hook_functions)

        for window in self.windows.values():
            self.m.mlx_clear_window(self.mlx_ptr, window)

        self.m.mlx_loop_hook(self.mlx_ptr, run_app, None)
        self.m.mlx_loop(self.mlx_ptr)

    def close_app(self) -> None:
        """Manually close all opened windows
        """
        for name in self.windows.keys():
            self._do_key_functions(0, name)


mlx = Mlx_Engine()
