import argparse


class CommandArgs:
    """ Static class for defining and parsing command-line arguments. """

    parser: argparse.ArgumentParser = None
    args: argparse.Namespace = None

    install: bool = False
    prefix: str = None
    restart_feedback_channel: int = None
    restart_feedback_message: int = None
    logs_file: str = None


    @classmethod
    def define(cls) -> None:
        """ Define the command-line arguments. """

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--install', '-i', action = 'store_true', required = False,
            help = 'Run the installer. This will make sure all required modules are installed and up to date.'
        )

        parser.add_argument(
            '--prefix', '-p', type = str, required = False,
            help = 'Set the command prefix for the bot.'
        )

        parser.add_argument(
            '--restart-feedback-channel', type = int, required = False,
            help = 'Set the restart feedback channel ID. This argument is set automatically when restarting the bot '
                   'through a command and should not be set manually.'
        )

        parser.add_argument(
            '--restart-feedback-message', type = int, required = False,
            help = 'Set the restart feedback message ID. This argument is set automatically when restarting the bot '
                   'through a command and should not be set manually.'
        )

        parser.add_argument(
            '--logs-file', type = str, required = False,
            help = 'Set a specific logs file by providing the file path.'
        )

        cls.parser = parser


    @classmethod
    def parse(cls) -> None:
        """ Parse the command-line arguments. """

        cls.args = cls.parser.parse_args()
        for key, val in cls.args.__dict__.items():
            setattr(cls, key, val)


__all__ = ['CommandArgs']
