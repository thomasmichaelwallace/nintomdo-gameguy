import sys
# correct import path when running on the Pico
sys.path.insert(0, '/src')

print("thomasmichaelwallace/tilt-out")

from src import main # pylint: disable=wrong-import-position, unused-import
