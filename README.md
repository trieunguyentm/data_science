## There are two ways to run the project

### 1. Run by install denpendencies and run app streamlit

#### Create enviroment

- Create .env
  `python3 -m venv .env`
- Enable enviroment
  `source .env/bin/active`

#### Install dependencies

- Install lib
  `pip3 install -r requirements.txt`

#### Run app

- Run
  `streamlit run demo_churn.py`

### 2. Run by docker

#### Build docker image and run container

- Build Docker Image from Dockerfile
  `docker build -t streamlit-churn-app`

- Run Docker Image
  `docker run -d -p 8501:8501 --name churn-app streamlit-churn-app`
- Test app
  `Access: http://localhost:8051`
