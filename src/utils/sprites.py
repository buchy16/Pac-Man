# from typing import Any
from ..Mlx import mlx
from .directions import Direction
from .paths import resource_path

# to use the “fixed or non-fixed executable” logic
ASSETS_DIR = resource_path("assets")


WALLS = {
    0b0000: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0000.png")
    ),
    0b0001: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0001.png")
    ),
    0b0010: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0010.png")
    ),
    0b0011: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0011.png")
    ),
    0b0100: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0100.png")
    ),
    0b0101: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0101.png")
    ),
    0b0110: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0110.png")
    ),
    0b0111: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/0111.png")
    ),
    0b1000: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1000.png")
    ),
    0b1001: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1001.png")
    ),
    0b1010: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1010.png")
    ),
    0b1011: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1011.png")
    ),
    0b1100: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1100.png")
    ),
    0b1101: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1101.png")
    ),
    0b1110: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1110.png")
    ),
    0b1111: mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Walls/1111.png")
    ),
}

J_WALK_SPRIT = {
    "0J": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/0J.png")
    )[0],
    "1J_Est": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/1J_Est.png")
    )[0],
    "1J_North": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/1J_North.png")
    )[0],
    "1J_South": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/1J_South.png")
    )[0],
    "1J_West": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/1J_West.png")
    )[0],
    "2J_Est": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/2J_Est.png")
    )[0],
    "2J_North": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/2J_North.png")
    )[0],
    "2J_South": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/2J_South.png")
    )[0],
    "2J_West": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Entities/2J_West.png")
    )[0],
}

MENU = {
    "Start Game": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Start_game.png")
    )[0],
    "View_Highscores": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/View_Highscores.png")
    )[0],
    "Instructions": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Instructions.png")
    )[0],
    "Exit": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Exit.png")
    )[0],
    "Start Game b": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Start_game_b.png")
    )[0],
    "View_Highscores b": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/View_Highscores_b.png")
    )[0],
    "Instructions b": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Instructions_b.png")
    )[0],
    "Exit b": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Exit_b.png")
    )[0],
    "Instructions_img": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Instructions.png")
    )[0],
    "PTS": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/PTS.png")
    )[0],
    "Resume": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Resume.png")
    )[0],
    "Resume b": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Resume_b.png")
    )[0],
}

DIGITS = {
    "0": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/0.png")
    )[0],
    "1": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/1.png")
    )[0],
    "2": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/2.png")
    )[0],
    "3": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/3.png")
    )[0],
    "4": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/4.png")
    )[0],
    "5": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/5.png")
    )[0],
    "6": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/6.png")
    )[0],
    "7": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/7.png")
    )[0],
    "8": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/8.png")
    )[0],
    "9": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/9.png")
    )[0],
    "-": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Texts/-.png")
    )[0],
}

ALPHA = mlx.get_tools().mlx_png_file_to_image(
    mlx.mlx_ptr, str(ASSETS_DIR / "Texts/Alpha.png")
)[0]

PACGUMS = {
    "Pacgum": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Pacgums/Pacgum.png")
    )[0],
    "Super pacgum": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Pacgums/Super_Pacgum.png")
    )[0],
    "No pacgum": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Pacgums/No_pacgum.png")
    )[0],
}


DIRECTIONS = (Direction.NORTH, Direction.EAST,
              Direction.SOUTH, Direction.WEST)
G_WALK_KEYS = ["1b", "2b", "1c", "2c", "1i", "2i", "1p", "2p",
               "1blue", "2blue", "1white", "2white", "eyes"]
G_WALK_SPRITES: dict[str, dict[Direction, int]] = {}
for key in G_WALK_KEYS:
    G_WALK_SPRITES[key] = {}
    for direction in DIRECTIONS:
        img_path = ASSETS_DIR / "Entities" / f"{key}_{direction.label}.png"
        image = mlx.get_tools().mlx_png_file_to_image(
            mlx.mlx_ptr, str(img_path)
        )[0]
        G_WALK_SPRITES[key][direction] = image

BACKGROUNDS = {
    "Pause menu": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Background/Pause_menu_Background.png")
    )[0],
    "Game over": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Background/Game_over.png")
    )[0],
    "You won": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "Background/You_won.png")
    )[0],
}

HUD = {
    "Lives": mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "HUD/Lives.png")
    )[0],
    "exp": (mlx.get_tools().mlx_png_file_to_image(
        mlx.mlx_ptr, str(ASSETS_DIR / "HUD/exp(lives).png")
    )[0]),
}


def second_impact() -> None:
    """Destroy all assets to free the memory
    """
    dict_assets = [J_WALK_SPRIT, MENU, DIGITS, PACGUMS, BACKGROUNDS, HUD]

    for dict_asset in dict_assets:
        for asset in dict_asset.values():
            mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, asset)

    for asset in WALLS.values():
        mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, asset[0])

    for ghost_asstes in G_WALK_SPRITES.values():
        for asset in ghost_asstes.values():
            mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, asset)

    mlx.get_tools().mlx_destroy_image(mlx.mlx_ptr, ALPHA)
