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
docker build -t rstudioimage . 
    : rstudioImage는 이미지 명
-----------------------------------------------------------------------------------------------------
출력결과
Sending build context to Docker daemon  414.2MB
Step 1/3 : FROM rocker/verse:latest
 ---> ca3c5d105cb2
Step 2/3 : RUN wget https://cran.r-project.org/src/contrib/gapminder_0.3.0.tar.gz
 ---> Using cache
 ---> d926649a109b
Step 3/3 : RUN R CMD INSTALL gapminder_0.3.0.tar.gz
 ---> Using cache
 ---> 2b6f0ce60434
Successfully built 2b6f0ce60434
Successfully tagged rstudioimage:latest
-----------------------------------------------------------------------------------------------------

step3 container 생성 및 실행
docker run -e PASSWORD=rstudio12345 -p 8787:8787 -v /home/encore/rstudioStorage/data:/home/rstudio/rstudioStorage --name rstudioContainer rstudioimage 
    : -e도 conntainer를 생성
    : password 변경 가능

----------------------------------------------------------------------------------------------------
출력결과
[s6-init] making user provided files available at /var/run/s6/etc...exited 0.
[s6-init] ensuring user provided files have correct perms...exited 0.
[fix-attrs.d] applying ownership & permissions fixes...
[fix-attrs.d] done.
[cont-init.d] executing container initialization scripts...
[cont-init.d] add: executing...
Nothing additional to add
[cont-init.d] add: exited 0.
[cont-init.d] userconf: executing...
[cont-init.d] userconf: exited 0.
[cont-init.d] done.
[services.d] starting services
[services.d] done.
^C[cont-finish.d] executing container finish scripts...
[cont-finish.d] done.
[s6-finish] syncing disks.
[s6-finish] sending all processes the TERM signal.
^C[s6-finish] sending all processes the KILL signal and exiting.
------------------------------------------------------------------------------------------------------

step4 방화벽 개방 
firewall-cmd --zone=public --permanent --add-port=8787/tcp  
systemctl restart firewalld.service

step5 ip:8787로 접속
username : rstudio
password : rstudio12345
    : gapminder 설치 확인

** 이미 설치되어 경우
sudo systemctl start docker
sudo systemctl enable docker

docker ps
start가 안되어 있는 경우
docker start rstudioContainer 
docker exec rstudioContainer /init
'''


