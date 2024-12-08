FROM python:3.12-slim

WORKDIR /app
COPY ./ /app/

# 빌드할 때 실행 
# 1. 가상 환경 설정
RUN python -m venv .venv

# 2. 종속성 설치
RUN pip install -r requirements.txt

# 컨테이너가 생성될 때 실행
# 3. 서버 실행
ENV DEBUG=True
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]