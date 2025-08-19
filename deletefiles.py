from pathlib import Path

# Folder containing your CSVs
folder = Path("Files")  # replace with your folder path

# Find files ending with "-1 2.csv"
files_to_delete = [f for f in folder.iterdir() if f.is_file() and f.name.endswith("-1 2.csv")]

# Preview the files first
if files_to_delete:
    print("Files that will be deleted:")
    for f in files_to_delete:
        print(f)
    
    # Confirm before deleting
    confirm = input("Do you want to delete these files? (y/n) ")
    if confirm.lower() == 'y':
        for f in files_to_delete:
            f.unlink()
        print(f"Deleted {len(files_to_delete)} files.")
    else:
        print("No files were deleted.")
else:
    print("No files matching the pattern were found.")