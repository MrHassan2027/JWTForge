import json
import base64
import click
from rich.console import Console
from rich.table import Table

console = Console()


def b64_decode(s: str) -> str:
    padding = 4 - len(s) % 4
    s += "=" * (padding % 4)
    return base64.urlsafe_b64decode(s).decode(errors="replace")


@click.group()
def cli():
    """JWTForge — JWT decode, validate, forge, and audit."""


@cli.command()
@click.argument("token")
def decode(token: str):
    """Decode and pretty-print a JWT without verifying the signature."""
    parts = token.split(".")
    if len(parts) != 3:
        console.print("[red]Invalid JWT — expected 3 parts separated by '.'[/red]")
        return
    try:
        header = json.loads(b64_decode(parts[0]))
        payload = json.loads(b64_decode(parts[1]))
    except Exception as e:
        console.print(f"[red]Failed to decode: {e}[/red]")
        return

    t = Table(title="JWT Header", show_header=False)
    for k, v in header.items():
        t.add_row(f"[cyan]{k}[/cyan]", str(v))
    console.print(t)

    t2 = Table(title="JWT Payload", show_header=False)
    for k, v in payload.items():
        t2.add_row(f"[green]{k}[/green]", str(v))
    console.print(t2)
    console.print("[dim]Signature: [unverified — no secret provided][/dim]")


@cli.command()
@click.argument("token")
def audit(token: str):
    """Check a JWT for common security weaknesses."""
    parts = token.split(".")
    if len(parts) != 3:
        console.print("[red]Invalid JWT[/red]")
        return

    header = json.loads(b64_decode(parts[0]))
    payload = json.loads(b64_decode(parts[1]))
    issues = []

    alg = header.get("alg", "").upper()
    if alg == "NONE":
        issues.append("[red]CRITICAL: alg=none — signature not verified[/red]")
    if alg.startswith("HS") and len(parts[2]) < 20:
        issues.append("[yellow]WARN: Signature looks unusually short — possible weak secret[/yellow]")

    import time
    if "exp" in payload and payload["exp"] < time.time():
        issues.append("[yellow]WARN: Token is expired[/yellow]")
    for claim in ("iss", "aud", "iat"):
        if claim not in payload:
            issues.append(f"[blue]INFO: Missing recommended claim '{claim}'[/blue]")

    if not issues:
        console.print("[green]No obvious issues found.[/green]")
    for issue in issues:
        console.print(issue)


if __name__ == "__main__":
    cli()
