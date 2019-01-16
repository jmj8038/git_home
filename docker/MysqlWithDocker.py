# Mysql wirh Docker

'''
1. DOCKER 설치
sudo curl -fsSL https://get.docker.com/ | sudo sh
sudo systemctl start docker
sudo systemctl enable docker

2. docker 그룹에 사용자 등록 : docker 명령시 마다 sudo 입력할 필요 없음
sudo usermod -aG docker $(whoami)
sudo reboot

3. 다운로드 가능한 mysql image들 검색
docker search mysql

4. mysql/mysql-server이라는 image 다운로드(pull) : 보통 가장 인기 있는 image를 pull하나 manual에 제시된 image를 pull 하였음
docker pull mysql/mysql-server

5. Mysql container 설치
docker run --detach --env MYSQL_ROOT_PASSWORD="비밀번호 설정" --env MYSQL_DATABASE="생성할 database이름" --name "container이름" --publish 13306:3306 mysql/mysql-server
    : 포트포워딩 => -p 13306:3306 (3306을 사용할 경우에는 굳이 포트포워딩 할 필요없으나 이미 서버에 Mysql이 설치되어 있어 포트포워딩 하였음) 
    : 위와 같이 비밀번호 설정을 하지 않으면 나중에 default로 주는 비밀번호를 주지만 너무 복잡하고 재설정 하여야 함. 
    : 마지막 줄의 mysql/mysql-server은 pull한 image 이름

6. container 시작
docker start container이름(stop, status를 통해 정지, 상태확인 가능)

7. Mysql 접속		
docker exec -it container이름 mysql -uroot -p
    : 접속시 mysql 비밀번호 입력

8. Mysql 권한설정(?)
CREATE USER 'root'@'%' IDENTIFIED BY '비밀번호'; 
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
    : 8버젼(?) 부터는 GRANT 만으로 안되고 위와 실행
    : 어디 ip 주소로 접속하여도 접속 가능

9. 5에서 설정한 포트에 대해 방화벽을 열어줌
sudo firewall-cmd --zone=public --permanent --add-port=13306/tcp
sudo firewall-cmd --zone=public --permanent --add-port=3306/tcp 
sudo systemctl restart firewalld.service
sudo iptables -L

10. Python을 활용한 Mysql 접속 및 CRUD
pip install pymysql (Window cmd)

'''
# 예제 코드
import pymysql
connect = pymysql.connect(host = '192.168.103.103',   
		port = 13306,
		user = 'root',
		password = 'root12345',
		db = 'test',
		charset = 'utf8mb4') #utf8 로 실행시 utf8mb4를 권장하는 warning 발생
cursor = connect.cursor()


sql = "CREATE TABLE customer(\
	id CHAR(10) NOT NULL PRIMARY KEY,\
	name VARCHAR(20) NOT NULL,\
	age INT(3),\
	address VARCHAR(40))"
	
cursor.execute(sql)
cursor.execute("SHOW TABLES")
cursor.fetchall()
cursor.execute("EXPLAIN customer")
result = cursor.fetchall()
for item in result:
	print(item)

id1 = ['hong','홍길동',22,'경기']
id2 = ['dang','당탕이',23,'충북']
id3 = ['ppuni','이뿌니',30,'서울']
id4 = ['john','존밴이',28,'강원']
ids = [id1, id2, id3, id4]

for id in ids:
	i = id[0]
	n = id[1]
	a = id[2]
	ad = id[3]
	sql = "INSERT INTO customer VALUES(\
			'{}', '{}', {}, '{}')".format(i,n,a,ad)
	cursor.execute(sql)
cursor.execute("SELECT * FROM customer")
result = cursor.fetchall()
for item in result:
	print(item)

answer = input("저장할까요? ")
if answer in ["yes", "y"]:
	cursor.execute("commit")
else:
	cursor.execute("rollback")

cursor.execute("commit")

'''
11. docker hub에 commit 및 push
docker commit -p container이름 jmj/mysql1:0.1 
    : container를 잠시 멈춰 저장하고(-p) jmj/mysql1:0.1이라는 이미지로 commit(jmj은 docker hub 아이디로 보통 붙여서 사용한다)
docker login
    : docker hub에 가입되어 있어야 하고 위의 명령문을 통해 로그인 한다.
docker push jmj/mysql1:0.1
    : docker hub에 push 한다.

12. docker hub에서 pull
docker rmㅑ jmj/mysql1:0.1
    : commit 시 해당 동일 이름의 이미지가 생성되어 있으므로 동일 머신에서 pull 할때는 기존의 image를 삭제한다.
docker pull jmj/mysql1:0.1

참고링크
https://subicura.com/2017/02/10/docker-guide-for-beginners-create-image-and-deploy.html
https://cache798.blog.me/221055737192
http://gyus.me/?p=546
https://tech.osci.kr/docker/2018/09/10/45749387/
'''