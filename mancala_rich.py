#!/usr/bin/env python3
"""
MANCALA GAME - Enhanced with Rich Library
Beautiful terminal graphics version

This version adds visual polish using the Rich library:
- Colorful tables for the board
- Styled announcements
- Visual seed representations
- Professional game over screen

Install Rich first: pip install rich
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.live import Live
from rich.spinner import Spinner
import time
import random

console = Console()


# ========================================
# CORE GAME FUNCTIONS (from Days 1-3)
# ========================================

def create_board():
    """Create a new Mancala board with starting positions."""
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


def get_opposite_pocket(pocket):
    """Get the pocket directly opposite on the board."""
    return 12 - pocket


def is_valid_move(board, pocket, player):
    """Check if a move is valid."""
    if pocket < 0 or pocket > 12:
        return False, "Invalid pocket number."
    
    if player == 1:
        if pocket < 0 or pocket > 5:
            return False, "That pocket is not on your side. Choose 0-5."
    else:
        if pocket < 7 or pocket > 12:
            return False, "That pocket is not on your side. Choose 7-12."
    
    if board[pocket] == 0:
        return False, "That pocket is empty. Choose a different pocket."
    
    return True, "Valid move!"


def check_free_turn(last_position, player):
    """Check if player gets a free turn."""
    if player == 1 and last_position == 6:
        return True
    elif player == 2 and last_position == 13:
        return True
    return False


def check_capture(board, last_position, player):
    """Check if a capture occurred and execute it."""
    player_pockets = range(0, 6) if player == 1 else range(7, 13)
    player_store = 6 if player == 1 else 13
    
    if last_position not in player_pockets:
        return board, 0
    
    if board[last_position] != 1:
        return board, 0
    
    opposite = get_opposite_pocket(last_position)
    
    if board[opposite] == 0:
        return board, 0
    
    # CAPTURE!
    captured_seeds = board[opposite] + board[last_position]
    
    board[player_store] += captured_seeds
    board[opposite] = 0
    board[last_position] = 0
    
    return board, captured_seeds


def make_move(board, pocket, player):
    """Make a complete move with all Mancala rules."""
    valid, message = is_valid_move(board, pocket, player)
    if not valid:
        return board, False, 0, message
    
    if player == 1:
        opponent_store = 13
    else:
        opponent_store = 6
    
    seeds_in_hand = board[pocket]
    board[pocket] = 0
    
    current_position = pocket
    
    while seeds_in_hand > 0:
        current_position = (current_position + 1) % 14
        
        if current_position == opponent_store:
            continue
        
        board[current_position] += 1
        seeds_in_hand -= 1
    
    board, captured = check_capture(board, current_position, player)
    gets_free_turn = check_free_turn(current_position, player)
    
    return board, gets_free_turn, captured, "Success"


def is_side_empty(board, player):
    """Check if a player's side is completely empty."""
    if player == 1:
        return all(board[i] == 0 for i in range(0, 6))
    else:
        return all(board[i] == 0 for i in range(7, 13))


def collect_remaining_seeds(board):
    """Collect all remaining seeds to their respective stores."""
    player1_remaining = sum(board[i] for i in range(0, 6))
    board[6] += player1_remaining
    for i in range(0, 6):
        board[i] = 0
    
    player2_remaining = sum(board[i] for i in range(7, 13))
    board[13] += player2_remaining
    for i in range(7, 13):
        board[i] = 0
    
    return board


# ========================================
# RICH VISUAL ENHANCEMENTS
# ========================================

def display_board_rich(board, player1_name="Player 1", player2_name="Player 2", current_player=1):
    """Display the Mancala board using Rich tables."""
    
    # Create a table
    table = Table(
        title="🎮 MANCALA BOARD 🎮",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta",
        border_style="blue"
    )
    
    # Add columns
    table.add_column("Store", justify="center", style="yellow", width=10)
    for i in range(6):
        table.add_column(str(12-i), justify="center", style="cyan", width=8)
    
    # Player 2's row (top)
    player2_style = "bold cyan" if current_player == 2 else ""
    player2_row = [
        f"[bold yellow]{board[13]:2d}[/bold yellow]",
        *[f"[cyan]{board[i]:2d}[/cyan]" for i in range(12, 6, -1)]
    ]
    table.add_row(*player2_row, style=player2_style)
    
    # Separator
    separator = [""] + ["―" * 5] * 6
    table.add_row(*separator, style="dim")
    
    # Create second table for Player 1
    table2 = Table(show_header=True, header_style="bold magenta", border_style="green")
    for i in range(6):
        table2.add_column(str(i), justify="center", style="green", width=8)
    table2.add_column("Store", justify="center", style="yellow", width=10)
    
    # Player 1's row (bottom)
    player1_style = "bold green" if current_player == 1 else ""
    player1_row = [
        *[f"[green]{board[i]:2d}[/green]" for i in range(0, 6)],
        f"[bold yellow]{board[6]:2d}[/bold yellow]"
    ]
    table2.add_row(*player1_row, style=player1_style)
    
    # Display both tables
    console.print()
    console.print(table)
    console.print(table2)
    console.print(
        f"\n[bold green]{player1_name}[/bold green] vs "
        f"[bold cyan]{player2_name}[/bold cyan]"
    )
    console.print()


