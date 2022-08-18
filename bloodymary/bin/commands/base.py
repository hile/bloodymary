"""
CLI 'bloodymary' subcommands base class
"""
from typing import Optional

from cli_toolkit.command import Command

from ...constants import FileFormat
from ...exceptions import ConfigurationError
from ...formats import BloodPressureData


class BloodyMaryCommand(Command):
    """
    Base class of subcommand for 'bloodymary' CLI
    """
    data: Optional[BloodPressureData] = None

    def register_parser_arguments(self, parser):
        """
        Register required parser arguments
        """
        parser.add_argument(
            '-f-', '--format',
            choices=[item.value for item in FileFormat],
            help='File format to load'
        )
        parser.add_argument(
            'filename',
            help='Path to file to load'
        )
        return parser

    def parse_args(self, args=None, namespace=None):
        """
        Parse CLI arguments
        """
        try:
            self.data = BloodPressureData(file_format=args.format)
            self.data.records.load(args.filename)
        except ConfigurationError as error:
            self.exit(1, error)
        return args
