# 產生其餘場景（對應 docs/video_script.md 第四節的設計腳本）。
# 用法：cd video && python3 generator/scenes.py
# ⚠ 會覆蓋 src/scenes/ 裡同名的檔案；已在 Studio 修改過的場景不要再產生。
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib import *  # noqa: E402,F403

OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'scenes')


def caption(name, y, parts, size=52, weight=700, color=INK, dur=None, out=12, extra=None):
    st = {'position': 'absolute', 'left': 0, 'top': y, 'width': 1920, 'textAlign': 'center',
          'fontFamily': SANS, 'fontSize': size, 'fontWeight': weight, 'color': color,
          'opacity': fade(dur, 12, out) if dur else fade(1, 12, 0), 'translate': rise()}
    if extra:
        st.update(extra)
    return tag(name, st, spans(parts, color) if isinstance(parts, list) else jtext(parts))


def dim_to(dur, at, low=0.3):
    """淡入 → 在 at 格時變暗到 low。"""
    return raw(kf([0, 15, at, at + 20], [0, 1, 1, low]))


# ---------------------------------------------------------------- S1Question
def s1():
    sc = Scene('S1Question', '段 1｜問題（設計腳本鏡頭 1-1～1-3）', 900,
               '// 事實來源：F6（HbS：β 鏈 E→V，教科書寫作 E6V）')
    # 1-1 紅血球：圓形 → 鐮刀形
    cell_svg = ('<svg width="320" height="320" viewBox="0 0 320 320">'
                '<circle cx="160" cy="160" r="140" fill="#C8463D" /><circle cx="160" cy="160" r="70" fill="#D9675F" /></svg>')
    sickle_svg = ('<svg width="320" height="320" viewBox="0 0 320 320">'
                  '<path d="M25,235 Q95,25 300,120 Q170,165 25,235 Z" fill="#C8463D" /></svg>')
    sc.add('紅血球（正常）', 0, 170, tag('正常紅血球', {
        'position': 'absolute', 'left': 800, 'top': 230, 'width': 320, 'height': 320,
        'opacity': raw(kf([0, 20, 135, 170], [0, 1, 1, 0])),
    }, cell_svg))
    sc.add('紅血球（鐮刀形）', 135, 135, tag('鐮刀形紅血球', {
        'position': 'absolute', 'left': 800, 'top': 230, 'width': 320, 'height': 320,
        'opacity': fade(135, 30, 15), 'rotate': raw(kf([0, 40], ['-12deg', '0deg'])),
    }, sickle_svg))
    sc.add('標題：鐮刀型貧血', 20, 250, caption('標題文字', 620, '鐮刀型貧血', size=72, dur=250, out=15))

    # 1-2 β 鏈上一格 E → V（不標編號，編號留到示範段）
    sc.add('標籤：血紅素 β 鏈', 270, 300, caption('標籤文字', 250, '血紅素 β 鏈', size=40, weight=400, color=MUTED, dur=300))
    n, size, gap = 7, 110, 30
    left0 = (1920 - (n * size + (n - 1) * gap)) // 2
    beads = []
    for i in range(n):
        if i == 3:
            continue
        a = 4 * i
        beads.append(box(f'胺基酸 {i + 1}', left0 + i * (size + gap), 360, size, size, bg='#E4E1DA', extra={
            'opacity': raw(kf([a, a + 15], [0, 1])), 'translate': raw(kf([a, a + 15], ['0px 20px', '0px 0px'], 'translate'))}))
    sc.add('β 鏈的其他胺基酸', 270, 300, beads)
    mid = left0 + 3 * (size + gap)
    letter = centered({'fontFamily': MONO, 'fontSize': 64, 'fontWeight': 700, 'color': INK,
                       'borderWidth': 5, 'borderStyle': 'solid', 'borderColor': ACCENT})
    sc.add('方塊：E（原本）', 282, 138, box('E 方塊', mid, 360, size, size, extra={
        **letter, 'opacity': raw(kf([0, 15], [0, 1])), 'scale': raw(kf([0, 108, 138], ['1 1', '1 1', '1 0'], 'scale'))}, children='E'))
    sc.add('方塊：V（突變後）', 420, 150, box('V 方塊', mid, 360, size, size, extra={
        **letter, 'color': ACCENT, 'scale': raw(kf([0, 30], ['1 0', '1.12 1.12'], 'scale')),
        'opacity': raw(kf([0, 1, 138, 150], [0, 1, 1, 0]))}, children='V'))
    sc.add('文字：E → V', 330, 240, caption('文字', 560, [('E', None), (' → ', MUTED), ('V', ACCENT)], size=64, dur=240,
                                             extra={'fontFamily': MONO}))
    sc.add('文字：教科書 E6V', 450, 120, caption('文字', 680, [('教科書：E', None), ('6', ACCENT), ('V', None)], size=48, weight=400, dur=120))
    sc.source(270, 300, 'F6')

    # 1-3 兩個問題 → AlphaFold DB
    sc.add('問題 1', 570, 330, caption('問題 1 文字', 300, '在結構的哪裡？', size=80, extra={'opacity': dim_to(330, 120)}))
    sc.add('問題 2', 690, 210, caption('問題 2 文字', 460, '可不可信？', size=80, extra={'opacity': dim_to(210, 110)}))
    sc.add('答案：AlphaFold DB', 800, 100, caption('答案文字', 660, [('→ ', MUTED), ('AlphaFold DB', ACCENT)], size=72))
    return sc


