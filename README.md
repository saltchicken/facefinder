# Facer

Facer is a Python-based facial recognition tool that uses deep learning to analyze images and videos, extract facial embeddings, and manage them in a PostgreSQL database.

Please note that this project is still in development and has the potential to be far more efficient. It is still far more efficient than rudimentary practices.

## Features

- **Embedding Extraction**: Extract facial embeddings from images and videos (realtime support in development).
- **Database Integration**: Store, retrieve, and manage facial embeddings using PostgreSQL with support for vector-based matching.
- **Multi-File Support**: Handle individual images, folders, and video files.
- **Command-Line Interface**: Simple CLI for inserting and matching embeddings and interactive prompt for continuous exploration and analysis.

## Prerequisites

Command line access of ffmpeg required
```bash
pip install ffmpeg
```

[PostgreSQL](https://www.postgresql.org/)\
[pgvector](https://github.com/pgvector/pgvector)

Table creation is handled automatically.\
\
*IMPORTANT* If you are running PostgreSQL remotely there are additional server-side steps to allow the connection (outside the scope of this project)

### Installation

```
pip install git+https://github.com/saltchicken/facer
```
or
```
git clone https://github.com/saltchicken/facer.git
cd facer
pip install .

```

### Environment Variables

A .env file is required for PostgreSQL server connection. If not automatically detected env_loader will prompt for the following variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_NAME=postgres
DB_PASSWORD=
```

## Usage

Facer provides a command-line interface for interacting with the tool. Below are the available commands.

### Inserting Embeddings

Insert embeddings from an image, video, or folder:

```bash
facer insert <input_file> <name> --verbose
```

- `<input_file>`: Path to the image, folder, or video file.
- `<name>`: Name of the person in the input.
- `--verbose`: Optional flag to display debug logs.

### Matching Embeddings

Match an input image, folder, or video file with stored embeddings:

```bash
facer match <input_file> --verbose
```

- `<input_file>`: Path to the image, folder, or video file.
- `--verbose`: Optional flag to display debug logs.

### Examples

#### Insert an Image

```bash
facer insert /path/to/image.jpg JohnDoe --verbose
```

#### Match a Video File

```bash
facer match /path/to/video.mp4 --verbose
```

## Project Structure

```
.
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── src/
│   ├── facer/              # Main application source code
│   │   ├── analyze.py      # Facial analysis and embedding extraction
│   │   ├── database.py     # PostgreSQL database interaction
│   │   ├── facer.py        # Main Facer class for core functionality
│   │   ├── utils/
│   │   │   ├── helper.py   # Utility functions
│   │   ├── __init__.py     # Package initialization
│   │   ├── __main__.py     # Command-line entry point
```

## Dependencies

Key dependencies include:

- [DeepFace](https://github.com/serengil/deepface) for facial analysis.
- [Dlib](http://dlib.net/) for face detection.
- [Psycopg](https://www.psycopg.org/) for PostgreSQL interaction.
- [Loguru](https://github.com/Delgan/loguru) for logging.
- [Env Loader](https://github.com/saltchicken/env_loader) for environment variable management.
- [Fripper](https://github.com/saltchicken/fripper) for video frame extraction.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or fix bugs.

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the authors of the libraries used in this project for their amazing work.


