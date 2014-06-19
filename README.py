B0129042
========

期末project


import random, sys, time, math, pygame
from pygame.locals import *

畫面更新率 = 30 
視窗寬度 = 640 
視窗高度= 480 
半個視窗寬度 = int(視窗寬度/ 2)
半個視窗高度 = int(視窗高度 / 2)

草地顏色 = (24, 255, 0) #  RGB 調色盤表示法的綠色
白色 = (255, 255, 255) # 表示白色
紅色 = (255, 0, 0) # 表示紅色

中心與松鼠距離 = 0    
松鼠移動速度 = 9       # 玩家移動速度
松鼠跳躍頻率 = 6       # 松鼠跳躍的頻率
松鼠跳躍高度 = 30      # 松鼠跳躍的高度
玩家松鼠起始大小 = 25   # 玩家一開始的大小
成為鼠王的大小 = 300   # 勝利條件(長多大)
受傷時的無敵時間 = 2    # 和比自己大隻的松鼠碰撞時的無敵時間(避免瞬間重複傷害,造成遊戲瞬間結束)
遊戲結束字樣停留秒數 = 4  # "遊戲結束"字樣停留在螢幕的時間(秒數)
玩家起始生命值 = 3        # 一開始玩家有多少點生命值

草叢數量 = 80        # 在活動範圍內的草叢數量
松鼠數量 = 30    # 在活動範圍內的松鼠數量
松鼠速度最低值 = 3 # 松鼠速度最低值
松鼠速度最高值 = 7 # 松鼠速度最高值
轉方向頻率 = 2    # % 每個畫格的轉向次數
左 = 'left'
右 = 'right'


遊戲楨數鐘 = pygame.time.Clock
啟動= pygame.init
影像下載1= pygame.image.load
幕設標題= pygame.display.set_caption
幕設大小= pygame.display.set_mode
圖標=pygame.display.set_icon
字型類=pygame.font.Font
隨機=random.randint
松鼠大小=pygame.transform.scale
設框大小=pygame.Rect
事件取得= pygame.event.get
時間函式=time.time
遊戲面板更新=pygame.display.update
塗框框顏色=pygame.draw.rect
系統結束=sys.exit
離開遊戲=pygame.quit


def main():
    global 楨數鐘, 幕設大小, 字形類, 松鼠影像1, 松鼠影像2, 草叢影像

    啟動()
    楨數鐘 = 遊戲楨數鐘()
    圖標(影像下載1('gameicon.png'))
    幕設大小 = 幕設大小((視窗寬度, 視窗高度))
    幕設標題('Squirrel Eat Squirrel')
    字形類 = 字型類('freesansbold.ttf', 32)
     
    # 載入圖檔
    松鼠影像1 = 影像下載1('squirrel.png')
    松鼠影像2 = pygame.transform.flip(松鼠影像1, True, False)
    草叢影像 = []
    for i in range(1, 5):
        草叢影像.append(影像下載1('grass%s.png' % i))

    while True:
        runGame()


