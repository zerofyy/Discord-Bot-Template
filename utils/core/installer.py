import sys
import os
import subprocess
from importlib import metadata
from packaging import requirements

from utils.logging import Logger


Logger = Logger()


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

        Logger.info('Installer', 'Checking requirements...')

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
                Logger.info('Installer', f'Module {module.name} is {info}.')

            else:
                Logger.info('Installer', f'Module {module.name} is already installed.')

        Logger.ok('Installer', 'Finished checking requirements.')
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

        Logger.info('Installer', f'Installing module {module}...')
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', module],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        Logger.ok('Installer', f'Finished installing module: {module}.')


    @staticmethod
    def update_module(module: str) -> None:
        """
        Update a python module.

        ------

        Arguments:
             module: The python module to update with optional version specifiers.
        """

        Logger.info('Installer', f'Updating module {module}...')
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', module, '--upgrade'],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        Logger.ok('Installer', f'Finished updating module: {module}.')


    @staticmethod
    def ensure_requirements() -> None:
        """ Check for and install any missing or outdated requirements. """

        Logger.info('Installer', 'Checking requirements...')

        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            module, is_ok, info = Installer.check_module(line)
            if is_ok:
                Logger.info('Installer', f'Module {module.name} is up to date.')
                continue

            Logger.info('Installer', f'Module {module.name} is {info}.')

            if info == 'missing':
                Installer.install_module(line)

            elif info == 'outdated':
                Installer.update_module(line)


    @staticmethod
    def restart() -> None:
        """ Restart the application. """

        Logger.warning('Installer', 'Restarting...')
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('python main.py')
        sys.exit(0)


__all__ = ['Installer']
