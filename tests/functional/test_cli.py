from netrc import netrc

import pytest
from update_netrc.cli import main


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help__main(capsys, option):
    with pytest.raises(SystemExit):
        main([option])

    output = capsys.readouterr().out
    assert "usage:" in output
    assert "{update}" in output  # There should be an update subcommand


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help__update(capsys, option):
    with pytest.raises(SystemExit):
        main(["update", option])

    output = capsys.readouterr().out
    # Check that something is shown from the {update} subcommand help text
    assert "--password PASSWORD" in output


@pytest.mark.parametrize(
    "credentials",
    (
        ("my-updated-login", "", ""),
        ("", "my-updated-account", ""),
        ("", "", "my-updated-password"),
        ("my-updated-login", "my-updated-account", "my-updated-password"),
        ("", "", ""),
    ),
)
def test_update_host(capsys, test_netrc_path, credentials):
    new_login, new_account, new_password = credentials

    cli_options = [
        "--netrc-path",
        str(test_netrc_path),
        "update",
        "localhost",
        "--login",
        new_login,
        "--account",
        new_account,
        "--password",
        new_password,
    ]
    main(cli_options)

    output = capsys.readouterr().out
    assert f"Updating {test_netrc_path}..." in output
    assert "Done!" in output

    netrc_instance = netrc(file=test_netrc_path)
    login, account, password = netrc_instance.hosts["localhost"]

    # Sanity check that the new credentials are written to the .netrc file,
    # but only when they are not an empty string
    assert login == new_login if new_login else login
    assert account == new_account if new_account else account
    assert password == new_password if new_password else password
