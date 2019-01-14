'''

1. 사전준비 (https://docs.docker.com/compose/install/#install-compose)
    1. docker-compose 설치
    (sudo) curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    2. 권한변경
    sudo chmod +x /usr/local/bin/docker-compose

    3. 버젼확인
    $ docker-compose --version

2. 장고 설치
    (https://docs.docker.com/compose/django/)
    (https://teamlab.github.io/jekyllDecent/blog/tutorials/docker%EB%A1%9C-django-%EA%B0%9C%EB%B0%9C%ED%95%98%EA%B3%A0-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0(+-nginx,-gunicorn)

     step1. dockerfile 생성

    # vim dockerfile                      # 확장자는 없음

---------------------------------------------------------------------------------------------------------
 FROM python:3.5                       # 기본 이미지를 python3.5 로 설정
 ENV PYTHONUNBUFFERED 1                # 환경변수 설정 삭제할까?
 RUN mkdir /code                       # docker 내에서 /code 라는 이름의 폴더 생성
 WORKDIR /code                         # docker 내에서 코드를 실행할 폴더 위치를 /code 로 지정
 ADD requirements.txt /code/           # 로컬의 requirements.txt 파일을 docker /code/ 폴더로 마운트
 RUN pip install -r requirements.txt   # docker 내 requirements.txt 파일을 이용하여 패키지 설치
 ADD . /code/                          # 로컬 내 현재 위치에 있는 모든 파일 및 폴더를 docker 의 /code/ 폴더로 마운트
----------------------------------------------------------------------------------------------------------

    step2. requirement.txt 생성

    # vim requirements.txt
    - django project 생성 및 실행에 필요한 최소한의 파이썬 패키지
------------------------------------------------------------------------------------------------------------
 Django>2.0
 psycopg2
------------------------------------------------------------------------------------------------------------

    step3. docker-compose.yml 생성

-------------------------------------------------------------------------------------------------------------
version: '3'

services:
  db:                        > 사이에 넣을 수 있음. container_name: mydb(예시)
    container_name: xxx
    image: postgres
    ports:
      - "5432:5432"

  web:
    container_name: xxx
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
-------------------------------------------------------------------------------------------------------------------

3. 프로젝트 만들기
    sudo docker-compose run web django-admin.py startproject composeexample (docker 사용자를 그룹에 넣은 경우 sudo 불필)
        주의! web은 service 이름이며 docker-compose.yml 에 적힌 이름과 동일해야 함.

    sudo chown -R $USER:$USER 디렉토리 및 파일 명
        주의! django-admin의 권한은 root가 가지고 있으므로 소유권을 변경하여야 한다.
              root 계정으로 처음부터 시작한 경우에는 위 과정은 필요 없음
            chowwn 예시chown -R apache:apache /var/www/html/*
4. 프로젝트 생성 확인 및 디렉토리 변경
    sudo ll
------------------------------------------------------------------------------------------------
-rw-r--r--  1 user  staff  145 Feb 13 23:00 dockerfile
drwxr-xr-x  6 user  staff  204 Feb 13 23:07 composeexample
-rw-r--r--  1 user  staff  159 Feb 13 23:02 docker-compose.yml
-rw-r--r--  1 user  staff   16 Feb 13 23:01 requirements.txt
------------------------------------------------------------------------------------------------
    문제점 : composeexample 디렉토리 하위에 composeexample 디렉토리와 manage.py 파일이 존재
            이 상태에서  server를 run하면 manage.py 파일을 찾을 수 없다는 error가 발생.
    해결책 : 하위의 composeexample 디렉토리와 manage.py 파일을 상위 디렉토리로 이동시킨다.

    sudo cd composeexampe

    sudo mv composeexample composeexample1
    sudo cp -r composeexample1 /root/           # 디렉토리 복사시 -r을 사용
    sudo cp manage.py /root

    sudo cd ..
    sudo rm -rf composeexample
    sudo mv composeexample1 composeexample

------------------------------------------------------------------------------------------------
-rw-r--r--  1 user  staff  145 Feb 13 23:00 dockerfile
drwxr-xr-x  6 user  staff  204 Feb 13 23:07 composeexample
-rw-r--r--  1 user  staff  159 Feb 13 23:02 docker-compose.yml
-rwxr-xr-x  1 user  staff  257 Feb 13 23:07 manage.py
-rw-r--r--  1 user  staff   16 Feb 13 23:01 requirements.txt
------------------------------------------------------------------------------------------------

5. database 연결
    sudo cd compseexample
    sudo vim settings.py

------------------------------:ㅈㅂ:-------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
--------------------------------------------------------------------------------------------------------
    주의! django의 경우 DB는 sqlite이므로 postgres DB를 사용할 경우 설정을 변경하여야 한다.

6. server 구동
    1. sudo docker-compose up
        : DB에 대한 설정 변경이 있었으므로 docker-compose를 update 시킴
        : docker-compose 내의 command :  python3 manage.py runserver 0.0.0.0:8000이 실행 됨

        문제점 :
        1. 가상머신에 docker가 설치된 경우 가상머신 ip와 docker 사이의 포트포워딩이 필요하다.
        2. 가상머신 ip:8000으로 진입할 경우 가상머신 ip를 ALLOWED_HOST에 add하라는 error가 발생한다.
             Invalid HTTP_HOST header: '192.168.100.113:8000'. You may need to add '192.168.100.113' to ALLOWED_HOSTS.

        해결책 :
        1. 방화벽 개방
        sudo firewall-cmd --zone=public --permanent --add-port=8000/tcp
        sudo systemctl restart firewalld.service
        2. sudo vim settings.py 설정
         -------------------------------------------------------------
            ALLOWED_HOSTS = ["*"]
         --------------------------------------------------------------

    2. 웹브라우저에서 ip:8000으로 접속

7. 설문조사 app 만들기
sudo docker-compose exec web ./manage.py startapp polls
** Django tutorial 참고 https://docs.djangoproject.com/ko/2.1/intro/tutorial02/

8. runserver again
sudo docker-compose exec web ./manage.py migrate
sudo docker-compose exec web ./manage.py runserver

ip:8000/polls 접속

9. postgres 접속
docker exec -it DOCKER_NAME psql -U postgres -W postgres

** 참고
다른 디렉터리에서 다른 프로젝트를 생성하는 경우
1. 다른 디렉터리로 docker-compose.yam, dockerfile, requirements.txt를 복사하여 이동
2. 기존의 docker-compose를 가지고 생성하는 경우
    - docker-compose up --build
