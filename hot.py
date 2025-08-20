import itertools
import random

import CHaser  # 同じディレクトリに CHaser.py がある前提

FLOOR = 0
ENEMY = 1
BLOCK = 2
ITEM = 3
class coordinate:
    #4はわからないこと#左上から数える
    ItemPlace=[[]] #アイテムの位置 2次元目が座標(x,y)自己中心的座標
    Itemway=[]
    coordvalue=[0,0,0,0,0,0,0,0,0]
    a=True#位置がわかったらtrueになる
    d=0
    nearItem=[]#アイテムまでの距離道のり？
    nearItemway=0#一番近いアイテムの座標？
    lastvalue=[
        [0,0]
    ]#何ターン目か、座標(x,y)
    ItemTurn=0 #アイテムを何ターンとってないか
    turn=0
    rightmost=0
    leftmost=0
    upmost=0
    downmost=0
    MaxSizeX=1
    MaxSizeY=1
    map=[[[4]*15 for i in range(17)]]
    PlayerPlace=(1,1)
    #５は行ったことある場所#[[4]*3]*3
    def ready(self,value,d,resetturn,Spawnplace):
        self.coordvalue=value
        if self.coordvalue[0]==3:
            self.ItemPlace.append([-1,-1])
        elif self.coordvalue[1]==3:
            self.ItemPlace.append([0,-1])
        elif self.coordvalue[2]==3:
            self.ItemPlace.append([1,-1])
        elif self.coordvalue[3]==3:
            self.ItemPlace.append([-1,0])
        elif self.coordvalue[5]==3:
            self.ItemPlace.append([1,0])
        elif self.coordvalue[6]==3:
            self.ItemPlace.append([-1,1])
        elif self.coordvalue[7]==3:
            self.ItemPlace.append([0,1])
        elif self.coordvalue[8]==3:
            self.ItemPlace.append([1,1])
        self.lastvalue.append([0,0])
        self.ItemTurn+=1
        
        for row in self.ItemPlace:
    # 各要素をprintする
            for elem in row:
                print(elem, end=" ")
            print()
        
        self.Itemway.clear()

        for i in reversed(range(len(self.ItemPlace))):
            print(i,end=" ")
            if self.ItemPlace[i]==[-1,-1] and self.coordvalue[0]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[0,-1] and self.coordvalue[1]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[1,-1] and self.coordvalue[2]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[-1,0] and self.coordvalue[3]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[1,0] and self.coordvalue[5]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[-1,1] and self.coordvalue[6]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[0,1] and self.coordvalue[7]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[1,1] and self.coordvalue[8]!=3:
                del self.ItemPlace[i]
        
        for i in range(1,len(self.ItemPlace)):
            self.Itemway.append(abs(self.ItemPlace[i][0]) + abs(self.ItemPlace[i][1]))
        self.nearItemway = max(self.Itemway,default=0)#nullにならないようにしている
        if self.nearItemway != 0:
            self.nearItem = self.ItemPlace[self.Itemway.index(self.nearItemway)]#これ頭いい
        #ここにdownmostとかの数字を決めるプログラムを入れる
        '''
        self.MaxSizeX=self.rightmost+self.leftmost+3
        self.MaxSizeY=self.upmost+self.downmost+3
        self.map=[[[4]*self.MaxSizeX for i in range(self.MaxSizeY)]]
        '''
        #print(self.nearItemway)
