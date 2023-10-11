import netrc
import os

NETRC_PATH = os.path.join(os.path.expanduser("~"), ".netrc")


class UpdateNetrc(netrc.netrc):
    def __init__(self, netrc_path: str = NETRC_PATH):
        self.netrc_path = netrc_path

        if not os.path.exists(netrc_path):
            open(netrc_path, "w").close()

        super().__init__(file=netrc_path)

    def __repr__(self) -> str:
        """
        Override from https://github.com/python/cpython/blob/8f22504d745c4a843ff30b6810ab606817480746/Lib/netrc.py#L175-L189
        Updated this a bit to respect the 'default' keyword "as is",
        improved readability of the code
        """
        output = []

        for host in self.hosts.keys():
            login, account, password = self.hosts[host]

            if host == "default":
                output.append(f"default\n\tlogin {login}")
            else:
                output.append(f"machine {host}\n\tlogin {login}")

            if account:
                output.append(f"\taccount {account}")

            output.append(f"\tpassword {password}")

        for macro in self.macros.keys():
            output.append(f"macdef {macro}")

            output_line = []
            for line in self.macros[macro]:
                output_line.append(line)
            output.append("".join(output_line))

        return "\n".join(output) + "\n"

    def update_entry(
        self, host: str, *, login: str = "", account: str = "", password: str = ""
    ) -> None:
        if host not in self.hosts:
            self.hosts[host] = ("", "", "")

        old_login, old_account, old_password = self.hosts[host]

        self.hosts[host] = (
            login or old_login,
            account or old_account,
            password or old_password,
        )

    def is_valid(self) -> bool:
        """ "
        Makes sure all login / password (required fields) have a value
        """
        for host in self.hosts:
            login, account, password = self.hosts[host]

            if login == "":
                raise ValueError(f"{host}: login is empty, please provide a value")
            if password == "":
                raise ValueError(f"{host}: password is empty, please provide a value")
        return True

    def save(self) -> None:
        with open(self.netrc_path, "w") as f:
            f.write(str(self))