def runGame():
    # 設定遊戲
    無敵模式 = False  # 玩家無敵時
    無敵時間 = 0 # 變成無敵的時間
    遊戲結束模式 = False      # 玩家輸了
    遊戲結束開始時間 = 0     # 玩家死去的時間
    勝利模式 = False           # 玩家贏了

    # 創造遊戲字幕
    遊戲結束字幕 = 字形類.render('game over', True, 白色)
    遊戲結束框 = 遊戲結束字幕.get_rect()
    遊戲結束框.center = (半個視窗寬度, 半個視窗高度)

    遊戲勝利字幕 = 字形類.render('WIN!', True, 白色)
    遊戲勝利框 = 遊戲勝利字幕.get_rect()
    遊戲勝利框.center = (半個視窗寬度, 半個視窗高度)

    遊戲勝利字幕2 = 字形類.render('(press"r"to restart)', True, 白色)
    遊戲勝利框2 = 遊戲勝利字幕2.get_rect()
    遊戲勝利框2.center = (半個視窗寬度, 半個視窗高度 + 30)

    # camerax cameray :camera視野的左上
    camerax = 0
    cameray = 0

    草叢 = []    # 儲存草叢物件
    松鼠 = [] # 儲存非玩家松鼠物件
    # 儲存玩家的物件:
    玩家松鼠 = {'surface': 松鼠大小(松鼠影像1, (玩家松鼠起始大小, 玩家松鼠起始大小)),
                 'facing': 左,
                 'size': 玩家松鼠起始大小,
                 'x': 半個視窗寬度,
                 'y': 半個視窗高度,
                 'bounce':0,
                 'health': 玩家起始生命值}

    左移 = False
    右移 = False
    上移 = False
    下移 = False

    # 在螢幕增加隨機的草叢
    for i in range(10):
        草叢.append(製造草叢(camerax, cameray))
        草叢[i]['x'] = 隨機(0, 視窗寬度)
        草叢[i]['y'] = 隨機(0, 視窗高度)

    while True: # 主要程式迴圈
        # 檢查是否該解除無敵
        if 無敵模式 and 時間函式() - 無敵時間 > 受傷時的無敵時間:
            無敵模式 = False

        # 讓所有松鼠移動
        for 松鼠物件 in 松鼠:
            # 移動松鼠, 並調整他們的跳躍
            松鼠物件['x'] += 松鼠物件['movex']
            松鼠物件['y'] += 松鼠物件['movey']
            松鼠物件['bounce'] += 1
            if 松鼠物件['bounce'] > 松鼠物件['bouncerate']:
                松鼠物件['bounce'] = 0 # 重設彈跳

            # 隨機轉方向
            if 隨機(0, 99) < 轉方向頻率:
                松鼠物件['movex'] = 隨機速度()
                松鼠物件['movey'] = 隨機速度()
                if 松鼠物件['movex'] > 0: # 面向右
                    松鼠物件['surface'] = 松鼠大小(松鼠影像2, (松鼠物件['width'], 松鼠物件['height']))
                else: # 面向左
                    松鼠物件['surface'] = 松鼠大小(松鼠影像1, (松鼠物件['width'], 松鼠物件['height']))


        # 刪除掉該被刪除的物件
        for i in range(len(草叢) - 1, -1, -1):
            if 超過活動區域(camerax, cameray, 草叢[i]):
                del 草叢[i]
        for i in range(len(松鼠) - 1, -1, -1):
            if 超過活動區域(camerax, cameray, 松鼠[i]):
                del 松鼠[i]

        # 當松鼠和草叢數量不夠時,增加些松鼠和草叢
        while len(草叢) < 草叢數量:
            草叢.append(製造草叢(camerax, cameray))
        while len(松鼠) < 松鼠數量:
            松鼠.append(產生新的松鼠(camerax, cameray))

        # 調整camera
        玩家中央水平座標 = 玩家松鼠['x'] + int(玩家松鼠['size'] / 2)
        玩家中央垂直座標 = 玩家松鼠['y'] + int(玩家松鼠['size'] / 2)
        if (camerax + 半個視窗寬度) - 玩家中央水平座標 > 中心與松鼠距離:
            camerax = 玩家中央水平座標 + 中心與松鼠距離 - 半個視窗寬度
        elif 玩家中央水平座標 - (camerax + 半個視窗寬度) > 中心與松鼠距離:
            camerax = 玩家中央水平座標 - 中心與松鼠距離 - 半個視窗寬度
        if (cameray + 半個視窗高度) - 玩家中央垂直座標 > 中心與松鼠距離:
            cameray = 玩家中央垂直座標 + 中心與松鼠距離 - 半個視窗高度
        elif 玩家中央垂直座標 - (cameray + 半個視窗高度) > 中心與松鼠距離:
            cameray = 玩家中央垂直座標 - 中心與松鼠距離 - 半個視窗高度

        # 幫背景草地著上綠色
        幕設大小.fill(草地顏色)

        # 產生草叢
        for 草物件 in 草叢:
            gRect = 設框大小( (草物件['x'] - camerax,
                                  草物件['y'] - cameray,
                                  草物件['width'],
                                  草物件['height']) )
            幕設大小.blit(草叢影像[草物件['grassImage']], gRect)


        # 產生松鼠
        for 松鼠物件 in 松鼠:
            松鼠物件['rect'] = 設框大小( (松鼠物件['x'] - camerax,
                                         松鼠物件['y'] - cameray - 得到跳躍值(松鼠物件['bounce'], 松鼠物件['bouncerate'], 松鼠物件['bounceheight']),
                                         松鼠物件['width'],
                                         松鼠物件['height']) )
            幕設大小.blit(松鼠物件['surface'], 松鼠物件['rect'])


        # 產生玩家的松鼠
        松鼠閃動 = round(時間函式(), 1) * 10 % 2 == 1
        if not 遊戲結束模式 and not (無敵模式 and 松鼠閃動):
            玩家松鼠['rect'] = 設框大小( (玩家松鼠['x'] - camerax,
                                             玩家松鼠['y'] - cameray - 得到跳躍值(玩家松鼠['bounce'], 松鼠跳躍頻率, 松鼠跳躍高度),
                                              玩家松鼠['size'],
                                              玩家松鼠['size']) )
            幕設大小.blit(玩家松鼠['surface'], 玩家松鼠['rect'])


        # 產生血條
        畫血條(玩家松鼠['health'])

        for event in 事件取得(): # 處理事件迴圈
            if event.type == QUIT:
                終止()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    下移 = False
                    上移 = True
                elif event.key in (K_DOWN, K_s):
                    上移 = False
                    下移 = True
                elif event.key in (K_LEFT, K_a):
                    右移 = False
                    左移 = True
                    if 玩家松鼠['facing'] != 左: # 向左走的松鼠圖
                        玩家松鼠['surface'] = 松鼠大小(松鼠影像1, (玩家松鼠['size'], 玩家松鼠['size']))
                    玩家松鼠['facing'] = 左
                elif event.key in (K_RIGHT, K_d):
                    左移 = False
                    右移 = True
                    if 玩家松鼠['facing'] != 右: # 向右走的松鼠圖
                        玩家松鼠['surface'] = 松鼠大小(松鼠影像2, (玩家松鼠['size'], 玩家松鼠['size']))
                    玩家松鼠['facing'] = 右
                elif 勝利模式 and 事件.key == K_r:
                    return

            elif event.type == KEYUP:
                # 玩家松鼠停止
                if event.key in (K_LEFT, K_a):
                    左移 = False
                elif event.key in (K_RIGHT, K_d):
                    右移 = False
                elif event.key in (K_UP, K_w):
                    上移 = False
                elif event.key in (K_DOWN, K_s):
                    下移 = False

                elif event.key == K_ESCAPE:
                    終止()

        if not 遊戲結束模式:
            # 玩家松鼠移動
            if 左移:
                玩家松鼠['x'] -= 松鼠移動速度
            if 右移:
                玩家松鼠['x'] += 松鼠移動速度
            if 上移:
                玩家松鼠['y'] -= 松鼠移動速度
            if 下移:
                玩家松鼠['y'] += 松鼠移動速度

            if (左移 or 右移 or 上移 or 下移) or 玩家松鼠['bounce'] != 0:
                玩家松鼠['bounce'] += 1

            if 玩家松鼠['bounce'] > 松鼠跳躍頻率:
                玩家松鼠['bounce'] = 0 # 重設彈跳

            # 檢查玩家松鼠是否碰撞其他松鼠
            for i in range(len(松鼠)-1, -1, -1):
                野松鼠 = 松鼠[i]
                if 'rect' in 野松鼠 and 玩家松鼠['rect'].colliderect(野松鼠['rect']):
                    # 碰撞發生

                    if 野松鼠['width'] * 野松鼠['height'] <= 玩家松鼠['size']**2:
                        # 玩家松鼠較大並吃掉小松鼠
                        玩家松鼠['size'] += int( (野松鼠['width'] * 野松鼠['height'])**0.2 ) + 1
                        del 松鼠[i]

                        if 玩家松鼠['facing'] == 左:
                            玩家松鼠['surface'] = 松鼠大小(松鼠影像1, (玩家松鼠['size'], 玩家松鼠['size']))
                        if 玩家松鼠['facing'] == 右:
                            玩家松鼠['surface'] = 松鼠大小(松鼠影像2, (玩家松鼠['size'], 玩家松鼠['size']))

                        if 玩家松鼠['size'] > 成為鼠王的大小:
                            勝利模式 = True #  "勝利模式"

                    elif not 無敵模式:
                        # 玩家松鼠較小並受到傷害
                        無敵模式 = True
                        無敵時間 = 時間函式()
                        玩家松鼠['health'] -= 1
                        if 玩家松鼠['health'] == 0:
                            遊戲結束模式 = True #  "遊戲結束模式"
                            遊戲結束開始時間 = 時間函式()
        else:
            # 遊戲結束,game over字樣
            幕設大小.blit(遊戲結束字幕, 遊戲結束框)
            if 時間函式() - 遊戲結束開始時間 > 遊戲結束字樣停留秒數:
                return # 結束當前遊戲

        # 檢查玩家是否勝利
        if 勝利模式:
            幕設大小.blit(遊戲勝利字幕, 遊戲勝利框)
            幕設大小.blit(遊戲勝利字幕2, 遊戲勝利框2)

        遊戲面板更新()
        楨數鐘.tick(畫面更新率)




