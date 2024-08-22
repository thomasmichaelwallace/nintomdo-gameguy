import sys

print("thomasmichaelwallace/nintomdo-gameguy")

# correct import path when running on the Pico
sys.path.insert(0, '/src')
from src import main # pylint: disable=wrong-import-position, unused-import
