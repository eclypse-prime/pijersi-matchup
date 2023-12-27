import math


def _elo_difference(win_percentage: float) -> float:
    if win_percentage == 0:
        return float('NaN')
    elif win_percentage >= 1:
        return float("inf")
    elif win_percentage < 0:
        return float('NaN')
    return -400 * math.log10(1 / win_percentage - 1)

def elo_difference(n_wins: int, n_draws: int, n_games: int) -> float:
    return _elo_difference((n_wins + n_draws/2)/n_games)

def elo_incertitude(n_wins: int, n_losses: int, n_draws: int) -> float:
    n_games = n_wins + n_losses + n_draws
    win_rate = n_wins / n_games
    loss_rate = n_losses / n_games
    draw_rate = n_draws / n_games
    percentage = (n_wins + n_draws * 0.5) / n_games
    wins_deviation = win_rate * (1 - percentage) ** 2
    draws_deviation = draw_rate * (0.5 - percentage) ** 2
    losses_deviation = loss_rate * (0 - percentage) ** 2
    std = math.sqrt(wins_deviation + draws_deviation + losses_deviation) / math.sqrt(n_games)

    confidence = 0.95
    min_confidence = (1 - confidence) / 2
    max_confidence = 1 - min_confidence
    min_deviation = percentage + phi_inv(min_confidence) * std
    max_deviation = percentage + phi_inv(max_confidence) * std

    difference = _elo_difference(max_deviation) - _elo_difference(min_deviation)
    return difference/2


def phi_inv(x: float):
    return math.sqrt(2) * inverse_erf(2 * x - 1)

def inverse_erf(x: float):
    pi = math.pi
    a = 8 * (pi - 3) / (3 * pi * (4 - pi))
    y = math.log(1 - x * x)
    z = 2 / (pi * a) + y / 2

    ret = math.sqrt(math.sqrt(z * z - y / a) - z)

    if x < 0:
        return -ret

    return ret