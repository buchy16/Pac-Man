from . import mlx


WALLS = {
    0b0000: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0000.png"),
    0b0001: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0001.png"),
    0b0010: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0010.png"),
    0b0011: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0011.png"),
    0b0100: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0100.png"),
    0b0101: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0101.png"),
    0b0110: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0110.png"),
    0b0111: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/0111.png"),
    0b1000: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1000.png"),
    0b1001: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1001.png"),
    0b1010: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1010.png"),
    0b1011: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1011.png"),
    0b1100: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1100.png"),
    0b1101: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1101.png"),
    0b1110: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1110.png"),
    0b1111: mlx.get_tools().mlx_png_file_to_image(mlx.mlx_ptr,
                                                  "assets/Walls/1111.png"),
}

J_WALK_SPRIT = {
    "0J": (mlx.get_tools().
           mlx_png_file_to_image(mlx.mlx_ptr, "assets/Entities/0J.png")[0]),
    "1J_Est": (mlx.get_tools().
               mlx_png_file_to_image(mlx.mlx_ptr,
                                     "assets/Entities/1J_Est.png")[0]),
    "1J_North": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/1J_North.png")[0]),
    "1J_South": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/1J_South.png")[0]),
    "1J_West": (mlx.get_tools().
                mlx_png_file_to_image(mlx.mlx_ptr,
                                      "assets/Entities/1J_West.png")[0]),
    "2J_Est": (mlx.get_tools().
               mlx_png_file_to_image(mlx.mlx_ptr,
                                     "assets/Entities/2J_Est.png")[0]),
    "2J_North": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/2J_North.png")[0]),
    "2J_South": (mlx.get_tools().
                 mlx_png_file_to_image(mlx.mlx_ptr,
                                       "assets/Entities/2J_South.png")[0]),
    "2J_West": (mlx.get_tools().
                mlx_png_file_to_image(mlx.mlx_ptr,
                                      "assets/Entities/2J_West.png")[0]),
}
