# My API Project

This FastAPI app connects to a MySQL database hosted on cPanel.

## Database Config:
- **User**: declient_ajeigbe
- **DB Name**: declient_clientbot
- **Host**: localhost

## To run locally:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploying to Render:
Add an environment variable `DATABASE_URL` with:
```
mysql+pymysql://declient_ajeigbe:Bolatito@1980@localhost:3306/declient_clientbot
```
Then start the app with:
```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker
```
#   c l i e n t b o t - a p i  
 