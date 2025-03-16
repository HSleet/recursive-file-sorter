# Recursive File Sorter

This project is a simple recursive file sorter written in Python. It traverses directories and sorts files based on their extensions into corresponding folders.

## Features

- Recursively traverses directories
- Sorts files based on their extensions
- Creates folders for each file type if they do not exist
- Optional cleanup of empty directories

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/recursive-file-sorter.git
    ```
2. Navigate to the project directory:
    ```sh
    cd recursive-file-sorter
    ```

## Usage

Run the script with the directory you want to sort as an argument:
```sh
python sorter.py /path/to/directory [path/to/destination] [options]

# Example

python sorter.py /path/to/directory -d path/to/destination --cleanup

# Options
-d, --destination    Specify the destination directory
--cleanup            Remove empty directories after sorting

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Author

- Your Name - [yourusername](https://github.com/yourusername)
