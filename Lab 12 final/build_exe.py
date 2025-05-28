import os
import shutil
import subprocess
import datetime

def main():
    print("Building Smart Mart System executable...")
    
    # Clean build directories if they exist
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)
    
    # Build executable
    print("Building executable with PyInstaller...")
    subprocess.run(['pyinstaller', '--onefile', '--windowed', 'main.py'])
    
    # Create release folder
    release_dir = f"release_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(release_dir, exist_ok=True)
    
    # Copy executable to release folder
    print("Copying executable to release folder...")
    shutil.copy('dist/main.exe', f"{release_dir}/SmartMartSystem.exe")
    
    # Copy data files to release folder
    print("Copying data files to release folder...")
    os.makedirs(f"{release_dir}/data", exist_ok=True)
    os.makedirs(f"{release_dir}/images", exist_ok=True)
    
    # Copy data files
    for data_file in ['admin.txt', 'cashiers.txt', 'products.txt', 'bills.txt']:
        if os.path.exists(f"data/{data_file}"):
            shutil.copy(f"data/{data_file}", f"{release_dir}/data/{data_file}")
    
    # Copy images
    for image_file in os.listdir('images'):
        if os.path.isfile(f"images/{image_file}"):
            shutil.copy(f"images/{image_file}", f"{release_dir}/images/{image_file}")
    
    # Copy README.md
    shutil.copy('README.md', f"{release_dir}/README.md")
    
    print(f"Build completed! Executable is in the '{release_dir}' folder.")

if __name__ == "__main__":
    main() 