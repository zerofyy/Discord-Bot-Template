# TODO
- Database 
  - Implement an object-based system where operations on documents inside the database are done through Python objects,
    allowing for type-hinting, avoiding errors, and better updating of existing documents.
- Extension Manager
  - Add an argument to `Command` extensions to choose between `prefix`, `slash`, or `hybrid` commands.
  - Commands are automatically synced, probably to all servers. This shouldn't be the default behavior.
  - Extensions should not self-register to the ExtensionRegistry; instead, this should be done by the ExtensionManager
    so extension categories can be properly updated.
  - Every Extension has an `authorized_servers` attribute which should be properly implemented...
    Either through a `prerun_check` or injected automatically, avoiding running the extension logic if called from an
    unauthorized server.
- Assets
  - The `assets` module is supposed to act as a template, but currently it required manual modifications.
    There should be a way to load in custom emojis and constants. This could be done with a config file or through a
    creator-level command that collects emojis from a server or bot and writing them in a config by matching emoji names
    with variable names in the `Emoji` module.
- Exceptions Manager
  - Implement custom exceptions and replace the existing ones inside functions.
  - Previously, the `ExceptionManager` required access to the `ExtensionManager` for providing extra information when an
    extension error occurs. This could be avoided by relying solely on the `ExtensionRegistry`, possibly allowing for
    custom exceptions to be used in all other modules.

---

# Notes & Ideas
Database Structure
```
📦 Database
├── 📁 example_collection
│   ├── 🔹 example_attribute_1: str
│   └── 🔹 example_attribute_2: int
└── ...
```

---

# Latest Changes
Began implementing the dynamic extension management system.

- Began implementing dynamic extension management (`utils/extension_manager/`):
  - Added `ExtensionRegistry` for storing all extension instances.
  - Added an abstract `Extension` class representing a Discord extension.
  - Added `Command`, `Listener`, and `Task` classes that inherit from `Extension`.
  - Implemented logic to use these classes as decorators when defining extensions.
  - Implemented dynamic injection of the `setup()` function when loading extensions.
- Implemented a simple `ping` command for testing the new extensions system.
- Converted all singleton classes from `utils` to static classes utilizing `@classmethod` decorators.
- Moved `CommandArgs` from `utils/assets/` to `utils/core/`.
- Added new emojis to the `Emoji` module:
  - Added two general-use emojis: `avatar` and `event`.
  - Added an `ext_status` emoji section for extension statuses.
- Added previously missing information about functions raising errors to their doc-strings.
- Other minor doc-string changes.
- Updated `project.md`.
