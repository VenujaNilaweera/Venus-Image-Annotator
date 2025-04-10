# 🖼️ Venus Image Annotator

Venus Image Annotator is a fast, user-friendly, and modern tool for drawing bounding boxes and saving annotations in **YOLO format**. Designed for both beginners and professionals working on image labeling and machine learning datasets.

---

## 🚀 Features

- 🎯 **Draw Bounding Boxes** by click + drag
- 🎨 **Class Editor GUI**: Easily add, remove, or update class names and IDs
- 🔁 **Auto-save annotations** when navigating between images
- 🔍 **Zoom with mouse wheel** (anchored around cursor)
- ⌨️ **Keyboard Shortcuts**:
  - `Spacebar` → next image
  - `1`–`9` → quick class selection
- 🔧 **Edit Classes GUI** to manage labels (with color auto-assignment)
- 🧽 **Erase a box** with `Ctrl + Click`
- ❌ **Remove all boxes** and auto-delete label + image copy from output folder
- 🔄 **Auto-load previous annotations** if available
- 🧠 **Supports dynamic classes** (no need to edit YAML manually!)

---

## 📁 Folder Structure

After selecting your **input image folder** and **output folder**, the structure will be:

```
output/
├── images/   → contains copied annotated images
└── labels/   → contains .txt files with YOLO-style annotations
```

Each label `.txt` file has this format:

```
<class_id> <x_center> <y_center> <width> <height>
```

All values are **normalized** to [0, 1].

---

## ⚙️ Class Configuration

- On first launch, a `classes.yaml` file is auto-generated in:
  ```
  C:\Users\<YourName>\AppData\Local\VenusAnnotator\classes.yaml
  ```
- You can **edit classes using the GUI** (via the "Edit Classes" button).
- Colors are assigned automatically from a friendly color palette.

No manual YAML editing is required.

---

## 🎥 How to Use

1. **Launch** the EXE or run the Python script.
2. Click **"Select Images Folder"** to load your dataset.
3. Click **"Select Output Folder"** to store results.
4. **Draw boxes** by dragging on the image.
5. Use class buttons or keys `1`–`9` to assign classes.
6. **Save manually** or press **Spacebar** to go to the next image (auto-save enabled).
7. Use **"Clear All Boxes"** to remove all annotations.
8. Use **"Edit Classes"** to change your labels at any time.

---

## 🛠️ Building the EXE

Use `pyinstaller` to bundle the app:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile your_script.py
```

Or, to include an icon and name:

```bash
pyinstaller --noconsole --onefile --name VenusAnnotator --icon=icon.ico your_script.py
```

> ✅ No need to bundle `classes.yaml` — the app will create it on first run.

---

## 📷 Screenshot

*You can add demo screenshots here!*

---

## 📃 License

MIT License — use freely and share with others.

---

## 🤝 Credits

Created by an enthusiast for the global coding community ❤️

---

## 🛠️ Developer Notes – How to Customize

If you want to adapt or extend the tool, here are key parts of the code you may want to change:

### 🔧 1. Class Definitions & Color Assignment
📍 In `load_classes()` – Line ~95

```python
def load_classes(self):
    ...
    default_yaml = {
        "classes": [
            {"id": 1, "name": "Round Worm"},
            {"id": 2, "name": "Hook Worm"},
            {"id": 3, "name": "Whip Worm"}
        ]
    }
```

> 📝 You can change default classes or customize how color is auto-assigned from a palette.

---

### 🎨 2. UI Class Button Creation
📍 In `setup_ui()` – Line ~160

```python
for idx, cls in enumerate(self.classes):
    display_text = f"{cls['name']} ({cls['color_name']})"
    btn = QRadioButton(display_text)
    ...
```

> 📝 Modify how classes are shown on screen, or style them differently.

---

### 💾 3. Saving Annotations (YOLO Format)
📍 In `save_annotation()` – Line ~940

```python
f.write(f"{cid} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
```

> 📝 You can change the annotation format or output logic here.

---

### 🧼 4. Auto-remove empty annotations
📍 Still in `save_annotation()` – Line ~926

```python
if not self.boxes:
    if os.path.exists(label_output_path):
        os.remove(label_output_path)
```

> 📝 This is where the tool deletes the annotation and image copy if no boxes exist.

---

### ⚙️ 5. Class Editing Window (Dialog Logic)
📍 In `edit_classes()` – Line ~330

```python
table = QTableWidget(len(self.classes), 2)
...
add_btn.clicked.connect(on_add_row)
remove_btn.clicked.connect(on_remove_row)
```

> 📝 You can expand this to support extra fields, like description or class hierarchy.

---

### 📤 6. Output Folder Structure
📍 In `select_output_folder()` – Line ~610

```python
self.images_output = os.path.join(self.output_folder, "images")
self.labels_output = os.path.join(self.output_folder, "labels")
```

> 📝 Change where or how outputs are stored if needed.

---

Feel free to fork the repo and make improvements!
