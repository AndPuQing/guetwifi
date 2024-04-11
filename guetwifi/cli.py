import click
import importlib.metadata as metadata
from guetwifi.guetwifirunner import NetWork

__version__ = metadata.version("guetwifi")


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
@click.option("-a", "--account", default=None, help="Your GUET-WIFI account", type=int)
@click.option("-p", "--password", default=None, help="Your GUET-WIFI password")
@click.option(
    "-i",
    "--isp",
    default="",
    type=click.Choice(["cmcc", "unicom", "telecom", ""], case_sensitive=False),
    help="Your want to login isp",
)
def connect(account: int, password: str, isp: str):
    """Config your GUET-WIFI account and password"""
    if NetWork.checkNetwork():
        print("You have already connected to the network")
        return
    net = NetWork(account=account, password=password, isp=isp)
    net.login()


def main():
    guetwifi()


if __name__ == "__main__":
    guetwifi()