# ---------------------------------------------------------------- S2Tool
def s2():
    sc = Scene('S2Tool', '段 2｜工具與輸入（設計腳本鏡頭 2-1～2-4）', 1500,
               '// 事實來源：F2（免費、CC-BY-4.0）、F15（搜尋方式）、F16（pLDDT 與 PAE）')
    # 2-1
    sc.add('標題：AlphaFold DB', 0, 450, caption('標題文字', 170, 'AlphaFold DB', size=120, dur=450, out=15,
                                                  extra={'color': INK}))
    sc.add('副標：AI 預測的結構', 30, 420, caption('副標文字', 340, 'AI 預測的蛋白質立體結構', size=52, weight=400, color=MUTED, dur=420, out=15))
    ribbon = ('<svg width="1200" height="260" viewBox="0 0 1200 260"><defs><linearGradient id="plddt" x1="0" x2="1">'
              f'<stop offset="0" stop-color="{P_VLOW}" /><stop offset="0.3" stop-color="{P_LOW}" />'
              f'<stop offset="0.6" stop-color="{P_HIGH}" /><stop offset="1" stop-color="{P_VHIGH}" /></linearGradient></defs>'
              '<path d="M30,130 C130,20 200,240 300,130 S470,20 570,130 S740,240 840,130 S1010,20 1170,130" '
              'fill="none" stroke="url(#plddt)" stroke-width="30" stroke-linecap="round" /></svg>')
    sc.add('結構示意（pLDDT 配色）', 60, 390, tag('結構示意圖', {
        'position': 'absolute', 'left': 360, 'top': 470, 'width': 1200, 'height': 260,
        'opacity': fade(390, 25, 15), 'transformOrigin': 'left center', 'scale': raw(kf([0, 40], ['0 1', '1 1'], 'scale')),
    }, ribbon))
    sc.add('標籤：免費查詢與下載', 150, 300, caption('標籤文字', 820, '免費查詢與下載（CC-BY-4.0）', size=40, weight=400, dur=300, out=15))
    sc.source(0, 450, 'F2')

    # 2-2 搜尋框
    sc.add('標籤：輸入', 450, 300, caption('標籤文字', 230, '輸入', size=44, weight=400, color=MUTED, dur=300))
    sc.add('搜尋框', 450, 300, box('搜尋框外框', 460, 330, 1000, 130, radius=65, extra={
        'boxShadow': '0 8px 30px rgba(0,0,0,0.08)', 'opacity': fade(300, 15, 12)}))
    items = [('HBB', '基因名稱', 470, 100), ('hemoglobin subunit beta', '蛋白質名稱', 580, 100), ('P68871', 'UniProt 編號', 690, 60)]
    for word, label, frm, dur in items:
        typed = tag('打字區（超出部分隱藏）', {
            'position': 'absolute', 'left': 520, 'top': 345, 'width': 880, 'height': 100, 'overflow': 'hidden',
            'opacity': fade(dur, 1, 10)},
            tag('輸入文字', {'position': 'absolute', 'left': 0, 'top': 18, 'fontFamily': MONO, 'fontSize': 54, 'color': INK,
                            'whiteSpace': 'pre'}, word)
            + tag('遮蓋塊（往右移＝打字）', {'position': 'absolute', 'left': 0, 'top': 0, 'width': 900, 'height': 100,
                                       'backgroundColor': CARD,
                                       'translate': raw(kf([5, 5 + 3 * len(word)], ['0px 0px', '900px 0px'], 'translate'))}))
        sc.add(f'輸入：{word}', frm, dur, typed)
        sc.add(f'說明：{label}', frm, dur, caption('說明文字', 510, label, size=44, color=ACCENT, dur=dur, out=10))
    sc.source(450, 300, 'F15')

    # 2-3 三張卡片
    cards = [('立體座標', '蛋白質的 3D 結構', 40), ('pLDDT', '每個胺基酸的信心分數', 140), ('PAE', '兩個區域之間的相對位置', 260)]
    icons = [
        '<svg width="200" height="110" viewBox="0 0 200 110"><path d="M10,60 C40,0 60,110 100,55 S160,0 190,55" fill="none" stroke="#1F2430" stroke-width="12" stroke-linecap="round" /></svg>',
        f'<svg width="200" height="110" viewBox="0 0 200 110"><rect x="0" y="35" width="50" height="40" fill="{P_VLOW}" /><rect x="50" y="35" width="50" height="40" fill="{P_LOW}" /><rect x="100" y="35" width="50" height="40" fill="{P_HIGH}" /><rect x="150" y="35" width="50" height="40" fill="{P_VHIGH}" /></svg>',
        '<svg width="200" height="110" viewBox="0 0 110 110">' + ''.join(
            f'<rect x="{c * 22}" y="{r * 22}" width="21" height="21" fill="{"#3C4352" if abs(r - c) < 2 else "#C9CDD6"}" />'
            for r in range(5) for c in range(5)) + '</svg>',
    ]
    for i, ((title, sub, bright), icon) in enumerate(zip(cards, icons)):
        x = 230 + i * 510
        body = box(f'卡片：{title}', x, 300, 440, 420, extra={
            'boxShadow': '0 8px 30px rgba(0,0,0,0.06)', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
            'justifyContent': 'center', 'gap': 26,
            'opacity': raw(kf([0, 15, bright, bright + 15], [0, 0.3, 0.3, 1]))},
            children=tag('圖示', {'width': 200, 'height': 110}, icon)
            + tag('卡片標題', {'fontFamily': SANS, 'fontSize': 52, 'fontWeight': 700, 'color': INK}, title)
            + tag('卡片說明', {'fontFamily': SANS, 'fontSize': 32, 'color': MUTED}, sub))
        sc.add(f'卡片 {i + 1}：{title}', 750, 450, body)
    sc.source(750, 450, 'F16')

    # 2-4 終端機
    term = box('終端機視窗', 360, 300, 1200, 280, radius=20, bg=TERM_BG, extra={
        'translate': raw(kf([0, 25], ['700px 0px', '0px 0px'], 'translate')), 'opacity': raw(kf([0, 15], [0, 1])),
        'boxShadow': '0 12px 40px rgba(0,0,0,0.18)'},
        children=tag('視窗按鈕', {'position': 'absolute', 'left': 28, 'top': 22, 'fontSize': 26, 'color': '#5B6275',
                                 'letterSpacing': 6}, '● ● ●')
        + tag('指令', {'position': 'absolute', 'left': 50, 'top': 120, 'fontFamily': MONO, 'fontSize': 44,
                      'color': TERM_INK, 'whiteSpace': 'pre'}, spans([('$ ', MUTED), ('python3 -m af_confidence ', None), ('HBB E6V', P_HIGH)], TERM_INK)))
    sc.add('終端機：HBB E6V', 1200, 300, term)
    sc.add('標籤：編號檢查工具', 1230, 270, caption('標籤文字', 660, '＋ 我們的編號檢查工具', size=56, color=ACCENT))
    sc.add('說明：檢查編號', 1260, 240, caption('說明文字', 760, '檢查文獻的突變編號，在模型上對不對得上', size=38, weight=400, color=MUTED))
    return sc