def show_welcome():
    """Display a welcome message."""
    welcome_text = """
    [bold cyan]Welcome to Mancala![/bold cyan]
    
    🎯 Goal: Collect the most seeds in your store
    ⭐ Land in your store for a free turn
    💰 Land in an empty pocket to capture!
    """
    
    panel = Panel(
        welcome_text,
        title="🎮 Game Rules 🎮",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(panel)


def announce_move(player, pocket, seeds, player_name):
    """Announce a player's move with style."""
    player_color = "green" if player == 1 else "cyan"
    
    console.print(
        f"\n[bold {player_color}]{player_name}[/bold {player_color}] "
        f"picks pocket [yellow]{pocket}[/yellow] "
        f"([yellow]{seeds}[/yellow] seeds)"
    )


def announce_capture(player, captured_seeds, player_name):
    """Announce a capture."""
    console.print(
        f"\n[bold red]💰 CAPTURE![/bold red] "
        f"[bold]{player_name}[/bold] captures "
        f"[yellow]{captured_seeds}[/yellow] seeds!"
    )


def announce_free_turn(player_name):
    """Announce a free turn."""
    console.print(
        f"\n[bold green]🎉 FREE TURN![/bold green] "
        f"{player_name} goes again!"
    )


def show_game_over(board, player1_name, player2_name):
    """Display game over screen with final scores."""
    player1_score = board[6]
    player2_score = board[13]
    
    # Create scores table
    scores_table = Table(show_header=True, header_style="bold magenta")
    scores_table.add_column("Player", style="cyan", justify="left")
    scores_table.add_column("Final Score", style="yellow", justify="center")
    
    scores_table.add_row(player1_name, str(player1_score))
    scores_table.add_row(player2_name, str(player2_score))
    
    # Determine winner
    if player1_score > player2_score:
        winner_text = f"[bold green]🏆 {player1_name} WINS! 🏆[/bold green]"
    elif player2_score > player1_score:
        winner_text = f"[bold cyan]🏆 {player2_name} WINS! 🏆[/bold cyan]"
    else:
        winner_text = "[bold yellow]🤝 TIE GAME! 🤝[/bold yellow]"
    
    # Create game over panel
    console.print()
    console.print(Panel.fit(
        "[bold red]GAME OVER[/bold red]",
        border_style="red"
    ))
    console.print()
    console.print(scores_table)
    console.print()
    console.print(Panel.fit(
        winner_text,
        border_style="gold1"
    ))
    console.print()


def show_statistics(stats):
    """Display game statistics in a formatted table."""
    table = Table(
        title="📊 Game Statistics",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Statistic", style="cyan")
    table.add_column("Value", style="yellow", justify="right")
    
    table.add_row("Total Moves", str(stats.get('moves', 0)))
    table.add_row("Player 1 Moves", str(stats.get('player1_moves', 0)))
    table.add_row("Player 2 Moves", str(stats.get('player2_moves', 0)))
    table.add_row("Free Turns", str(stats.get('free_turns', 0)))
    table.add_row("Captures", str(stats.get('captures', 0)))
    
    console.print()
    console.print(table)
    console.print()


def ai_thinking():
    """Show AI thinking animation."""
    spinner = Spinner("dots", text="[cyan]AI is thinking...[/cyan]")
    
    with Live(spinner, refresh_per_second=10, console=console):
        time.sleep(1.5)
    
    console.print("[green]✓[/green] AI has chosen!")


# ========================================
# AI PLAYER
# ========================================

class AIPlayer:
    """Computer player with difficulty levels."""
    
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
    
    def choose_move(self, board, player):
        """Choose a move based on difficulty level."""
        valid_moves = [i for i in (range(0, 6) if player == 1 else range(7, 13)) 
                       if board[i] > 0]
        
        if not valid_moves:
            return None
        
        # Show thinking animation
        ai_thinking()
        
        if self.difficulty == 'easy':
            return random.choice(valid_moves)
        else:
            # Simple strategy: prefer moves that land in store
            for pocket in valid_moves:
                target = (pocket + board[pocket]) % 14
                if (player == 1 and target == 6) or (player == 2 and target == 13):
                    return pocket
            return random.choice(valid_moves)


# ========================================
# MAIN GAME FUNCTION
# ========================================

def play_mancala_rich():
    """Play Mancala with Rich visual enhancements."""
    
    # Show welcome
    show_welcome()
    
    # Game mode selection
    console.print("\n[bold]Select game mode:[/bold]")
    console.print("1. Two Players")
    console.print("2. vs AI (Easy)")
    console.print("3. vs AI (Medium)")
    
    mode = Prompt.ask("Choice", choices=["1", "2", "3"], default="1")
    
    # Get player names
    player1_name = Prompt.ask(
        "\n[green]Player 1, enter your name[/green]",
        default="Player 1"
    )
    
    if mode == "1":
        player2_name = Prompt.ask(
            "[cyan]Player 2, enter your name[/cyan]",
            default="Player 2"
        )
        ai_opponent = None
    else:
        player2_name = "AI"
        difficulty = 'easy' if mode == '2' else 'medium'
        ai_opponent = AIPlayer(difficulty)
        console.print(f"\n[yellow]You're playing against AI ({difficulty} difficulty)[/yellow]")
    
    input("\nPress Enter to start...")
    
    # Initialize game
    board = create_board()
    current_player = 1
    
    stats = {
        'moves': 0,
        'player1_moves': 0,
        'player2_moves': 0,
        'free_turns': 0,
        'captures': 0
    }
    
    # Main game loop
    while True:
        # Check if game is over
        if is_side_empty(board, 1) or is_side_empty(board, 2):
            console.print("\n[bold red]🏁 One side is empty - Game Over![/bold red]")
            board = collect_remaining_seeds(board)
            display_board_rich(board, player1_name, player2_name)
            show_statistics(stats)
            show_game_over(board, player1_name, player2_name)
            break
        
        # Display board
        display_board_rich(board, player1_name, player2_name, current_player)
        
        # Get current player name
        current_name = player1_name if current_player == 1 else player2_name
        color = "green" if current_player == 1 else "cyan"
        
        console.print(f"\n[bold]--- Move #{stats['moves'] + 1} ---[/bold]")
        console.print(f"Current turn: [{color}]{current_name}[/{color}]")
        
        # Get move
        if current_player == 2 and ai_opponent:
            pocket = ai_opponent.choose_move(board, current_player)
        else:
            range_text = "0-5" if current_player == 1 else "7-12"
            while True:
                pocket = IntPrompt.ask(
                    f"[{color}]Choose your pocket ({range_text})[/{color}]"
                )
                valid, msg = is_valid_move(board, pocket, current_player)
                if valid:
                    break
                console.print(f"[red]❌ {msg}[/red]")
        
        # Announce move
        seeds_picked = board[pocket]
        announce_move(current_player, pocket, seeds_picked, current_name)
        
        # Make move
        board, gets_free_turn, captured, msg = make_move(board, pocket, current_player)
        
        # Announce special events
        if captured > 0:
            announce_capture(current_player, captured, current_name)
            stats['captures'] += 1
        
        if gets_free_turn:
            announce_free_turn(current_name)
            stats['free_turns'] += 1
        
        # Update stats
        stats['moves'] += 1
        if current_player == 1:
            stats['player1_moves'] += 1
        else:
            stats['player2_moves'] += 1
        
        # Switch players
        if not gets_free_turn:
            current_player = 2 if current_player == 1 else 1
        
        # Pause
        if not (current_player == 2 and ai_opponent):
            input("\n[dim]Press Enter to continue...[/dim]")
    
    console.print("\n[bold green]Thanks for playing Mancala![/bold green]\n")


# ========================================
# RUN THE GAME
# ========================================

if __name__ == "__main__":
    try:
        play_mancala_rich()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Game interrupted. Thanks for playing![/yellow]\n")
