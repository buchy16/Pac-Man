import mlx
from mazegenerator import MazeGenerator

m = mlx.Mlx()


def get_maze(display: bool = False) -> None:
    maze = MazeGenerator()
    maze.generate()
    if (display is True):
        print(maze.maze)


def exit(keynum, mlx_tools):
    mlx_ptr, screen = mlx_tools

    m.mlx_destroy_window(mlx_ptr, screen)
    m.mlx_loop_exit(mlx_ptr)


def main():
    print("begining tests")

    get_maze()

    m = mlx.Mlx()

    mlx_ptr = m.mlx_init()
    screen = m.mlx_new_window(mlx_ptr, 256, 256, "Pac-man")

    m.mlx_clear_window(mlx_ptr, screen)

    m.mlx_string_put(mlx_ptr, screen, 128, 128, 255, ":D")

    m.mlx_key_hook(screen, exit, (mlx_ptr, screen))

    m.mlx_loop(mlx_ptr)

    m.mlx_destroy_window(mlx_ptr, screen)
    m.mlx_loop_exit(mlx_ptr)


if __name__ == "__main__":
    main()
