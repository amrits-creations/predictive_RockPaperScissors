from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

MOVES   = {0: "Rock", 1: "Paper", 2: "Scissors"}
SYMBOLS = {0: "✊",   1: "✋",    2: "✌️ "}

def _beats(a, b): # Does 'a' beat 'b'?
    return (a - b) % 3 == 1


def _counter(move): # What move beats 'move'?
    return (move + 1) % 3


def _prompt_move(console):
    while True:
        raw = input("  Your move [r/p/s, q=quit]: ").strip().lower()
        if raw == "q":
            return None
        if raw in "rps" and len(raw) == 1:
            return "rps".index(raw)
        console.print("[red]  Invalid — enter r, p, or s.[/]")


def _show_scoreboard(console, model_name, human, model_wins, ties, total):
    table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold")
    table.add_column("Player", style="cyan")
    table.add_column("Wins", justify="center")
    table.add_column("Win %", justify="center")

    def pct(w):
        return f"{100 * w / total:.0f}%" if total else "—"

    table.add_row("You",          str(human),     pct(human))
    table.add_row(model_name,     str(model_wins), pct(model_wins))
    table.add_row("[dim]Ties[/]", str(ties),       pct(ties))

    console.print(Panel(table, title="[bold]Final Score[/]", expand=False))


def play(model, rounds=10):
    console = Console()
    history = []
    human_score = model_score = ties = completed = 0

    console.print(Panel(
        f"[bold cyan]Rock · Paper · Scissors[/]\n"
        f"Opponent: [yellow]{model.name}[/]\n\n"
        f"[dim]The model predicts your move and plays its counter.\n"
        f"R = Rock   P = Paper   S = Scissors   Q = Quit[/]",
        expand=False
    ))
    console.print()

    for round_num in range(1, rounds + 1):
        console.rule(f"[dim]Round {round_num} / {rounds}[/dim]")

        human_move = _prompt_move(console)
        if human_move is None:
            break

        predicted  = model.predict(history) # The model predicts the human's next move
        model_move = _counter(predicted) # ,plays the move that beats the predicted move

        if human_move == model_move:
            ties += 1
            outcome = "[dim]Tie[/dim]"
        elif _beats(human_move, model_move):
            human_score += 1
            outcome = "[green bold]You win![/]"
        else:
            model_score += 1
            outcome = f"[red bold]{model.name} wins![/]"

        history.append((human_move, model_move))
        completed += 1

        console.print(
            f"\n  You:   {SYMBOLS[human_move]} {MOVES[human_move]}\n"
            f"  Model played {SYMBOLS[model_move]} {MOVES[model_move]}\n"
            f"  {outcome}\n"
        )

    _show_scoreboard(console, model.name, human_score, model_score, ties, completed)


if __name__ == "__main__":
    from Models.random_model import RandomModel
    play(RandomModel(), rounds=50)
