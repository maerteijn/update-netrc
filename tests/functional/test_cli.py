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
    "params",
    (
        ("localhost", "my-updated-login", "", ""),
        ("localhost", "", "my-updated-account", ""),
        ("localhost", "", "", "my-updated-password"),
        ("localhost", "my-updated-login", "my-updated-account", "my-updated-password"),
        ("localhost", "", "", ""),
    ),
)
def test_update__existing_host(capsys, test_netrc_path, params):
    host, new_login, new_account, new_password = params

    cli_options = [
        "--netrc-path",
        str(test_netrc_path),
        "update",
        host,
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


@pytest.mark.parametrize(
    "params",
    (
        # new-host is a new entry
        ("new-host", "my-updated-login", "", "", False),
        ("new-host", "", "my-updated-account", "", False),
        ("new-host", "", "", "my-updated-password", False),
        ("new-host", "", "", "", False),
        ("new-host", "my-updated-login", "", "my-updated-password", True),
        (
            "new-host",
            "my-updated-login",
            "my-updated-account",
            "my-updated-password",
            True,
        ),
    ),
)
def test_update__new_host(capsys, test_netrc_path, params):
    host, new_login, new_account, new_password, is_valid = params

    cli_options = [
        "--netrc-path",
        str(test_netrc_path),
        "update",
        host,
        "--login",
        new_login,
        "--account",
        new_account,
        "--password",
        new_password,
    ]
    main(cli_options)

    if is_valid:
        output = capsys.readouterr().out
        assert f"Updating {test_netrc_path}..." in output
        assert "Done!" in output
    else:
        output = capsys.readouterr().err
        assert "is empty, please provide a value" in output
