# MongoDB wirh Docker

'''
1. DOCKER 설치
sudo curl -fsSL https://get.docker.com/ | sudo sh
sudo systemctl start docker
sudo systemctl enable docker

2. docker 그룹에 사용자 등록 : docker 명령시 마다 sudo 입력할 필요 없음
sudo usermod -aG docker $(whoami)
sudo reboot

3. 다운로드 가능한 mongp image들 검색
docker search mongo

4. mongo라는 image 다운로드(pull) : pull을 가장 많이 한 image를 pull
docker pull mongo

    * mongoDB를 docker에서 사용시 server와 client container를 각자 만들고 link하여 client container 를 통해 server 접속
    * python을 이용하여 외부에서 접속시에는 바로 server를 통해 접속을 한다. 다만, 내부에서 CRUD시에는 client를 통해 실행

5. mongo server 설치
docker run --name container이름 -d -v /data:/data/db -p 27017:27017 mongo --noauth --bind_ip=0.0.0.0 
    : 몽고 데몬은 기본적으로 /data/db 폴더에 데이터를 기록한다. 호스트의 /data 폴더를 컨테이너의 /data/db 폴더에 마운트한다. 
        결과적으로 호스트의 /data 폴더에 몽고디비 데이터가 저장
	: 외부접속시 27017 포트로 포트포워딩
	: mongo는 image 이름이고 noauth는 계정업이 접속 가능 
	: bind_ip=0.0.0.0는 아무 ip 주소로 접속 가능


6. mongo client 설치
docker run -itd --name container이름(client) -p 37017:27017 --link container이름(server):mongo mongo /bin/bash
	: container이름(server):별칭(mongo) 와 연결(link)
	: mongo 라는 이미지로 bash shell로 작동
    : 클라이언트에서 서버로 접속하는 것이므로 클라이언트를 포트포워딩(-p 37017:27017)
        다만, 외부접속시 바로 server로 접속하므로 client에서 포트포워딩은 필요 없은 것 같음

7. mongo client	container 실행
ㅇocker attach mongo1-client -> Enter (Enter키를 꼭 클릭)

8. (옵션) mongoDB 정상 여부 확인 (client container 상에서 실행)
cd bin
env
echo $MONGO_PORT_27017_TCP_ADDR
    : docker 내부에서 server로 접속하기 위해 할당 받은 IP 주소
echo $MONGO_PORT_27017_TCP_PORT
    : docker 내부에서 server로 접속하기 위해 할당 받은 PORT

9. mongoDB 접속 
mongo $MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT
    : 8단계에서 입력 후 확인 받은 주소 및 PORT를 집적 입력 가능
docker exec -it container이름 mysql -uroot -p
    : 접속시 mysql 비밀번호 입력

10. 방화벽 개방
sudo firewall-cmd --zone=public --permanent --add-port=27017/tcp
sudo firewall-cmd --zone=public --permanent --add-port=37017/tcp 
sudo systemctl restart firewalld.service
sudo iptables -L

11. Python을 활용한 mongoDB 접속 및 CRUD
python -m pip install pymongo (Window cmd)
'''
# 예제코드
import pymongo
myclient = pymongo.MongoClient("mongodb://192.168.103.103:27017/")
mydb = myclient["mydatabase"] # database 생성
mycol = mydb["customers"] # table 생성
# 한개 data 입력
mydict = { "name": "John", "address": "Highway 37" } 
mycol.insert_one(mydict) 
# 여러개 data 입력
mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]
mycol.insert_many(mylist) 
# 한개 data 출력
x = mycol.find_one()
print(x)
# 모든 data 출력
for y in mycol.find():
    print(y)
