import os

desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Get the desktop path
folder_name = "Result_123234"  # Set the folder name
folder_path = os.path.join(desktop_path, folder_name)  # Create the full path to the new folder

#folder_path = "result"
print(folder_path)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)  # Create the new folder
else:
    print("Folder already exists.")