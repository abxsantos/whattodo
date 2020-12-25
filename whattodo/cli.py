"""CLI for whattodo project."""

import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="0.0.0")
def whattodo_cli():
    """What Todo"""


if __name__ == "__main__":
    whattodo_cli()
