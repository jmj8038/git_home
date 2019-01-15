'''
AWS EC2 ubuntu에서 R, Rstudio, Rstudio-server 설치 및 설정
    참고 url : https://cran.rstudio.com/bin/linux/ubuntu/README.html (UBUNTU PACKAGES FOR R)
              ** https://docs.rstudio.com/ide/server-pro/index.html#debian-8-ubuntu-12.04 (RStudio Server Professional Edition)
1.R 설치
    1. 간단한 방법
        $sudo apt-get install r-base
        : apt-get 미설치시 먼저 설치 
            $yum install -y apt
    2. 복잡하지만 보다 정확한 방법
        : 간단한 방법에 따를 경우 최신버젼이 설치되지 않을 수 있음.
        : CRAN repository를 먼저 지정하여 설치 
        1.1 case1 - vim 활용
            $vim /etc/apt/source.list.d/r.list
            ---------------------------------------------------
            deb
            http://cran.stat.ucla.edu/bin/linux/ubuntu trusty/
            -------------------------------------------------- 
        
        1.2 case2 - echo 활용
            $echo "deb http://cran.cnr.Berkeley.edu/bin/linux/ubuntu `lsb_release -sc`/" | sudo tee --append /etc/apt/sources.list.d/cran.list 

        1.3 공식 다큐먼트 참고
            https://cran.rstudio.com/bin/linux/ubuntu/README.html 
            : 1.1을 응용하여 적용

        2. 설치
            $sudo apt-get update 
            $sudo apt-get install r-base

        3. 설정
            : 설치 완성을 위해 다음 명령어 실행
            : rstudio 및 rstudio-server 설치하는 것으로 판단 됨
                $sudo apt-get install gdebi-core
                $sudo gdebi <rstudio-server-package.deb>
                    : gdebi 미설치시 $yum install -y gdebi
                    : <rstudio-server-package.deb> 
                        r-studio server download에서 최신버젼 확인 필요 (https://www.rstudio.com/products/rstudio/download/#download)
                        예시) $sudo gdebi rstudio-server-1.1.463-amd64.deb

        4. key 받기 
            : 공식 문서 내용 
                RStudio Server Pro binary is signed with a key belonging to RStudio, Inc.
                필수는 아닌 것으로 판단되나 절차는 다음과 같음
            $sudo gpg --keyserver keys.gnupg.net --recv-keys 3F32EE77E331692F
                : 3F32EE77E331692F 이 부분은 수동으로 입력해야 하는 부분으로 판단됨 공식 문서에서 위와 같이 제시
                : (my case) 
                    $sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 
                        참고 url : https://m.blog.naver.com/PostView.nhn?blogId=jjy0501&logNo=221042352311&proxyReferer=https%3A%2F%2Fwww.google.com%2F
                : 일부 블로그에는 위의 과정이 생략되어 있거나  error 발생시 설정하도록 함
                    참고 url : http://ngee.tistory.com/294
        5. 승인
            : 공식 문서 내용
                Once you have obtained the key, you can validate the .deb file as follows
            $sudo dpkg-sig --verify <rstudio-server-package.deb>
                예시) dpkg-sig --verify rstudio-server-1.1.463-amd64.deb 
                : 특정 번호를 부여 받음 (E331692F)

        6. 위의 과정을 통해 R 설치 완료
            다만, 공식 문서에 의하면 위 과정 후 
            rstudio-server start 명령어르 제시 한 것으로 보아 rstudio 및 rstudio-server도 설치되는 것으로 판단
            rstudio 및 rstudio-server 설치에 관한 내용도 있으나 위 과정 중 
            '3'의 설정 부분과 같음(추가 과정이 있기는 함)

        7. rstudio 및 rstudio-server
            참고 url : https://www.rstudio.com/products/rstudio/download-server/
                $sudo apt-get install gdebi-core
                ($sudo apt-get install libapparmor1) # Required only for Ubuntu, not Debian
                $wget https://download2.rstudio.org/rstudio-server-1.1.463-amd64.deb
                $sudo gdebi rstudio-server-1.1.463-amd64.deb
        8. rstudio-server 접속
            1. 일반적인 경우 : https://리눅스_서버_ip_주소:8787
            2. ec2 : http://public DNS:8787
                예시) http://ec2-54-180-162-14.ap-northeast-2.compute.amazonaws.com:8787
        9. 기타 사항
            1. 에러 발생
                apt-get 설치시 아래와 같은 에러메시지가 발생할 경우 처리
                참고 url : http://www.beexury.com/apt-get-install-%ED%8C%A8%ED%82%A4%EC%A7%80-%EC%84%A4%EC%B9%98%EC%8B%9C-the-following-packages-have-unmet-dependencies-%EC%97%90%EB%9F%AC-%EB%B0%9C%EC%83%9D%EC%8B%9C/
                ------------------------------------------------------------------------------------------------------
                에러 메시지
                The following packages have unmet dependencies:
                letsencrypt : Depends: certbot but it is not going to be installed
                linux-headers-4.4.0-92-generic : Depends: linux-headers-4.4.0-92 but it is not going to be installed
                E: Unmet dependencies. Try ‘apt-get -f install’ with no packages (or specify a solution).
                ------------------------------------------------------------------------------------------------------
                해결 명령어
                $sudo apt-get install -f
            2. ubuntu 설치 package 확인
                $sudo dpkg -l
                $sudo dpkg -l | grep mysql (특정 package 검색)
            3. user id 및 pw 설정
                
            












'''