# ---------------------------------------------------------------- S4Plddt
def s4():
    sc = Scene('S4Plddt', '段 4｜pLDDT 分級與 TP53 對比（設計腳本鏡頭 4-1、4-2）', 1380,
               '// 事實來源：F1（分級）、F17（網站顏色）、F4（TP53 R175 96.62、P72 48.25）、F13（< 50 不應解讀）')
    L, W, Y, H = 260, 1400, 450, 80
    segs = [('非常低', '< 50', 0, 50, P_VLOW), ('低', '50–70', 50, 70, P_LOW), ('高', '70–90', 70, 90, P_HIGH), ('非常高', '> 90', 90, 100, P_VHIGH)]
    xs = lambda v: L + round(W * v / 100)  # noqa: E731
    sc.add('標題：pLDDT', 0, 1380, caption('標題文字', 170, [('pLDDT', ACCENT), ('：每個胺基酸的信心分數', None)], size=56))
    bar = []
    for i, (name, rng, a, b, col) in enumerate(segs):
        bar.append(box(f'色段：{name}', xs(a), Y, xs(b) - xs(a), H, radius=0, bg=col, extra={
            'opacity': raw(kf([10 + 8 * i, 25 + 8 * i], [0, 1]))}))
    for v in (0, 50, 70, 90, 100):
        bar.append(text(f'刻度 {v}', xs(v) - 50, Y + H + 12, str(v), size=30, color=MUTED, font=MONO, align='center', width=100,
                        extra={'opacity': raw(kf([30, 45], [0, 1]))}))
    sc.add('刻度尺（四個色段）', 20, 1360, bar)
    # 依旁白順序：非常高 → 高 → 低 → 非常低
    order = [(3, 90), (2, 220), (1, 350), (0, 480)]
    for idx, frm in order:
        name, rng, a, b, col = segs[idx]
        cx = (xs(a) + xs(b)) // 2
        sc.add(f'聚焦：{name}', frm, 130 if idx else 210, ring('聚焦框', xs(a), Y, xs(b) - xs(a), H, INK, 130 if idx else 210, width=4, radius=4))
        sc.add(f'標籤：{name} {rng}', frm, 690 - frm, text('標籤文字', cx - 150, Y + H + 70, [(name + '\n', None), (rng, MUTED)],
                                                         size=40, weight=700, align='center', width=300,
                                                         extra={'whiteSpace': 'pre', 'lineHeight': 1.3, 'opacity': fade(690 - frm, 12, 15)}))
    sc.source(0, 690, 'F1、F17')

    # 4-2 TP53 兩個位置
    for label, val, col, frm in [('R175', 96.62, P_VHIGH, 720), ('P72', 48.25, P_VLOW, 870)]:
        x = xs(val)
        pin = [box('標記線', x - 3, Y - 70, 6, H + 70, radius=3, bg=INK),
               text('標記文字', x - 180, Y - 150, [(label + '：', None), (f'{val}', col)], size=48, weight=700,
                    font=MONO, align='center', width=360)]
        sc.add(f'標記：{label} {val}', frm, 1380 - frm, tag('標記（位置與動畫）', {
            'position': 'absolute', 'left': 0, 'top': 0, 'width': 1920, 'height': 1080,
            'opacity': raw(kf([0, 15], [0, 1])), 'translate': raw(kf([0, 20], ['0px -40px', '0px 0px'], 'translate'))},
            ''.join(pin)))
    sc.add('結論：< 50 不應解讀', 1000, 380, caption('結論文字', 700, [('pLDDT < 50', P_VLOW), ('：座標不應拿來解讀', None)], size=54, out=0))
    sc.add('說明：可能沒有固定結構', 1060, 320, caption('說明文字', 790, '可能在生理狀態下沒有固定結構，或只在和其他分子結合時才有結構',
                                                    size=36, weight=400, color=MUTED, out=0))
    sc.source(690, 690, 'F4、F13')
    return sc


