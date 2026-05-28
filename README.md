# WPM Anomaly Detector

A simple Flask web app that estimates typing anomaly from words and seconds.

## Local run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:8000` in your browser.

## Deploying to Render (free tier)

1. Sign up at https://render.com and connect your GitHub repository.
2. Create a new Web Service.
3. Select the `WPM_Anomaly_Detector` repository.
4. Choose `Python` and set the build command to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the start command to:
   ```bash
   gunicorn app:app
   ```
6. Deploy the service.

Render has a free tier for small hobby apps. The app may sleep after periods of inactivity, but it will be publicly accessible when running.

## Deploying to Railway (free tier)

1. Sign up at https://railway.app.
2. Create a new project and connect the repository.
3. Use the default Python deployment settings.
4. Set the start command to:
   ```bash
   gunicorn app:app
   ```

Railway also offers a free tier for hobby projects.
