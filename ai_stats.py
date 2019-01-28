import statistics
import time

# settings
file_path = "data/20190128-171025-897713_scores.txt"
refresh = True
pause_seconds = 30

# stat functions
def correlation(x_vals, x_bar, sx, y_vals, y_bar, sy):
    numerator = 0
    denominator = (len(x_vals) - 1) * sx * sy
    
    for x, y in zip(x_vals, y_vals):
        numerator += (x - x_bar) * (y - y_bar)

    return numerator / denominator
    
# let's do this
running = True
last_num_games = 0

while running:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    scores = []
    coins = []

    for line in lines:
        line = line.split(',')
        scores.append(int(line[0]))
        coins.append(int(line[1]))

    scores, coins = zip(*sorted(zip(scores, coins)))

    ''' summary stats '''
    num_games = len(scores)
    
    low_score = min(scores)
    high_score = max(scores)
    median_score = round(statistics.median(scores))
    q1_score = round(statistics.median(scores[:len(scores)//2]))
    q3_score = round(statistics.median(scores[len(scores)//2:]))
    mean_score = round(statistics.mean(scores))
    st_dev_score = round(statistics.stdev(scores))

    low_coins = min(coins)
    high_coins = max(coins)
    median_coins = round(statistics.median(coins))
    mean_coins = round(statistics.mean(coins))
    q1_coins = round(statistics.median(coins[:len(coins)//2]))
    q3_coins = round(statistics.median(coins[len(coins)//2:]))
    st_dev_coins = round(statistics.stdev(coins))

    ''' regression '''
    r = correlation(coins, mean_coins, st_dev_coins, scores, mean_score, st_dev_score)
    r2 = r * r
    a = r * st_dev_score / st_dev_coins
    b = mean_score - a * mean_coins
    
    print("+--------------------------------+")
    print("| The CoopBot's Block Life Stats |")
    print("|                                |")
    print(f"| Games played: {num_games:6}           |")
    print("|                                |")
    print("|             Scores    Coins    |")
    print("|             ------    -----    |")
    print(f"| Maximum:    {high_score:6}      {high_coins:3}    |")
    print(f"| Q3:         {q3_score:6}      {q3_coins:3}    |")
    print(f"| Median:     {median_score:6}      {median_coins:3}    |")
    print(f"| Q1:         {q1_score:6}      {q1_coins:3}    |")
    print(f"| Minimum:    {low_score:6}      {low_coins:3}    |")
    print("|                                |")
    print(f"| Mean:       {mean_score:6}      {mean_coins:3}    |")
    print(f"| St. Dev.:   {st_dev_score:6}      {st_dev_coins:3}    |")
    print("|                                |")
    print("| Least Squares Regression       |")
    print(f"| r:   {r:.4}                    |")
    print(f"| r^2: {r2:.4}                    |")
    print(f"| a:   {a:.5}                    |")
    print(f"| b:   {b:.5}                    |")
    print(f"| score = {a:.4}*coins + {b:.5}   |")
    print("+--------------------------------+")
    print()
    print()

    
    if refresh:
        time.sleep(pause_seconds)

    if last_num_games != num_games:
        running = refresh
        last_num_games = num_games
    else:
        running = False