# ---------------------------------------------------------------- S4ToolOutput
def s4tool():
    sc = Scene('S4ToolOutput', '段 4｜工具輸出怎麼讀（設計腳本鏡頭 4-4）', 300,
               '// 事實來源：工具對 HBB E6V 的實際輸出（docs/video_script.md 3C）')
    TX, TY, CW, LH = 210, 360, 22.8, 70  # 文字起點、字寬（JetBrains Mono 38px ≈ 0.6em）、行高
    l1 = 'XX E6V: model has P at 6, not E'
    l2 = '     -> [medium] annotated_offset: +1: E7V matches …'
    term = box('終端機視窗', 160, 300, 1600, 230, radius=20, bg=TERM_BG, extra={'opacity': raw(kf([0, 12], [0, 1]))},
               children=tag('第 1 行', {'position': 'absolute', 'left': 50, 'top': 60, 'fontFamily': MONO, 'fontSize': 38,
                                       'color': TERM_INK, 'whiteSpace': 'pre'}, jtext(l1))
               + tag('第 2 行', {'position': 'absolute', 'left': 50, 'top': 60 + LH, 'fontFamily': MONO, 'fontSize': 38,
                                'color': TERM_INK, 'whiteSpace': 'pre'}, jtext(l2)))
    sc.add('終端機：工具輸出', 0, 300, term)

    def tok(line, s):
        i = (l1 if line == 1 else l2).index(s)
        return TX + round(i * CW), TY + (line - 1) * LH, round(len(s) * CW)

    marks = [('XX', 1, 'XX', 30, [('XX', BAD), ('：對不上（OK：對得上）', None)], 210, 600),
             ('E7V', 2, 'E7V', 100, [('->', ACCENT), (' 後面：建議的位置', None)], 1000, 600),
             ('[medium]', 2, '[medium]', 170, [('[medium]', ACCENT), ('：這個建議有多可信', None)], 330, 700)]
    for name, line, s, frm, label, lx, ly in marks:
        x, y, w = tok(line, s)
        sc.add(f'聚焦：{name}', frm, 300 - frm, ring('聚焦框', x, y + 4, w, 46, P_LOW, 300 - frm, width=4, radius=4, pad=6))
        sc.add(f'說明：{name}', frm, 300 - frm, text('說明文字', lx, ly, label, size=42, weight=700,
                                                    extra={'opacity': fade(1, 12, 0), 'translate': rise()}))
    return sc


