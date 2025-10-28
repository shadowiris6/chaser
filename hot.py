import itertools
import random
import CHaser  # 同じディレクトリに CHaser.py がある前提
from collections import Counter

FLOOR = 0
ENEMY = 1
BLOCK = 2
ITEM = 3
class coordinate:
    #4はわからないこと#左上から数える
    ItemPlace=[[]] #アイテムの位置 2次元目が座標(x,y)自己中心的座標
    Itemway=[]
    coordvalue=[0,0,0,0,0,0,0,0,0]
    d=0
    nearItem=[]#アイテムまでの距離道のり？
    nearItemway=0#一番近いアイテムの座標？
    lastvalue=[
        [0,0]
    ]#何ターン目か、座標(x,y)
    nearItemPlace=[4,4]#ItemRatioとか参考にする
    PreferPoint=[4,4]
    ItemTurn=0 #アイテムを何ターンとってないか
    turn=0
    map=[[(4) for j in range(17)] for i in range(15)]
    PlayerPlace=[1,1]
    ItemPoint=[[4,4]]
    SearchPoint=[[4,4]]
    SearchRatio = [[0,0,0],[0,0,0],[0,0,0]]#横555縦555で間にノーカン*2
    ItemRatio = [[0,0,0],[0,0,0],[0,0,0]]
    change=0
    resetturn=0
    #５は行ったことある場所#[[4]*3]*3
    def ready(self,value,d):
        print("r")
        self.coordvalue=value
        #アイテム座標
        if self.coordvalue[0]==3:
            self.ItemPlace.append([-1,-1])
        if self.coordvalue[1]==3:
            self.ItemPlace.append([0,-1])
        if self.coordvalue[2]==3:
            self.ItemPlace.append([1,-1])
        if self.coordvalue[3]==3:
            self.ItemPlace.append([-1,0])
        if self.coordvalue[5]==3:
            self.ItemPlace.append([1,0])
        if self.coordvalue[6]==3:
            self.ItemPlace.append([-1,1])
        if self.coordvalue[7]==3:
            self.ItemPlace.append([0,1])
        if self.coordvalue[8]==3:
            self.ItemPlace.append([1,1])
        self.lastvalue.append([0,0])
        self.ItemTurn+=1
        self.Itemway.clear()
        
        if self.turn==0:#ItemPlaceは7,8-PlayerPlace
            self.PlayerPlace = SpawnPlace
            self.ItemPlace[0]= [7-self.PlayerPlace[0],8-self.PlayerPlace[1]]
            self.turn+=1
            self.map[7][8]=3
        #取ったアイテムの削除処理

        for i in reversed(range(len(self.ItemPlace))):
            k=0
            print(i)
            for j in range(len(self.lastvalue)):
                if self.ItemPlace[i] == self.lastvalue[j]:
                    k=1
            if k==1:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[-1,-1] and self.coordvalue[0]!=3:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[0,-1] and self.coordvalue[1]!=3:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[1,-1] and self.coordvalue[2]!=3:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[-1,0] and self.coordvalue[3]!=3:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[1,0] and self.coordvalue[5]!=3:
                del self.ItemPlace[i]
                print("del")
            elif self.ItemPlace[i]==[-1,1] and self.coordvalue[6]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[0,1] and self.coordvalue[7]!=3:
                del self.ItemPlace[i]
            elif self.ItemPlace[i]==[1,1] and self.coordvalue[8]!=3:
                del self.ItemPlace[i]
        
        for i in range(len(self.ItemPlace)):
            if len(self.ItemPlace[i])>0:
                print(self.ItemPlace[i])
                self.Itemway.append(abs(self.ItemPlace[i][0]) + abs(self.ItemPlace[i][1]))
        self.nearItemway = min(self.Itemway,default=99)#nullにならないようにしている
        if self.nearItemway != 99 and len(self.Itemway) > 0:
            self.nearItem = self.ItemPlace[self.Itemway.index(self.nearItemway)]#これ頭いい←ミスってて草
        print(self.nearItem,"nearItem")
