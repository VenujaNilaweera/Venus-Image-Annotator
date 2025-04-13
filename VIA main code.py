import os
import sys
import shutil
import yaml  # pip install pyyaml
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QMessageBox, QScrollArea,
    QRadioButton, QGroupBox, QFrame, QDialog, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialogButtonBox, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt5.QtCore import Qt, QRect, QPoint, QEvent, QStandardPaths


def resource_path(filename: str) -> str:
    """
    Returns the absolute path to the given filename.
    Works for normal execution and PyInstaller bundles.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


class BoundingBoxAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()

        # Determine a configuration directory in a user-writable location.
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        # YAML file will be stored here.
        self.yaml_path = os.path.join(config_dir, "classes.yaml")

        # Load classes from YAML (or create default if missing) and auto-assign colors.
        self.load_classes()

        self.setWindowTitle("Venus Image Annotator")
        self.setGeometry(100, 100, 1200, 800)
        self.setFocusPolicy(Qt.StrongFocus)

        # Image annotation variables.
        self.image_folder = ""
        self.output_folder = ""
        self.image_list = []
        self.current_idx = -1
        self.current_image_path = ""
        self.boxes = []  # (QRect, class_id)

        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.current_box = None
        self.image_modified = False
        self.erasing = False

        if self.classes:
            self.current_class = self.classes[0]["id"]
        else:
            self.current_class = 1

        # Image display variables.
        self.original_pixmap = None
        self.scaled_pixmap = None
        self.image_rect = None

        self.background_color = QColor(40, 40, 40, 255)
        self.x_offset = 0
        self.y_offset = 0
        self.zoom_factor = 1.0

        self.setup_ui()

    def load_classes(self):
        """
        Loads classes from the YAML file located at self.yaml_path.
        Each class entry should have 'id' and 'name'; 'color' is optional.
        If missing or unrecognized, a random friendly color is assigned.
        """
        if not os.path.exists(self.yaml_path):
            default_yaml = {
                "classes": [
                    {"id": 1, "name": "Human"},
                    {"id": 2, "name": "dog"},
                    {"id": 3, "name": "cat"}
                ]
            }
            try:
                with open(self.yaml_path, "w") as f:
                    yaml.dump(default_yaml, f)
            except Exception as e:
                print(f"Failed to write default YAML: {e}")

        try:
            with open(self.yaml_path, "r") as f:
                config = yaml.safe_load(f)
            self.classes = config.get("classes", [])
            if not self.classes:
                raise ValueError("No 'classes' found in YAML.")
        except Exception as e:
            print(f"Error loading classes.yaml: {e}. Using default classes.")
            self.classes = [
                {"id": 1, "name": "human"},
                {"id": 2, "name": "dog"},
                {"id": 3, "name": "cat"}
            ]

        # Named color choices for random assignment.
        self.named_color_choices = [
            ("Red", "#FF0000"),
            ("Green", "#00FF00"),
            ("Blue", "#0000FF"),
            ("Yellow", "#FFFF00"),
            ("Cyan", "#00FFFF"),
            ("Magenta", "#FF00FF"),
            ("Orange", "#FFA500"),
            ("Purple", "#800080"),
            ("Gray", "#808080"),
            ("Black", "#000000")
        ]

        used_names = set()
        for cls in self.classes:
            user_color = cls.get("color", "").strip()
            if user_color:
                user_color = user_color.upper()
                found = False
                for friendly, hex_val in self.named_color_choices:
                    if user_color == hex_val.upper() or user_color == friendly.upper():
                        cls["color_name"] = friendly
                        cls["color_hex"] = hex_val
                        used_names.add(friendly)
                        found = True
                        break
                if not found:
                    user_color = ""
            if not user_color:
                while True:
                    friendly, hex_val = random.choice(self.named_color_choices)
                    if friendly not in used_names:
                        cls["color_name"] = friendly
                        cls["color_hex"] = hex_val
                        used_names.add(friendly)
                        break

        self.class_colors = {cls["id"]: QColor(cls["color_hex"]) for cls in self.classes}

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Toolbar layout.
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(10)

        self.input_btn = QPushButton("Select Images Folder")
        self.input_btn.clicked.connect(self.select_input_folder)
        toolbar.addWidget(self.input_btn)

        self.output_btn = QPushButton("Select Output Folder")
        self.output_btn.clicked.connect(self.select_output_folder)
        toolbar.addWidget(self.output_btn)

        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(lambda: self.change_image(-1))
        toolbar.addWidget(self.prev_btn)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(lambda: self.change_image(1))
        toolbar.addWidget(self.next_btn)

        self.save_btn = QPushButton("Save Annotation")
        self.save_btn.clicked.connect(self.save_annotation)
        toolbar.addWidget(self.save_btn)

        self.clear_btn = QPushButton("Clear All Boxes")
        self.clear_btn.clicked.connect(self.clear_boxes)
        toolbar.addWidget(self.clear_btn)

        # Replace Debug button with Edit Classes button.
        self.config_btn = QPushButton("Edit Classes")
        self.config_btn.clicked.connect(self.edit_classes)
        toolbar.addWidget(self.config_btn)

        self.status_label = QLabel("No image loaded")
        toolbar.addWidget(self.status_label)

        main_layout.addLayout(toolbar)

        # Help text.
        help_text = QLabel(
            "Draw: Click and drag  |  Erase: Ctrl+Click on box  |  "
            "Save: Auto on image change  |  Space Bar to navigate  |  "
            "Wheel to zoom (anchored; min=1.0)."
        )
        main_layout.addWidget(help_text)

        # Dynamic class selection.
        self.class_group = QGroupBox("Select Class")
        class_layout = QHBoxLayout()
        self.class_buttons = []
        for idx, cls in enumerate(self.classes):
            display_text = f"{cls['name']} ({cls['color_name']})"
            btn = QRadioButton(display_text)
            btn.setFocusPolicy(Qt.NoFocus)
            if idx == 0:
                btn.setChecked(True)
            btn.toggled.connect(
                lambda checked, cid=cls['id']: self.set_class(cid) if checked else None
            )
            class_layout.addWidget(btn)
            self.class_buttons.append(btn)
        self.class_group.setLayout(class_layout)
        main_layout.addWidget(self.class_group)

        # Scroll area for the image.
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("border: none; background-color: #1E1E1E;")

        self.image_container = QWidget()
        container_layout = QVBoxLayout(self.image_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setMinimumSize(800, 600)
        self.image_display.setMouseTracking(True)
        self.image_display.setStyleSheet("background-color: #1E1E1E;")

        container_layout.addWidget(self.image_display)
        self.scroll_area.setWidget(self.image_container)
        main_layout.addWidget(self.scroll_area)

        self.image_display.installEventFilter(self)
        self.resizeEvent = self.on_resize

        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #4C4C4C;
            }
            QLabel {
                color: #FFFFFF;
            }
            QRadioButton {
                color: #FFFFFF;
            }
            QGroupBox {
                color: #FFFFFF;
                border: 1px solid #444444;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 10px;
            }
            QScrollArea, QScrollBar {
                border: none;
                background-color: #1E1E1E;
            }
        """)

    def edit_classes(self):
        """
        Opens a dialog with a table to view, add, or remove classes.
        The dialog uses a white background so text is easily readable.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Classes")
        dialog.resize(400, 300)
        # Set white background for the dialog and its widgets.
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                color: black;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
            }
            QLineEdit {
                background-color: white;
                color: black;
            }
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #555555;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout(dialog)
        table = QTableWidget(len(self.classes), 2)
        table.setHorizontalHeaderLabels(["ID", "Name"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        for row, cls in enumerate(self.classes):
            id_item = QTableWidgetItem(str(cls.get("id", "")))
            name_item = QTableWidgetItem(cls.get("name", ""))
            table.setItem(row, 0, id_item)
            table.setItem(row, 1, name_item)
        layout.addWidget(table)

        add_remove_layout = QHBoxLayout()
        add_btn = QPushButton("Add Row")
        remove_btn = QPushButton("Remove Row")
        add_remove_layout.addWidget(add_btn)
        add_remove_layout.addWidget(remove_btn)
        layout.addLayout(add_remove_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        def on_add_row():
            row_count = table.rowCount()
            table.insertRow(row_count)
            table.setItem(row_count, 0, QTableWidgetItem(""))
            table.setItem(row_count, 1, QTableWidgetItem(""))

        add_btn.clicked.connect(on_add_row)

        def on_remove_row():
            selected = table.selectionModel().selectedRows()
            for sel in sorted(selected, key=lambda x: x.row(), reverse=True):
                table.removeRow(sel.row())

        remove_btn.clicked.connect(on_remove_row)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            new_classes = []
            for row in range(table.rowCount()):
                id_item = table.item(row, 0)
                name_item = table.item(row, 1)
                if id_item and name_item:
                    try:
                        cid = int(id_item.text())
                        cname = name_item.text().strip()
                        if cname:
                            new_classes.append({"id": cid, "name": cname})
                    except Exception as e:
                        print(f"Error reading row {row}: {e}")
            self.classes = new_classes
            self.save_updated_classes()
            self.reload_class_buttons()
        else:
            # Discard changes.
            pass

    def save_updated_classes(self):
        try:
            with open(self.yaml_path, "w") as f:
                yaml.dump({"classes": self.classes}, f)
        except Exception as e:
            self.show_warning("Error", f"Could not save configuration: {e}")
            return
        self.load_classes()

    def reload_class_buttons(self):
        layout_group = self.class_group.layout()
        while layout_group.count():
            item = layout_group.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.class_buttons.clear()
        for idx, cls in enumerate(self.classes):
            display_text = f"{cls['name']} ({cls['color_name']})"
            btn = QRadioButton(display_text)
            btn.setFocusPolicy(Qt.NoFocus)
            if idx == 0:
                btn.setChecked(True)
                self.current_class = cls["id"]
            btn.toggled.connect(
                lambda checked, cid=cls['id']: self.set_class(cid) if checked else None
            )
            layout_group.addWidget(btn)
            self.class_buttons.append(btn)
        self.show_information("Saved", "Classes updated successfully.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.change_image(1)
        elif Qt.Key_1 <= event.key() <= Qt.Key_9:
            idx = event.key() - Qt.Key_1
            if 0 <= idx < len(self.class_buttons):
                self.class_buttons[idx].setChecked(True)
        else:
            super().keyPressEvent(event)

    def set_class(self, class_id):
        self.current_class = class_id

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Images Folder")
        if folder:
            self.image_folder = folder
            self.load_images_from_folder()
            self.status_label.setText(f"Loaded {len(self.image_list)} images from {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
            self.images_output = os.path.join(self.output_folder, "images")
            self.labels_output = os.path.join(self.output_folder, "labels")
            if not os.path.exists(self.images_output):
                os.makedirs(self.images_output)
            if not os.path.exists(self.labels_output):
                os.makedirs(self.labels_output)

    def load_images_from_folder(self):
        self.image_list = []
        valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
        for file in os.listdir(self.image_folder):
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                self.image_list.append(os.path.join(self.image_folder, file))
        if self.image_list:
            self.current_idx = 0
            self.load_current_image()
            self.prev_btn.setEnabled(True)
            self.next_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)

    def load_current_image(self):
        if 0 <= self.current_idx < len(self.image_list):
            self.current_image_path = self.image_list[self.current_idx]
            self.boxes = []
            self.image_modified = False
            self.zoom_factor = 1.0
            self.x_offset = 0
            self.y_offset = 0

            pixmap = QPixmap(self.current_image_path)
            self.original_pixmap = pixmap

            file_name = os.path.basename(self.current_image_path)
            base_name, _ = os.path.splitext(file_name)
            if self.output_folder:
                image_output_path = os.path.join(self.images_output, file_name)
                lbl_path = os.path.join(self.labels_output, base_name + ".txt")
                if os.path.exists(image_output_path) and os.path.exists(lbl_path):
                    self.load_annotation(lbl_path, pixmap.width(), pixmap.height())
            self.update_display()
            self.status_label.setText(f"Image {self.current_idx+1}/{len(self.image_list)}: {file_name}")

    def load_annotation(self, lbl_path, img_width, img_height):
        try:
            with open(lbl_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id = int(parts[0])
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        w_norm = float(parts[3])
                        h_norm = float(parts[4])
                        x = int((x_center - w_norm/2) * img_width)
                        y = int((y_center - h_norm/2) * img_height)
                        w = int(w_norm * img_width)
                        h = int(h_norm * img_height)
                        self.boxes.append((QRect(x, y, w, h), class_id))
            if self.boxes:
                self.image_modified = True
        except Exception as e:
            print(f"Error loading annotation: {e}")

    def update_display(self):
        if self.original_pixmap is None:
            return
        w = int(self.original_pixmap.width() * self.zoom_factor)
        h = int(self.original_pixmap.height() * self.zoom_factor)
        self.scaled_pixmap = self.original_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_size = self.image_display.size()
        if self.zoom_factor == 1.0:
            px = max(0, (lbl_size.width() - w) // 2)
            py = max(0, (lbl_size.height() - h) // 2)
            self.x_offset = px
            self.y_offset = py
        self.image_rect = QRect(self.x_offset, self.y_offset, self.scaled_pixmap.width(), self.scaled_pixmap.height())
        canvas = QPixmap(lbl_size)
        canvas.fill(self.background_color)
        painter = QPainter(canvas)
        painter.drawPixmap(self.image_rect, self.scaled_pixmap)
        pen = QPen(QColor(60, 60, 60))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.image_rect)
        for box, class_id in self.boxes:
            disp_box = self.map_to_display_coords(box)
            self.draw_box(painter, disp_box, class_id)
        if self.drawing and self.current_box:
            color = self.class_colors.get(self.current_class, QColor("#FFFF00"))
            pen = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(self.current_box)
        painter.end()
        self.image_display.setPixmap(canvas)

    def map_to_display_coords(self, orig_box):
        if not self.original_pixmap or not self.scaled_pixmap or not self.image_rect:
            return orig_box
        x_scale = self.scaled_pixmap.width() / self.original_pixmap.width()
        y_scale = self.scaled_pixmap.height() / self.original_pixmap.height()
        sx = int(orig_box.x() * x_scale) + self.x_offset
        sy = int(orig_box.y() * y_scale) + self.y_offset
        sw = int(orig_box.width() * x_scale)
        sh = int(orig_box.height() * y_scale)
        return QRect(sx, sy, sw, sh)

    def map_to_original_coords(self, disp_box):
        if not self.original_pixmap or not self.scaled_pixmap or not self.image_rect:
            return disp_box
        x_scale = self.original_pixmap.width() / self.scaled_pixmap.width()
        y_scale = self.original_pixmap.height() / self.scaled_pixmap.height()
        ox = int((disp_box.x() - self.image_rect.x()) * x_scale)
        oy = int((disp_box.y() - self.image_rect.y()) * y_scale)
        ow = int(disp_box.width() * x_scale)
        oh = int(disp_box.height() * y_scale)
        ox = max(0, min(ox, self.original_pixmap.width() - 1))
        oy = max(0, min(oy, self.original_pixmap.height() - 1))
        ow = min(ow, self.original_pixmap.width() - ox)
        oh = min(oh, self.original_pixmap.height() - oy)
        return QRect(ox, oy, ow, oh)

    def point_within_image(self, pt):
        return self.image_rect is not None and self.image_rect.contains(pt)

    def draw_box(self, painter, box, class_id):
        color = self.class_colors.get(class_id, QColor("#FFFF00"))
        pen = QPen(color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(box)
        cname = self.get_class_name(class_id)
        painter.setBrush(QColor(0, 0, 0, 128))
        txt_rect = QRect(box.x(), box.y() - 20, 80, 20)
        painter.drawRect(txt_rect)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(txt_rect, Qt.AlignCenter, cname)

    def get_class_name(self, class_id):
        for cls in self.classes:
            if cls["id"] == class_id:
                return cls.get("name", "Unknown")
        return "Unknown"

    def on_resize(self, event):
        if self.original_pixmap:
            self.update_display()
        super().resizeEvent(event)

    def change_image(self, direction):
        if not self.image_list:
            return
        if self.image_modified and self.boxes:
            self.save_annotation(auto_save=True)
        ni = self.current_idx + direction
        if 0 <= ni < len(self.image_list):
            self.current_idx = ni
            self.load_current_image()

    def clear_boxes(self):
        self.boxes = []
        self.image_modified = True
        self.update_display()

    def eventFilter(self, source, event):
        if source == self.image_display and event.type() == QEvent.Wheel:
            if not self.original_pixmap or not self.image_rect:
                return False
            old_rect = self.image_rect
            if event.angleDelta().y() > 0:
                new_zoom = self.zoom_factor * 1.1
            else:
                new_zoom = self.zoom_factor / 1.1
                if new_zoom < 1.0:
                    new_zoom = 1.0
            new_width = self.original_pixmap.width() * new_zoom
            new_height = self.original_pixmap.height() * new_zoom
            mouse_pt = event.pos()
            rel_x = (mouse_pt.x() - old_rect.x()) / old_rect.width() if old_rect.width() else 0.5
            rel_y = (mouse_pt.y() - old_rect.y()) / old_rect.height() if old_rect.height() else 0.5
            new_x_offset = int(mouse_pt.x() - rel_x * new_width)
            new_y_offset = int(mouse_pt.y() - rel_y * new_height)
            if new_zoom == 1.0:
                lbl_size = self.image_display.size()
                new_x_offset = (lbl_size.width() - new_width) // 2
                new_y_offset = (lbl_size.height() - new_height) // 2
            self.zoom_factor = new_zoom
            self.x_offset = new_x_offset
            self.y_offset = new_y_offset
            self.update_display()
            return True
        if source == self.image_display:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                if not self.output_folder:
                    self.show_warning("Warning", "Please select input and output folder before annotating.")
                    return super().eventFilter(source, event)
                pt = event.pos()
                if not self.point_within_image(pt):
                    return super().eventFilter(source, event)
                self.erasing = (QApplication.keyboardModifiers() == Qt.ControlModifier)
                if self.erasing:
                    removed = False
                    for i, (box, _) in enumerate(self.boxes):
                        disp_box = self.map_to_display_coords(box)
                        if disp_box.contains(pt):
                            self.boxes.pop(i)
                            self.image_modified = True
                            removed = True
                            break
                    if removed:
                        self.update_display()
                else:
                    self.drawing = True
                    self.start_point = pt
                    self.end_point = pt
                    self.current_box = QRect(self.start_point, self.end_point)
                    self.update_display()
            elif event.type() == QEvent.MouseMove and self.drawing:
                self.end_point = event.pos()
                self.current_box = QRect(self.start_point, self.end_point).normalized()
                self.update_display()
            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton and self.drawing:
                self.drawing = False
                self.end_point = event.pos()
                final_box = QRect(self.start_point, self.end_point).normalized()
                if final_box.width() > 5 and final_box.height() > 5:
                    orig_box = self.map_to_original_coords(final_box)
                    if orig_box.width() > 0 and orig_box.height() > 0:
                        self.boxes.append((orig_box, self.current_class))
                        self.image_modified = True
                self.current_box = None
                self.update_display()
        return super().eventFilter(source, event)

    def show_warning(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                background-color: white;
                color: black;
            }
            QMessageBox QDialogButtonBox {
                background-color: white;
            }
        """)
        msg.exec_()

    def show_information(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                background-color: white;
                color: black;
            }
            QMessageBox QDialogButtonBox {
                background-color: white;
            }
        """)
        msg.exec_()

    def save_annotation(self, auto_save=False):
        if not self.image_folder or not self.output_folder:
            if not auto_save:
                self.show_warning("Warning", "Please select input and output folders first.")
            return
        file_name = os.path.basename(self.current_image_path)
        base_name, ext = os.path.splitext(file_name)
        image_output_path = os.path.join(self.images_output, file_name)
        label_output_path = os.path.join(self.labels_output, base_name + ".txt")
        if not self.boxes:
            if os.path.exists(label_output_path):
                os.remove(label_output_path)
                print(f"Deleted annotation file: {label_output_path}")
            if os.path.exists(image_output_path):
                os.remove(image_output_path)
                print(f"Deleted image copy: {image_output_path}")
            if not auto_save:
                self.show_information("Removed", "No bounding boxes drawn. Existing annotation and image copy removed.")
            return
        shutil.copy2(self.current_image_path, image_output_path)
        img = QImage(self.current_image_path)
        img_width = img.width()
        img_height = img.height()
        with open(label_output_path, 'w') as f:
            for box, cid in self.boxes:
                x_center = (box.x() + box.width() / 2) / img_width
                y_center = (box.y() + box.height() / 2) / img_height
                w = box.width() / img_width
                h = box.height() / img_height
                f.write(f"{cid} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
        if not auto_save:
            self.show_information("Success", f"Annotation saved to {label_output_path}")


def main():
    app = QApplication(sys.argv)
    window = BoundingBoxAnnotator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
