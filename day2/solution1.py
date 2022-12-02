
shape = {
    'A': 'Rock',
    'B': 'Paper',
    'C': 'Scissors',
    'X': 'Rock',
    'Y': 'Paper',
    'Z': 'Scissors',
}

shape_score = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3,
}
# Rock > Scissors: 1 - 3 = -2
# Scissors > Paper: 3 - 2 = 1
# Paper > Rock: 2 - 1 = 1
win = [-2, 1]

score = 0
with open('input.txt') as f:
    for line in f:
        elf, me = line.strip().split()
        elf = shape_score[shape[elf]]
        me = shape_score[shape[me]]
        d = me - elf
        print(elf, me, d)
        score += me
        # tie
        if d == 0:
            score += 3
        # win
        if d in win:
            score += 6

print(score)