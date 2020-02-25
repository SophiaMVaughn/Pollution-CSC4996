tsv = open("saular-200-articles-tsv.txt", "r").readlines()
lastTwentyThousand = open("last-twenty-thousand.tsv", "a+")

count = 1
for line in tsv:
    if count >= 100000:
        lastTwentyThousand.write(line)

# lastTwentyThousand = open("last-twenty-thousand.tsv", "r")
#
# for line in lastTwentyThousand:
#     print(line)