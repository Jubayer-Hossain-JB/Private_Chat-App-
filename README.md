# Private Chat App

Private Chat App is a  Python project that provides a private chat solution in the local network without Internet. This repository contains the server and alsoclient entry point.

## Features
- Socket-based chat backend
- Web interface (templates/static under `web/`)
- Desktop GUI client
- Uploads directory for handling user files

## Repository layout
- LICENSE
- Private_Chat.spec — packaging spec (PyInstaller or similar)
- web.py — web backend / web server
- soket.py — socket/chat server
- window.py — desktop GUI client
- loader.cpp — optional native loader/build helper
- web/ — web assets (templates/static)
- resources/ — application resources
- uploads/ — directory for user uploads
- dist/ — distribution output (usually generated)
- icon.ico — app icon

## Prerequisites
- Python 3.8+ recommended
- A C/C++ toolchain to compile `loader.cpp` if you intend to use the native loader (optional)
- Virtual environment recommended


## File uploads & storage
- Uploaded files are stored in `uploads/`. Ensure this directory is writable by the process.
- Sanitize and validate uploads before use if you plan to deploy publicly.


## Contributing
- Open issues or PRs on the repo.
- When contributing, include tests or manual reproduction steps for bugs.

## License
The project includes a LICENSE file. Check it for the full license text.