#インデックスを使って、playerplaceを中心として、itemplaceをいれる
        '''
        for row in self.map:
            for element in row:
                print(element, end=' ')
            print() 
        '''

        if (resetturn %22 == 1 or self.ItemTurn >5) and len(self.nearItem) !=0 :
            preferX=0
            preferY=0
            if self.nearItem[0] > 0:
                preferX=1
            if self.nearItem[1] > 0:
                preferY=1
            if abs(self.nearItem[0]) > abs(self.nearItem[1]):
                if preferX == 1:
                    d[0]=1
                    d[2]=3
                else:
                    d[0]=3
                    d[2]=1
                if preferY == 1:
                    d[1]=4
                    d[3]=2
                else:
                    d[1]=2
                    d[2]=4
            else:
                if preferY == 1:
                    d[0]=4
                    d[2]=2
                else:
                    d[0]=2
                    d[2]=4
                if preferX == 1:
                    d[1]=1
                    d[3]=3
                else:
                    d[1]=3
                    d[3]=1
        
        if self.turn==0:
            if Spawnplace==0:
                self.ItemPlace[0]=[6,7]#spawn1,1
                self.PlayerPlace=[1,1]
            elif Spawnplace==1:
                self.ItemPlace[0]=[0,7]#6,1
                self.PlayerPlace=[6,1]
            elif Spawnplace==2:
                self.ItemPlace[0]=[-6,7]#13,1
                self.PlayerPlace=[13,1]
            elif Spawnplace==3:
                self.ItemPlace[0]=[6,0]#1,8
                self.PlayerPlace=[1,8]
            elif Spawnplace==4:
                self.ItemPlace[0]=[5,5]#null
            elif Spawnplace==5:
                self.ItemPlace[0]=[-6,0]#13,8
                self.PlayerPlace=[13,8]
            elif Spawnplace==6:
                self.ItemPlace[0]=[6,-7]#1,15
                self.PlayerPlace=[1,15]
            elif Spawnplace==7:
                self.ItemPlace[0]=[0,-7]#6,15
                self.PlayerPlace=[6,15]
            elif Spawnplace==8:
                self.ItemPlace[0]=[-6,-7]#13,15
                self.PlayerPlace=[13,15]
            else:
                self.ItemPlace[0]=[5,5]
            self.turn+=1
        
        self.map[self.PlayerPlace[0]][self.PlayerPlace[1]]=5

        #自己中心的マップを神視点マップに入れる
        for i in range(len(self.lastvalue)):
            if self.lastvalue[i][0] + self.PlayerPlace[0] > 14 and self.lastvalue[i][1] + self.PlayerPlace[1] >16 and self.map[self.PlayerPlace[0] + self.lastvalue[i][0]][self.PlayerPlace[1] * self.lastvalue[i][1]] != 2:
                self.map[self.PlayerPlace[0] + self.lastvalue[i][0]][self.PlayerPlace[1] + self.lastvalue[i][1]] = 5

        if (len(self.nearItem)!= 0 and resetturn %12 == 1) or self.ItemTurn > 5:#一旦ランダムにしとくあとでアイテムの方向とかにするといい
            if random.randint(0,1)==1:
                d[0],d[2]=d[2],d[0]
            if random.randint(0,1)==1:
                d[1],d[3]=d[3],d[1]
            if random.randint(0,1):
                d[0],d[1]=d[1],d[0]
                d[2],d[3]=d[3],d[2]
        return d
    def walk(self,walk):#まだ置いてない#右=1 上＝2 左=3 下=4
        #ここにplayerplaceを動かすの書いて、新しいとこに行く時はplayerplaceを調整する
        if self.a:
            print(range(len(self.lastvalue)))
            print(range(len(self.ItemPlace)))
            if walk==1:
                for i in range(len(self.lastvalue)):
                    self.lastvalue[i][0]-=1
                for i in range(len(self.ItemPlace)):
                    self.ItemPlace[i][0]-=1
                self.PlayerPlace[0]-=1
            elif walk==2:
                for i in range(len(self.lastvalue)):
                    self.lastvalue[i][1]+=1
                for i in range(len(self.ItemPlace)):
                    self.ItemPlace[i][1]+=1
                self.PlayerPlace[1]+=1
            elif walk==3:
                for i in range(len(self.lastvalue)):
                    self.lastvalue[i][0]+=1
                for i in range(len(self.ItemPlace)):
                    self.ItemPlace[i][0]+=1
                self.PlayerPlace[0]+=1
            elif walk==4:
                for i in range(len(self.lastvalue)):
                    self.lastvalue[i][1]-=1
                for i in range(len(self.ItemPlace)):
                    self.ItemPlace[i][1]-=1
                self.PlayerPlace[1]-=1
    '''
            for row in self.ItemPlace:
    # 各要素をprintする
                for elem in row:
                    print(elem, end=" ")
                print("in walk")
    '''
    def getitem(self):
        '''
        for i in range(len(self.ItemPlace)):
            if self.ItemPlace[i]==[0,0]:
                del self.ItemPlace[i]
        
        if [0,0] in self.ItemPlace:
            self.ItemPlace.remove()
        '''
        self.ItemPlace=[i for i in self.ItemPlace if i !=[0,0]]
        self.ItemTurn=0

