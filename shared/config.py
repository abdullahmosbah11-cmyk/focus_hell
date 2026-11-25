from pathlib import Path

APP_NAME = "focus-hell"

INSTALL_DIR = Path("/opt")  / APP_NAME
DATA_DIR = Path("/var/lib") / APP_NAME
RUN_DIR = Path("/run") / APP_NAME

STATE_FILE = DATA_DIR / "state.json"
DB_FILE = DATA_DIR / "stats.db"
SOCKET_PATH = RUN_DIR / "focus.sock"

MODE_EMBER = "ember"
MODE_INFERNO = "inferno"
MODE_ABYSS = "abyss"

VALID_MODES = (MODE_EMBER, MODE_INFERNO, MODE_ABYSS)

DEFAULT_DURATION_SECONDS = 25 * 60
TICK_INTERVAL_SECONDS = 1