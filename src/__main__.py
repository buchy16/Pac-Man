import mlx
from mazegenerator import MazeGenerator
# from keysymdef import keysymdef
from . import KEYNAME

m = mlx.Mlx()


def get_maze(display: bool = False) -> None:
    maze = MazeGenerator()
    maze.generate()
    if (display is True):
        print(maze.maze)


def exit(keynum, mlx_tools):
    mlx_ptr, screen = mlx_tools

    print("Key id is = ", keynum, "name is = ", KEYNAME[keynum])

    if (keynum == 65307 or KEYNAME[keynum] == "BackSpace"):
        m.mlx_destroy_window(mlx_ptr, screen)
        m.mlx_loop_exit(mlx_ptr)


def engine(i: int) -> None:
    i += 1
    print(i // 10000)


def main():
    print("begining tests")

    get_maze()

    mlx_ptr = m.mlx_init()
    screen = m.mlx_new_window(mlx_ptr, 256, 256, "Pac-man")

    m.mlx_clear_window(mlx_ptr, screen)

    m.mlx_string_put(mlx_ptr, screen, 128, 128, 255, ":D")

    m.mlx_key_hook(screen, exit, (mlx_ptr, screen))

    m.mlx_loop_hook(mlx_ptr, engine, 0)
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
