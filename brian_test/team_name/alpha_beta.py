import numpy as np
max_depth = 3
branching_factor = 2
min_alpha = -1000000
max_beta = 1000000


def alpha_beta(values, current_depth, index, maximizer, alpha, beta):
    if current_depth == max_depth:
        return values[index]
    if maximizer:
        best_score = min_alpha
        for i in range(0, branching_factor):
            score = alpha_beta(values, current_depth + 1, index * branching_factor + i, False, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(best_score, alpha)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = max_beta
        for i in range(0, branching_factor):
            score = alpha_beta(values, current_depth + 1, index * branching_factor + i, True, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def evaluation(board_dict, node):
    score = 0
    for element in list(board_dict.values()):
        if element == 'red':
            score += 1
    return score + np.random.randint(0, 10)


print("The optimal value is :", alpha_beta([3, 5, 6, 9, 1, 2, 0, -1, 2, 4, 6, 7, ], 0, 0, True, min_alpha, max_beta))