#インデックスを使って、playerplaceを中心として、itemplaceをいれる
# #mapに直接入れるifで範囲内か確認するブロック位置デバックしてねー
        if self.coordvalue[0]==2 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]-1]=2
        if self.coordvalue[1]==2 and 0 <= self.PlayerPlace[0] <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]][self.PlayerPlace[1]-1]=2
        if self.coordvalue[2]==2 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]-1]=2
        if self.coordvalue[3]==2 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1] <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]]=2
        if self.coordvalue[5]==2 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1] <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]]=2
        if self.coordvalue[6]==2 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]+1]=2
        if self.coordvalue[7]==2 and 0 <= self.PlayerPlace[0] <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]][self.PlayerPlace[1]+1]=2
        if self.coordvalue[8]==2 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]+1]=2
        #mapに何もない場所を入れる
        if self.coordvalue[0]==0 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]-1]=5
        if self.coordvalue[1]==0 and 0 <= self.PlayerPlace[0] <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]][self.PlayerPlace[1]-1]=5
        if self.coordvalue[2]==0 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1]-1 <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]-1]=5
        if self.coordvalue[3]==0 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1] <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]]=5
        if self.coordvalue[5]==0 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1] <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]]=5
        if self.coordvalue[6]==0 and 0 <= self.PlayerPlace[0]-1 <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]-1][self.PlayerPlace[1]+1]=5
        if self.coordvalue[7]==0 and 0 <= self.PlayerPlace[0] <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]][self.PlayerPlace[1]+1]=5
        if self.coordvalue[8]==0 and 0 <= self.PlayerPlace[0]+1 <=14 and 0 <= self.PlayerPlace[1]+1 <=16:
            self.map[self.PlayerPlace[0]+1][self.PlayerPlace[1]+1]=5
        
        self.ItemPoint=[[4,4]]
        self.nearItemPlace=[4,4]
        for i in range(3):
            for j in range(3):
                if self.ItemRatio[i][j]>0.04:
                    self.ItemPoint.append([i,j])       
        for i in range(len(self.ItemPoint)):
            if i!=0 and (self.nearItemPlace[0]==4 or abs(self.ItemPoint[i][0]*5+2 - self.PlayerPlace[1]) +abs(self.ItemPoint[i][1]*6+2 - self.PlayerPlace[0]) < abs(self.nearItemPlace[0]*5+2 - self.PlayerPlace[1])+abs(self.nearItemPlace[1]*6+2 - self.PlayerPlace[0])):
                self.nearItemPlace[0]=self.ItemPoint[i][0]
                self.nearItemPlace[1]=self.ItemPoint[i][1]
        print(self.nearItemPlace,"nearItemPlace")
        
        self.SearchPoint=[[4,4]]
        self.PreferPoint=[4,4]
        for i in range(3):
            for j in range(3):
                if self.SearchRatio[i][j]<0.4:
                    self.SearchPoint.append([i,j])     
        for i in range(len(self.SearchPoint)):
            if (self.PreferPoint[0]==4 or abs(self.SearchPoint[i][0]*5+2 - self.PlayerPlace[1]) +abs(self.SearchPoint[i][1]*6+2 - self.PlayerPlace[0]) < abs(self.PreferPoint[0]*5+2 - self.PlayerPlace[1])+abs(self.PreferPoint[1]*6+2 - self.PlayerPlace[0])):
                self.PreferPoint[0]=self.SearchPoint[i][0]
                self.PreferPoint[1]=self.SearchPoint[i][1]
        print(self.PreferPoint,"PreferPoint")
        #22turn
        if (self.resetturn / 20 >= 1 or self.ItemTurn >6) and len(self.nearItem) !=0 and self.nearItem[0]+self.nearItem[1]<7:
            preferX=0
            preferY=0
            if self.nearItem[0]> 0:#(self.nearItemPlace[0]*5+2) - self.PlayerPlace[0] 
                preferX=1#優先右
            if self.nearItem[1] > 0:
                preferY=1#優先下
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
                    d[3]=4
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
            self.resetturn=0
            self.ItemTurn=0
            print(d,"Itemplace")
        
        
        print(self.PlayerPlace,"playerplacex")
        if self.PlayerPlace[0]<len(self.map) and self.PlayerPlace[1] < len(self.map[0]) and self.PlayerPlace[0]>=0 and self.PlayerPlace[1]>=0:
            self.map[self.PlayerPlace[0]][self.PlayerPlace[1]]=5

        #自己中心的マップを神視点マップに入れる
        for i in range(len(self.lastvalue)):
            if self.lastvalue[i][0] + self.PlayerPlace[0] <= 14 and self.lastvalue[i][1] + self.PlayerPlace[1] <=16  and self.lastvalue[i][0] + self.PlayerPlace[0]>=0 and self.lastvalue[i][1] + self.PlayerPlace[1]>=0 and \
                self.map[self.PlayerPlace[0] + self.lastvalue[i][0]][self.PlayerPlace[1] + self.lastvalue[i][1]] != 2:
                self.map[self.PlayerPlace[0] + self.lastvalue[i][0]][self.PlayerPlace[1] + self.lastvalue[i][1]] = 5
        for i in range(len(self.ItemPlace)):
            if self.ItemPlace[i][0] + self.PlayerPlace[0] <= 14 and self.ItemPlace[i][1] + self.PlayerPlace[1] <=16  and self.ItemPlace[i][0] + self.PlayerPlace[0]>=0 and self.ItemPlace[i][1] + self.PlayerPlace[1]>=0 and \
                self.map[self.PlayerPlace[0] + self.ItemPlace[i][0]][self.PlayerPlace[1] + self.ItemPlace[i][1]] == 4:
                self.map[self.PlayerPlace[0] + self.ItemPlace[i][0]][self.PlayerPlace[1] + self.ItemPlace[i][1]] = 3
            if self.ItemPlace[i][0] + self.PlayerPlace[0] <= 14 and self.ItemPlace[i][1] + self.PlayerPlace[1] <=16 and self.ItemPlace[i][0] + self.PlayerPlace[0]>=0 and self.ItemPlace[i][1] + self.PlayerPlace[1]>=0 and \
                self.map[(self.PlayerPlace[0] + self.ItemPlace[i][0])*(-1)-1][(self.PlayerPlace[1] + self.ItemPlace[i][1])*(-1)-1] == 4:
                self.map[(self.PlayerPlace[0] + self.ItemPlace[i][0])*(-1)-1][(self.PlayerPlace[1] + self.ItemPlace[i][1])*(-1)-1] = 3
                #print((14+(self.PlayerPlace[0] + self.ItemPlace[i][0])*(-1)) - self.PlayerPlace[0],(16+(self.PlayerPlace[1] + self.ItemPlace[i][1])*(-1)) - self.PlayerPlace[1],"PointSymmetry")
                #print([(self.PlayerPlace[0] + self.ItemPlace[i][0])*(-1)-1],[(self.PlayerPlace[1] + self.ItemPlace[i][1])*(-1)-1])
                self.ItemPlace.append([(14+(self.PlayerPlace[0] + self.ItemPlace[i][0])*(-1)) - self.PlayerPlace[0],(16+(self.PlayerPlace[1] + self.ItemPlace[i][1])*(-1)) - self.PlayerPlace[1]])
        #縦0基準の5,11はカウントしないマップの調査率を調べる
        
        c=[itertools.chain.from_iterable([l[:5] for l in self.map[:5]]),
        itertools.chain.from_iterable([l[:5] for l in self.map[5:10]]),
        itertools.chain.from_iterable([l[:5] for l in self.map[10:]]),
        itertools.chain.from_iterable([l[6:11] for l in self.map[:5]]),
        itertools.chain.from_iterable([l[6:11] for l in self.map[5:10]]),
        itertools.chain.from_iterable([l[6:11] for l in self.map[10:]]),
        itertools.chain.from_iterable([l[12:] for l in self.map[:5]]),
        itertools.chain.from_iterable([l[12:] for l in self.map[5:10]]),
        itertools.chain.from_iterable([l[12:] for l in self.map[10:]])]
        S=[Counter(sublist) for sublist in c]
        print(S[0][2])
        self.SearchRatio[0][0]=1-(S[0][4] / 25)
        self.SearchRatio[0][1]=1-(S[1][4] / 25)
        self.SearchRatio[0][2]=1-(S[2][4] / 25)
        self.SearchRatio[1][0]=1-(S[3][4] / 25)
        self.SearchRatio[1][1]=1-(S[4][4] / 25)
        self.SearchRatio[1][2]=1-(S[5][4] / 25)
        self.SearchRatio[2][0]=1-(S[6][4] / 25)
        self.SearchRatio[2][1]=1-(S[7][4] / 25)
        self.SearchRatio[2][2]=1-(S[8][4] / 25)
        self.ItemRatio[0][0]=S[0][3] / 25
        self.ItemRatio[0][1]=S[1][3] / 25
        self.ItemRatio[0][2]=S[2][3] / 25
        self.ItemRatio[1][0]=S[3][3] / 25
        self.ItemRatio[1][1]=S[4][3] / 25
        self.ItemRatio[1][2]=S[5][3] / 25
        self.ItemRatio[2][0]=S[6][3] / 25
        self.ItemRatio[2][1]=S[7][3] / 25
        self.ItemRatio[2][2]=S[8][3] / 25
        print(self.SearchRatio)#触ったか、アイテムの割合
        print(self.ItemRatio)#アイテムの割合

        print(self.change)
        #(nearItem and resetturn) or Itemturn→ nearItem(0) and (resetturn or Itemturn)
        if self.nearItemPlace[0]!=[4] and (self.resetturn / 24 >= 1 or self.ItemTurn > 10 or self.change >= 6):#アイテムのある割合9分割
            preferX=0
            preferY=0
            if (self.nearItemPlace[0]*5+2) - self.PlayerPlace[1] > 0: 
                preferX=1#優先右
            if (self.nearItemPlace[1]*6+2) - self.PlayerPlace[0] > 0:
                preferY=1#優先下
            if abs((self.nearItemPlace[0]*5+2) - self.PlayerPlace[0]) > abs((self.nearItemPlace[1]*6+2) - self.PlayerPlace[1]):
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
            self.resetturn=0
            self.ItemTurn=0
            self.change-=5
            print(d,"Itempoint")
        if self.PreferPoint[0]!=[4] and (self.resetturn / 24 >= 1 or self.ItemTurn > 10 or self.change>=6) and self.ItemTurn > 3 and self.resetturn and abs((self.PreferPoint[0]*5+2) - self.PlayerPlace[1]) + abs((self.PreferPoint[1]*6+2) - self.PlayerPlace[0]) >=5:#アイテムのある割合9分割
            preferX=0
            preferY=0
            if (self.PreferPoint[0]*5+2) - self.PlayerPlace[1] > 0: 
                preferX=1#優先右
            if (self.PreferPoint[1]*6+2) - self.PlayerPlace[0] > 0:
                preferY=1#優先下
            if abs((self.PreferPoint[0]*5+2) - self.PlayerPlace[0]) > abs((self.PreferPoint[1]*6+2) - self.PlayerPlace[1]):
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
            print(d,"preferpoint")
            self.ItemTurn=0
            self.resetturn=0
            self.change-=5
        '''if (len(self.nearItem)!= 0 and self.resetturn / 24 >= 1) or self.ItemTurn > 5:#一旦ランダムにしとくあとでアイテムの方向とかにするといい
            if random.randint(0,1)==1:#あとでアイテムエリアじゃなくて調査度でやる
                d[0],d[2]=d[2],d[0]
            if random.randint(0,1)==1:
                d[1],d[3]=d[3],d[1]
            if random.randint(0,1) == 1:
                d[0],d[1]=d[1],d[0]
                d[2],d[3]=d[3],d[2]
            self.resetturn=0'''
        print(d)
        return d
    def walk(self,walk):#右=1 上＝2 左=3 下=4
        print(range(len(self.lastvalue)))
        print(range(len(self.ItemPlace)))
        if walk==1:
            for i in range(len(self.lastvalue)):
                self.lastvalue[i][0]-=1
            for i in range(len(self.ItemPlace)):
                self.ItemPlace[i][0]-=1
            self.PlayerPlace[0]+=1
        elif walk==2:
            for i in range(len(self.lastvalue)):
                self.lastvalue[i][1]+=1
            for i in range(len(self.ItemPlace)):
                self.ItemPlace[i][1]+=1
            self.PlayerPlace[1]-=1
        elif walk==3:
            for i in range(len(self.lastvalue)):
                self.lastvalue[i][0]+=1
            for i in range(len(self.ItemPlace)):
                self.ItemPlace[i][0]+=1
            self.PlayerPlace[0]-=1
        elif walk==4:
            for i in range(len(self.lastvalue)):
                self.lastvalue[i][1]-=1
            for i in range(len(self.ItemPlace)):
                self.ItemPlace[i][1]-=1
            self.PlayerPlace[1]+=1
        for i in range(len(self.ItemPlace)):
            print(self.ItemPlace[i])
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
        if len(self.ItemPlace) == 0:
            self.change+=4
