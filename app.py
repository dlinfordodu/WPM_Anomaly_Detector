from flask import Flask, request, render_template_string
from detector import to_wpm, calculate_probability, calculate_z_score, data

app = Flask(__name__)

PAGE_HTML = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Typing Anomaly Detector</title>
    <style>
      body { font-family: Arial, sans-serif; background: #f3f4f6; color: #111827; padding: 24px; }
      .container { max-width: 640px; margin: auto; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,.08); }
      label { display: block; margin: 12px 0 4px; font-weight: 600; }
      input { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; }
      button { margin-top: 18px; padding: 12px 18px; border: none; background: #2563eb; color: white; border-radius: 8px; cursor: pointer; }
      button:hover { background: #1d4ed8; }
      .result { margin-top: 24px; padding: 18px; background: #eef2ff; border-radius: 10px; }
      .error { color: #b91c1c; margin-top: 16px; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Typing Anomaly Detector</h1>
      <p>Enter the words typed and the time in seconds to check whether the typing speed is anomalous. (App developed by Daniel Linford.)</p>
      <form method="post">
        <label for="words">Words</label>
        <input id="words" name="words" type="number" step="0.01" required value="{{ words }}">

        <label for="seconds">Seconds</label>
        <input id="seconds" name="seconds" type="number" step="0.01" required value="{{ seconds }}">

        <button type="submit">Check Anomaly</button>
      </form>

      {% if result %}
      <div class="result">
        <p><strong>Typing rate:</strong> {{ result.rate }} words per minute</p>
        <p><strong>Average human rate:</strong> {{ result.mean }} ± {{ result.std_dev }} words per minute</p>
        <p><strong>Faster than:</strong> {{ result.faster }}% of students</p>
        <p><strong>Z-score:</strong> {{ result.z_score }}</p>
        <p><strong>Conclusion:</strong> {{ result.conclusion }}</p>
      </div>
      {% endif %}

      {% if error %}
      <div class="error">{{ error }}</div>
      {% endif %}
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    words = ''
    seconds = ''

    if request.method == 'POST':
        try:
            words = request.form.get('words', '').strip()
            seconds = request.form.get('seconds', '').strip()
            words_value = float(words)
            seconds_value = float(seconds)
            if seconds_value <= 0:
                raise ValueError('Seconds must be greater than zero.')

            rate = to_wpm(words_value, seconds_value)
            probability = calculate_probability(rate, data) * 100
            mean, std_dev, z_score = calculate_z_score(rate, data)
            mean = round(mean, 2)
            std_dev = round(std_dev, 2)
            rate = round(rate, 2)

            result = {
                'rate': rate,
                'mean': mean,
                'std_dev': std_dev,
                'faster': round(100 - probability, 2),
                'z_score': round(z_score, 4),
                'conclusion': ('This z-score is anomalous and may suggest generative AI usage.'
                               if z_score > 2.5 else
                               'This z-score is not anomalous and might not suggest generative AI usage.')
            }
        except ValueError as exc:
            error = str(exc)

    return render_template_string(PAGE_HTML, result=result, error=error, words=words, seconds=seconds)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
