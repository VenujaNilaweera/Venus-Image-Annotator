<p align="center">
  <img src="assets/logoVIA.png" alt="VIA Logo" width="250" height="250">
</p>

<h1 align="center">Venus Image Annotator</h1>
<p align="center"><i>Fast, minimal, and YOLO-friendly image bounding box tool</i></p>

Venus Image Annotator is a fast, user-friendly, and modern tool for drawing bounding boxes and saving annotations in YOLO format. Designed for both beginners and professionals working on image labeling and machine learning datasets.

## 🖥️ Download

👉 [Click here to download the latest VIA application (.exe)](insert-your-download-link-here)

**✅ No installation needed — just run it!**

## 💎 Why Venus Annotator is Better Than Most Annotation Tools

While most open-source annotation tools offer basic box drawing and label saving, Venus Annotator focuses on developer ease, speed, and flexibility. Here's what makes it stand out:

### ✅ 1. Dynamic Class System with GUI Editor
- Easily add, remove, or update classes via the GUI
- Colors are auto-assigned from a friendly palette

### ✅ 2. Auto Cleanup of Empty Annotations
- Deletes .txt labels and copied image if no boxes are drawn

### ✅ 3. Portable EXE — No Install Needed
- No Python or extra steps — just run the app

### ✅ 4. Smart Navigation & Shortcuts
- Space to go to next image
- 1–9 to switch classes
- Zoom with mouse wheel

### ✅ 5. YOLO Format Ready + Customizable
- Saves in YOLO format (class_id x_center y_center width height)
- Auto-loads existing annotations

### ✅ 6. Friendly Codebase (PyQt5)
- Modular, readable, and easy to contribute to

## 🚀 Features

- 🎯 Draw Bounding Boxes with click + drag
- 🎨 Class Editor GUI for label management
- 🔁 Auto-save annotations on image switch
- 🔍 Zoom with mouse wheel (anchored)
- ⌨️ Keyboard Shortcuts:
  - Spacebar → next image
  - 1–9 → select class
- 🧽 Ctrl + Click to erase boxes
- ❌ Clear all = auto-delete annotation and image
- 🔄 Auto-load previous annotations if found
- 🧠 Dynamic class system with YAML or GUI

## 📦 Installation

Install required libraries:

```bash
pip install PyQt5 pyyaml
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

✅ If you're using pyinstaller to make an EXE, others don't need to install these.

## 📁 Folder Structure

After selecting input and output folders:

```
output/
├── images/   → contains copied annotated images
└── labels/   → contains .txt files with YOLO-style annotations
```

YOLO label format:
```
<class_id> <x_center> <y_center> <width> <height>
```
All values are normalized to [0, 1].

## ⚙️ Class Configuration

### YAML Auto-Generation

On first launch, a `classes.yaml` file is created automatically at:

```
Windows: C:\Users\<YourName>\AppData\Local\VenusAnnotator\classes.yaml  
Linux/macOS: ~/.config/VenusAnnotator/classes.yaml
```

Example Structure:
```yaml
classes:
  - id: 1
    name: "Round Worm"
  - id: 2
    name: "Hook Worm"
  - id: 3
    name: "Whip Worm"
```

✅ Or use the "Edit Classes" GUI to manage classes (no YAML editing required).

## 🎥 How to Use

1. Launch the EXE or run the script
2. Select Images Folder
3. Select Output Folder
4. Draw bounding boxes
5. Press Space to go to next image
6. Use class buttons or keys 1–9
7. Save annotations or auto-save on switch
8. Use Edit Classes to update labels
9. Clear boxes to auto-remove annotations

## 🛠️ Building the EXE

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile your_script.py
```

With icon and name:
```bash
pyinstaller --noconsole --onefile --name VenusAnnotator --icon=icon.ico your_script.py
```

✅ `classes.yaml` is created automatically — no need to bundle it.

## 🧾 Developer Notes – How to Customize

### 1. Class Loading 
📍 `load_classes()` ~ Line 95
```python
default_yaml = { "classes": [...] }
```

### 2. UI Class Buttons 
📍 `setup_ui()` ~ Line 160
```python
for idx, cls in enumerate(self.classes):
```

### 3. Saving Annotations 
📍 `save_annotation()` ~ Line 940
```python
f.write(f"{cid} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
```

### 4. Auto-delete Empty Annotations 
📍 `save_annotation()` ~ Line 926
```python
if not self.boxes:
    os.remove(label_output_path)
```

### 5. Class Editor Window 
📍 `edit_classes()` ~ Line 330
```python
table = QTableWidget(len(self.classes), 2)
```

### 6. Output Structure 
📍 `select_output_folder()` ~ Line 610
```python
self.labels_output = os.path.join(self.output_folder, "labels")
```

## 📁 Example Project Structure

```
VIA-Annotator/
├── via_annotator.py
├── README.md
├── assets/
│   └── demo-thumbnail.png
├── requirements.txt
└── classes.yaml  ← Optional (auto-generated if not present)
```

## 📃 License

MIT License — use freely and share with others.

## 🤝 Credits

Created by an enthusiast for the global coding community ❤️
