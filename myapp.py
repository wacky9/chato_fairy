import sys
DIR_HEAD = 'log/'

print("test")

sys.stdout = open(DIR_HEAD + "output.log", "w", buffering=1)  # Redirects stdout to "output.log"

print("This will be written to the file instead of the console.")

sys.stdout.close()
sys.stdout = sys.__stdout__

print("test2")