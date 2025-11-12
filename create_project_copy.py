"""
Skapa en säker kopia av LinkDB-projektet.

Detta skript kopierar hela projektet till en ny mapp så du kan experimentera
utan att riskera att förstöra originalet.
"""
from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime
from rich import print
from rich.prompt import Prompt, Confirm
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# Nuvarande projekt
CURRENT_PROJECT = Path(__file__).resolve().parent

# Exkludera vissa mappar/filer från kopiering
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.pytest_cache',
    '.venv',
    'venv',
    '.env',
    '.git',
    '.idea',
    '.vscode',
    '*.db-wal',
    '*.db-shm',
]

def get_project_size(path: Path) -> tuple[int, int]:
    """Räkna antalet filer och total storlek."""
    total_size = 0
    total_files = 0

    for item in path.rglob('*'):
        if item.is_file():
            # Skippa exkluderade
            skip = False
            for pattern in EXCLUDE_PATTERNS:
                if pattern.startswith('*.'):
                    if item.suffix == pattern[1:]:
                        skip = True
                        break
                elif pattern in str(item):
                    skip = True
                    break

            if not skip:
                try:
                    total_size += item.stat().st_size
                    total_files += 1
                except:
                    pass

    return total_files, total_size


def should_exclude(path: Path, base_path: Path) -> bool:
    """Kontrollera om en fil/mapp ska exkluderas."""
    rel_path = str(path.relative_to(base_path))

    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*.'):
            # Filextension
            if path.suffix == pattern[1:]:
                return True
        else:
            # Mappnamn eller del av sökväg
            if pattern in rel_path or pattern == path.name:
                return True

    return False


def copy_project(source: Path, destination: Path, progress=None, task=None):
    """Kopiera projektet med exkludering av vissa filer."""
    destination.mkdir(parents=True, exist_ok=True)

    # Räkna totalt antal filer först (för progress)
    total_files, total_size = get_project_size(source)

    if progress and task:
        progress.update(task, total=total_files)

    copied_files = 0
    copied_size = 0
    skipped = []

    for item in source.rglob('*'):
        if should_exclude(item, source):
            skipped.append(item.name)
            continue

        try:
            rel_path = item.relative_to(source)
            dest_path = destination / rel_path

            if item.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)
                copied_files += 1
                copied_size += item.stat().st_size

                if progress and task:
                    progress.update(task, completed=copied_files)

        except Exception as e:
            print(f"[yellow]Warning: Could not copy {item.name}: {e}[/yellow]")

    return copied_files, copied_size, skipped


def create_readme_for_copy(destination: Path, original_path: Path):
    """Skapa en README i kopian som förklarar vad det är."""
    readme_content = f"""# LinkDB - Utvecklingskopia

Detta är en kopia av LinkDB-projektet skapad för utveckling och experiment.

## Ursprung
- **Kopierad från:** `{original_path}`
- **Kopierad:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Syfte:** Säker utvecklingsmiljö utan risk för originalprojektet

## Vad har kopierats?

✅ All källkod (.py filer)
✅ Databaser (.db filer)
✅ Data-filer (Excel, output, etc.)
✅ Dokumentation (.md filer)
✅ Batch-filer och scripts

❌ Virtuella miljöer (.venv, venv)
❌ Cache-filer (__pycache__, .pyc)
❌ IDE-inställningar (.idea, .vscode)
❌ Git-historik (.git)
❌ Temporära databasfiler (.db-wal, .db-shm)

## Nästa steg

### 1. Skapa ny virtuell miljö
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

### 2. Installera dependencies
```bash
pip install rich openpyxl tldextract
```

### 3. Testa att allt fungerar
```bash
python show_columns.py
```

### 4. Börja utveckla!
Nu kan du experimentera fritt utan att påverka originalprojektet.

## Viktiga filer

- `build_customer_db.py` - Bygg kunddatabaser
- `app/build_all_customer_dbs.py` - Bygg alla kunddatabaser
- `app/build_history_db.py` - Bygg historikdatabas
- `export_to_airtable_csv.py` - Exportera till CSV
- `export_advanced.py` - Avancerad export

## Tips

1. **Backups:** Detta är en kopia, men ta backups innan stora ändringar
2. **Testing:** Testa nya funktioner här innan du flyttar till original
3. **Dokumentation:** Dokumentera dina ändringar
4. **Synkronisering:** Kopiera tillbaka fungerande kod till originalet

## Original-projektet

Original-projektet finns kvar oförändrat på:
```
{original_path}
```

---
**OBS:** Detta är en utvecklingskopia. Förändringar här påverkar INTE originalet.
"""

    readme_path = destination / "README_COPY.md"
    readme_path.write_text(readme_content, encoding='utf-8')
    return readme_path


