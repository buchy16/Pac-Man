from dataclasses import asdict, dataclass
from pathlib import Path
import json

MAX_USERNAME_LENGTH = 10


# ---------------------------------------------------------------------------
#                                                                  VALIDATION
# pseudo valide, score valide
# PAS d'accès disque, PAS d'input()
# ---------------------------------------------------------------------------

def username_errors(raw_user: object) -> str | None:
    """Checks whether a username complies with the rules.

    Returns a clear error message if there is a problem,
    or None if the username is valid.
    """
    if not isinstance(raw_user, str):
        return "The username must be a string of characters."

    stripped = raw_user.strip()
    if not stripped:
        return "The username can not be left blank."

    if len(stripped) > MAX_USERNAME_LENGTH:
        return (
            f"The username must not exceed {MAX_USERNAME_LENGTH} characters "
            f"({len(stripped)} provided)."
        )

    if not stripped.replace(" ", "").isalnum():
        return "Usernames may only contain letters, numbers and spaces."

    return None


def score_errors(raw_score: object) -> str | None:
    """Checks whether a score is valid (an integer >= 0)."""
    if type(raw_score) is not int:
        return "The score must be an integer."
    if raw_score < 0:
        return "The score can not be negative."
    return None


@dataclass(frozen=True)
class HighScore:
    username: str
    score: int

    def __post_init__(self) -> None:
        """ add custom logic on init """
        username_error = username_errors(self.username)
        if username_error is not None:
            raise ValueError(username_error)
        score_error = score_errors(self.score)
        if score_error is not None:
            raise ValueError(score_error)


# ---------------------------------------------------------------------------
#                                                                    STOCKAGE
# Lire le JSON
# écrire le JSON
# PAS affichage
# ---------------------------------------------------------------------------

class HighScoreStorage:
    """Handles only reading and writing the JSON file to the disk."""

    def __init__(self, file_path: str | Path = "highscores.json") -> None:
        self.file_path = Path(file_path)

    def _json_item_to_highscore(self, item: object) -> HighScore | None:
        """Converts the dictionary from JSON into a valid HighScore."""
        if not isinstance(item, dict):
            return None

        json_user = item.get("username")  # None if the key is missing
        if (username_errors(json_user) is not None):
            return None

        json_score = item.get("score")
        if (score_errors(json_score) is not None):
            return None

        return HighScore(username=json_user.strip(), score=json_score)

    def load_scores(self) -> list[HighScore]:
        """Lit le fichier JSON et retourne la liste des scores valides.

        SANS effet de bord : ne modifie JAMAIS le fichier sur le disque.
        """
        if not self.file_path.exists():
            return []

        try:
            highscores_file = self.file_path.read_text(encoding="utf-8")

            if not highscores_file.strip():
                return []

            highscores_data = json.loads(highscores_file)

        except (OSError, ValueError) as err:
            # NE DOIT RIEN AFFICHER
            print(f"Unreadable score file: {err}")
            return []

        if not isinstance(highscores_data, list):
            # NE DOIT RIEN AFFICHER
            print("Unexpected JSON format (a list was expected).")
            return []

        valid_highscores: list[HighScore] = []
        nb_corrupted_highscores = 0

        for item in highscores_data:
            highscore = self._json_item_to_highscore(item)
            if highscore is not None:
                valid_highscores.append(highscore)
            else:
                nb_corrupted_highscores += 1

        if nb_corrupted_highscores > 0:
            # NE DOIT RIEN AFFICHER
            print(f"{nb_corrupted_highscores} invalid data in the file have been ignored.")

        return valid_highscores

    def _write_all(self, entries: list[HighScore]) -> None:
        """Writes the complete list to the backup file, via a temporary file.

        Using a “.tmp” file, which is then renamed,
        prevents the original file from being corrupted if a crash occurs.
        """

        temp_path = self.file_path.with_name(f"{self.file_path.name}.tmp")
        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(entries, file, default=asdict, ensure_ascii=False, indent=4)
            temp_path.replace(self.file_path)
        except OSError as err:
            # Supprime le fichier s'il existe, sinon ne fait rien
            temp_path.unlink(missing_ok=True)

            # conserve la trace de la cause d’origine :D
            raise OSError(f"Unable to save scores: {err}") from err

    def add_score(self, username: str, score: int) -> None:
        """Checks and saves a new score."""
        user_err = username_errors(username)
        if user_err:
            raise ValueError(f"Invalid username: {user_err}")

        score_err = score_errors(score)
        if score_err:
            raise ValueError(f"Invalid score: {score_err}")

        scores = self.load_scores()
        scores.append(HighScore(username=username.strip(), score=score))
        self._write_all(scores)

    def get_top_scores(self, limit: int = 10) -> list[HighScore]:
        """Returns the N best scores, sorted from highest to lowest."""
        all_scores = self.load_scores()
        return sorted(all_scores, key=lambda e: e.score, reverse=True)[:limit]


# ---------------------------------------------------------------------------
#                                                                         CLI
# saisie et affichage
# RAF du format du fichier
# ---------------------------------------------------------------------------

def prompt_username() -> str:
    """Requires a valid username to be entered."""
    prompt_msg = (
        f"Enter your username (max {MAX_USERNAME_LENGTH} characters, "
        "letters/numbers/spaces) : "
    )
    while True:
        username_entered = input(prompt_msg).strip()
        username_error = username_errors(username_entered)
        if username_error is None:
            return username_entered
        print(f"Error : {username_error}")


def display_best_scores(scores: list[HighScore]) -> None:
    """Displays the score table passed as an argument."""
    if not scores:
        print("No scores have been recorded so far.")
        return

    print("\n------- BEST SCORES -------")
    for rank, entry in enumerate(scores, start=1):
        print(f"{rank:>3}. {entry.username:<12} {entry.score:>12,}")
    print("----------------------------\n")


# ---------------------------------------------------------------------------
#                                                                        MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    my_backup = HighScoreStorage("highscores.json")

    try:
        my_backup.add_score(prompt_username(), 12345)
    except (OSError, ValueError) as err:
        print(f"Highscore not saved: {err}")

    try:
        display_best_scores(my_backup.get_top_scores())
    except (OSError, ValueError) as err:
        print(f"Highscores can not be displayed: {err}")
