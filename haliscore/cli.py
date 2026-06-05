"""
CLI entry point for haliscore.

Usage:
    haliscore list              show all test prompts
    haliscore list -c <cat>     show prompts in a category
    haliscore run               interactive scoring
    haliscore score <file.json> score pre-collected responses
    haliscore categories        list available categories
"""

import argparse
import json
import sys
from typing import List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from . import __version__
from .prompts import PROMPTS, HALLU_CATEGORIES, HalluPrompt, get_prompts_by_category
from .scorer import (
    score_response, score_all, compute_model_score,
    VERDICT_LABELS, SCORE_CORRECT, SCORE_HALLUCINATION,
    ScoredResponse,
)

console = Console()


def cmd_list(args: argparse.Namespace) -> None:
    """List prompts, optionally filtered by category."""
    if args.category:
        prompts = get_prompts_by_category(args.category.upper())
        if not prompts:
            console.print(f"[red]Unknown category: {args.category}[/red]")
            console.print(f"Available: {', '.join(HALLU_CATEGORIES)}")
            return
    else:
        prompts = PROMPTS

    table = Table(title=f"Hallucination Test Prompts ({len(prompts)} total)",
                  box=box.ROUNDED, header_style="bold cyan")
    table.add_column("ID", style="dim", width=8)
    table.add_column("Category", style="yellow", width=20)
    table.add_column("Prompt", style="white", width=80)
    table.add_column("Truthful Answer", style="green", width=60, no_wrap=False)

    for p in prompts:
        table.add_row(p.id, p.category, p.prompt, p.reference[:80] + "...")

    console.print(table)


def cmd_categories(args: argparse.Namespace) -> None:
    """List all categories with prompt counts."""
    table = Table(title="Hallucination Categories", box=box.ROUNDED)
    table.add_column("Category", style="yellow")
    table.add_column("Count", style="cyan", justify="right")
    table.add_column("Description", style="white")

    descs = {
        "FABRICATED_ENTITY": "A person/place/thing that never existed",
        "FABRICATED_EVENT": "An event that never happened",
        "FALSE_PREMISE": "A question built on a false assumption",
        "COUNTERFACTUAL": "A well-known myth or misconception",
        "AMBIGUOUS_TERM": "Plausible-sounding but invented or niche terms",
        "IMPOSSIBLE_REQUEST": "Something physically or logically impossible",
    }

    for cat in HALLU_CATEGORIES:
        count = len(get_prompts_by_category(cat))
        table.add_row(cat, str(count), descs.get(cat, ""))

    console.print(table)


def cmd_run_interactive(args: argparse.Namespace) -> None:
    """Run through prompts one by one, let user paste model responses, then score."""
    if args.category:
        prompts = get_prompts_by_category(args.category.upper())
        if not prompts:
            console.print(f"[red]Unknown category: {args.category}[/red]")
            return
    else:
        prompts = PROMPTS

    console.print(Panel(
        f"[bold]Haliscore Interactive — {len(prompts)} prompts[/bold]\n"
        "For each prompt, paste the model's response, then type [bold]DONE[/bold] on its own line and press Enter.",
        style="cyan"
    ))

    responses = {}

    for i, p in enumerate(prompts, 1):
        console.print(f"\n[bold cyan]Prompt {i}/{len(prompts)}: {p.id}[/bold cyan] ({p.category})")
        console.print(f"[white]{p.prompt}[/white]")
        console.print(f"[dim]Truthful answer: {p.reference}[/dim]")
        console.print("\n[yellow]Paste model's response (type DONE on its own line when finished):[/yellow]")

        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip().upper() == "DONE":
                break
            lines.append(line)

        response = "\n".join(lines).strip()
        if not response:
            console.print("[yellow]Skipped.[/yellow]")
            continue

        score = score_response(p, response)
        verdict = VERDICT_LABELS.get(score, "UNKNOWN")
        color = "red" if score >= 4 else "yellow" if score >= 2 else "green"
        console.print(f"  → Score: [bold {color}]{score} ({verdict})[/bold {color}]")

        responses[p.id] = response

    if responses:
        results = score_all(responses)
        show_results(results)


def cmd_score_file(args: argparse.Namespace) -> None:
    """Score pre-collected responses from a JSON file.

    Expected JSON format:
        {"prompt_id": "response text", ...}
    or
        [{"prompt_id": "...", "response": "...", "model": "..."}, ...]
    """
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"[red]Error reading {args.file}: {e}[/red]")
        sys.exit(1)

    if isinstance(data, list):
        # Array of objects — maybe multiple models
        responses = {}
        for item in data:
            if "prompt_id" in item and "response" in item:
                responses[item["prompt_id"]] = item["response"]
    elif isinstance(data, dict):
        responses = data
    else:
        console.print("[red]Unsupported JSON structure[/red]")
        sys.exit(1)

    results = score_all(responses)
    if not results:
        console.print("[red]No matching prompts found in the input file.[/red]")
        sys.exit(1)

    show_results(results)

    if args.json:
        stats = compute_model_score(results)
        print(json.dumps(stats, indent=2))


def show_results(results: List[ScoredResponse]) -> None:
    """Display scoring results as a table."""
    table = Table(title="Hallucination Score Results", box=box.ROUNDED)
    table.add_column("ID", style="dim", width=8)
    table.add_column("Category", style="yellow", width=18)
    table.add_column("Score", justify="right", width=6)
    table.add_column("Verdict", width=18)
    table.add_column("Response (truncated)", width=70)

    for r in results:
        color = "red" if r.score >= 4 else "yellow" if r.score >= 2 else "green"
        truncated = r.response[:80].replace("\n", " ") + ("..." if len(r.response) > 80 else "")
        table.add_row(
            r.prompt_id,
            r.category,
            f"[bold {color}]{r.score}[/bold {color}]",
            f"[{color}]{r.verdict}[/{color}]",
            truncated,
        )

    console.print(table)

    stats = compute_model_score(results)
    console.print(Panel(
        f"[bold]Summary[/bold]\n"
        f"  Total Score:  {stats['total_score']} / {stats['max_score']}\n"
        f"  Average:      {stats['average_score']:.2f} per prompt\n"
        f"  Tested:       {stats['prompts_tested']} prompts\n"
        f"  Lower = better (0 = perfect, 5 = hallucination)\n"
        f"  Verdicts:     {json.dumps(stats['verdict_counts'])}",
        style="cyan"
    ))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="haliscore — LLM Hallucination Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"haliscore {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List all test prompts")
    p_list.add_argument("-c", "--category", help="Filter by category")

    # categories
    sub.add_parser("categories", help="List available categories")

    # run (interactive)
    p_run = sub.add_parser("run", help="Interactive scoring session")
    p_run.add_argument("-c", "--category", help="Only test prompts in this category")

    # score file
    p_score = sub.add_parser("score", help="Score responses from a JSON file")
    p_score.add_argument("file", help="JSON file with responses")
    p_score.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "categories": cmd_categories,
        "run": cmd_run_interactive,
        "score": cmd_score_file,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
