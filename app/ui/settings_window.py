import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class SettingsWindow(Gtk.Window):
    def __init__(self, settings, on_saved=None):
        super().__init__(
            title="Klyro Settings",
            default_width=550,
            default_height=450,
            modal=True,
        )

        self.settings = settings
        self.on_saved_callback = on_saved

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=20,
            margin_top=24,
            margin_bottom=24,
            margin_start=24,
            margin_end=24,
        )

        title = Gtk.Label(label="Settings")
        title.add_css_class("title-1")
        main_box.append(title)

        general_label = Gtk.Label(label="General")
        general_label.add_css_class("title-3")
        general_label.set_halign(Gtk.Align.START)
        main_box.append(general_label)

        screenshot_label = Gtk.Label(
            label="Screenshot save location"
        )
        screenshot_label.set_halign(Gtk.Align.START)

        self.screenshot_entry = Gtk.Entry()
        self.screenshot_entry.set_text(
            self.settings.get("screenshot_directory")
        )

        main_box.append(screenshot_label)
        main_box.append(self.screenshot_entry)

        recording_label = Gtk.Label(
            label="Recording save location"
        )
        recording_label.set_halign(Gtk.Align.START)

        self.recording_entry = Gtk.Entry()
        self.recording_entry.set_text(
            self.settings.get("recording_directory")
        )

        main_box.append(recording_label)
        main_box.append(self.recording_entry)

        screenshot_section = Gtk.Label(label="Screenshot")
        screenshot_section.add_css_class("title-3")
        screenshot_section.set_halign(Gtk.Align.START)
        main_box.append(screenshot_section)

        format_label = Gtk.Label(label="Image format")
        format_label.set_halign(Gtk.Align.START)

        self.format_dropdown = Gtk.DropDown.new_from_strings(
            ["PNG", "JPEG"]
        )

        if self.settings.get("screenshot_format") == "JPEG":
            self.format_dropdown.set_selected(1)
        else:
            self.format_dropdown.set_selected(0)

        main_box.append(format_label)
        main_box.append(self.format_dropdown)

        recording_section = Gtk.Label(label="Recording")
        recording_section.add_css_class("title-3")
        recording_section.set_halign(Gtk.Align.START)
        main_box.append(recording_section)

        fps_label = Gtk.Label(label="Frame rate")
        fps_label.set_halign(Gtk.Align.START)

        self.fps_dropdown = Gtk.DropDown.new_from_strings(
            ["24", "30", "60"]
        )

        fps = str(self.settings.get("recording_fps"))

        if fps == "24":
            self.fps_dropdown.set_selected(0)
        elif fps == "60":
            self.fps_dropdown.set_selected(2)
        else:
            self.fps_dropdown.set_selected(1)

        main_box.append(fps_label)
        main_box.append(self.fps_dropdown)

        buttons = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            halign=Gtk.Align.END,
        )

        cancel_button = Gtk.Button(label="Cancel")
        save_button = Gtk.Button(label="Save")

        save_button.add_css_class("suggested-action")

        cancel_button.connect(
            "clicked",
            lambda button: self.close(),
        )

        save_button.connect(
            "clicked",
            self.on_save,
        )

        buttons.append(cancel_button)
        buttons.append(save_button)

        main_box.append(buttons)

        self.set_child(main_box)

    def on_save(self, button):
        self.settings.set(
            "screenshot_directory",
            self.screenshot_entry.get_text().strip(),
        )

        self.settings.set(
            "recording_directory",
            self.recording_entry.get_text().strip(),
        )

        selected_format = (
            self.format_dropdown
            .get_selected_item()
            .get_string()
        )

        self.settings.set(
            "screenshot_format",
            selected_format,
        )

        selected_fps = int(
            self.fps_dropdown
            .get_selected_item()
            .get_string()
        )

        self.settings.set(
            "recording_fps",
            selected_fps,
        )

        if self.on_saved_callback:
            self.on_saved_callback()

        self.close()