def 畫血條(當前血條):
    for i in range(當前血條): # 幫血條畫上紅色
        塗框框顏色(幕設大小, 紅色,   (15, 5 + (10 * 玩家起始生命值) - i * 10, 20, 10))
    for i in range(玩家起始生命值): # 幫扣血的格子畫上白色
        塗框框顏色(幕設大小, 白色, (15, 5 + (10 * 玩家起始生命值) - i * 10, 20, 10), 1)


def 終止():
    離開遊戲()
    系統結束()


def 得到跳躍值(當前跳躍, 松鼠跳躍頻率, 松鼠跳躍高度):



    
    return int(math.sin( (math.pi / float(松鼠跳躍頻率)) * 當前跳躍 ) * 松鼠跳躍高度)

def 隨機速度():
    速度 = 隨機(松鼠速度最低值, 松鼠速度最高值)
    if 隨機(0, 1) == 0:
        return 速度
    else:
        return -速度


def 得鏡頭隨機位置(camerax, cameray, objWidth, objHeight):
    
    相框 = 設框大小(camerax, cameray, 視窗寬度, 視窗高度)
    while True:
        x = 隨機(camerax - 視窗寬度, camerax + (2 * 視窗寬度))
        y = 隨機(cameray - 視窗高度, cameray + (2 * 視窗高度))

      
        物件框框 = 設框大小(x, y, objWidth, objHeight)
        if not 物件框框.colliderect(相框):
            return x, y


