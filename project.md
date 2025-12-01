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
❌      ├── 📁 core/
❌      │   ├── 📝 __init__.py
❌      │   ├── 📝 bot.py
❌      │   ├── 📝 database.py
❌      │   └── 📝 installer.py
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

# TODO
...

---

# Latest Changes
Added project skeleton.

- Renamed `utils/functions/` to `utils/helpers/`.
- Removed `testing` folder from `extensions/`.
- Removed `destruct.py` and `revive.py` from `extensions/creator/`.
- Added `test.py` to `extensions/creator/`.
- Added `testing` folder to `utils/helpers/`.
- Updated `project.md`.