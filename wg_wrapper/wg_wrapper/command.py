import asyncio

from wg_wrapper.schemas import CommandResult


async def run_command(cmd: str) -> CommandResult:
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return CommandResult(stdout.decode(), stderr.decode(), process.returncode)


def must_zero_code(result: CommandResult) -> CommandResult:
    if result.code != 0:
        raise ChildProcessError(result)
    return result


async def run_command_zero(cmd: str) -> CommandResult:
    """
    Check that command returns 0.
    """
    return must_zero_code(await run_command(cmd))
