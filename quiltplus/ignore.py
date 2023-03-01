# Manage GitIgnore

from pathlib import Path

IGNORE_FILE = ".gitignore"


class GitIgnore:
    def __init__(self):
        self.path = Path(IGNORE_FILE)
        lines = self.path.read_text().splitlines() if self.path.exists() else []
        self._lines = set(lines)

    def lines(self):
        return list(self._lines)

    def size(self):
        return len(self._lines)

    def text(self):
        return "\n".join(self.lines())

    def save(self):
        self.path.write_text(self.text())

    def ignore(self, files):
        self._lines = self._lines.union(set(files))
        return self.lines()

    def unignore(self, files):
        self._lines = self._lines - set(files)
        return self.lines()
