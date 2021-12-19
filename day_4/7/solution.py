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
    
    winning_board = None
    winning_board_marker = None
    for i, draw in enumerate(draw_order):
        for board, marker in zip(boards, markers):
            marker[board == draw] = True
        
        for board, marker in zip(boards, markers):
            for row in marker:
                if row.sum() == 5:
                    winning_board = board
                    winning_board_marker = marker
            for row in marker.T:
                if row.sum() == 5:
                    winning_board = board
                    winning_board_marker = marker
            if winning_board is not None:
                break
        if winning_board is not None:
            print("board win on draw", i + 1, draw)
            break
    print("winning board:\n", winning_board)
    print("winnning board marker:\n", winning_board_marker)
    score = winning_board[~winning_board_marker].sum() * draw
    print("score:", score)
    

if __name__ == "__main__":
    main()