def 產生新的松鼠(camerax, cameray):
    松鼠們 = {}
    起始尺寸 = 隨機(5, 25)
    倍數 = 隨機(1, 3)
    松鼠們['width']  = (起始尺寸 + 隨機(0, 10)) * 倍數
    松鼠們['height'] = (起始尺寸 + 隨機(0, 10)) * 倍數
    松鼠們['x'], 松鼠們['y'] = 得鏡頭隨機位置(camerax, cameray, 松鼠們['width'], 松鼠們['height'])
    松鼠們['movex'] = 隨機速度()
    松鼠們['movey'] = 隨機速度()
    if 松鼠們['movex'] < 0: # 松鼠向左看
        松鼠們['surface'] = 松鼠大小(松鼠影像1, (松鼠們['width'], 松鼠們['height']))
    else: # 松鼠右要看
        松鼠們['surface'] = 松鼠大小(松鼠影像2, (松鼠們['width'], 松鼠們['height']))
    松鼠們['bounce'] = 0
    松鼠們['bouncerate'] = 隨機(10, 18)
    松鼠們['bounceheight'] = 隨機(10, 50)
    return 松鼠們


def 製造草叢(camerax, cameray):
    草叢們 = {}
    草叢們['grassImage'] = 隨機(0, len(草叢影像) - 1)
    草叢們['width']  = 草叢影像[0].get_width()
    草叢們['height'] = 草叢影像[0].get_height()
    草叢們['x'], 草叢們['y'] = 得鏡頭隨機位置(camerax, cameray, 草叢們['width'], 草叢們['height'])
    草叢們['rect'] = 設框大小( (草叢們['x'], 草叢們['y'], 草叢們['width'], 草叢們['height']) )
    return 草叢們


def 超過活動區域(camerax, cameray, obj):
    
    跳躍左邊邊界 = camerax - 視窗寬度
    跳躍上邊邊界 = cameray - 視窗高度
    跳躍框 = 設框大小(跳躍左邊邊界, 跳躍上邊邊界, 視窗寬度 * 3, 視窗高度 * 3)
    物件框框 = 設框大小(obj['x'], obj['y'], obj['width'], obj['height'])
    return not 跳躍框.colliderect(物件框框)


if __name__ == '__main__':
    main()
