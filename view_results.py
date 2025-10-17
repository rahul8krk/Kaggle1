"""
View the generated analysis results
"""
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Display the steady state results
img1 = Image.open('steady_state_results.png')
img2 = Image.open('transient_results.png')

print("Steady State Results Image:")
print(f"  Size: {img1.size}")
print(f"  Mode: {img1.mode}")

print("\nTransient Results Image:")
print(f"  Size: {img2.size}")
print(f"  Mode: {img2.mode}")

print("\nVisualization files generated successfully!")
print("  - steady_state_results.png: Shows bus voltages, angles, line loading, and generation vs load")
print("  - transient_results.png: Shows dynamic response to fault with voltage, power, and loading over time")
