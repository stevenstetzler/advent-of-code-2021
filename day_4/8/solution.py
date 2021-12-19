import numpy as np
import io

def main():
    with open("input", "r") as f:
        lines = f.readlines()

    draw_order = [int(n) for n in lines[0].strip().split(",")]
    lines = lines[2:]
    boards = []
    markers = []
    while len(lines) > 0:
        with io.StringIO() as f:
            # write 5 lines
            f.write("\n".join(lines[0:6]))
            f.seek(0)
            # read as numpy array
            board = np.loadtxt(f, dtype=int)
            boards.append(board)
            markers.append(np.zeros_like(board).astype(bool))
            lines = lines[6:]
    
    print("there will be", len(draw_order), "draws")

    winning_boards = []
    winning_board_indices = []
    winning_board_draws = []
    winning_board_markers = []
    for i, draw in enumerate(draw_order):
        for j, (board, marker) in enumerate(zip(boards, markers)):
            if j in winning_board_indices:
                continue

            marker[board == draw] = True
        
        for j, (board, marker) in enumerate(zip(boards, markers)):
            if j in winning_board_indices:
                continue

            for row in marker:
                if row.sum() == 5:
                    winning_boards.append(board)
                    winning_board_indices.append(j)
                    winning_board_draws.append(draw)
                    winning_board_markers.append(marker)
                    print("board", j, "wins on draw", i)
                    break
            
            if j in winning_board_indices:
                continue

            for row in marker.T:
                if row.sum() == 5:
                    winning_boards.append(board)
                    winning_board_indices.append(j)
                    winning_board_draws.append(draw)
                    winning_board_markers.append(marker)
                    print("board", j, "wins on draw", i)
                    break
    
    print("there are", len(winning_boards), "winning boards")
    last_winning_board = winning_boards[-1]
    last_winning_board_index = winning_board_indices[-1]
    last_winning_board_draw = winning_board_draws[-1]
    last_winning_board_marker = winning_board_markers[-1]
    print("last winning board:\n", last_winning_board)
    print("last winning board index:", last_winning_board_index)
    print("last winning board draw:", last_winning_board_draw)
    print("last winnning board marker:\n", last_winning_board_marker)
    score = last_winning_board[~last_winning_board_marker].sum() * last_winning_board_draw
    print("score:", score)

if __name__ == "__main__":
    main()