coo=coordinate()
def main(SpawnPlace):#valueの値と同じ4はわからない
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

# ---- コードを書くのは基本的にここから -----

    a=0#1個前の向き
    a2=0#１個前の行動1がwalk,2がlook,3がsearch,4がput
    turn=0
    S_right=0
    S_left=0
    S_up=0
    S_down=0
    d=[3,2,1,4]#右下左上の逆
    resetturn=0
    check=turn#なんだっけ
    search=0
    change=0
    #lookした情報からブロック判断する(敵も)
    #1個前の敵をよける
    def dir(dirr, value,a,right,up,left,down):
        if dirr==0:
            if value[5]==0 and a!=3 and right!=1:
                value=client.walk_right()
                a=1
                a2=1
                coo.walk(1)
        elif dirr==1:
            if value[1]==0 and a!=4 and up!=1:
                value=client.walk_up()
                a=2
                a2=1
                coo.walk(2)
        elif dirr==2:
            if value[3]==0 and a!=1 and left!=1:
                value=client.walk_left()
                a=3
                a2=1
                coo.walk(3)
        elif dirr==3:
            if value[7]==0 and a!=2 and down!=1:
                value=client.walk_down()
                a=4
                a2=1
                coo.walk(4)
        return a
    ddir=[]
    #hotの場合ここをけす
    '''
    value=client.get_ready()
    d=coo.ready(value,d,resetturn)
    resetturn+=1
    turn+=1
    value=client.search_right()
    print("1stturn_search_right")
    '''

    while True:#右=1 上＝2 左=3 下=4
        up=0
        down=0
        left=0
        right=0
        value=client.get_ready()
        d=coo.ready(value,d,resetturn,SpawnPlace)
        resetturn+=1
        turn+=1
        #ここで優先方向に行けなかった時のを変えてる
        '''
        if change==1:
            if a==1:
                d[0]=1
                d[2]=3
                random_int = random.randint(1, 10)
                if random_int<=3:
                    d[1]=2
                    d[3]=4
                elif 4<=random_int<=5:
                    d[0]=2
                    d[1]=1
                    d[2]=4
                    d[3]=3
                elif 6<=random_int<=7:
                    d[0]=4
                    d[1]=1
                    d[2]=2
                    d[3]=3
                else:
                    d[1]=4
                    d[3]=2
            if a==2:
                d[0]=2
                d[2]=4
                random_int = random.randint(1, 10)
                if random_int<=3:
                    d[1]=1
                    d[3]=3
                elif 4<=random_int<=5:
                    d[0]=1
                    d[1]=2
                    d[2]=3
                    d[3]=4
                elif 6<=random_int<=7:
                    d[0]=3
                    d[1]=2
                    d[2]=1
                    d[3]=4
                else:
                    d[1]=3
                    d[3]=1
            if a==3:
                d[0]=3
                d[2]=1
                random_int = random.randint(1, 10)
                if random_int<=3:
                    d[1]=2
                    d[3]=4
                elif 4<=random_int<=5:
                    d[0]=2
                    d[1]=3
                    d[2]=4
                    d[3]=1
                elif 6<=random_int<=7:
                    d[0]=4
                    d[1]=3
                    d[2]=2
                    d[3]=1
                else:
                    d[1]=4
                    d[3]=2
            if a==4:
                d[0]=4
                d[2]=2
                random_int = random.randint(1, 10)
                if random_int<=3:
                    d[1]=1
                    d[3]=3
                elif 4<=random_int<=5:
                    d[0]=1
                    d[1]=4
                    d[2]=3
                    d[3]=2
                elif 6<=random_int<=7:
                    d[0]=3
                    d[1]=4
                    d[2]=1
                    d[3]=2
                else:
                    d[1]=3
                    d[3]=1
            resetturn=-8
        '''
        ##print(turn)
        #斜めに敵がいる時
        if value[0]==1:
            up=1
            left=1
        elif value[2]==1:
            up=1
            right=1
        elif value[6]==1:
            down=1
            left=1
        elif value[8]==1:
            down=1
            right=1
        
        #通常行動条件
        ddir=[(value[5]==0 or value[5]==3) and a!=3 and right!=1 and coo.coordvalue[5]!=5 and coo.lastvalue.count([1,0]) > 1,
            (value[1]==0 or value[1]==3) and a!=4 and up!=1 and coo.coordvalue[1]!=5 and coo.lastvalue.count([0,-1]) > 1,
            (value[3]==0 or value[3]==3) and a!=1 and left!=1 and coo.coordvalue[3]!=5 and coo.lastvalue.count([-1,0]) > 1,
            (value[7]==0 or value[7]==3) and a!=2 and down!=1 and coo.coordvalue[7]!=5 and coo.lastvalue.count([0,1]) > 1]
        ddir2=[(value[5]==0 or value[5]==3) and a!=3 and right!=1 and coo.coordvalue[5]!=5,
            (value[1]==0 or value[1]==3) and a!=4 and up!=1 and coo.coordvalue[1]!=5,
            (value[3]==0 or value[3]==3) and a!=1 and left!=1 and coo.coordvalue[3]!=5,
            (value[7]==0 or value[7]==3) and a!=2 and down!=1 and coo.coordvalue[7]!=5]#改善の余地ありマップシステムできたら変えてもいいかも
        print(ddir)
        #目の前に敵 
        if value[1]==1:
            value=client.put_up()
        elif value[3]==1:
            value=client.put_left()
        elif value[5]==1:
            value=client.put_right()
        elif value[7]==1:
            value=client.put_down()
        #斜め敵
        elif value[0]==1 and (value[3] != 2 or value[5] != 2 or value[7] != 2):
            value=client.put_up()
        elif value[2]==1 and (value[3] != 2 or value[1] != 2 or value[7] != 2):
            value=client.put_right()
        elif value[6]==1 and (value[1] != 2 or value[5] != 2 or value[7] != 2):
            value=client.put_left()
        elif value[8]==1 and (value[3] != 2 or value[5] != 2 or value[1] != 2):
            value=client.put_down()
        #目の前アイテムブロックなし
        elif value[3]==3 and left!=1 and (value[0]!=2 or value[6]!=2):
            value=client.walk_left()
            coo.getitem()
            coo.walk(3)
            a=3
            a2=1
        elif value[1]==3 and up!=1 and (value[0]!=2 or value[2]!=2):
            value=client.walk_up()
            coo.getitem()
            coo.walk(2)
            a=2
            a2=1
        elif value[7]==3 and down!=1 and (value[6]!=2 or value[8]!=2):
            value=client.walk_down()
            coo.getitem()
            coo.walk(4)
            a=4
            a2=1
        elif value[5]==3 and right!=1 and (value[2]!=2 or value[8]!=2):
            value=client.walk_right()
            coo.getitem()
            coo.walk(1)
            a=1
            a2=1
        #トラップ対策
        elif value[3]==3 and left!=1 and value[0]==2 and value[6]==2 and a2!=3:
            value=client.search_left()
            a2=3
            if value[1]!=2 and left!=1:
                value=client.get_ready()
                turn+=1
                value=client.walk_left()
                coo.walk(3)
                coo.getitem()
                a=3
                a2=1
        elif value[1]==3 and up!=1 and value[0]==2 and value[2]==2 and a2!=3:
            value=client.search_up()
            a2=3
            if value[1]!=2 and up!=1:
                value=client.get_ready()
                turn+=1
                value=client.walk_up()
                coo.walk(2)
                coo.getitem()
                a=2
                a2=1
        elif value[7]==3 and down!=1 and value[8]==2 and value[6]==2 and a2!=3:
            value=client.search_down()
            a2=3
            if value[1]!=2 and down!=1:
                value=client.get_ready()
                turn+=1
                value=client.walk_down()
                coo.walk(4)
                coo.getitem()
                a=4
                a2=1
        elif value[5]==3 and right!=1 and value[2]==2 and value[8]==2 and a2!=3:
            value=client.search_right()
            a2=3
            if value[1]!=2 and right!=1:
                value=client.get_ready()
                turn+=1
                value=client.walk_right()
                coo.walk(1)
                coo.getitem()
                a=1
                a2=1
        #斜めアイテム
        elif value[0]==3 and (value[1]!=2 or value[3]!=2):
            if value[1]!=2:
                value=client.walk_up()
                coo.walk(2)
            elif value[3]!=2:
                value=client.walk_left()
                coo.walk(3)
        elif value[2]==3 and (value[1]!=2 or value[5]!=2):
            if value[1]!=2:
                value=client.walk_up()
                coo.walk(2)
            elif value[5]!=2:
                value=client.walk_right()
                coo.walk(1)
        elif value[6]==3 and (value[3]!=2 or value[7]!=2):
            if value[7]!=2:
                value=client.walk_down()
                coo.walk(4)
            elif value[3]!=2:
                value=client.walk_left()
                coo.walk(3)
        elif value[8]==3 and (value[5]!=2 or value[7]!=2):
            if value[7]!=2:
                value=client.walk_down()
                coo.walk(4)
            elif value[5]!=2:
                value=client.walk_right()
                coo.walk(1)
        #マップは横15×縦17

        #通常行動
        elif bool(ddir[d[0]-1]):
            a=dir(d[0]-1, value,a,right,up,left,down)
        elif bool(ddir[d[1]-1]):
            a=dir(d[1]-1, value,a,right,up,left,down)
        elif bool(ddir[d[2]-1]):
            a=dir(d[2]-1, value,a,right,up,left,down)
        elif bool(ddir[d[3]-1]):
            a=dir(d[3]-1, value,a,right,up,left,down)
        #通常行動過去行ったところあり
        elif bool(ddir2[d[0]-1]):
            a=dir(d[0]-1, value,a,right,up,left,down)
        elif bool(ddir2[d[1]-1]):
            a=dir(d[1]-1, value,a,right,up,left,down)
        elif bool(ddir2[d[2]-1]):
            a=dir(d[2]-1, value,a,right,up,left,down)
        elif bool(ddir2[d[3]-1]):
            change=1
            a=dir(d[3]-1, value,a,right,up,left,down)
        #通常行動条件ゆるめ
        elif value[5]==0 and right!=1:
            change=1
            value=client.walk_right()
            a=1
            a2=1
            coo.walk(1)
        elif value[1]==0 and up!=1:
            change=1
            value=client.walk_up()
            a=2
            a2=1
            coo.walk(2)
        elif value[3]==0 and left!=1:
            change=1
            value=client.walk_left()
            a=3
            a2=1
            coo.walk(3)
        elif value[7]==0 and down!=1:
            change=1
            value=client.walk_down()
            a=4
            a2=1
            coo.walk(4)
        elif value[5]!=2:
            change=1
            value=client.walk_right()
            a=1
            a2=1
            coo.walk(1)
        elif value[1]!=2:
            change=1
            value=client.walk_up()
            a=2
            a2=1
            coo.walk(2)
        elif value[3]!=2:
            change=1
            value=client.walk_left()
            a=3
            a2=1
            coo.walk(3)
        elif value[7]!=2:
            change=1
            value=client.walk_down()
            a=4
            a2=1
            coo.walk(4)
        #真ん中に行くプログラム書く
        else:
            value=client.search_up()
            a=0
            a2=3
        

if __name__ == "__main__":
    main(4)