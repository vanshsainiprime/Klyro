from datetime import datetime
from pathlib import Path
import subprocess


class RecordingService:
    def __init__(self, save_directory=None):
        self.save_directory = Path(
            save_directory or Path.home() / "Videos" / "Klyro"
        )
        self.save_directory.mkdir(parents=True, exist_ok=True)

        self.process = None
        self.current_file = None

    def set_save_directory(self, directory):
        self.save_directory = Path(directory)
        self.save_directory.mkdir(parents=True, exist_ok=True)

    def set_fps(self, fps):
        self.fps = int(fps)

    @property
    def is_recording(self):
        return self.process is not None

    def start(self):
        if self.is_recording:
            raise RuntimeError("A recording is already running.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output = self.save_directory / f"Recording_{timestamp}.mp4"

        display = ":0"

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "x11grab",
            "-video_size",
            self._screen_size(),
            "-framerate",
            str(self.fps),
            "-i",
            display,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-pix_fmt",
            "yuv420p",
            str(output),
        ]

        try:
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            raise RuntimeError("FFmpeg is not installed.")

        self.current_file = output

    def stop(self):
        if not self.is_recording:
            return None

        self.process.stdin.write(b"q\n")
        self.process.stdin.flush()

        self.process.wait()

        output = self.current_file

        self.process = None
        self.current_file = None

        return output

    def _screen_size(self):
        result = subprocess.run(
            [
                "xdpyinfo",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in result.stdout.splitlines():
            if "dimensions:" in line:
                return line.split()[1]

        raise RuntimeError("Unable to determine screen resolution.")
