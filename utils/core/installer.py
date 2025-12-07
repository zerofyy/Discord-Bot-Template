import sys
import os
import subprocess
import time
from importlib import metadata

from utils.logging import PlainLogger


try:
    from packaging import requirements
    _PACKAGING_AVAILABLE = True

except ModuleNotFoundError:
    class requirements:
        """ Dummy class for the "requirements" module. """

        class Requirement:
            """ Dummy class for the "requirements" module. """

            name = None
            specifier = None

            def __init__(self, _):
                pass


    _PACKAGING_AVAILABLE = False


class Installer:
    """ Static class for installing python modules with pip. """

    @staticmethod
    def check_requirements() -> dict[str, str]:
        """
        Check the module requirements.

        ------

        Returns:
             A dictionary with missing or outdated requirements.
        """

        PlainLogger.info('Installer', 'Checking requirements...')

        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

        bad_modules = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            module, is_ok, info = Installer.check_module(line)

            if not is_ok:
                bad_modules[module.name] = info
                PlainLogger.warning('Installer', f'Module "{module.name}" is {info}.')

            else:
                PlainLogger.ok('Installer', f'Module "{module.name}" is up to date.')

        PlainLogger.ok('Installer', 'Finished checking requirements.')
        return bad_modules


    @staticmethod
    def check_module(module: str) -> tuple[requirements.Requirement, bool, str]:
        """
        Check whether a module is installed and up-to-date.

        ------

        Arguments:
            module: The python module being checked with optional version specifiers.

        ------

        Returns:
            The module, whether it is installed and up-to-date, and information regarding its state.
        """

        module = requirements.Requirement(module)

        try:
            metadata.distribution(module.name)

            installed_version = metadata.version(module.name)
            if module.specifier and not module.specifier.contains(installed_version):
                return module, False, 'outdated'

        except metadata.PackageNotFoundError:
            return module, False, 'missing'

        return module, True, 'OK'


    @staticmethod
    def install_module(module: str) -> None:
        """
        Install a python module.

        ------

        Arguments:
             module: The python module to install with optional version specifiers.
        """

        PlainLogger.info('Installer', f'Installing module "{module}"...')
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', module],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )

        PlainLogger.ok('Installer', f'Successfully installed module "{module}".')


    @staticmethod
    def update_module(module: str) -> None:
        """
        Update a python module.

        ------

        Arguments:
             module: The python module to update with optional version specifiers.
        """

        PlainLogger.info('Installer', f'Updating module "{module}"...')
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', module, '--upgrade'],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )

        PlainLogger.ok('Installer', f'Successfully updated module "{module}".')


    @staticmethod
    def ensure_requirements() -> None:
        """ Check for and install any missing or outdated requirements. """

        PlainLogger.ok('Installer', f'Checking requirements...')

        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

        do_restart = False

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            module, is_ok, info = Installer.check_module(line)
            if is_ok:
                PlainLogger.ok('Installer', f'Module "{module.name}" is up to date.')
                continue

            PlainLogger.warning('Installer', f'Module "{module.name}" is {info}.')

            if info == 'missing':
                Installer.install_module(line)
                do_restart = True

            elif info == 'outdated':
                Installer.update_module(line)
                do_restart = True

        if do_restart:
            Installer.restart()


    @staticmethod
    def restart(clear_cache: bool = True) -> None:
        """
        Restart the application.

        ------

        Arguments:
            clear_cache: Whether to clear the cache before restarting.
        """

        if clear_cache:
            PlainLogger.warning('Installer', 'Preparing for restart...')
            time.sleep(2)

            PlainLogger.info('Installer', 'Collecting cached modules...')

            with open('requirements.txt', 'r') as file:
                lines = file.readlines()

            cached_modules = []
            for module in sys.modules:
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    requirement = requirements.Requirement(line)
                    if module.startswith(requirement.name) or module.startswith('utils'):
                        cached_modules.append(module)
                        break

            PlainLogger.info('Installer', 'Clearing cached modules...')
            for module in cached_modules:
                del sys.modules[module]
                PlainLogger.info('Installer', f'Cleared module "{module}" from cache.')

        PlainLogger.warning('Installer', 'Restarting...')
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

        cmd_args = ' '.join(sys.argv[1:])
        os.system(f'"{sys.executable}" main.py {cmd_args}')
        sys.exit(0)


if not _PACKAGING_AVAILABLE:
    PlainLogger.error('Installer', 'Module "packaging" is missing.')
    Installer.install_module('packaging')
    Installer.restart(clear_cache = False)


__all__ = ['Installer']
