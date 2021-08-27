from pathlib import Path
import click  # type: ignore
import collections
from librelingo_yaml_loader import load_course
from librelingo_audios.update_audios import update_audios_for_course


Settings = collections.namedtuple(
    "Settings",
    [
        "dry_run",
        "destructive",
    ],
)

DEFAULT_SETTINGS = Settings(
    dry_run=False,
    destructive=False,
)


def ensure_output_directory(output_path, settings):
    if not settings.dry_run:
        Path(output_path).mkdir(parents=True, exist_ok=True)


@click.command()
@click.argument("input_path")
@click.argument("output_path")
@click.argument("course_name")
@click.option("--dry-run/--no-dry-run", default=DEFAULT_SETTINGS.dry_run)
@click.option(
    "--destructive/--non-destructive",
    default=DEFAULT_SETTINGS.destructive,
    show_default=True,
    help="--destructive deletes existing audio and re-generates from scratch. --non-destructive performs an iterative update."
)
def _command(input_path, output_path, course_name, dry_run, destructive):
    """
    Generate audios for a YAML course.
    """
    settings = Settings(
        dry_run=dry_run,
        destructive=destructive,
    )
    course = load_course(input_path)
    ensure_output_directory(output_path, settings)
    update_audios_for_course(output_path, course_name, course, settings)


if __name__ == "__main__":
    _command()
