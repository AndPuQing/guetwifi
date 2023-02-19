from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from subprocess import call


class PostInstallCommand(install):
    def run(self):
        install.run(self)

        # Set up the program as a system service
        with open("/etc/systemd/system/guetwifi.service", "w") as f:
            f.write(
                """[Unit]
            Description=GUET WiFi Monitor

            [Service]
            Type=simple
            ExecStart=/usr/bin/guetwifi start
            ExecStop=/usr/bin/guetwifi stop
            Restart=always

            [Install]
            WantedBy=multi-user.target
            """
            )
            call(["systemctl", "daemon-reload"])
            call(["systemctl", "enable", "guetwifi.service"])
            call(["systemctl", "start", "guetwifi.service"])


setup(
    name="guetwifi",
    version="0.1.0",
    packages=["guetwifi"],
    author="PuQing",
    author_email="me@puqing.work",
    install_requires=["click", "psutil", "requests"],
    entry_points={
        "console_scripts": [
            "guetwifi=guetwifi.cli:main",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
        "develop": PostInstallCommand,
        "egg_info": PostInstallCommand,
    },
    readme="README.md",
)
