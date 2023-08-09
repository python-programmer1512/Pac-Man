# Pac-Man
<div align="center">
  <img width="1200" alt="game_playing" src="https://github.com/python-programmer1512/Pac-Man/assets/68761453/58886a1e-2b61-4693-8d0d-8ed96ecfa2eb">
</div>  

<div align="center">

  ### Made by Pygame 🐍🎮
  
</div>  

  
## ▶️ 실행 방법



#### 1. pac_man.py 를 직접 실행 

#### 2. pac_man.exe 또는 pac_man_lite.exe 파일을 실행 


## 🕹️ 조작키

기본적으로 w,a,s,d 로 작동하며, 방향키로도 작동한다.


## 🛠 커스텀 맵 제작

####  1. pac_man.py 에서 developer 변수를 1로 설정 
  
####  2. 실행 후 마우스로 맵 변경 가능(실행 시 ghost 가 플레이어를 잡지 못함) 

* ####  왼쪽 클릭 : 벽 생성 , 오른쪽 클릭 : 벽 파괴 

#### 3. 맵 세팅 후 0 버튼(키보드)를 누르면 지금까지 만든 MAP 데이터와 해당 MAP 에 대한 플로이드 와샬 데이터가 출력됨

#### 4. 출력된 값들을 large_dataset.py 파일에 들어가서 해당하는 위치에 복붙(출력을 보면 배열 출력 전, dp, map 이 출력됨)

* #### 출력이 많기 때문에 복붙에 유의해야함(중간에 끊기거나 깨질 경우 제대로 작동하지 않음)

* #### 맵 변경 후 처음에는 로딩 시간이 걸릴 수 있음


## 🕹 아이템 설명 

#### 1. 빨간색 워프 아이템
* 점프 기능이 있는 아이템으로, 스페이스를 누르면 자신이 바라보고 있는 방향으로 점프를 한다. 
* 바로 앞에 벽이 있다면 벽 한칸을 뛰어 넘을 수 있다.(그러나 벽이 2칸이 이어져있으면 넘지 않는다.)
* 바라보고 있는 방향 이외에도 방향키를 누르고 스페이스를 누르면 그 방향으로 점프할 수 있다.  
  

## 🎮 이미 만들어진 파일
#### 만약 화면이 전부다 보이지 않을 경우 화면 배율을 조정하면 볼 수 있음
* [pac_man.zip](https://github.com/python-programmer1512/Pac-Man/blob/main/game_file/pac_man.zip)
* [pac_man_lite.zip](https://github.com/python-programmer1512/Pac-Man/blob/main/game_file/pac_man_lite.zip)

