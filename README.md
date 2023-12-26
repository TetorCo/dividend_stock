## 프로젝트 소개
당일 배당락이 발생하는 주식 중 가장 많은 배당금을 얻을 수 있는 주식을 조회하는 서비스

### 목표
1. 최대한의 배당금
2. 일주일 전에 목표 주식을 매매한다음 배당락이 발생한 다음 날 매도를 진행해 최소한의 매매차익을 실현하는 것

## 아키텍처
![dividend_stock_archi](https://github.com/TetorCo/dividend_stock/assets/76984534/d5205c4e-a5b6-413e-8ed2-56eefc1cf107)

## 기술 스택
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)


## 성과
- 매일 배당락이 발생하는 주식 중 가장 많은 배당금을 얻을 수 있는 주식을 찾을 수 있음
- PostgreSQL를 데이터 마트처럼 활용해서 배당금 계산과 분석에 필요한 데이터들만 모아서 보관함

## 개선할 점
- 배당금 계산이 단순 배당금 * 주식 수로 이루어지기 때문에 단순히 배당금을 많이 주는 회사가 선택될수 밖에 없고, 이후 매도 시 많은 손해를 볼 수 있음. -> 이전의 배당률 추이를 분석해 안정적인 기업을 선택해야 함