def create_setup_script(destination: Path):
    """Skapa ett setup-script för kopian."""
    setup_content = """@echo off
echo ========================================
echo LinkDB - Setup for Development Copy
echo ========================================
echo.

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call .venv\\Scripts\\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install rich openpyxl tldextract

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Virtual environment created and dependencies installed.
echo.
echo To activate the environment in the future:
echo   .venv\\Scripts\\activate
echo.
echo To test the installation:
echo   python show_columns.py
echo.
pause
"""

    setup_path = destination / "setup_dev_environment.bat"
    setup_path.write_text(setup_content, encoding='utf-8')
    return setup_path


def main():
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]  LinkDB Project Copy Tool[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print(f"[cyan]Nuvarande projekt:[/cyan] {CURRENT_PROJECT}\n")

    # Räkna projektets storlek
    total_files, total_size = get_project_size(CURRENT_PROJECT)
    size_mb = total_size / (1024 * 1024)

    console.print(f"[cyan]Projektinfo:[/cyan]")
    console.print(f"  • Filer att kopiera: [yellow]{total_files:,}[/yellow]")
    console.print(f"  • Total storlek: [yellow]{size_mb:.1f} MB[/yellow]")
    console.print(f"  • Exkluderade: [yellow]{', '.join(EXCLUDE_PATTERNS[:5])}...[/yellow]\n")

    # Föreslå namn baserat på datum
    default_name = f"linkdb_dev_{datetime.now().strftime('%Y%m%d')}"
    parent_dir = CURRENT_PROJECT.parent

    console.print("[cyan]Var vill du skapa kopian?[/cyan]")
    console.print(f"Standard: [yellow]{parent_dir}\\<projektnamn>[/yellow]\n")

    # Fråga efter projektnamn
    project_name = Prompt.ask(
        "Projektnamn",
        default=default_name
    )

    # Bygg fullständig sökväg
    destination = parent_dir / project_name

    # Kontrollera om mappen redan finns
    if destination.exists():
        console.print(f"\n[yellow]⚠ Varning: Mappen finns redan:[/yellow] {destination}")

        if not Confirm.ask("Vill du skriva över den befintliga mappen?", default=False):
            console.print("[red]Avbrutet av användaren[/red]")
            return

        console.print("[yellow]Tar bort befintlig mapp...[/yellow]")
        shutil.rmtree(destination)

    console.print(f"\n[green]✓ Skapar projektkopia:[/green] {destination}\n")

    # Bekräftelse
    if not Confirm.ask("Fortsätt med kopiering?", default=True):
        console.print("[red]Avbrutet av användaren[/red]")
        return

    console.print()

    # Kopiera projektet med progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Kopierar filer...", total=total_files)

        copied_files, copied_size, skipped = copy_project(
            CURRENT_PROJECT,
            destination,
            progress,
            task
        )

    # Skapa extra filer för kopian
    console.print("\n[cyan]Skapar utvecklingsfiler...[/cyan]")
    readme_path = create_readme_for_copy(destination, CURRENT_PROJECT)
    setup_path = create_setup_script(destination)

    # Sammanfattning
    console.print("\n[bold green]═══════════════════════════════════════════════[/bold green]")
    console.print("[bold green]  Kopiering Klar![/bold green]")
    console.print("[bold green]═══════════════════════════════════════════════[/bold green]\n")

    console.print(f"[cyan]Kopian skapad i:[/cyan] [yellow]{destination}[/yellow]\n")

    console.print("[cyan]Statistik:[/cyan]")
    console.print(f"  • Kopierade filer: [green]{copied_files:,}[/green]")
    console.print(f"  • Total storlek: [green]{copied_size / (1024*1024):.1f} MB[/green]")
    console.print(f"  • Överhoppade: [yellow]{len(set(skipped))}[/yellow] typer\n")

    console.print("[cyan]Extra filer skapade:[/cyan]")
    console.print(f"  • [green]{readme_path.name}[/green] - Info om kopian")
    console.print(f"  • [green]{setup_path.name}[/green] - Setup-script för utveckling\n")

    console.print("[bold cyan]Nästa steg:[/bold cyan]")
    console.print(f"  1. [yellow]cd {destination}[/yellow]")
    console.print(f"  2. [yellow]setup_dev_environment.bat[/yellow] (skapa .venv och installera dependencies)")
    console.print(f"  3. [yellow].venv\\Scripts\\activate[/yellow] (aktivera miljön)")
    console.print(f"  4. [yellow]python show_columns.py[/yellow] (testa att allt fungerar)")
    console.print(f"\n[green]Nu kan du utveckla fritt utan att påverka originalet![/green]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Avbrutet av användaren[/red]")
    except Exception as e:
        console.print(f"\n[red]ERROR: {e}[/red]")
        import traceback
        traceback.print_exc()

