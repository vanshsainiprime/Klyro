from datetime import datetime
from pathlib import Path
import subprocess
import tempfile


class ScreenshotService:
    def __init__(self, save_directory=None, image_format="PNG"):
        self.save_directory = Path(
            save_directory
            or Path.home() / "Pictures" / "Klyro"
        )

        self.image_format = image_format.upper()

        self.save_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def set_save_directory(self, directory):
        self.save_directory = Path(directory)
        self.save_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def set_format(self, image_format):
        self.image_format = image_format.upper()

    def _filename(self):
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S_%f"
        )

        extension = {
            "PNG": "png",
            "JPEG": "jpg",
        }.get(self.image_format, "png")

        return (
            self.save_directory
            / f"Screenshot_{timestamp}.{extension}"
        )

    def capture_fullscreen(self):
        return self._capture([])

    def capture_region(self):
        return self._capture(["-s"])

    def _capture(self, scrot_arguments):
        output = self._filename()

        with tempfile.TemporaryDirectory(
            dir=self.save_directory
        ) as temporary_directory:

            temporary_file = (
                Path(temporary_directory)
                / "capture.png"
            )

            try:
                subprocess.run(
                    [
                        "scrot",
                        *scrot_arguments,
                        str(temporary_file),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                if not temporary_file.exists():
                    raise RuntimeError(
                        "Screenshot was not created."
                    )

                if temporary_file.stat().st_size == 0:
                    raise RuntimeError(
                        "Screenshot capture produced an empty file."
                    )

                if self.image_format == "PNG":
                    temporary_file.replace(output)

                elif self.image_format == "JPEG":
                    subprocess.run(
                        [
                            "magick",
                            str(temporary_file),
                            "-quality",
                            "95",
                            str(output),
                        ],
                        check=True,
                        capture_output=True,
                        text=True,
                    )

                else:
                    temporary_file.replace(output)

            except FileNotFoundError as error:
                if error.filename == "scrot":
                    raise RuntimeError(
                        "Screenshot backend is unavailable. "
                        "Please install scrot."
                    )

                raise RuntimeError(
                    "Image conversion requires ImageMagick."
                )

            except subprocess.CalledProcessError as error:
                message = (
                    error.stderr.strip()
                    or "Screenshot capture failed."
                )

                raise RuntimeError(message)

        return output
