import pytest

from wg_wrapper.command import run_command, run_command_zero


@pytest.mark.asyncio
async def test_correct_command():
    ls_result = await run_command("ls .")
    assert ls_result.code == 0
    assert ls_result.stdout != ""
    assert ls_result.stderr == ""


@pytest.mark.asyncio
async def test_unknown_command():
    ls_result = await run_command("i-just-made-up-this-command .")
    assert ls_result.code == 127
    assert ls_result.stdout == ""
    assert ls_result.stderr.find("command not found") != -1


@pytest.mark.asyncio
async def test_run_command_zero():
    ls_result = await run_command_zero("ls .")
    assert ls_result.code == 0
    assert ls_result.stdout != ""
    assert ls_result.stderr == ""


@pytest.mark.asyncio
async def test_run_command_zero_unknown_command():
    with pytest.raises(ChildProcessError, match=""):
        ls_result = await run_command_zero("i-just-made-up-this-command .")
        assert ls_result.code == 0
        assert ls_result.stdout != ""
        assert ls_result.stderr == ""