# ---------------------------------------------------------------- S5Limits
def s5():
    sc = Scene('S5Limits', '段 5｜三個限制（設計腳本鏡頭 5-1～5-3）', 1530,
               '// 事實來源：F13（低 pLDDT）、F14（未驗證突變影響）、F3/F5（單鏈模型）、F6/F7（編號）、F10（ProtVar 截圖）')
    cards = ['① 低 pLDDT 不解讀', '② 正常序列・單鏈預測', '③ 編號：網站不提醒']
    vals = [[0, 1, 1, 0.35, 0.35, 0.35], [0, 0.35, 0.35, 1, 1, 0.35], [0, 0.35, 0.35, 0.35, 0.35, 1]]
    for i, (c, v) in enumerate(zip(cards, vals)):
        sc.add(f'卡片 {i + 1}', 0, 1530, box(f'卡片 {i + 1}', 160 + i * 540, 110, 520, 150, extra={
            **centered({'fontFamily': SANS, 'fontSize': 44, 'fontWeight': 700, 'color': INK}),
            'boxShadow': '0 8px 30px rgba(0,0,0,0.06)',
            'opacity': raw(kf([0, 15, 360, 375, 930, 945], v))}, children=c))

    # 第 1 點
    loose = (f'<svg width="560" height="260" viewBox="0 0 560 260"><path d="M20,200 C90,40 150,250 230,120 S360,10 420,170 S520,220 540,60" '
             f'fill="none" stroke="{P_VLOW}" stroke-width="22" stroke-linecap="round" /></svg>')
    sc.add('圖：低信心區（橘色）', 30, 330, tag('低信心區示意', {'position': 'absolute', 'left': 300, 'top': 450, 'width': 560, 'height': 260,
                                                           'opacity': fade(330, 20, 15)}, loose))
    sc.add('文字：pLDDT < 50', 50, 310, text('文字', 960, 470, [('pLDDT < 50', P_VLOW)], size=64, weight=700, font=MONO,
                                              extra={'opacity': fade(310, 15, 15), 'translate': rise()}))
    sc.add('文字：座標不應解讀', 80, 280, text('文字', 960, 570, '座標不應拿來解讀', size=50, weight=700,
                                              extra={'opacity': fade(280, 15, 15), 'translate': rise()}))
    sc.add('文字：常是無序區', 110, 250, text('文字', 960, 650, '（常是沒有固定結構的區域）', size=36, color=MUTED,
                                             extra={'opacity': fade(250, 15, 15), 'translate': rise()}))
    sc.source(0, 360, 'F13')

    # 第 2 點
    lt = centered({'fontFamily': MONO, 'fontSize': 80, 'fontWeight': 700})
    sc.add('方塊：E（模型裡的）', 375, 555, box('E 方塊', 300, 420, 170, 170, extra={
        **lt, 'color': INK, 'borderWidth': 5, 'borderStyle': 'solid', 'borderColor': INK, 'opacity': fade(555, 15, 15)}, children='E'))
    sc.add('箭頭', 405, 525, text('箭頭', 500, 445, '→', size=90, color=MUTED, extra={'opacity': fade(525, 15, 15)}))
    sc.add('方塊：V（虛線，看不到）', 435, 495, box('V 方塊', 620, 420, 170, 170, bg='transparent', extra={
        **lt, 'color': MUTED, 'borderWidth': 5, 'borderStyle': 'dashed', 'borderColor': ACCENT,
        'opacity': raw(kf([0, 20, 50, 70, 90, 110, 480, 495], [0, 1, 0.3, 1, 0.3, 1, 1, 0]))}, children='V'))
    sc.add('文字：看不到突變後的形狀', 470, 460, text('文字', 300, 630, '看不到突變後的形狀', size=40, weight=700,
                                                  extra={'opacity': fade(460, 15, 15)}))
    sc.add('引文：未驗證突變影響', 520, 410, text('引文', 960, 420, [('官方說明：\n', MUTED), ('AlphaFold 沒有被驗證\n能預測突變的影響', None)],
                                                size=46, weight=700, extra={'whiteSpace': 'pre', 'lineHeight': 1.4,
                                                                            'opacity': fade(410, 15, 15), 'translate': rise()}))
    sc.add('文字：單一條 β 鏈', 680, 250, text('文字', 960, 640, [('這個模型：', MUTED), ('單一條 β 鏈的預測', None)], size=40,
                                              weight=700, extra={'opacity': fade(250, 15, 15), 'translate': rise()}))
    sc.source(360, 570, 'F14、F3、F5')

    # 第 3 點
    sc.add('文字：兩種編號', 945, 160, caption('文字', 430, [('文獻：', MUTED), ('成熟蛋白質的編號', None)], size=50, dur=160))
    sc.add('文字：兩種編號（模型）', 975, 130, caption('文字', 530, [('模型：', MUTED), ('完整序列的編號', None)], size=50, dur=130))
    IX, IY, IW = 160, 375, 1600
    sc.add('ProtVar 截圖', 1100, 430, tag('截圖（位置與動畫）', {
        'position': 'absolute', 'left': IX, 'top': IY, 'width': IW, 'boxShadow': '0 8px 30px rgba(0,0,0,0.10)',
        'opacity': raw(kf([0, 15], [0, 1])), 'translate': rise(20, 15)},
        "<Img src={staticFile('protvar_P68871_E6V_crop.png')} style={{width: '100%', display: 'block'}} />"))
    k = IW / 1585  # 截圖縮放比例（原圖裁切後寬 1585）
    sc.add('聚焦：改用 Pro 繼續', 1180, 350, ring('聚焦框', IX + round(796 * k), IY + round(33 * k), round(352 * k), round(26 * k),
                                              BAD, 350, width=4, radius=4, pad=6))
    sc.add('聚焦：結果都是 Pro6', 1280, 250, ring('聚焦框', IX + round(1008 * k), IY + round(92 * k), round(84 * k), round(410 * k),
                                              BAD, 250, width=4, radius=6, pad=6))
    sc.add('說明：ProtVar', 1180, 350, caption('說明文字', 925, [('ProtVar 會警告，但改用', None), ('第 6 個（Pro）', BAD), ('繼續分析', None)],
                                               size=44, out=0))
    sc.source(930, 170, 'F6、F7')
    sc.source(1100, 430, 'F10')
    return sc


