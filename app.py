import random
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ROWS = 5
COLS = 5
TIER_POINTS = [[25, 2], [50, 3], [100, 5], [200, 10], [500, 20], [1000, 50]]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
score = 0
tier = 0
worth = 1

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.put('/place-flower')
def place_flower():
    empty = [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == " "]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = "F"

@app.post('/init')
def init_board():
    if any(cell == "F" for row in board for cell in row):
        return
    for _ in range(5):
        place_flower()

def print_board():
    print(f"\n  Score: {score}\n")
    print("    " + "   ".join(str(c) for c in range(COLS)))
    print("  +" + "---+" * COLS)
    for r in range(ROWS):
        row_str = " | ".join(board[r][c] for c in range(COLS))
        print(f"{r} | {row_str} |")
        print("  +" + "---+" * COLS)
    print()

@app.get('/show-board')
def show_board():
    return {"board": board, "score": score, "tier": tier, "worth": worth}

@app.put('/collect-flower', status_code=status.HTTP_200_OK)
def collect_flower(row: int, col: int):
    global score
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return "Out of bounds!"
    if board[row][col] != "F":
        return "No flower there!"
    board[row][col] = " "
    score += worth
    place_flower()
    return f'Collected! Current score: {score}'

@app.put('/upgrade')
def upgrade():
    global score
    global tier
    global worth
    
    if score >= TIER_POINTS[tier][0]:
        worth = TIER_POINTS[tier][1]
        score -= TIER_POINTS[tier][0]
        tier += 1
        return f"Upgraded to Tier {tier}! New points per flower: {worth}"
    
    return f"Not enough points to upgrade. Current score: {score}, needed: {TIER_POINTS[tier][0]}"

# def main():
#     init_board()

#     print("Welcome to Flower Collector!")
#     print("Flowers (F) appear on the 5x5 board.")
#     print("Enter row and column to collect a flower.")
#     print("Type 'u' to upgrade your collection tier for more points per flower.")
#     print("Type 'q' to quit.\n")

#     while True:
#         print_board()

#         inp = input("Enter row col (e.g. 2 3), 'q' to quit, or 'u' to upgrade: ").strip()

#         if inp.lower() == "q":
#             print(f"\nGame over! Final score: {score}")
#             print("Thanks for playing!")
#             break
#         elif inp.lower() == "u":
#             print(upgrade())
#             continue

#         parts = inp.split()
#         if len(parts) != 2:
#             print("Please enter two numbers separated by a space.")
#             continue

#         try:
#             row, col = int(parts[0]), int(parts[1])
#         except ValueError:
#             print("Invalid input. Enter numbers like: 2 3")
#             continue

#         print(collect(row, col))


# if __name__ == "__main__":
#     main()