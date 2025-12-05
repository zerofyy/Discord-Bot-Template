# Project Structure
```
    📦 Project
❌  ├── 📝 main.py
❌  ├── 📝 requirements.txt
❌  ├── 📝 .env
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
✅      │   └── 📝 coloring.py
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
✅          └── 📝 logger.py
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
...

---

# Changelogs

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