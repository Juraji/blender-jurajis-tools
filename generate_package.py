"""
Development tool: Generate ZIP package for Blender to install
"""
from zipfile import ZipFile, ZIP_DEFLATED
import os

if __name__ == '__main__':
    pkg_base_name: str = "blender_jurajis_tools"
    pkg_name: str = f"{pkg_base_name}.zip"

    try:
        os.remove(pkg_name)
    except OSError:
        pass

    excludes: list[str] = [
        "generate_package.py",
        ".idea",
        ".git",
        ".venv",
    ]

    with ZipFile(pkg_name, 'w', ZIP_DEFLATED) as zipf:
        for folder_name, subdir, filenames in os.walk("."):
            for excluded in excludes:
                if excluded in subdir:
                    subdir.remove(excluded)

            for filename in filenames:
                if filename in excludes:
                    continue

                file_path = os.path.join(folder_name, filename)
                zipf.write(file_path)
