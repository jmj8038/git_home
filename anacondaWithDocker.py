'''
1. continuumio/anaconda3

2. docker search anaconda3
3. docker pull continuumio/anaconda3
4. docker run -it -d --name jupyterNotebook -p 8888:8888 -v $(pwd):/notebooks continuumio/anaconda3 /bin/bash 
    - $(pwd)자리에 별도의 디렉터리를 쓸 수 있음
5. docker attach jupyterNotebook

---------------------------------------------------------------------------------------
    방화벽 개방 
    firewall-cmd --zone=public --permanent --add-port=8888/tcp  
    systemctl restart firewalld.service
--------------------------------------------------------------------------------------

6. jupyter notebook --ip='*' --port=8888 --no-browser --allow-root
    -> 화면에 보이는 url을 브라우저에 입력

http://(2ba3844c4800 or 127.0.0.1):8888/?token=ccafdb577f2d3f6b1d4f69cb830afb4129da45a6dadcec6d

** 이미 설치되어 경우
sudo systemctl start docker
sudo systemctl enable docker



docker ps
start가 안되어 있는 경우
docker start jupyterNotebook 
docker attach jupyterNotebook
jupyter notebook --ip='*' --port=8888 --no-browser --allow-root
'''


#docker run -it -d --name jupyterNotebook -p 8888:8888 -v $(pwd):/ec2-54-180-162-14.ap-northeast-2.compute.amazonaws.com continuumio/anaconda3 /bin/bash