### Config enviroment
* Create .env
```python3 -m venv .env```
* Enable enviroment
```source .env/bin/active```

### Install dependencies
* Install lib
```pip3 install -r requirements.txt```

### Run app
* Run
```streamlit run demo_churn.py```

### Run app by Docker
* Build Docker Image from Dockerfile
```docker build -t streamlit-churn-app```
* Run Docker Image
```docker run -d -p 8501:8501 --name churn-app streamlit-churn-app```
* Test app
```Access: http://localhost:8051```


