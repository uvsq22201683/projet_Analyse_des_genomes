
def calculate_score(seq):
    seq_score = []
    for aa in seq:
        seq_score.append(SCALE[aa])
    return seq_score