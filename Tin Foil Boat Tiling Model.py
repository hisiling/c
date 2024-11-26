import numpy as np
import time

# Constants
foil_area = 900  # cm^2 (total area of the foil)
foil_thickness = 0.0016  # cm (thickness of the foil)
foil_density = 2.7  # g/cm^3
foil_weight = foil_area * foil_thickness * foil_density  # Weight of the foil

coin_weight = 2.5  # g (weight of one coin)
coin_diameter = 1.905  # cm (diameter of a coin)
coin_thickness = 0.155  # cm (thickness of a coin)
water_density = 1  # g/cm^3 (density of water)

# Variables
best_config = (0, 0, 0, 0)  # Track length, width, height, and coin layers
max_coins = 0

# Timer start
start_time = time.time()

# Iterate over feasible dimensions with partial coverage in mind
for length in np.linspace(10, 25, 100):  # Boat length (cm)
    for width in np.linspace(10, 25, 100):  # Boat width (cm)
        for height in np.linspace(1, 5, 50):  # Boat height (cm)
            # Calculate foil usage
            foil_used = 2 * (length * height + width * height) + length * width
            if foil_used <= foil_area:  # Check foil usage constraint
                # Calculate inner dimensions for coins
                inner_length = length - foil_thickness * 2
                inner_width = width - foil_thickness * 2

                # Allow partial coverage of coins on the base
                for coins_per_row in range(1, int(inner_length // coin_diameter) + 1):
                    for coins_per_col in range(1, int(inner_width // coin_diameter) + 1):
                        total_coins_per_layer = coins_per_row * coins_per_col

                        # Optimize number of layers
                        for layers in range(1, int(height // coin_thickness) + 1):
                            total_coins = total_coins_per_layer * layers
                            total_coin_weight = total_coins * coin_weight
                            total_weight = foil_weight + total_coin_weight

                            # Buoyant force (displaced water weight)
                            boat_volume = length * width * height
                            displaced_water_weight = boat_volume * water_density

                            if total_weight <= displaced_water_weight:
                                if total_coins > max_coins:
                                    max_coins = total_coins
                                    best_config = (length, width, height, layers, coins_per_row, coins_per_col)

# Timer end
end_time = time.time()

# Results
print("Best Configuration:")
print(f"Length: {best_config[0]:.2f} cm")
print(f"Width: {best_config[1]:.2f} cm")
print(f"Height: {best_config[2]:.2f} cm")
print(f"Layers of Coins: {best_config[3]}")
print(f"Coins per Row: {best_config[4]}")
print(f"Coins per Column: {best_config[5]}")
print(f"Total Coins: {max_coins}")
print(f"Computation Time: {end_time - start_time:.2f} seconds")
