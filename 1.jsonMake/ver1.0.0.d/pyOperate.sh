#!/bin/bash
# 그냥 귀찮아서 만듬

# 3 param.
# 이부분 관련해서 크롤링이 잘 될 수 있도록 . 명령어 구조도 생각해보자
# 우선 한번에 다 짜놓고, 나중에 상황에 따라서 구별해서 작동할 수 있도록!
# 즉 쉘로 커맨드로 작동시킬건지 아니면 그냥 모듈로 나누어서 작동할 수 있도록 할건지를 생각합시다!



echo "시작합니다........."
echo " d = Text Delete 
	   lottedotcom Crawl Operate.
"
if [ $1 = "d" ];
then
	echo " Text File 을 삭제합니다."
	rm ./*.txt
fi

if [ $1 = "dj" ];
then
	echo "Json File 을 삭제합니다."
	rm ./*.json
fi

if [ $1 = "a" ];
then
	echo "Make All crawl data.."
	for tc in {0..4}
		do
			echo "Make $tc th lottedotcom crawling..."
			python lottedotcom_All_$tc.py
		done
fi

if [ $1 = "hyu" ];
then
	python hyundai_crawling.py
fi

if [ $1 = "dot" ];
then
	python lottedotcom_crawling.py
fi



echo "끝났습니다..."
