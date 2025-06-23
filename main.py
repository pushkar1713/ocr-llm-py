from pathlib import Path

import typer
from rich import print

import src.pipeline as pipeline

DOC_TYPES = ["receipt", "licence", "resume"]

app = typer.Typer(add_completion=False, help="Hybrid OCR-LLM extractor")


@app.command("run")
def run(
    doc_type: str = typer.Option(
        ...,
        "--type",
        "-t",
        prompt=f"Document type ({', '.join(DOC_TYPES)})",
        case_sensitive=False,
        show_choices=False,
    ),
    path: Path = typer.Option(
        ...,
        "--path",
        "-p",
        prompt="Path to file or folder",
        exists=True,
        file_okay=True,
        dir_okay=True,
    ),
    out_dir: Path = typer.Option(
        Path("./output"),
        "--out",
        "-o",
        help="Destination for JSON files",
    ),
):
    doc_type = doc_type.lower()  # type: ignore[arg-type]
    if doc_type not in DOC_TYPES:
        print(f"[red]✖ Unsupported type '{doc_type}'. Choose from {DOC_TYPES}.[/red]")
        raise typer.Exit(1)

    path, out_dir = path.resolve(), out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[bold cyan]▶ Extracting {doc_type}[/bold cyan]")
    print(f"Source : {path}")
    print(f"Output : {out_dir}\n")

    try:
        if path.is_file():
            models = pipeline.process_document(path, doc_type)
            pipeline.save_outputs(models, (out_dir / path.stem).as_posix())
            print(f"[green]✓ {len(models)} page(s) processed[/green]")
        else:
            pipeline.process_folder(
                root=path,
                out_dir=out_dir,
                doc_type=doc_type,
            )
    except Exception as err:
        print(f"[red]✖ Error: {err}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
