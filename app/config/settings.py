import json
from pathlib import Path


class Settings:
    def __init__(self):
        self.config_directory = (
            Path.home() / ".config" / "klyro"
        )
        self.config_file = self.config_directory / "settings.json"

        self.config_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.data = {
            "screenshot_directory": str(
                Path.home() / "Pictures" / "Klyro"
            ),
            "recording_directory": str(
                Path.home() / "Videos" / "Klyro"
            ),
            "screenshot_format": "PNG",
            "recording_fps": 30,
        }

        self.load()

    def load(self):
        if not self.config_file.exists():
            self.save()
            return

        try:
            with self.config_file.open("r", encoding="utf-8") as file:
                saved = json.load(file)

            self.data.update(saved)

        except (OSError, json.JSONDecodeError):
            # Keep safe defaults if the settings file is damaged.
            self.save()

    def save(self):
        with self.config_file.open("w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                indent=4,
            )

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()
