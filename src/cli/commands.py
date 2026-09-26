import click
import asyncio
import json
from src.models.alert import UnifiedAlert
from src.analyzers.classifier import AlertClassifier
from src.utils.logging import setup_logging

setup_logging()


@click.group()
def cli():
    """AlertSentry-AI CLI"""


@cli.command()
@click.option("--file", "-f", help="Path to alert JSON file", required=True)
@click.option("--output", "-o", help="Output file for report")
def analyze(file, output):
    """Analyze a single alert from a file"""

    async def _analyze():
        try:
            with open(file, "r") as f:
                data = json.load(f)

            alert = UnifiedAlert(**data)
            classifier = AlertClassifier()
            result = await classifier.analyze(alert)

            if result:
                click.echo(json.dumps(result.model_dump(), indent=2, default=str))
                if output:
                    with open(output, "w") as f:
                        json.dump(result.model_dump(), f, indent=2, default=str)
            else:
                click.echo("Analysis failed")
        except Exception as e:
            click.echo(f"Error: {e}")

    asyncio.run(_analyze())


@cli.command()
@click.option("--source", "-s", help="SIEM source to watch", required=True)
def watch(source):
    """Watch for new alerts from a SIEM source"""
    click.echo(f"Watching {source} for new alerts... (Not implemented)")


if __name__ == "__main__":
    cli()