coo=coordinate()
SpawnPlace=[0,0]
def main(X,Y):#valueの値と同じ4はわからない
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

# ---- コードを書くのは基本的にここから -----

    a=0#1個前の向き
    a2=0#１個前の行動1がwalk,2がlook,3がsearch,4がput
    turn=0
    d=[3,2,1,4]#右下左上の逆
    check=turn#なんだっけ
    search=0
    SpawnPlace[0]=X
    SpawnPlace[1]=Y
    #lookした情報からブロック判断する(敵も)
    #1個前の敵をよける
    def dir(dirr, value,right,up,left,down):
        if dirr==0:
            value=client.walk_right()
            a=1
            a2=1
            coo.walk(1)
        elif dirr==1:
            value=client.walk_up()
            a=2
            a2=1
            coo.walk(2)
        elif dirr==2:
            value=client.walk_left()
            a=3
            a2=1
            coo.walk(3)
        elif dirr==3:
            value=client.walk_down()
            a=4
            a2=1
            coo.walk(4)
        return a
    ddir=[]
    #hotの場合ここをけす
    if X<7 or (X==7 and Y<8):
        value=client.get_ready()
        d=coo.ready(value,d)
        coo.resetturn+=1
        turn+=1
        value=client.search_right()
        print("1stturn_search_right")
    if X<7:
        d[0]=1
        d[2]=3
        if Y<8:
            d[1]=2
            d[3]=4
        else:
            d[1]=4
            d[3]=2
    elif X>7:
        d[0]=3
        d[2]=1
        if Y<8:
            d[1]=2
            d[3]=4
        else:
            d[1]=4
            d[3]=2
    else:
        if Y<8:
            d[0]=2
            d[2]=4
        else:
            d[0]=4
            d[2]=2
        d[1]=1
        d[3]=3
    while True:#右=1 上＝2 左=3 下=4
        up=0
        down=0
        left=0
        right=0
        value=client.get_ready()
        d=coo.ready(value,d)
        coo.resetturn+=1
        turn+=1
        if coo.change>0:
            coo.change-=1
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
        
        sub_list = coo.lastvalue[len(coo.lastvalue)-15:]
        if sub_list.count([0,0]) >=2:
            coo.change+=3

        #通常行動条件
        ddir2=[value[5]==0 and a!=3 and right!=1,
            value[1]==0 and a!=4 and up!=1,
            value[3]==0 and a!=1 and left!=1,
            value[7]==0 and a!=2 and down!=1]
        #妥協ターン
        ddir=[value[5]==0 and right!=1,
            value[1]==0 and up!=1,
            value[3]==0 and left!=1,
            value[7]==0 and down!=1]
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
            coo.walk(3)
            coo.getitem()
            a=3
            a2=1
        elif value[1]==3 and up!=1 and (value[0]!=2 or value[2]!=2):
            value=client.walk_up()
            coo.walk(2)
            coo.getitem()
            a=2
            a2=1
        elif value[7]==3 and down!=1 and (value[6]!=2 or value[8]!=2):
            value=client.walk_down()
            coo.walk(4)
            coo.getitem()
            a=4
            a2=1
        elif value[5]==3 and right!=1 and (value[2]!=2 or value[8]!=2):
            value=client.walk_right()
            coo.walk(1)
            coo.getitem()
            a=1
            a2=1
        #トラップ対策
        elif value[3]==3 and left!=1 and value[0]==2 and value[6]==2 and a2!=3:
            value=client.search_left()
            a2=3
            if value[1]!=2 and left!=1:
                value=client.get_ready()
                d=coo.ready(value,d)
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
                d=coo.ready(value,d)
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
                d=coo.ready(value,d)
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
                d=coo.ready(value,d)
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
        elif bool(ddir2[d[0]-1]):
            a=dir(d[0]-1, value,right,up,left,down)
        elif bool(ddir2[d[1]-1]):
            a=dir(d[1]-1, value,right,up,left,down)
        elif bool(ddir2[d[2]-1]):
            a=dir(d[2]-1, value,right,up,left,down)
        elif bool(ddir2[d[3]-1]):
            a=dir(d[3]-1, value,right,up,left,down)
        #通常行動過去行ったところあり
        elif bool(ddir2[d[0]-1]):
            a=dir(d[0]-1, value,right,up,left,down)
        elif bool(ddir2[d[1]-1]):
            a=dir(d[1]-1, value,right,up,left,down)
        elif bool(ddir2[d[2]-1]):
            a=dir(d[2]-1, value,right,up,left,down)
        elif bool(ddir2[d[3]-1]):
            coo.change+=3
            a=dir(d[3]-1, value,right,up,left,down)
        #通常行動条件ゆるめ
        elif bool(ddir[d[0]-1]):
            coo.change+=3
            a=dir(d[0]-1, value,right,up,left,down)
            a2=1
        elif bool(ddir[d[1]-1]):
            coo.change+=3
            a=dir(d[1]-1, value,right,up,left,down)
            a2=1
        elif bool(ddir[d[2]-1]):
            coo.change+=3
            a=dir(d[2]-1, value,right,up,left,down)
            a2=1
        elif bool(ddir[d[3]-1]):
            coo.change+=3
            a=dir(d[3]-1, value,right,up,left,down)
            a2=1
        else:
            value=client.search_up()
            a=0
            a2=3
        

if __name__ == "__main__":
    main(5,5)