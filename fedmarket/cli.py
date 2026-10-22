"""
Command-line interface for fedmarket.

Provides commands for assessing PSC codes, comparing codes, and getting
profile-based recommendations using the two-axis framework.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from rich.console import Console
from rich.table import Table

from .core import (
    assess_code,
    compare_codes,
    budget_accessible_pct,
    CODES,
)
from .decision import decide_code, format_recommendation, TWO_AXIS_CONTEXT
from .dynamic import (
    assess_code_dynamic,
    two_axis_recommendation,
    format_dynamic_result,
    format_recommendation_dynamic,
)

app = typer.Typer(
    name="fedmarket",
    help="Federal Marketplace Assessment Toolkit — evidence-backed PSC code analysis for small software teams",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()


def format_result(r: Dict[str, Any]) -> str:
    """Format an assessment result as a readable string."""
    rec = r["recommendation"]
    lines = [
        f"\n=== Fedmarket Assessment: {r['code']} — {r['name']} ===",
        f"Screen score: {r['screen_score']}",
        f"Distinct recipients: {r['recipient_count']:,}",
        f"Top-10 share: {r['top_10_share_pct']}%",
        f"≤$40k fraction: {r['leq_40k_pct']}%",
        f"≤$100k fraction: {r['leq_100k_pct']}%",
        f"Single-award recipients: {r['single_award_pct']}%",
        f"Software (% of awards): {r['software_pct_awards']}%",
        f"Software (% of obligation): {r['software_pct_obligation']}%",
        f"Software ≤$40k: {r['software_leq_40k_pct']}%",
        f"Software ≤$100k: {r['software_leq_100k_pct']}%",
        f"Software median award: ${r['software_median_award']:,}",
        f"DOD %: {r['dod_pct']}%",
        f"GSA awarding agency: {r['gsa_awarding_pct']}%",
        "Small vendor GSA MAS by SIN [Inferred: E210 heuristic; E213 validated G1/G2 FAIL]:",
    ]
    sv_mas = r.get("small_vendor_gsa_mas_by_sin", {})
    for sin, pct in sv_mas.items():
        lines.append(f"  {sin}: {pct}%")
    lines += [
        f"SEWP Cat B small vendor [Inferred]: {r['sewp_catb_small_vendor_pct']}%",
        f"Sub/prime ratio [Observed]: {r['sub_prime_ratio_pct']}%",
        f"Small vendor GWAC share [Observed, E207]: {r['small_vendor_gwac_share_pct']}%",
        f"Total obligation: ${r['total_obligation_b']:.2f}B",
        "",
    ]

    # E204 Trend warnings
    trend = r.get("trend", {})
    if trend:
        direction = trend.get("direction", "unknown")
        warning = trend.get("warning", "")
        top10_change = trend.get("top10_change", "")
        small_award_change = trend.get("small_award_change", "")
        new_entrant_change = trend.get("new_entrant_change", "")
        new_mega_vendors = trend.get("new_mega_vendors", [])
        obligation_growth = trend.get("obligation_growth", "")

        trend_icon = "🔴" if direction == "concentrating" else ("🟢" if direction == "diversifying" else ("🟡" if direction == "hardening" else "⚪"))
        lines += [
            f"{trend_icon} TREND WARNING (E204 12mo vs 5yr): {direction.upper()}",
            f"  Top-10 share change: {top10_change}",
            f"  ≤$40k fraction change: {small_award_change}",
            f"  New entrant change: {new_entrant_change}",
        ]
        if new_mega_vendors:
            lines.append(f"  New mega-vendors: {', '.join(new_mega_vendors)}")
        if obligation_growth:
            lines.append(f"  Obligation growth: {obligation_growth}")
        if warning:
            lines.append(f"  ⚠ {warning}")
        lines.append("")

    # E211 Survival/Graduation (Two-Axis Sustainability)
    survival = r.get("survival_pct", 0)
    graduation = r.get("graduation_pct", 0)
    survival_cleaned = r.get("survival_cleaned_pct", 0)
    graduation_cleaned = r.get("graduation_cleaned_pct", 0)
    lines += [
        "SUSTAINABILITY (E211 Entry Survival — 3yr follow-up of ≤$100k FY20-21 cohort):",
        f"  Survival (UEI match): {survival:.1f}%  |  Cleaned (all-small): {survival_cleaned:.1f}%",
        f"  Graduation (>$100k agg): {graduation:.1f}%  |  Cleaned (all-small): {graduation_cleaned:.1f}%",
        "",
        f"Entry axis: {rec['entry_axis']}",
        f"Primary vehicle: {rec['primary_vehicle']}",
        f"Caveats: {rec['caveats']}",
    ]
    e213_note = r.get("e213_validation_note", "")
    if e213_note:
        lines += ["", f"E213 validation: {e213_note}"]
    return "\n".join(lines)


def print_comparison(comparison: Dict[str, Any]) -> None:
    """Print a comparison table of multiple PSC codes."""
    results = comparison["by_code"]
    if not results:
        console.print("[red]No codes found in lookup.[/red]")
        return

    table = Table(title="PSC Code Comparison", show_header=True, header_style="bold")
    table.add_column("PSC Code", style="cyan")
    table.add_column("Screen", justify="right")
    table.add_column("Recipients", justify="right")
    table.add_column("≤$40k", justify="right")
    table.add_column("Software%", justify="right")
    table.add_column("GWAC%", justify="right")
    table.add_column("Grad% (clean)", justify="right")
    table.add_column("Surv% (clean)", justify="right")
    table.add_column("Trend", style="yellow")

    for code in sorted(results.keys()):
        r = results[code]
        sv_gwac = r["small_vendor_gwac_share_pct"]
        grad = r.get("graduation_cleaned_pct", 0)
        surv = r.get("survival_cleaned_pct", 0)
        trend = r.get("trend", {})
        trend_dir = trend.get("direction", "?")[:1].upper()

        trend_color = {
            "C": "red",    # concentrating
            "D": "green",  # diversifying
            "H": "yellow", # hardening
            "S": "white",  # stable
            "N": "dim",    # not software market
        }.get(trend_dir, "white")

        table.add_row(
            code,
            str(r["screen_score"]),
            f"{r['recipient_count']:,}",
            f"{r['leq_40k_pct']:.1f}%",
            f"{r['software_pct_awards']:.1f}%",
            f"{sv_gwac:.1f}%",
            f"{grad:.1f}%",
            f"{surv:.1f}%",
            f"[{trend_color}]{trend_dir}[/{trend_color}]",
        )

    console.print(table)
    console.print()
    console.print(f"By screen score (desc): {' '.join(comparison['ranked_by_screen_score'])}")
    console.print(f"By ≤$40k access (desc): {' '.join(comparison['ranked_by_leq_40k_access'])}")
    console.print()
    console.print("Legend: GWAC% = Small vendor GWAC share, Grad% = Graduation (cleaned), Surv% = Survival (cleaned)")
    console.print("Trend: C=Concentrating, D=Diversifying, H=Hardening, S=Stable, N=Not software market")


@app.command()
def assess(
    codes: List[str] = typer.Argument(..., help="PSC code(s) to assess (e.g., 7030 DA10)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file"),
    refresh: bool = typer.Option(False, "--refresh", help="Fetch fresh data from USAspending API"),
    dynamic: bool = typer.Option(False, "--dynamic", help="Show dynamic assessment (requires --refresh)"),
):
    """Assess one or more PSC codes for small-team entry."""
    if len(codes) == 1:
        code = codes[0]
        try:
            # Static assessment
            r = assess_code(code)
            console.print(format_result(r))

            # Dynamic assessment if requested
            if refresh or dynamic:
                console.print("\n[bold]Fetching live data from USAspending...[/bold]")
                dyn_result = assess_code_dynamic(code, refresh=refresh)
                console.print(format_dynamic_result(dyn_result))

                # Two-axis recommendation
                static_metrics = assess_code(code)
                dyn_rec = two_axis_recommendation(code, static_metrics, dyn_result)
                console.print(format_recommendation_dynamic(dyn_rec))

            if output:
                output_data = {
                    "experiment": "fedmarket",
                    "psc_code": code,
                    "static": r,
                }
                if refresh or dynamic:
                    output_data["dynamic"] = dyn_result
                    output_data["two_axis"] = dyn_rec
                output.parent.mkdir(parents=True, exist_ok=True)
                with open(output, "w") as f:
                    json.dump(output_data, f, indent=2, default=str)
                console.print(f"\n[green]JSON output saved to {output}[/green]")

        except KeyError as e:
            console.print(f"[red]Error: {e}[/red]")
            console.print(f"Available codes: {', '.join(sorted(CODES.keys()))}")
            raise typer.Exit(1)
    else:
        # Multiple codes - comparison mode
        comparison = compare_codes(codes)
        print_comparison(comparison)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w") as f:
                json.dump(comparison, f, indent=2, default=str)
            console.print(f"\n[green]JSON output saved to {output}[/green]")


@app.command()
def compare(
    codes: List[str] = typer.Argument(..., help="PSC codes to compare (e.g., 7030 DA10 7A21)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """Compare multiple PSC codes side by side."""
    comparison = compare_codes(codes)
    print_comparison(comparison)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            json.dump(comparison, f, indent=2, default=str)
        console.print(f"\n[green]JSON output saved to {output}[/green]")


@app.command()
def decide(
    budget: str = typer.Option(..., "--budget", "-b", help="Budget focus: leq_40k, leq_100k, enterprise"),
    gtm: str = typer.Option(..., "--gtm", "-g", help="Go-to-market: direct, gsa_mas, subcontract"),
    focus: str = typer.Option(..., "--focus", "-f", help="Technical focus: software, saas, services"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode with prompts"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """Get a PSC code recommendation based on your team profile.

    Uses the two-axis framework (entry accessibility vs. business sustainability).

    Examples:
      fedmarket decide --budget leq_40k --gtm direct --focus software
      fedmarket decide --budget leq_100k --gtm gsa_mas --focus saas
      fedmarket decide --budget enterprise --gtm subcontract --focus services
    """
    if interactive:
        console.print("=" * 60)
        console.print("FEDMARKET DECISION GUIDE")
        console.print("=" * 60)
        console.print()
        console.print("Answer 3 questions about your team so we can recommend")
        console.print("the best PSC code and entry strategy using our two-axis")
        console.print("framework (entry accessibility vs. business sustainability).")
        console.print()

        # Question 1: Budget focus
        console.print("Q1. What is your primary budget focus?")
        console.print("  a) ≤ $40k per award — quick entry, faster revenue cycles")
        console.print("  b) ≤ $100k per award — moderate ambition")
        console.print("  c) Enterprise deals ($100k+) — larger deals, longer cycles")
        budget_q = typer.prompt("  Your choice (a/b/c)", default="a").strip().lower()
        budget_map = {"a": "leq_40k", "b": "leq_100k", "c": "enterprise"}
        budget = budget_map.get(budget_q, "leq_40k")

        # Question 2: Go-to-market approach
        console.print()
        console.print("Q2. What is your preferred go-to-market approach?")
        console.print("  a) Direct sales — build your own sales capability")
        console.print("  b) GSA Schedule/MAS — pursue government contracting")
        console.print("  c) Subcontracting — partner with large primes (Carahsoft, Dell, etc.)")
        gtm_q = typer.prompt("  Your choice (a/b/c)", default="a").strip().lower()
        gtm_map = {"a": "direct", "b": "gsa_mas", "c": "subcontract"}
        gtm = gtm_map.get(gtm_q, "direct")

        # Question 3: Technical focus
        console.print()
        console.print("Q3. What is your product's technical focus?")
        console.print("  a) Pure software product (offline/installed software)")
        console.print("  b) SaaS / Cloud service (web-based, subscription)")
        console.print("  c) IT services / Integration (consulting, implementation)")
        focus_q = typer.prompt("  Your choice (a/b/c)", default="a").strip().lower()
        focus_map = {"a": "software", "b": "saas", "c": "services"}
        focus = focus_map.get(focus_q, "software")

        console.print()
        console.print("=" * 60)
        console.print("Analyzing your profile against all 5 PSC codes...")
        console.print()

    # Run decision
    rec = decide_code(budget, gtm, focus)

    # Output results
    console.print()
    console.print("=" * 60)
    console.print("RECOMMENDATION")
    console.print("=" * 60)
    console.print()
    console.print(f"Recommended PSC code: [bold cyan]{rec.get('recommended_code', 'N/A')}[/bold cyan]")
    console.print(f"Entry axis: {rec.get('entry_axis', 'N/A')}")
    console.print(f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}")
    console.print(f"Axis 1 (Accessibility) score: {rec.get('axis1_score', 0)}")
    console.print(f"Axis 2 (Sustainability) score: {rec.get('axis2_score', 0)}")
    console.print()
    console.print("RATIONALE:")
    console.print(rec.get('rationale', 'N/A'))
    console.print()
    console.print("NEXT STEPS:")
    for i, step in enumerate(rec.get('next_steps', []), 1):
        console.print(f"  {i}. {step}")
    console.print()
    console.print("=" * 60)
    console.print("TWO-AXIS FRAMEWORK CONTEXT")
    console.print("=" * 60)
    console.print(TWO_AXIS_CONTEXT)
    console.print()
    console.print(f"[bold]YOUR PROFILE:[/bold] budget={budget}, gtm={gtm}, focus={focus}")
    console.print(f"  → Recommended code: [bold cyan]{rec.get('recommended_code', 'N/A')}[/bold cyan]")

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            json.dump(rec, f, indent=2, default=str)
        console.print(f"\n[green]JSON output saved to {output}[/green]")


@app.command()
def list_codes():
    """List all available PSC codes with basic info."""
    table = Table(title="Available PSC Codes", show_header=True, header_style="bold")
    table.add_column("Code", style="cyan")
    table.add_column("Name")
    table.add_column("Screen Score", justify="right")
    table.add_column("Recipients", justify="right")
    table.add_column("≤$40k", justify="right")
    table.add_column("Software%", justify="right")
    table.add_column("Type")

    type_map = {
        "7030": "Software Product",
        "DA10": "Software Product + GWAC",
        "7A21": "Software Product (Concentrated)",
        "DA01": "Services Market",
        "D304": "Telecom Market",
    }

    for code in sorted(CODES.keys()):
        d = CODES[code]
        table.add_row(
            code,
            d["name"],
            str(d["screen_score"]),
            f"{d['recipients']:,}",
            f"{d['leq_40k_pct']}%",
            f"{d['software_pct_awards']}%",
            type_map.get(code, "Unknown"),
        )

    console.print(table)


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"fedmarket version {__version__}")
    console.print("Data from experiments E196-E213 (2026-10-20/21)")
    console.print("Evidence labels: docs/policy/evidence-labels.md")


if __name__ == "__main__":
    app()