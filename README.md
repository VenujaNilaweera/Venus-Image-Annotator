<p align="center">
  <img src="assets/logoVIA.png" alt="VIA Logo" width="520" height="300">
</p>

<h1 align="center">Venus Image Annotator</h1>
<p align="center"><i>Fast, minimal, and YOLO-friendly image bounding box tool</i></p>

Venus Image Annotator is a fast, user-friendly, and modern tool for drawing bounding boxes and saving annotations in YOLO format. Designed for both beginners and professionals working on image labeling and machine learning datasets.

## 🖥️ Download

👉 [Click here to download the latest VIA application (.exe)](https://github.com/VenujaNilaweera/Venus-Image-Annotator/releases)

**✅ No installation needed — just run it!**

## 📖 User Manual - How to Get Started

<div align="center">

### 🚀 QUICK START GUIDE 🚀

</div>

<table>
<tr>
<td width="50%" align="center">
<h3>📁 Step 1: Select Input Folder</h3>
<ul align="left">
<li>Launch the application</li>
<li>Click <b>"Select Images Folder"</b></li>
<li>Browse and select the folder containing your images</li>
</ul>
</td>
<td width="50%" align="center">
<h3>💾 Step 2: Set Output Folder</h3>
<ul align="left">
<li>Click <b>"Select Output Folder"</b></li>
<li>Choose where to save annotations and processed images</li>
<li>Folders will be created automatically</li>
</ul>
</td>
</tr>
<tr>
<td width="50%" align="center">
<h3>🏷️ Step 3: Configure Classes</h3>
<ul align="left">
<li>Click <b>"Edit Classes"</b> button</li>
<li>In the popup window, add/edit/remove classes</li>
<li>Each class gets auto-assigned a color</li>
<li>Click <b>"Save"</b> when done</li>
</ul>
</td>
<td width="50%" align="center">
<h3>✏️ Step 4: Start Annotating!</h3>
<ul align="left">
<li>Click and drag to draw boxes around objects</li>
<li>Select different classes using number keys 1-9</li>
<li>Ctrl+Click inside a box to delete it</li>
<li>Use mouse wheel to zoom in/out</li>
</ul>
</td>
</tr>
</table>

### ⌨️ Time-Saving Shortcuts

| Action | How To Do It |
|--------|--------------|
| **Go to next image** | Press **Spacebar** (auto-saves current annotations) |
| **Go to previous image** | Click **"Previous"** button |
| **Change class** | Press keys **1-9** to quickly switch between classes |
| **Delete a box** | **Ctrl+Click** inside the box you want to remove |
| **Clear all boxes** | Click **"Clear"** button (removes annotation file too) |
| **Zoom in/out** | Use **mouse wheel** (anchored zoom at cursor position) |

> **Pro Tip:** You don't need to manually save! Annotations are automatically saved when you move to the next image.

## 💎 Why this Annotator easier 

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

## 💻 Getting the Code & Implementation

### Clone the Repository
```bash
git clone https://github.com/yourusername/venus-image-annotator.git
cd venus-image-annotator
```

### Setting Up the Development Environment

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required libraries:
```bash
pip install PyQt5 pyyaml
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python via_annotator.py
```

### Implementation for Your Own Project

To integrate Venus Image Annotator into your own project:

1. Copy the core files:
   - `via_annotator.py` (main application)
   - `classes.yaml` (if you have predefined classes)

2. Import and use in your code:
```python
from via_annotator import VenusAnnotator

# Initialize the application
app = QApplication(sys.argv)
annotator = VenusAnnotator()
annotator.show()
sys.exit(app.exec_())
```

## 🔄 Updating & Customizing the Code

### Adding New Features

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-new-feature
```

3. Make your changes to the code
4. Test thoroughly
5. Submit a pull request

### Common Customization Points

1. **Adding new annotation types** (e.g., polygons, lines):
   - Modify `draw_box` method in `via_annotator.py`
   - Add new drawing tools to the UI

2. **Customizing output format**:
   - Modify `save_annotation` method to support your format
   - Update the loading functions to recognize your format

3. **Adding new keyboard shortcuts**:
   - Find the `keyPressEvent` method and add your shortcuts

4. **UI Customization**:
   - All UI elements are defined in the `setup_ui` method
   - Modify colors, sizes, and layouts as needed

### Troubleshooting Common Issues

- **Classes not loading?** Check your YAML file format and make sure paths are correct
- **UI elements not appearing?** Ensure PyQt5 is properly installed
- **Performance issues with large images?** Consider implementing image downscaling

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
Linux/macOS: ~/.config/VenusAnnotator\classes.yaml
```

Example Structure:
```yaml
classes:
  - id: 1
    name: "human"
  - id: 2
    name: "dog"
  - id: 3
    name: "cat"
```

✅ Or use the "Edit Classes" GUI to manage classes (no YAML editing required).


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
