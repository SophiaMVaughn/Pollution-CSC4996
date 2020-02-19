import sys
from time import sleep

lines = []
lines.append("hello this is saular")
lines.append("no this is what i want")
lines.append("i like toitles")
lines.append("what the hell is going on?")



for line in lines:
    print("\r" + line, end="")
    sys.stdout.flush()