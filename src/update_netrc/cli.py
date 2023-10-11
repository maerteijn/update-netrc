import argparse
import sys
from typing import Union

from update_netrc import NETRC_PATH, UpdateNetrc

parser = argparse.ArgumentParser(
    description=f"Default .netrc path: {NETRC_PATH}",
)
parser.add_argument(
    "--netrc-path",
    help="Specify an alternative location for the used netrc file",
    type=str,
    default=NETRC_PATH,
)

subparsers = parser.add_subparsers(dest="command")
update_cmd_parser = subparsers.add_parser("update")


update_cmd_parser.add_argument(
    "host", help="Selects the host (machine) you want to update"
)

update_cmd_parser.add_argument(
    "--login", help="Update the login of the specified host", type=str, default=""
)
update_cmd_parser.add_argument(
    "--account", help="Update the account of the specified host", type=str, default=""
)
update_cmd_parser.add_argument(
    "--password", help="Update the password of the specified host", type=str, default=""
)


def main(args: Union[list, None] = None) -> None:
    parsed_args = parser.parse_args(args)

    if parsed_args.command == "update":
        netrc_instance = UpdateNetrc(netrc_path=parsed_args.netrc_path)
        netrc_instance.update_entry(
            host=parsed_args.host,
            login=parsed_args.login,
            account=parsed_args.account,
            password=parsed_args.password,
        )
        sys.stdout.write(f"Updating {parsed_args.netrc_path}...\n")

        try:
            netrc_instance.is_valid()
            netrc_instance.save()
            sys.stdout.write("Done!\n")
        except ValueError as e:
            sys.stderr.write(f"{e}\n")
