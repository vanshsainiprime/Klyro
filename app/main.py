import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gdk, Gtk

from app.config.settings import Settings
from app.services.recorder import RecordingService
from app.services.screenshot import ScreenshotService
from app.ui.capture_overlay import CaptureOverlay


CSS = """
window {
    background: #0b0d14;
}

.main {
    background:
        radial-gradient(
            circle at 20% 25%,
            rgba(82, 57, 180, 0.30),
            transparent 38%
        ),
        radial-gradient(
            circle at 80% 70%,
            rgba(39, 88, 190, 0.22),
            transparent 42%
        ),
        #0b0d14;
}

/* Top navigation */

.topbar {
    background: rgba(25, 27, 39, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 28px;
    padding: 5px;
}

.top-button {
    min-height: 44px;
    padding: 0 22px;
    border-radius: 22px;
    font-size: 14px;
    font-weight: 600;
}

.top-button:hover {
    background: rgba(255, 255, 255, 0.07);
}

.top-active {
    background: #397cff;
    color: white;
}

.top-active:hover {
    background: #4b88ff;
}

.icon-button {
    min-width: 44px;
    min-height: 44px;
    padding: 0;
    border-radius: 22px;
}

/* Main workspace */

.workspace {
    background: rgba(19, 21, 32, 0.62);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 22px;
    padding: 20px;
}

.preview {
    background:
        linear-gradient(
            135deg,
            rgba(78, 55, 163, 0.60),
            rgba(29, 67, 145, 0.58)
        );
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: 10px;
    min-width: 720px;
    min-height: 470px;
}

.preview-title {
    font-size: 22px;
    font-weight: 700;
}

.preview-subtitle {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.58);
}

.size-badge {
    background: rgba(8, 9, 16, 0.72);
    border-radius: 9px;
    padding: 6px 11px;
    font-size: 12px;
}

/* Right control panel */

.control-panel {
    background: rgba(20, 22, 34, 0.94);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 22px;
    padding: 22px;
    min-width: 330px;
}

.panel-title {
    font-size: 19px;
    font-weight: 700;
}

.mode-card {
    min-height: 74px;
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.07);
}

.mode-card:hover {
    background: rgba(255, 255, 255, 0.075);
}

.mode-selected {
    background: rgba(57, 124, 255, 0.24);
    border: 1px solid rgba(57, 124, 255, 0.90);
}

.mode-icon {
    font-size: 21px;
}

.mode-label {
    font-size: 12px;
    font-weight: 600;
}

.setting-row {
    min-height: 46px;
}

.setting-name {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.78);
}

/* Capture button */

.capture-button {
    min-height: 56px;
    border-radius: 16px;
    background: #397cff;
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.capture-button:hover {
    background: #4b88ff;
}

/* Annotation toolbar */

.toolbar {
    background: rgba(20, 22, 34, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 25px;
    padding: 5px;
}

.tool-button {
    min-width: 42px;
    min-height: 42px;
    padding: 0;
    border-radius: 21px;
    font-size: 17px;
}

.tool-button:hover {
    background: rgba(255, 255, 255, 0.08);
}

.tool-selected {
    background: #397cff;
}

/* Footer */

.footer {
    color: rgba(255, 255, 255, 0.42);
    font-size: 12px;
}
"""


class KlyroWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(
            application=application,
            title="Klyro",
        )

        self.set_default_size(1200, 760)
        self.set_resizable(True)

        self.settings = Settings()

        self.screenshot_service = ScreenshotService(
            self.settings.get("screenshot_directory"),
            self.settings.get("screenshot_format"),
        )

        self.recording_service = RecordingService(
            self.settings.get("recording_directory")
        )

        self.load_css()
        self.build_ui()

    def build_ui(self):
        root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18,
            margin_top=18,
            margin_bottom=18,
            margin_start=24,
            margin_end=24,
        )
        root.add_css_class("main")

        root.append(self.build_top_bar())

        content = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=22,
            hexpand=True,
            vexpand=True,
        )

        content.append(self.build_workspace())
        content.append(self.build_control_panel())

        root.append(content)

        footer = Gtk.Label(label="Klyro  •  Ready")
        footer.add_css_class("footer")
        footer.set_halign(Gtk.Align.CENTER)

        root.append(footer)

        self.set_child(root)

    def build_top_bar(self):
        container = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
        )

        topbar = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=4,
        )
        topbar.add_css_class("topbar")

        cancel = Gtk.Button(label="Esc   Cancel")
        cancel.add_css_class("top-button")
        cancel.connect("clicked", self.on_cancel)

        screenshot = Gtk.Button(label="Screenshot")
        screenshot.add_css_class("top-button")
        screenshot.add_css_class("top-active")
        screenshot.connect(
            "clicked",
            self.open_capture_overlay,
        )

        record = Gtk.Button(label="Record")
        record.add_css_class("top-button")

        more = Gtk.Button(label="More")
        more.add_css_class("top-button")

        settings = Gtk.Button(label="⚙")
        settings.add_css_class("icon-button")

        topbar.append(cancel)
        topbar.append(screenshot)
        topbar.append(record)
        topbar.append(more)
        topbar.append(settings)

        container.append(topbar)

        return container

    def build_workspace(self):
        workspace = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=14,
            hexpand=True,
            vexpand=True,
        )
        workspace.add_css_class("workspace")

        preview_holder = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            hexpand=True,
            vexpand=True,
        )

        preview = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        preview.add_css_class("preview")

        title = Gtk.Label(label="Capture Area")
        title.add_css_class("preview-title")

        subtitle = Gtk.Label(label="Selection mode")
        subtitle.add_css_class("preview-subtitle")

        size = Gtk.Label(label="1280 × 720")
        size.add_css_class("size-badge")

        preview.append(title)
        preview.append(subtitle)
        preview.append(size)

        preview_holder.append(preview)
        workspace.append(preview_holder)

        workspace.append(self.build_annotation_toolbar())

        return workspace

    def build_annotation_toolbar(self):
        container = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            halign=Gtk.Align.CENTER,
        )

        toolbar = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=2,
        )
        toolbar.add_css_class("toolbar")

        tools = [
            ("↖", "Pointer"),
            ("□", "Rectangle"),
            ("○", "Ellipse"),
            ("↗", "Arrow"),
            ("✎", "Pen"),
            ("T", "Text"),
            ("▦", "Blur"),
            ("●", "Color"),
            ("↶", "Undo"),
            ("↷", "Redo"),
            ("×", "Clear"),
        ]

        for icon, tooltip in tools:
            button = Gtk.Button(label=icon)
            button.add_css_class("tool-button")
            button.set_tooltip_text(tooltip)

            if tooltip == "Pointer":
                button.add_css_class("tool-selected")

            toolbar.append(button)

        container.append(toolbar)

        return container

    def build_control_panel(self):
        panel = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=17,
            valign=Gtk.Align.CENTER,
        )
        panel.add_css_class("control-panel")

        title = Gtk.Label(label="Capture")
        title.set_halign(Gtk.Align.START)
        title.add_css_class("panel-title")

        panel.append(title)
        panel.append(self.build_capture_modes())

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
        )
        panel.append(separator)

        cursor = Gtk.Switch(active=True)
        panel.append(
            self.build_setting_row(
                "Include cursor",
                cursor,
            )
        )

        delay = Gtk.DropDown.new_from_strings(
            [
                "No delay",
                "2 seconds",
                "5 seconds",
                "10 seconds",
            ]
        )

        panel.append(
            self.build_setting_row(
                "Delay capture",
                delay,
            )
        )

        format_dropdown = Gtk.DropDown.new_from_strings(
            ["PNG", "JPEG"]
        )

        if self.settings.get("screenshot_format") == "JPEG":
            format_dropdown.set_selected(1)
        else:
            format_dropdown.set_selected(0)

        panel.append(
            self.build_setting_row(
                "Format",
                format_dropdown,
            )
        )

        save_path = Gtk.Label(
            label="~/Pictures/Klyro"
        )
        save_path.set_halign(Gtk.Align.END)

        panel.append(
            self.build_setting_row(
                "Save to",
                save_path,
            )
        )

        capture = Gtk.Button(
            label="Capture    Enter"
        )
        capture.add_css_class("capture-button")
        capture.connect(
            "clicked",
            self.on_capture,
        )

        panel.append(capture)

        return panel

    def build_capture_modes(self):
        modes = Gtk.Grid(
            column_spacing=7,
            row_spacing=7,
            column_homogeneous=True,
        )

        mode_data = [
            ("▢", "Selection"),
            ("▣", "Screen"),
            ("▣", "Window"),
            ("↕", "Scrolling"),
        ]

        for index, (icon, label) in enumerate(mode_data):
            content = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=4,
                halign=Gtk.Align.CENTER,
                valign=Gtk.Align.CENTER,
            )

            icon_label = Gtk.Label(label=icon)
            icon_label.add_css_class("mode-icon")

            text = Gtk.Label(label=label)
            text.add_css_class("mode-label")

            content.append(icon_label)
            content.append(text)

            button = Gtk.Button()
            button.set_child(content)
            button.add_css_class("mode-card")

            if label == "Selection":
                button.add_css_class("mode-selected")

            modes.attach(
                button,
                index % 2,
                index // 2,
                1,
                1,
            )

        return modes

    def build_setting_row(self, name, widget):
        row = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
        )
        row.add_css_class("setting-row")

        label = Gtk.Label(label=name)
        label.add_css_class("setting-name")
        label.set_halign(Gtk.Align.START)
        label.set_hexpand(True)

        row.append(label)
        row.append(widget)

        return row

    def open_capture_overlay(self, button):
        overlay = CaptureOverlay(
            self,
            self.screenshot_service,
        )
        overlay.present()

    def on_capture(self, button):
        try:
            path = self.screenshot_service.capture_fullscreen()
            print(f"Screenshot captured: {path}")
        except RuntimeError as error:
            print(error)

    def on_cancel(self, button):
        self.close()

    def load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode("utf-8"))

        display = Gdk.Display.get_default()

        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


class KlyroApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.klyro.app"
        )

    def do_activate(self):
        window = self.props.active_window

        if window is None:
            window = KlyroWindow(self)

        window.present()


app = KlyroApp()
app.run()