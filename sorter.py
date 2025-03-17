from os import walk, mkdir, rmdir
from os.path import join, splitext, exists, isdir
import argparse
import shutil
import logging

# Logging configuration
log_file = 'sorter.log'
log_format = '%(asctime)s - %(levelname)s - %(message)s'

log_level = logging.INFO
logging.basicConfig(filename=log_file, level=log_level, format=log_format)


def get_args():
    """
    Get command line arguments
    
    Returns:
    args: Namespace - the parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to the directory to sort')
    parser.add_argument('-d', '--destination', help='Destination directory')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup empty directories')
    
    return parser.parse_args()

def get_files(path):
    """
    Get all files in a directory
    
    Args:
    path: str - the path to the directory
    """
    for root, dirs, files in walk(path):
        for file in files:
            yield join(root, file)
            
def sort_by_extension(filepath, destination_folder):
    """
    Sort a file by its extension
    
    Args:
    filepath: str - the path to the file
    destination_folder: str - the path to the destination folder
    """
    global skipped_files # Use global variable to keep track of skipped files
    
    logging.info(f'Getting extension of {filepath}')
    _, extension = splitext(filepath)
    
    if not extension:
        # If no extension is found, log a warning and skip the file
        logging.warning(f'No extension found for {filepath} - skipping')
        skipped_files += 1
        return
    
    # Remove the dot and convert to lowercase
    extension = extension.lstrip('.').lower()
    logging.info(f'Extension found: {extension}')
    
    # Create a folder for the extension if it doesn't exist
    extension_folder_name = f'{extension}_files'
    extension_folder_path = join(destination_folder, extension_folder_name)
    # Check if the folder exists and create it if it doesn't
    if not exists(extension_folder_path):
        try:
            logging.info(f'Creating folder {extension_folder_path}')
            mkdir(extension_folder_path)
        except Exception as e:
            logging.error(f'Failed to create folder {extension_folder_path}: {e}')
            skipped_files += 1
            return
        
    # Move the file to the extension folder
    try:
        new_path = shutil.move(filepath, extension_folder_path)
        
    except shutil.Error as e:
        # If the file already exists in the destination folder, log a warning and skip the file
        logging.error(f'Failed to move {filepath}: {e} - skipping file')
        skipped_files += 1
        return
    
    except Exception as e:
        # Log an error and skip the file
        logging.error(f'An error occurred: {e} - skipping file {filepath}')
        skipped_files += 1
        return
    
    else:
        # Log the successful move
        logging.info(f'Moved {filepath} to {new_path}')
            

def cleanup(path):
    """
    Cleanup function to remove empty folders
    
    Args:
    
    path: str - the path to the directory to clean up
    """
    skipped_folders = 0
    
    # Traverse the directory bottom-up to remove empty folders
    for root, dirs, files in walk(path, topdown=False):  # Traverse bottom-up
        for dir_name in dirs:
            # Get the full path of the directory
            dir_path = join(root, dir_name)
            # Check if the directory is empty
            if not exists(join(dir_path)):  # In case it's already removed
                logging.info(f'Directory {dir_path} already removed')
                continue
            if not any(isdir(join(dir_path, item)) or exists(join(dir_path, item)) for item in files + dirs):
                try:
                    rmdir(dir_path)  # Remove the empty folder
                    logging.info(f'Deleted empty directory: {dir_path}')
                except OSError as e:
                    logging.error(f'Failed to delete directory {dir_path}: {e}')
                    skipped_folders += 1
    logging.info(f'Cleanup finished. Skipped folders: {skipped_folders}')
    print(f'Cleanup finished. Skipped folders: {skipped_folders}')
                    
                    
if __name__ == '__main__':
    args = get_args()
    
    logging.info(f'Processing files with provided arguments - source: {args.path}, destination: {args.destination}')
    
    # Counters
    skipped_files = 0
    total_files = 0
    
    # Get source and destination folders 
    source_folder = args.path
    
    if args.destination:
        logging.warning(f'Destination folder not provided. Using source folder {source_folder} as destination folder')
        destination_folder = args.destination
    else:
        destination_folder = source_folder
    
    # Process files
    for file in get_files(source_folder):
        total_files += 1
        sort_by_extension(file, destination_folder)
    
    logging.info(f'Finished processing files. Total files: {total_files}, skipped files: {skipped_files}')
    print(f'Finished processing files. Total files: {total_files}, skipped files: {skipped_files}')
    
    # Cleanup
    if args.cleanup:
        logging.info('Cleaning up empty directories')
        cleanup(source_folder)
    else:
        logging.info('Cleanup skipped')