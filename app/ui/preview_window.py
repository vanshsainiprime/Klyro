import subprocess
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf


class ScreenshotPreview(Gtk.Window):
    def __init__(self, image_path, on_delete=None):
        super().__init__(
            title="Screenshot",
            default_width=700,
            default_height=500,
            modal=True,
        )

        self.image_path = Path(image_path)
        self.on_delete_callback = on_delete

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )

        image = Gtk.Image()

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                str(self.image_path),
                650,
                380,
                True,
            )
            image.set_from_pixbuf(pixbuf)
        except Exception:
            image.set_from_icon_name("image-missing")

        main_box.append(image)

        filename = Gtk.Label(label=self.image_path.name)
        filename.add_css_class("dim-label")
        main_box.append(filename)

        buttons = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            halign=Gtk.Align.CENTER,
        )

        back_button = Gtk.Button(label="← Back")
        save_button = Gtk.Button(label="Save")
        copy_button = Gtk.Button(label="Copy")
        open_button = Gtk.Button(label="Open")
        delete_button = Gtk.Button(label="Delete")

        copy_button.add_css_class("suggested-action")
        delete_button.add_css_class("destructive-action")

        back_button.connect("clicked", lambda button: self.close())
        save_button.connect("clicked", self.on_save)
        copy_button.connect("clicked", self.on_copy)
        open_button.connect("clicked", self.on_open)
        delete_button.connect("clicked", self.on_delete)

        buttons.append(back_button)
        buttons.append(save_button)
        buttons.append(copy_button)
        buttons.append(open_button)
        buttons.append(delete_button)

        main_box.append(buttons)

        self.set_child(main_box)

    def on_save(self, button):
        self.close()

    def on_copy(self, button):
        try:
            subprocess.run(
                [
                    "xclip",
                    "-selection",
                    "clipboard",
                    "-target",
                    "image/png",
                    "-i",
                    str(self.image_path),
                ],
                check=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    def on_open(self, button):
        try:
            subprocess.Popen(
                ["xdg-open", str(self.image_path)]
            )
        except FileNotFoundError:
            pass

    def on_delete(self, button):
        try:
            self.image_path.unlink(missing_ok=True)
        finally:
            if self.on_delete_callback:
                self.on_delete_callback()

            self.close()


class RecordingPreview(Gtk.Window):
    def __init__(self, video_path, on_delete=None):
        super().__init__(
            title="Recording",
            default_width=550,
            default_height=300,
            modal=True,
        )

        self.video_path = Path(video_path)
        self.on_delete_callback = on_delete

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=16,
            margin_top=24,
            margin_bottom=24,
            margin_start=24,
            margin_end=24,
        )

        title = Gtk.Label(label="🎥 Recording Complete")
        title.add_css_class("title-2")

        filename = Gtk.Label(label=self.video_path.name)
        filename.add_css_class("dim-label")

        location = Gtk.Label(
            label=f"Saved to:\n{self.video_path.parent}"
        )

        buttons = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            halign=Gtk.Align.CENTER,
        )

        back_button = Gtk.Button(label="← Back")
        open_button = Gtk.Button(label="▶ Open")
        reveal_button = Gtk.Button(label="📁 Reveal")
        delete_button = Gtk.Button(label="🗑 Delete")

        open_button.add_css_class("suggested-action")
        delete_button.add_css_class("destructive-action")

        back_button.connect("clicked", lambda button: self.close())
        open_button.connect("clicked", self.on_open)
        reveal_button.connect("clicked", self.on_reveal)
        delete_button.connect("clicked", self.on_delete)

        buttons.append(back_button)
        buttons.append(open_button)
        buttons.append(reveal_button)
        buttons.append(delete_button)

        main_box.append(title)
        main_box.append(filename)
        main_box.append(location)
        main_box.append(buttons)

        self.set_child(main_box)

    def on_open(self, button):
        try:
            subprocess.Popen(
                ["xdg-open", str(self.video_path)]
            )
        except FileNotFoundError:
            pass

    def on_reveal(self, button):
        try:
            subprocess.Popen(
                ["xdg-open", str(self.video_path.parent)]
            )
        except FileNotFoundError:
            pass

    def on_delete(self, button):
        try:
            self.video_path.unlink(missing_ok=True)
        finally:
            if self.on_delete_callback:
                self.on_delete_callback()

            self.close()
