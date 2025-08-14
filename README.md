Dynamic Project Structure Generator
A Python script to quickly generate complete project folder and file structures from a text description.

✨ Features
Auto-detects format of the user-provided structure
Parses and creates nested folders & files to any depth
In-line comment support — Comments are stripped before processing
No duplication bug — Correctly handles paths like
admin/index.php without creating extra unwanted folders
Auto-generated file content based on file extension (.py, .php, .js, .css, .html, .md, .txt, .json, .htaccess, etc.)
Cross-platform — Works on Windows, macOS, and Linux
Preview mode — See the parsed structure before creation
Unlimited nesting — Create as deeply nested structures as needed


📦 Installation
1. Make sure Python 3.6+ is installed:
   python --version

2. Clone or download the script to your local machine:
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

3. Make script executable (Linux/macOS):
   chmod +x app.py


▶ Usage
1. Run the script:
app.py
The script detects format, previews it, and creates folders/files

2. Paste your structure description when prompted, for example:
Example:
ecommerce/
    assets/
        css/
            style.css
        js/
            script.js
    index.php         # Main entry point
    README.md

3. End input with a double Enter.

4. The script will:
    Detect the format
    Parse and preview the structure
    Generate actual folders and files on disk


🛡 Notes
This tool never overwrites existing files unless you manually remove them first.
Works offline no third-party library dependencies.
Designed to speed up project scaffolding for developers.

📜 License
This project is licensed under the MIT License — you may modify and distribute with attribution.
