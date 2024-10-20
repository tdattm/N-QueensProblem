import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt

def QueensPosition():
    # Create model
    model = gp.Model("Ex6")

    # Create 8x8 = 64 binary variables x(i,j)
    x = model.addVars(8, 8, vtype=GRB.BINARY, name="x")

    # Objective function: maximize the number of queens on the board
    model.setObjective(gp.quicksum(x[i, j] for i in range(8) 
                                   for j in range(8)), GRB.MAXIMIZE)

    # Row constraint: each row has at most 1 queen
    for i in range(8):
        model.addConstr(gp.quicksum(x[i, j] for j in range(8)) <= 1, 
                        name=f"row_{i+1}")

    # Column constraint: each column has at most 1 queen
    for j in range(8):
        model.addConstr(gp.quicksum(x[i, j] for i in range(8)) <= 1, 
                        name=f"col_{j+1}")

    # Main diagonal constraint: sum along each diagonal i - j = k
    for k in range(-6, 7):
        model.addConstr(gp.quicksum(x[i, j] for i in range(8) for j in range(8) 
                                    if i - j == k) <= 1, name=f"diag1_{k}")

    # Anti-diagonal constraint: sum along each diagonal i + j = k
    for k in range(3, 16):
        model.addConstr(gp.quicksum(x[i, j] for i in range(8) for j in range(8) 
                                    if i + j == k) <= 1, name=f"diag2_{k}")

    # Optimize the problem
    model.optimize()

    # Check the status of the model
    if model.status == GRB.OPTIMAL:
        solution = model.getAttr('x', x)
        print("Optimal solution:")
        for i in range(8):
            for j in range(8):
                print(f"x({i+1},{j+1}) = {solution[i, j]}")
        
        # Call the function to draw the board with the queens
        draw_board(solution)
    else:
        print("No optimal solution exists!")

def draw_board(solution):
    """Draw an 8x8 board and place the queens according to the optimal solution."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the checkerboard pattern
    for i in range(8):
        for j in range(8):
            color = 'white' if (i + j) % 2 == 0 else 'gray'
            ax.add_patch(plt.Rectangle((j, 7 - i), 1, 1, color=color))

    # Place queens according to the solution
    for i in range(8):
        for j in range(8):
            if solution[i, j] > 0.5:
                ax.text(j + 0.5, 7 - i + 0.5, '♕', ha='center', va='center', 
                        fontsize=36, color='black')

    # Index the squares above (columns) and to the left (rows)
    for i in range(8):
        # Column index
        ax.text(i + 0.5, 8.1, f'{i + 1}', ha='center', va='center', fontsize=14)  
        # Row index
        ax.text(-0.5, 7 - i + 0.5, f'{i + 1}', ha='center', va='center', fontsize=14)  

    # Set limits and turn off all axes
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


QueensPosition()
