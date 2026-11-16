import logging
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


PATH_SCORES = "src/data/highscores.json"
MAX_USERNAME_LENGTH = 10

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
#                                                                  VALIDATION
# ---------------------------------------------------------------------------

def username_errors(raw_user: object) -> str | None:
    """Checks whether a username complies with the rules.

    Returns a clear error message if there is a problem,
    or `None` if the username is valid.
    """
    if not isinstance(raw_user, str):
        return "The username must be a string of characters."

    stripped = raw_user.strip()
    if not stripped:
        return "The username can not be only spaces neither left blank."

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
#                                                                     STORAGE
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LoadResult:
    """Full result of an attempt to read the file.

    entries: list of valid highscores
    corrupted: True if the file existed but content could not be fully parsed
    (invalid JSON, unexpected structure, or at least one invalid entry).
    """
    entries: list["HighScore"]
    corrupted: bool


class HighScoreStorage:
    """Handles only reading and writing the JSON file to the disk."""

    def __init__(self, file_path: str | Path = PATH_SCORES) -> None:
        self.file_path = Path(file_path)

    def _json_item_to_highscore(self, item: object) -> HighScore | None:
        """Converts the dictionary from JSON into a valid HighScore."""
        if not isinstance(item, dict):
            return None

        json_user = item.get("username")
        if (username_errors(json_user) is not None):
            return None

        json_score = item.get("score")
        if (score_errors(json_score) is not None):
            return None

        return HighScore(username=str(json_user).strip(),
                         score=int(json_score or 0))

    def _load_raw(self) -> LoadResult:
        """Handles reading/decoding/validation of scores stored in JSON file
        Returns:
            empty list, not corrupted if File not found or Empty file;
            empty list, corrupted if Malformed JSON or Not a list
            else
            list of valid scores and corrupted set to True if nb_corrupted > 0
        """
        if not self.file_path.exists():
            return LoadResult(entries=[], corrupted=False)

        content = self.file_path.read_text(encoding="utf-8")

        if not content.strip():
            return LoadResult(entries=[], corrupted=False)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as err:
            logger.warning("Scores file: invalid JSON (%s).", err)
            return LoadResult(entries=[], corrupted=True)

        if not isinstance(data, list):
            logger.warning("Scores file: a JSON list was expected.")
            return LoadResult(entries=[], corrupted=True)

        valid_entries: list[HighScore] = []
        nb_corrupted = 0
        for item in data:
            entry = self._json_item_to_highscore(item)
            if entry is not None:
                valid_entries.append(entry)
            else:
                nb_corrupted += 1

        if nb_corrupted:
            logger.warning(
                "%d Invalid entry(ies) ignored in the score file.",
                nb_corrupted,
            )

        return LoadResult(entries=valid_entries, corrupted=nb_corrupted > 0)

    def load_scores(self) -> list["HighScore"]:
        """Reads the JSON file and returns the list of valid scores.

        Return: only the first argument returned by _load_raw().
        """
        return self._load_raw().entries

    def _copy_corrupted_file(self) -> None:
        """Set the corrupted file aside before it is overwritten.
        If the copy fails, the original file remains in place, intact.
        """
        if not self.file_path.exists():
            return  # rien à mettre en quarantaine

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        copy_path = self.file_path.with_name(
            f"{self.file_path.name}.corrupt-{timestamp}"
        )

        try:
            shutil.copy2(self.file_path, copy_path)
        except OSError as err:
            raise OSError(
                f"Unable to copy the corrupted file,"
                f"operation cancelled: {err}"
            ) from err

        logger.warning("Corrupted file placed in quarantine: %s", copy_path)

    def _write_all(self, entries: list[HighScore]) -> None:
        """Writes the complete list to the backup file, via a temporary file.

        Using a “.tmp” file, which is then renamed,
        prevents the original file from being corrupted if a crash occurs.
        """

        temp_path = self.file_path.with_name(f"{self.file_path.name}.tmp")
        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(entries, file, default=asdict,
                          ensure_ascii=False, indent=4)
            temp_path.replace(self.file_path)
        except OSError as err:
            temp_path.unlink(missing_ok=True)

            raise OSError(f"Unable to save scores: {err}") from err

    def add_score(self, username: str, score: int) -> None:
        """Validates and saves a new score."""
        user_err = username_errors(username.strip())

        if user_err:
            raise ValueError(f"Invalid username: {user_err}")

        score_err = score_errors(score)
        if score_err:
            raise ValueError(f"Invalid score: {score_err}")

        result = self._load_raw()
        if result.corrupted:
            self._copy_corrupted_file()

        entries = result.entries
        entries.append(HighScore(username=username.strip(), score=score))
        self._write_all(entries)

    def get_top_scores(self, limit: int = 10) -> list[HighScore]:
        """Returns the best scores, sorted from highest to lowest."""
        all_scores = self.load_scores()
        return sorted(all_scores, key=lambda e: e.score, reverse=True)[:limit]

# ---------------------------------------------------------------------------
#                                                                         CLI
# ---------------------------------------------------------------------------


def prompt_username() -> str:
    """Requires a valid username to be entered."""
    prompt_msg = (
        f"Enter your username (max {MAX_USERNAME_LENGTH} characters, "
        "only letters/numbers/spaces) : "
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
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    my_backup = HighScoreStorage()

    try:
        my_backup.add_score(prompt_username(), 4321)
    except (OSError, ValueError) as err:
        print("Highscore not saved:", err)

    try:
        display_best_scores(my_backup.get_top_scores())
    except (OSError, ValueError) as err:
        print("Highscores can not be displayed:", err)
