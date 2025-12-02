# Project Structure
```
    📦 Project
❌  ├── 📝 main.py
❌  ├── 📝 requirements.txt
❌  ├── 📝 .env
✅  ├── 📝 .gitignore
✅  ├── 📝 project.md
❌  ├── 📝 README.md
❌  ├── 📁 logs/
❌  │   └── ...
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
❌      ├── 📁 assets/
❌      │   ├── 📝 __init__.py
❌      │   ├── 📝 emojis.py
❌      │   └── 📝 coloring.py
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
❌      │   ├── 📝 __init__.py
❌      │   ├── 📝 misc.py
❌      │   ├── 📁 testing/
❌      │   │   ├── 📝 tests_manager.py
❌      │   │   └── 📝 ...
❌      │   └── ...
❌      └── 📁 logging/
❌          ├── 📝 __init__.py
❌          └── 📝 logger.py
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

# Latest Changes
Finished the `core` module.

- Finished the `utils/core/` module.
  - Added imports to `__init__.py`.
  - Added a singleton wrapper for the Discord bot client in `bot.py`.
  - Added a singleton wrapper for the Mongo databae in `database.py`.
  - Added a static class for installing python modules (requirements) in `installer.py`.
- Updated `requirements.txt`.
- Added a database structure example to `project.md` for future reference.
- Updated `project.md`.