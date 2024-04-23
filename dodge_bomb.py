import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1000, 600
DELTA = {  # 移動量辞書（押下キー：移動量タプル）
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect,または,爆弾Rectの画面内外判定用の関数
    引数:こうかとんRect,または,爆弾Rect
    戻り値:横方向判定結果,縦方向判定結果（True:画面内/False:画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # ここから爆弾の設定
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 横方向速度，縦方向速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
               sum_mv[0] += v[0]
               sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の移動と表示
        bd_rct.move_ip(vx, vy)       
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx *= -1
        if not tate:  # 縦方向にはみ出てたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()