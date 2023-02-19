#!/usr/bin/env python
# coding:utf-8

import subprocess
import psutil
import click
import os
import json

__version__ = "0.1.0"
_path = os.path.dirname(os.path.abspath(__file__))


def _start():
    cmd = "python {}/GuetWifiRunner.py".format(_path)
    subprocess.Popen(cmd, shell=True)


def _stop():
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "cmdline"])
            cmdline = "".join(pinfo["cmdline"])
            if "GuetWifiRunner" in cmdline:
                p = psutil.Process(pinfo["pid"])
                p.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


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
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "cmdline"])
            cmdline = "".join(pinfo["cmdline"])
            if "GuetWifiRunner" in cmdline:
                click.echo("guetwifi is running")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    click.echo("guetwifi is not running")


@guetwifi.command()
def upgrade():
    """Upgrade guetwifi"""
    click.echo("Upgrade guetwifi...")
    stop()
    cmd = "pip install guetwifi --upgrade"
    subprocess.Popen(cmd, shell=True)
    start()


@guetwifi.command()
def uninstall():
    """Uninstall guetwifi"""
    click.echo("Uninstall guetwifi...")
    stop()
    cmd = "pip uninstall guetwifi"
    subprocess.Popen(cmd, shell=True)


@guetwifi.command()
@click.option("-a", "--account", default=None, help="Your GUET-WIFI account")
@click.option("-p", "--password", default=None, help="Your GUET-WIFI password")
@click.option("-o", "--operator", default="", help="Your want to login operator")
def config(account, password, operator):
    """Config your GUET-WIFI account and password"""
    config = {"account": account, "password": password, "operator": operator}
    config = {k: v for k, v in config.items() if v is not None}
    config_path = os.path.join(_path, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config.update(json.load(f))
    with open(config_path, "w") as f:
        json.dump(config, f)


if __name__ == "__main__":
    guetwifi()
