# 📁 Dynamic Project Structure Generator

A lightweight Python script to **quickly generate full project folder and file structures** from a simple text-based description.

---

## ✨ Features

- 🔍 **Auto-detects format** of user input  
- 🗂️ **Parses and creates** deeply nested folders & files  
- 💬 **Inline comment support** — strips `# comments` before processing  
- 🛡️ **No duplication bug** — intelligently handles paths like `admin/index.php`  
- 🧠 **Auto-generates file content** based on file extension:
  - `.py`, `.php`, `.js`, `.css`, `.html`, `.md`, `.txt`, `.json`, `.htaccess`, etc.  
- 🧪 **Preview mode** — see the structure before it's created  
- 💻 **Cross-platform** — runs on **Windows**, **macOS**, and **Linux**  
- ♾️ **Unlimited nesting** — create structures as deep as you need  
- 📦 **No dependencies** — works offline with standard Python only  

---

## 📦 Installation

1. Ensure **Python 3.6+** is installed:
   ```bash
   python --version

2. Clone this repository:
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

3. (Optional) Make the script executable (Linux/macOS):
   chmod +x app.py

## ▶️ Usage
   1. Run the script:
      python app.py
      
   2. When prompted, paste your folder structure. Example:
      ecommerce/
          assets/
              css/
                  style.css
              js/
                  script.js
          index.php        # Main entry point
          README.md

   3. Press Enter twice to finish input.
      
   4. The script will:
        - 🧠 Detect and parse the format
        - 👁️ Preview the folder & file structure
        - 📂 Generate everything on disk
     
## 🛡 Notes
   - ⚠️ Existing files will NOT be overwritten
   - 🚀 Works offline with no third-party libraries
   - ⚡ Designed to speed up scaffolding for developers


## 📄 License

This project is licensed under the MIT License.
Feel free to use, modify, and distribute — just provide attribution.
