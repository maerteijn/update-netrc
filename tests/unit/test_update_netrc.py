from update_netrc import UpdateNetrc


def test_netrc_init__file_exists(test_netrc_path):
    netrc = UpdateNetrc(netrc_path=test_netrc_path)
    list(netrc.hosts.keys()) == ["myserver", "localhost", "default"]


def test_netrc_init__file_nonexisent(test_netrc_path_nonexisent):
    netrc = UpdateNetrc(netrc_path=test_netrc_path_nonexisent)
    netrc.hosts.keys() == []


def test_netrc__output(test_netrc_path):
    netrc = UpdateNetrc(netrc_path=test_netrc_path)
    string_output = str(netrc)

    # Make sure the dumped output is the same as the original file
    assert string_output == open(test_netrc_path, "r").read()


def test_netrc__create_entry(test_netrc_path_nonexisent):
    netrc = UpdateNetrc(netrc_path=test_netrc_path_nonexisent)
    netrc.update_entry(host="my_host", login="my_login")

    assert list(netrc.hosts.keys()) == ["my_host"]

    login, account, password = netrc.hosts["my_host"]
    assert login == "my_login"
    assert account == ""
    assert password == ""

    string_output = str(netrc)
    assert string_output == "machine my_host\n\tlogin my_login\n\tpassword \n"


def test_netrc__update_entry__password(test_netrc_path):
    netrc = UpdateNetrc(netrc_path=test_netrc_path)

    # We know that 'myserver' is an entry in the existing .netrc file
    existing_login, _, _ = netrc.hosts["myserver"]

    netrc.update_entry(host="myserver", password="my_updated_password")

    login, account, password = netrc.hosts["myserver"]

    # Check that the login is unchanged
    assert login == existing_login
    assert password == "my_updated_password"
