"""
CLI command 'bloodymary' main class
"""

from cli_toolkit.script import Script

from .commands.show import Show


class BloodyMary(Script):
    """
    Script main class for 'bloodymary' CLI command
    """
    subcommands = (
        Show,
    )


def main():
    """
    Main CLI entrypoint for bloodymary CLI
    """
    BloodyMary().run()
