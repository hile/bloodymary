"""
Command to load and plot blood pressure measurements
"""

from datetime import datetime, timedelta

import matplotlib.pyplot as mp

from .base import BloodyMaryCommand


COLUMNS = ['Systolic', 'Diastolic', 'Pulse']


class Show(BloodyMaryCommand):
    """
    Show blood pressure file graphically
    """
    name = 'show'

    def register_parser_arguments(self, parser):
        """
        Add date filter argument
        """
        parser = super().register_parser_arguments(parser)
        parser.add_argument(
            '--days',
            type=int,
            help='How many recent days to show'
        )
        parser.add_argument(
            '--columns',
            action='append',
            help='Columns to show in graph'
        )
        return parser

    def parse_args(self, args=None, namespace=None):
        """
        Parse arguments for 'bloodymary show' command
        """
        args = super().parse_args(args, namespace)
        if args.columns:
            columns = []
            for arg in args.columns:
                for value in arg.split(','):
                    if value not in COLUMNS:
                        self.exit(1, f'Invalid column: {value}')
                    columns.append(value)
            args.columns = columns
        else:
            args.columns = COLUMNS

        return args

    def run(self, args):
        """
        Load and plot the data
        """
        if args.days:
            records = self.data.records.filter(start_time=datetime.now() - timedelta(days=args.days))
        else:
            records = self.data.records

        max_systolic = max(measurement.systolic for measurement in records) + 20
        dataframe = self.data.get_dataframe(records)
        dataframe.plot(
            x='Time',
            y=args.columns,
            kind='bar',
            grid=True,
            rot=30,
            yticks=list(range(0, max_systolic, 5)),
            position=0.9,
            figsize=(15, 10),
        )
        mp.show()