# ---------------------------------------------------------------- S5ToolLimit
def s5tool():
    sc = Scene('S5ToolLimit', '段 5｜工具本身的限制（設計腳本鏡頭 5-4）', 570,
               '// 事實來源：F8（APP：Aβ 第 1 個 = APP770 第 672 個；D23N 正確位置 D694N；第 23 個碰巧也是 D）、F12（約 7～9%）')
    sc.add('標題：工具也有限制', 0, 570, caption('標題文字', 110, '我們的工具也有限制', size=56))
    sc.add('文字：D23N', 20, 550, caption('文字', 220, [('Aβ 編號的 ', MUTED), ('D23N', None), ('（Iowa 突變）', MUTED)], size=44, weight=400))
    lt = centered({'fontFamily': MONO, 'fontSize': 96, 'fontWeight': 700, 'color': INK})
    for name, x, frm, num, sub, col in [('第 23 個', 560, 50, 'APP 第 23 個', '照文獻的數字', BAD), ('第 694 個', 1180, 90, 'APP 第 694 個', '正確位置', GOOD)]:
        sc.add(f'方塊：{name}', frm, 570 - frm, [
            box('D 方塊', x, 330, 180, 180, extra={**lt, 'borderWidth': 6, 'borderStyle': 'solid', 'borderColor': col,
                                                  'opacity': raw(kf([0, 15], [0, 1])), 'scale': raw(kf([0, 15], ['0.9', '1'], 'scale'))}, children='D'),
            text('位置文字', x - 110, 540, [(num + '\n', None), (sub, col)], size=36, weight=700, align='center', width=400,
                 extra={'whiteSpace': 'pre', 'lineHeight': 1.4, 'opacity': raw(kf([0, 15], [0, 1]))})])
    sc.add('等號', 130, 440, text('等號', 860, 345, '＝', size=110, color=INK, align='center', width=200,
                                 extra={'opacity': raw(kf([0, 15], [0, 1]))}))
    sc.add('說明：碰巧對上', 160, 410, caption('說明文字', 690, '錯的位置剛好也是 D → 偵測不到', size=46, out=0))
    sc.add('說明：約 7–9%', 260, 310, caption('說明文字', 770, '單一突變約 7–9% 會碰巧對上', size=40, weight=400, color=MUTED, out=0))
    sc.add('結論：線索，不是結論', 380, 190, caption('結論文字', 880, [('工具的建議是', None), ('線索', ACCENT), ('，不是結論', None)], size=56, out=0))
    sc.source(0, 570, 'F8、F12')
    return sc


