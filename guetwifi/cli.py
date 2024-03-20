#!/usr/bin/env python
# coding:utf-8

import subprocess
import psutil
import click
import os
import json
import importlib.metadata as metadata

__version__ = metadata.version("guetwifi")
_path = os.path.dirname(os.path.abspath(__file__))
_runner = "guetwifirunner"


def _get_pid():
    runner_pids = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "cmdline"])
            cmdline = "".join(pinfo["cmdline"])
            if _runner in cmdline:
                runner_pids.append(pinfo["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return runner_pids


def _start():
    runner_pids = _get_pid()
    if runner_pids:
        click.echo("guetwifi is already running")
        return
    else:
        cmd = "python -m guetwifi.{}".format(_runner)
        subprocess.Popen(cmd, shell=True)
        runner_pids = _get_pid()
        if runner_pids:
            click.echo("guetwifi started")
        else:
            click.echo("guetwifi start failed")


def _stop():
    runner_pids = _get_pid()
    if not runner_pids:
        click.echo("guetwifi is not running")
        return
    else:
        for pid in runner_pids:
            p = psutil.Process(pid)
            p.terminate()
            click.echo("terminate pid: {}".format(pid))
        click.echo("guetwifi stopped")


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def guetwifi(ctx, debug):
    """GuetWifi is a command line tool for GUET-WIFI login"""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    if debug:
        click.echo("Debug mode is on")


@guetwifi.command()
@click.pass_context
def start(ctx):
    """Start guetwifi"""
    # TODO: enable debug mode
    click.echo("Start guetwifi...")
    _start()


@guetwifi.command()
def stop():
    """Stop guetwifi"""
    click.echo("Stop guetwifi...")
    _stop()


@guetwifi.command()
def restart():
    """Restart guetwifi"""
    click.echo("Restart guetwifi...")
    stop()
    start()


@guetwifi.command()
def version():
    """Show guetwifi version"""
    click.echo("guetwifi version: {}".format(__version__))


@guetwifi.command()
def status():
    """Check guetwifi status"""
    runner_pids = _get_pid()
    if runner_pids:
        click.echo("guetwifi is running")
        click.echo("pid: {}".format(runner_pids))
    else:
        click.echo("guetwifi is not running")


@guetwifi.command()
@click.option("-n", "--number", default=10, help="The number of log")
def log(number: int):
    """Show guetwifi log"""
    log_path = os.path.join(_path, "network.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            lines = f.readlines()
            if len(lines) > number:
                lines = lines[-number:]
            for line in lines:
                click.echo(line, nl=False)
    else:
        click.echo("No log file found")


@guetwifi.command()
@click.option("-a", "--account", default=None, help="Your GUET-WIFI account", type=int)
@click.option("-p", "--password", default=None, help="Your GUET-WIFI password")
@click.option(
    "-i",
    "--isp",
    default="",
    type=click.Choice(["cmcc", "unicom", "telecom", ""], case_sensitive=False),
    help="Your want to login isp",
)
def config(account: int, password: str, isp: str):
    """Config your GUET-WIFI account and password"""
    config = {"account": account, "password": password, "isp": isp}
    config = {k: v for k, v in config.items() if v is not None}
    config_path = os.path.join(_path, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config.update(json.load(f))
    with open(config_path, "w") as f:
        json.dump(config, f)


def main():
    guetwifi()


if __name__ == "__main__":
    guetwifi()
