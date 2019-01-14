'''
참조 url 
http://statkclee.github.io/r-docker/index.html

step1 dockerfile 생성

mkdir rstudioStorage
cd rstudioStorage
vim dockerfile
-----------------------------------------------------------------------------------
FROM rocker/verse:latest
#RUN R -e "install.packages('gapminder', repos = 'http://cran.us.r-project.org')" 
RUN wget https://cran.r-project.org/src/contrib/gapminder_0.3.0.tar.gz
RUN R CMD INSTALL gapminder_0.3.0.tar.gz
#ADD data/gapminder-FiveYearData.csv /home/rstudio/  #도커파일 생성시 파일 첨부 가능
------------------------------------------------------------------------------------

step2 bulid
docker build -t rstudioImage . 
    : rstudioImage는 이미지 명

step3 container 생성 및 실행
docker run -e PASSWORD=rstudio -p 8787:8787 --name rstudioContainer rstudioImage 
    : -e도 conntainer를 생성
    : password 변경 가능
 
step4 방화벽 개방 
firewall-cmd --zone=public --permanent --add-port=8787/tcp  
systemctl restart firewalld.service

step5 ip:8787로 접속
username : rstudio
password : rstudio
    : gapminder 설치 확인

** 이미 설치되어 경우
sudo systemctl start docker
sudo systemctl enable docker

docker ps
start가 안되어 있는 경우
docker start rstudioContainer 
docker exec rstudioContainer /init
'''