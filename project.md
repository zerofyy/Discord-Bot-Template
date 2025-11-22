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
❌  │   │   ├── 📝 help.py
❌  │   ├── 📁 admin/
❌  │   │   ├── 📝 settings.py
❌  │   ├── 📁 creator/
❌  │   │   ├── 📝 logs.py
❌  │   │   ├── 📝 extension.py
❌  │   │   ├── 📝 restart.py
❌  │   │   ├── 📝 sync.py
❌  │   │   ├── 📝 destruct.py
❌  │   │   ├── 📝 revive.py
❌  │   ├── 📁 events/
❌  │   │   ├── 📝 uptime.py
❌  │   └── 📁 testing/
❌  │       ├── 📝 test_find_member.py
❌  │       ├── 📝 test_autocomplete.py
❌  │       ├── 📝 test_perms_check.py
❌  │       ├── 📝 test_cooldowns.py
❌  │       ├── 📝 test_ext_helpers.py
❌  │       └── 📝 test_errors.py
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
❌      ├── 📁 functions/
❌      │   ├── 📝 __init__.py
❌      │   ├── 📝 misc.py
❌      │   └── ...
❌      └── 📁 logging/
❌          ├── 📝 __init__.py
❌          └── 📝 logger.py
```

---

# TODO
- Figure out whether helpers will be part of `utils` or will they be somehow bundled along with the
  extensions. **Note:** Multiple extensions may need to use the same helpers, so bundling them with each 
  extension separately wouldn't work. However, helpers still need to allow reloading, meaning that
  extensions need to have some sort of dependencies.
- Figure out how extensions will be parsed. The simple way is through a big list of extensions saved in a
  file. The other, more complex, way is to parse them by going through the extension folders. I'm not sure
  how to fetch extension data from the file though.

---

# Latest Changes
Created a project plan.

- Added `project.md`.
- Added `.gitignore`.