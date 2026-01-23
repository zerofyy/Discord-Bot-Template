# Project Structure
```
    📦 Project
🔄  ├── 📝 main.py
🔄  ├── 📝 requirements.txt
✅  ├── 📝 .env
✅  ├── 📝 .gitignore
✅  ├── 📝 project.md
❌  ├── 📝 README.md
✅  ├── 📁 logs/
✅  │   └── ...
❌  ├── 📁 extensions/
❌  │   ├── 📁 utility/
❌  │   │   ├── 📝 ping.py
❌  │   │   └── 📝 help.py
❌  │   ├── 📁 admin/
❌  │   │   └── 📝 settings.py
❌  │   ├── 📁 creator/
❌  │   │   ├── 📝 logs.py
❌  │   │   ├── 📝 extension.py
❌  │   │   ├── 📝 restart.py
❌  │   │   ├── 📝 test.py
❌  │   │   └── 📝 sync.py
❌  │   └── 📁 events/
❌  │       └── 📝 uptime.py
❌  └── 📁 utils/
✅      ├── 📁 assets/
✅      │   ├── 📝 __init__.py
✅      │   ├── 📝 emojis.py
✅      │   ├── 📝 constants.py
✅      │   ├── 📝 coloring.py
✅      │   ├── 📝 command_args.py
✅      │   └── 📝 logo.txt
✅      ├── 📁 core/
✅      │   ├── 📝 __init__.py
✅      │   ├── 📝 bot.py
✅      │   ├── 📝 database.py
✅      │   └── 📝 installer.py
❌      ├── 📁 extension_manager/
❌      │   ├── 📝 __init__.py
❌      │   ├── 📝 extension.py
❌      │   ├── 📝 extension_manager.py
❌      │   ├── 📝 cooldowns.py
❌      │   ├── 📝 permissions.py
❌      │   └── 📝 restrictions.py
❌      ├── 📁 exceptions_manager/
❌      │   ├── 📝 __init__.py
❌      │   └── 📝 exceptions_manager.py
❌      ├── 📁 helpers/
🔄      │   ├── 📝 __init__.py
🔄      │   ├── 📝 misc.py
❌      │   ├── 📁 testing/
❌      │   │   ├── 📝 tests_manager.py
❌      │   │   └── 📝 ...
❌      │   └── ...
✅      └── 📁 logging/
✅          ├── 📝 __init__.py
✅          ├── 📝 logger.py
```

---

# Database Structure
```
📦 Database
├── 📁 example_collection
│   ├── 🔹 example_attribute_1: str
│   └── 🔹 example_attribute_2: int
└── ...
```

---

# TODO
- Extensions Manager.
- Exceptions Manager.

---

# Changelogs

### Changelog 24.01.26A
Logger dependency handling and Installer compatibility update.

- Removed the `PlainLogger` module.
- Updates to the existing `Logger`:
  - Implemented handling of missing dependencies.
  - Added a `--logs-file` command-line argument to set a specific logs file.
  - Added safety checks to the following functions: `setup()`, `_report()`, `archive()`.
  - The `set_file()` function no longer reports logs to Discord.
  - Fixed the `_log()` function not adding new lines when writing log files.
- Updates to `Installer`:
  - The `restart()` function is now compatible with both Windows and Linux, and properly retains command-line arguments.
  - Now uses the existing `Logger` instead of the previous `PlainLogger`.
- Restructured the code in `main.py` to support the new changes.
- Updated `project.md`.

### Changelog 23.01.26A
Installer updates.

- Added the option to pass additional command-line arguments to `Installer.restart()`.
- Moved the imports in `main.py` to the top and made it so it automatically attempts to install missing requirements if
  the imports fail.
- Updated `project.md`.

### Changelog 07.12.25A
Updated the `Installer` module and added command-line arguments.

- Updates and fixes to the `Installer` module:
  - Fixed a major oversight where the module would import non-builtin packages before installing them, causing the
    program to crash.
  - Fixed the `restart()` function making an incorrect system call to restart the application. It now uses the correct
    Python executable and retains command-line arguments.
  - Added the option to clear cached requirements and modules to the `restart()` function. 
  - Added a safeguard to prevent crashing when the `packaging` requirement is missing. The module handles this issue by
    installing the package and restarting the application.
  - Replaced `Logger` with `PlainLogger` to avoid dependencies.
  - Added safeguards to all `__init__.py` files in `utils/`.
- Updates and fixes to `utils/logging/`:
  - Added a basic, static `PlainLogger` module that only relies on built-in packages.
  - Added imports to `__init__.py`.
  - Removed the `Coloring.init()` call from the `Logger.setup()` function. Coloring is now initialized in `main.py`.
  - Updated the `Logger.setup()` function to configure the system exception hook in order to log crash reports.
  - Fixed the spacing in the `Logger._log()` function.
  - Fixed the `Logger.get_path()` function returning `Path` objects instead of strings.
- Updates to `utils/assets/`:
  - Added a static `CommandArgs` module for defining and parsing command-line arguments.
  - Added imports to `__init__.py`.
  - Added a `logo.txt` file with a logo made from ASCII art. Very important.
- Restructured the code in `main.py`.
- Updated `project.md`.


### Changelog 05.12.25A
Finished the `assets` and `logging` modules.

- Finished the `utils/logging/` module:
  - Added a singleton `Logger` class for logging to the terminal, to log files, and to Discord channels.
  - Added a `LogsHandler` subclass of `logging.Handler` that redirects Discord logs to the custom logger.
  - Added imports to `__init__.py`.
- Finished the `utils/assets/` module:
  - Added a static `Coloring` class for formatting text in the terminal.
  - Added a `constants.py` file with a static `Channels` class for storing frequently used channels and potentially
    similar data in the future.
  - Added a static `Emoji` class for easy and consistent use of Discord emojis.
  - Added imports to `__init__.py`.
- Started work on the `utils/helpers/` module:
  - Added a static `Misc` class to `misc.py` for various functions.
  - Added imports to `__init__.py`.
- Added a `token` argument to `Bot.run()` so it is more consistent with `DB.setup()`.
- Changed `DB.setup()` to retrieve the connection URL from environment variables if not provided, so it is more
  consistent with `Bot.run()`.
- Added basic start code to `main.py`.
- Updated `requirements.txt`.
- Docstring changes.
- Changed the format of how changes are represented in `project.md`.
- Updated `project.md`.


### Changelog 02.12.25A
Finished the `core` module.

- Finished the `utils/core/` module.
  - Added imports to `__init__.py`.
  - Added a singleton wrapper for the Discord bot client in `bot.py`.
  - Added a singleton wrapper for the Mongo databae in `database.py`.
  - Added a static class for installing python modules (requirements) in `installer.py`.
- Updated `requirements.txt`.
- Added a database structure example to `project.md` for future reference.
- Updated `project.md`.