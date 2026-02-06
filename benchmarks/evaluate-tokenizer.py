import time
from pathlib import Path
import click
from transformers import AutoTokenizer


@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.argument("model_name", required=False, default="Qwen/Qwen3-0.6B")
def tokenize_path(path: Path, model_name: str):
    # Load tokenizer once
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Decide which files to process
    if path.is_file():
        files = [path]
    elif path.is_dir():
        # Non-recursive .pddl files; case-insensitive match
        files = [p for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".pddl"]
        if not files:
            click.echo(f"No .pddl files found in directory: {path}")
            return
    else:
        click.echo(f"Path is neither a file nor a directory: {path}")
        return

    for file_path in sorted(files):
        # Load file
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            click.echo(f"Skipping (not UTF-8): {file_path}")
            continue

        # Time the tokenization
        start = time.time()
        tokens = tokenizer(
            text,
            return_attention_mask=False,
            return_token_type_ids=False
        )["input_ids"]
        end = time.time()

        elapsed = end - start
        num_tokens = len(tokens)
        num_chars = len(text)

        click.echo(f"\nFile: {file_path}")
        click.echo(f"\tTime taken: {elapsed:.4f} seconds")
        click.echo(f"\t# Tokens: {num_tokens}")
        click.echo(f"\t# Characters: {num_chars}")


if __name__ == "__main__":
    tokenize_path()
