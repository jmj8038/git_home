'''
참고 tutorial : https://ko.hortonworks.com/tutorial/sandbox-deployment-and-install-guide/section/3/
step1. Docker용 Hortonworks Data Platform(HDP) 최신 스크립트를 다운로드하고 zip 파일을 압축 해제
https://ko.hortonworks.com/downloads/#sandbox

wget을 이용하거나 filezira 활용가능
root 하위디렉토리에 설치
unzip을 위하여 unzip 설치
    yum install unzip -y(apt-get install unzip)

cd /path/to/script <- 이 명령어는 안 먹혔음
sh docker-deploy-{HDPversion}.sh   
    예시> sh docker-deploy-hdp30.sh
'''
