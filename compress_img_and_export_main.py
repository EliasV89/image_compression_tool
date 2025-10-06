import os
import sys
import pathlib
import zipfile
from fnmatch import fnmatch
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn

console = Console()


def zip_directory(folder_path, zip_path):
    """Create a ZIP archive of a directory."""
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])


def get_compression_quality(default=30):
    """Prompt user to set image compression quality."""
    console.print("\n[bold cyan]Enter compression quality (1–100)[/bold cyan] "
                  f"(press [green]Enter[/green] for default {default}%): ", end="")
    user_input = input().strip()

    if not user_input:
        return default
    try:
        quality = int(user_input)
        if 1 <= quality <= 100:
            return quality
        else:
            console.print("[red]Please enter a number between 1 and 100.[/red]")
            return get_compression_quality(default)
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")
        return get_compression_quality(default)


def main():
    # --- Input ---
    # --- Get root path interactively ---
    console.print("\n[bold cyan]Enter the root folder path to compress images from:[/bold cyan]")
    root = input("→ ").strip()

    # Basic validation
    if not root or not os.path.exists(root):
        console.print(f"[red]Invalid path:[/red] {root}")
        sys.exit(1)

    image_quality = get_compression_quality(default=30)

    # --- Setup paths ---
    target_path = r'C:\Image Compression Exports'
    os.makedirs(target_path, exist_ok=True)

    root_subdir = pathlib.PurePath(root).name
    target_path = os.path.join(target_path, root_subdir + '_comp')
    os.makedirs(target_path, exist_ok=True)

    console.print(Panel.fit(
        f"[bold white]Image Compression Tool[/bold white]\n"
        f"[cyan]Root:[/cyan] {root}\n"
        f"[cyan]Target:[/cyan] {target_path}\n"
        f"[cyan]Quality:[/cyan] {image_quality}%",
        title="[bold blue]Setup[/bold blue]",
        border_style="blue"
    ))

    # --- Collect image paths ---
    patterns = ['*.tif', '*.bmp', '*.jpg', '*.png']
    file_list = []
    for pattern in patterns:
        for path, _, files in os.walk(root):
            for file in files:
                if fnmatch(file, pattern):
                    file_list.append(os.path.join(path, file))

    total_files = len(file_list)
    if total_files == 0:
        console.print("[yellow]No matching image files found.[/yellow]")
        sys.exit(0)

    # --- Processing with progress bar ---
    progress = Progress(
        SpinnerColumn("dots", style="cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("• [green]{task.completed}/{task.total}[/green]"),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    )

    with progress:
        task = progress.add_task("Compressing images", total=total_files)
        for file_path in file_list:
            rel_dir = os.path.dirname(file_path).replace(root, target_path)
            os.makedirs(rel_dir, exist_ok=True)

            name = os.path.basename(file_path)
            ext = os.path.splitext(name)[1]
            new_name = name.replace(ext, '.jpg')
            image_path = os.path.join(rel_dir, new_name)

            try:
                with console.status(f"[cyan]Processing {name}...", spinner="dots"):
                    im = Image.open(file_path)

                    # --- Draw overlay ---
                    draw = ImageDraw.Draw(im)
                    im_text = file_path
                    font = ImageFont.truetype("segoeui.ttf", 30)
                    position = (10, 0)
                    left, top, right, bottom = draw.textbbox(position, im_text, font=font)
                    draw.rectangle((left - 20, top - 20, right + 10, bottom + 3), fill='black')
                    draw.text(position, im_text, font=font, fill='white')

                    # --- Save compressed image ---
                    im.save(image_path, optimize=True, quality=image_quality)

            except Exception as e:
                console.print(f"[red]Error processing {file_path}: {e}[/red]")

            progress.advance(task)

    # --- Zipping result ---
    console.print("\n[cyan]Creating ZIP archive...[/cyan]")
    with console.status("[bold blue]Zipping files...[/bold blue]", spinner="earth"):
        zip_directory(target_path, target_path + '.zip')

    console.print(
        Panel.fit(
            f"[bold green]✅ Compression complete![/bold green]\n"
            f"Zip archive created at:\n[white]{target_path}.zip[/white]",
            title="[bold green]Done[/bold green]",
            border_style="green"
        )
    )


if __name__ == "__main__":
    main()
