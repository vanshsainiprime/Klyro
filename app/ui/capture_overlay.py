import subprocess
import tempfile
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib


class CaptureOverlay(Gtk.Window):
    def __init__(self, parent, screenshot_service):
        super().__init__(
            title="Klyro Capture",
            decorated=False,
        )

        self.parent = parent
        self.screenshot_service = screenshot_service

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.background_path = None
        self.background_pixbuf = None

        self.set_modal(True)

        self._load_css()
        self._capture_desktop()


    # Desktop background
    def _capture_desktop(self):
        self.parent.hide()

        def capture():
            try:
                temp_dir = tempfile.mkdtemp(
                    prefix="klyro_"
                )

                self.background_path = (
                    Path(temp_dir) / "desktop.png"
                )

                subprocess.run(
                    [
                        "scrot",
                        str(self.background_path),
                    ],
                    check=True,
                    capture_output=True,
                )

                self._load_background()
                self._show_overlay()

            except Exception as error:
                print(f"Capture overlay error: {error}")
                self.close()
                self.parent.present()

            return False

        GLib.timeout_add(150, capture)

    def _load_background(self):
        self.background_pixbuf = (
            GdkPixbuf.Pixbuf.new_from_file(
                str(self.background_path)
            )
        )


    # Overlay
    def _show_overlay(self):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()

        if monitor is None:
            monitors = display.get_monitors()

            if monitors.get_n_items() == 0:
                raise RuntimeError(
                    "No display monitor found."
                )

            monitor = monitors.get_item(0)

        geometry = monitor.get_geometry()

        self.set_default_size(
            geometry.width,
            geometry.height,
        )

        self.fullscreen()

        area = Gtk.DrawingArea()
        area.set_content_width(geometry.width)
        area.set_content_height(geometry.height)

        area.set_draw_func(self._draw)

        # Mouse press / release
        click = Gtk.GestureClick()
        click.connect(
            "pressed",
            self._mouse_pressed,
        )
        click.connect(
            "released",
            self._mouse_released,
        )

        area.add_controller(click)

        # Mouse movement
        motion = Gtk.EventControllerMotion()
        motion.connect(
            "motion",
            self._mouse_moved,
        )

        area.add_controller(motion)

        self.set_child(area)

        self.drawing_area = area

        self._setup_keyboard()

        self.present()


    # Drawing


    def _draw(
        self,
        area,
        context,
        width,
        height,
    ):
        # Desktop image
        if self.background_pixbuf:
            scale_x = (
                width
                / self.background_pixbuf.get_width()
            )

            scale_y = (
                height
                / self.background_pixbuf.get_height()
            )

            scale = max(scale_x, scale_y)

            image_width = (
                self.background_pixbuf.get_width()
                * scale
            )

            image_height = (
                self.background_pixbuf.get_height()
                * scale
            )

            offset_x = (
                width - image_width
            ) / 2

            offset_y = (
                height - image_height
            ) / 2

            context.save()

            context.translate(
                offset_x,
                offset_y,
            )

            context.scale(
                scale,
                scale,
            )

            Gdk.cairo_set_source_pixbuf(
                context,
                self.background_pixbuf,
                0,
                0,
            )

            context.paint()

            context.restore()

        # Dark overlay
        context.set_source_rgba(
            0.02,
            0.03,
            0.08,
            0.48,
        )

        context.rectangle(
            0,
            0,
            width,
            height,
        )

        context.fill()

        # Selection
        selection = self._selection()

        if selection:
            x, y, w, h = selection

            # Restore original desktop inside selection
            if self.background_pixbuf:
                scale_x = (
                    width
                    / self.background_pixbuf.get_width()
                )

                scale_y = (
                    height
                    / self.background_pixbuf.get_height()
                )

                scale = max(
                    scale_x,
                    scale_y,
                )

                image_width = (
                    self.background_pixbuf.get_width()
                    * scale
                )

                image_height = (
                    self.background_pixbuf.get_height()
                    * scale
                )

                offset_x = (
                    width - image_width
                ) / 2

                offset_y = (
                    height - image_height
                ) / 2

                context.save()

                context.rectangle(
                    x,
                    y,
                    w,
                    h,
                )

                context.clip()

                context.translate(
                    offset_x,
                    offset_y,
                )

                context.scale(
                    scale,
                    scale,
                )

                Gdk.cairo_set_source_pixbuf(
                    context,
                    self.background_pixbuf,
                    0,
                    0,
                )

                context.paint()

                context.restore()

            # Selection border
            context.set_source_rgba(
                0.25,
                0.52,
                1.0,
                1.0,
            )

            context.set_line_width(2)

            context.rectangle(
                x,
                y,
                w,
                h,
            )

            context.stroke()

            # Handles
            context.set_source_rgba(
                1,
                1,
                1,
                1,
            )

            handle_size = 8

            handles = [
                (x, y),
                (x + w, y),
                (x, y + h),
                (x + w, y + h),
            ]

            for hx, hy in handles:
                context.arc(
                    hx,
                    hy,
                    handle_size / 2,
                    0,
                    6.283,
                )

                context.fill()

            # Size badge
            self._draw_size_badge(
                context,
                x,
                y,
                w,
                h,
            )

        # Top hint
        context.set_source_rgba(
            0.05,
            0.06,
            0.10,
            0.90,
        )

        context.round_rectangle(
            width / 2 - 180,
            24,
            360,
            48,
            20,
        )

        context.fill()

        context.set_source_rgba(
            1,
            1,
            1,
            0.9,
        )

        context.select_font_face(
            "Sans",
            0,
            0,
        )

        context.set_font_size(15)

        context.move_to(
            width / 2 - 145,
            54,
        )

        context.show_text(
            "Drag to select  •  Enter to capture  •  Esc to cancel"
        )

    def _draw_size_badge(
        self,
        context,
        x,
        y,
        w,
        h,
    ):
        text = f"{int(w)} × {int(h)}"

        context.set_font_size(13)

        extents = context.text_extents(text)

        badge_width = extents.width + 20
        badge_height = 28

        badge_x = (
            x + (w - badge_width) / 2
        )

        badge_y = y + h + 12

        context.set_source_rgba(
            0.04,
            0.05,
            0.09,
            0.92,
        )

        context.round_rectangle(
            badge_x,
            badge_y,
            badge_width,
            badge_height,
            8,
        )

        context.fill()

        context.set_source_rgba(
            1,
            1,
            1,
            0.9,
        )

        context.move_to(
            badge_x + 10,
            badge_y + 19,
        )

        context.show_text(text)


    # Selection


    def _mouse_pressed(
        self,
        gesture,
        n_press,
        x,
        y,
    ):
        self.start_x = x
        self.start_y = y

        self.end_x = x
        self.end_y = y

        self.drawing_area.queue_draw()

    def _mouse_moved(
        self,
        controller,
        x,
        y,
    ):
        if self.start_x is None:
            return

        self.end_x = x
        self.end_y = y

        self.drawing_area.queue_draw()

    def _mouse_released(
        self,
        gesture,
        n_press,
        x,
        y,
    ):
        if self.start_x is None:
            return

        self.end_x = x
        self.end_y = y

        self.drawing_area.queue_draw()

    def _selection(self):
        if (
            self.start_x is None
            or self.start_y is None
            or self.end_x is None
            or self.end_y is None
        ):
            return None

        x = min(
            self.start_x,
            self.end_x,
        )

        y = min(
            self.start_y,
            self.end_y,
        )

        w = abs(
            self.end_x - self.start_x
        )

        h = abs(
            self.end_y - self.start_y
        )

        if w < 2 or h < 2:
            return None

        return (
            x,
            y,
            w,
            h,
        )


    # Keyboard


    def _setup_keyboard(self):
        controller = Gtk.EventControllerKey()

        controller.connect(
            "key-pressed",
            self._key_pressed,
        )

        self.add_controller(controller)

    def _key_pressed(
        self,
        controller,
        keyval,
        keycode,
        state,
    ):
        if keyval == Gdk.KEY_Escape:
            self._cancel()
            return True

        if keyval in (
            Gdk.KEY_Return,
            Gdk.KEY_KP_Enter,
        ):
            self._capture()
            return True

        return False


    # Capture


    def _capture(self):
        selection = self._selection()

        if not selection:
            return

        x, y, width, height = selection

        try:
            output = self._save_selection(
                x,
                y,
                width,
                height,
            )

            print(
                f"Screenshot captured: {output}"
            )

            self.close()

            self.parent.present()

        except Exception as error:
            print(
                f"Screenshot failed: {error}"
            )

    def _save_selection(
        self,
        x,
        y,
        width,
        height,
    ):
        output = (
            self.screenshot_service._filename()
        )

        with tempfile.TemporaryDirectory(
            prefix="klyro_crop_"
        ) as temp_dir:

            cropped = (
                Path(temp_dir)
                / "crop.png"
            )

            subprocess.run(
                [
                    "magick",
                    str(self.background_path),
                    "-crop",
                    f"{int(width)}x{int(height)}"
                    f"+{int(x)}+{int(y)}",
                    "+repage",
                    str(cropped),
                ],
                check=True,
                capture_output=True,
            )

            image_format = (
                self.screenshot_service.image_format
            )

            if image_format == "PNG":

                cropped.replace(output)

            elif image_format == "JPEG":

                subprocess.run(
                    [
                        "magick",
                        str(cropped),
                        "-quality",
                        "95",
                        str(output),
                    ],
                    check=True,
                    capture_output=True,
                )

            else:

                cropped.replace(output)

        return output


    # Cancel


    def _cancel(self):
        self.close()
        self.parent.present()

    def close_request(self):
        self._cancel()
        return True


    # CSS


    def _load_css(self):
        provider = Gtk.CssProvider()

        provider.load_from_data(
            b"""
            window {
                background: #080a12;
            }
            """
        )

        display = Gdk.Display.get_default()

        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
