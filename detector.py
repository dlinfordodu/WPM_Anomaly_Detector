def round_to_nearest_5(n):
# rounds to the nearest multiple of 5
    rounded = round(n / 5) * 5
    return rounded

def to_wpm(words, seconds):
# Given a number of words and a time in seconds, return words per minute
    minutes = seconds/60
    return words/minutes

def calculate_probability(n, data):
# returns the probability of a student typing text at least as fast as indicated
    n = round_to_nearest_5(n)
    if n < min(data):
        return data[min(data)][1] * 5
    if n in data:
        total = 0
        for i in range(n, max(data) + 1, 5):
            total += data[i][1] * 5
        return round(total, 2)
    else:
        return round(data[max(data)][1] * 5, 2)

def calculate_z_score(n, data):
# returns average, standard deviation, and z-score
# when the z-score is close to 0, it means the text was likely student generated
# high z-scores indicate text that was unlikely to be student generated
    total = 0
    sum_squares = 0
    for i in data:
        total += data[i][0]*data[i][1]*5
        sum_squares += data[i][0]*data[i][0]*data[i][1]*5
    std_dev = (sum_squares - total**2)**0.5
    z_score = (n-total)/std_dev
    return total, std_dev, z_score

# The data is taken from Dhakhal, et al, 2018, ‘Observations on Typing from 136 Million Keystrokes’, 
# CHI '18: Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems, pp. 1-12.
# The paper is available at https://userinterfaces.aalto.fi/136Mkeystrokes/

data = {
    5: [7.5, 0.000318],
    10: [12.5, 0.001783],
    15: [17.5, 0.005032],
    20: [22.5, 0.009936],
    25: [27.5, 0.015096],
    30: [32.5, 0.018025],
    35: [37.5, 0.018854],
    40: [42.5, 0.018854],
    45: [47.5, 0.018217],
    50: [52.5, 0.017134],
    55: [57.5, 0.015605],
    60: [62.5, 0.013949],
    65: [67.5, 0.012038],
    70: [72.5, 0.010064],
    75: [77.5, 0.007898],
    80: [82.5, 0.005860],
    85: [87.5, 0.004268],
    90: [92.5, 0.003057],
    95: [97.5, 0.001975],
    100: [102.5, 0.001274],
    105: [107.5, 0.000764],
    110: [112.5, 0.000446],
    115: [117.5, 0.000255],
    120: [122.5, 0.000127],
}

words = float(input("Enter the number of words:"))
seconds = float(input("Enter the number of seconds:"))
n = to_wpm(words, seconds)

probability = calculate_probability(n, data)
mean, std_dev, z_score = calculate_z_score(n, data)
probability = probability*100
mean = round(mean, 2)
std_dev = round(std_dev, 2)

print('The student typed at a rate of ' + str(n) + ' words per minute.')
print('The average human types at a rate of ' + str(mean) + '+/-' + str(std_dev) + ' words per minute.')
print('The student typed faster than at least ' + str(100-probability) + '% of students.')
print('The z-score is: ' + str(z_score))
if z_score > 2.5:
    print('This z-score is anomalous and may suggest generative AI usage.')
else:
    print('This z-score is not anomalous and might not suggest generative AI usage.')