# ---------------------------------------------------------------- S6Outro
def s6():
    sc = Scene('S6Outro', '段 6｜結尾（設計腳本鏡頭 6-1、6-2）', 600, '// 事實來源：無新事實（回顧）')
    pill = centered({'fontFamily': SANS, 'fontSize': 52, 'fontWeight': 700, 'color': INK,
                     'boxShadow': '0 8px 30px rgba(0,0,0,0.06)'})
    sc.add('步驟 ①：先確認編號', 0, 600, box('步驟 1', 330, 320, 560, 150, radius=75, extra={
        **pill, 'opacity': raw(kf([0, 15], [0, 1])), 'translate': rise(20, 15)}, children=spans([('① ', ACCENT), ('先確認編號', None)], INK)))
    sc.add('箭頭', 60, 540, box('箭頭線', 910, 390, 100, 10, radius=5, bg=ACCENT, extra={
        'transformOrigin': 'left center', 'scale': raw(kf([0, 25], ['0 1', '1 1'], 'scale'))}))
    sc.add('步驟 ②：再看 pLDDT', 90, 510, box('步驟 2', 1030, 320, 560, 150, radius=75, extra={
        **pill, 'opacity': raw(kf([0, 15], [0, 1])), 'translate': rise(20, 15)}, children=spans([('② ', ACCENT), ('再看 pLDDT', None)], INK)))
    sc.add('網址', 300, 300, caption('網址文字', 600, 'github.com/wangnick1004/af-confidence', size=44, weight=500, out=0,
                                   extra={'fontFamily': MONO}))
    sc.add('說明：只做編號對應', 340, 260, caption('說明文字', 680, '只做編號對應，不判斷突變是否致病', size=38, weight=400, color=MUTED, out=0))
    sc.add('謝謝收看', 420, 180, caption('文字', 840, '謝謝收看', size=60, out=0))
    return sc


if __name__ == '__main__':
    only = set(sys.argv[1:])
    for make in (s1, s2, s4, s4tool, s5, s5tool, s6):
        sc = make()
        if only and sc.comp not in only:
            continue
        path = os.path.join(OUT, sc.comp + '.tsx')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(sc.render())
        print('wrote', os.path.relpath(path))
