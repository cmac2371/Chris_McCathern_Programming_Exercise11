import random
from dataclasses import dataclass
from typing import List, Tuple

# ---------- Card / Deck ----------

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

def make_deck() -> List[Card]:
    """Create and return a shuffled 52-card deck."""
    deck = [Card(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

# ---------- Game helpers ----------

def deal_hand(deck: List[Card], n: int = 5) -> List[Card]:
    """Deal n cards from the deck."""
    hand = deck[:n]
    del deck[:n]
    return hand

def show_hand(hand: List[Card]) -> str:
    """Return a human-readable string for a hand."""
    return " | ".join(f"{i+1}:{c.rank}{c.suit}" for i, c in enumerate(hand))

def parse_selection(inp: str) -> List[int]:
    """
    Parse user input like '1, 3,5' or '2 4' into zero-based indices.
    Valid positions are 1..5; duplicates are removed.
    """
    # Replace commas with spaces, split, keep digits
    parts = inp.replace(",", " ").split()
    indices = []
    for p in parts:
        if p.isdigit():
            k = int(p)
            if 1 <= k <= 5:
                idx = k - 1  # convert to zero-based
                if idx not in indices:
                    indices.append(idx)
    return sorted(indices)

def draw_replace(deck: List[Card], hand: List[Card], replace_indices: List[int]) -> None:
    """Replace the cards at the specified indices with new cards from the deck."""
    for idx in replace_indices:
        if not deck:
            raise RuntimeError("Deck is out of cards.")
        hand[idx] = deck.pop(0)

# ---------- Main game loop ----------

def main():
    print("=== Five-Card Draw (Single Draw) ===")
    print("Deck is shuffled. Dealing 5 cards...")

    deck = make_deck()
    hand = deal_hand(deck, 5)

    print("\nYour initial hand:")
    print(show_hand(hand))

    print("\nEnter the card positions you want to replace (1-5).")
    print("Examples: 1,3,5  |  2 4  |  (press Enter for no change)")
    raw = input("Replace: ").strip()

    replace_indices = parse_selection(raw)
    if replace_indices:
        draw_replace(deck, hand, replace_indices)
        print("\nCards replaced at positions:", ", ".join(str(i+1) for i in replace_indices))
    else:
        print("\nNo cards replaced.")

    print("\nYour final hand:")
    print(show_hand(hand))
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()

