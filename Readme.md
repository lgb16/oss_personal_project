# This is Readme file

# Reference
[1] https://github.com/pygame/pygame "pygame"

#지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :x:  |
| Linux  | :o: |
|MacOS  | :x:  |

#실행 방법
### Linux

1. python3을 설치한다
2. game.py 파일에 권한을 준다 ( $:chmod 755 game.py )
3. game.py 파일을 python3를 통해 실행한다 ( $:python3 game.py )

#코드 설명
### datafile.py
- 게임 실행에 필요한 여러 전역 변수 및 클래스를 선언해둔 파일
- Spritesheet : spritesheet를 받아 여러 image로 나누어 저장하는 class
	+Def __init__ : SpriteSheet 초기화, spr에 이미지를 나누어 저장, 처음에는 spr 리스트는 비어있음
	+Def get image : 주어진 좌표에 크기, 배율에 따라 spritesheet에서 이미지를 추출에 spr리스트에 저장
- Flame, Player, Enemy : 각각 플레이어의 공격, 플레이어, 적 몬스터를 담당하는 class, pygame.sprite.Sprite를 상속함
	+Def __init__ : image를 불러와 초기화 및 주어진 좌표와 방향값으로 초기화
	+Def update : image의 위치와 애니메이션을 시간에 따라 업데이트 하기 위한 함수

### game.py
- 게임이 실행되는 파일
- start game : 게임이 실행될시 수행하는 함수, 여러 클래스들의 생성 및 소멸, 점수 계산, 업데이트를 진행
- while문 : 게임이 실제로 작동되는 부분, spacebar를 누를시 위 start game 함수가 실행됨
