# Fixed maze configuration (0 for path, 1 for wall)
fixed_maze = [[0 for _ in range(50)] for _ in range(50)]

# Add some walls to create a simple maze pattern
for i in range(10, 40):
    fixed_maze[20][i] = 1
    fixed_maze[30][i] = 1

for i in range(20, 31):
    fixed_maze[i][15] = 1
    fixed_maze[i][35] = 1

# Fixed weights configuration (1-3 for different weights)
fixed_weights = [[1 for _ in range(50)] for _ in range(50)]

# Add some weight variations
for i in range(10, 40):
    fixed_weights[20][i] = 2
    fixed_weights[30][i] = 2

for i in range(20, 31):
    fixed_weights[i][15] = 3
    fixed_weights[i][35] = 3 
#rint(fixed_maze)   