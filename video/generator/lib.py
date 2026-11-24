# 產生「可在 Remotion Studio 編輯」的場景檔（.tsx）用的小工具。
#
# 只在第一次建立場景時使用：產生的 .tsx 裡所有數值都是固定值，
# 之後請直接在 Studio 或 .tsx 裡修改。重新執行產生器會覆蓋你在 Studio 的修改。
#
# 結構原則（與 HbSOpeningEditable 相同）：
# - 每個畫面元素包成一個有名字的 <Sequence>，在 Studio 時間軸上各自一條軌道
# - 元素內的動畫是關鍵影格 interpolate(frame, [...], [...])，影格從元素開始算起，
#   所以拖動元素時動畫跟著移動
# - 一段文字裡有不同顏色時拆成 Interactive.Span，每段文字都能在 Studio 直接改

BG = '#F6F4EF'
INK = '#1F2430'
MUTED = '#8A8F99'
ACCENT = '#2F6FEB'
GOOD = '#1E9E6A'
BAD = '#D9483B'
CARD = '#FFFFFF'
TERM_BG = '#1E2230'
TERM_INK = '#E6E9EF'
# pLDDT 顏色：AFDB 網站實際使用的色碼（F17）
P_VHIGH = '#0053D6'
P_HIGH = '#65CBF3'
P_LOW = '#FFDB13'
P_VLOW = '#FF7D45'

SANS = "'Noto Sans TC', sans-serif"
MONO = "'JetBrains Mono', monospace"
EASE = 'Easing.bezier(0.33, 0, 0.2, 1)'


def js(v):
    if isinstance(v, str):
        return ('"' + v + '"') if "'" in v else ("'" + v + "'")
    return repr(v)


def kf(frames, values, out=None):
    ease = ', '.join([EASE] * (len(frames) - 1))
    extra = ''
    if out == 'translate':
        extra = ", outputType: 'translate'"
    elif out == 'scale':
        extra = ", output: 'perceptual-scale', outputType: 'scale'"
    return (f"interpolate(frame, [{', '.join(map(str, frames))}], [{', '.join(js(v) for v in values)}], "
            f"{{extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: [{ease}]{extra}}})")


class raw(str):
    """A JS expression written verbatim."""


def fade(dur, inn=12, out=12):
    """淡入；out=0 表示不淡出。"""
    if out:
        return raw(kf([0, inn, dur - out, dur], [0, 1, 1, 0]))
    return raw(kf([0, inn], [0, 1]))


def rise(px=16, inn=12):
    return raw(kf([0, inn], [f'0px {px}px', '0px 0px'], 'translate'))


def style(d):
    if d.get('fontFamily') == MONO and 'fontVariantLigatures' not in d:
        d = {**d, 'fontVariantLigatures': 'none'}  # 等寬字型不合字（-> 保持原樣，和終端機一致）
    parts = []
    for k, v in d.items():
        parts.append(f"{k}: {v}" if isinstance(v, raw) else f"{k}: {js(v)}")
    return '{' + ', '.join(parts) + '}'


def tag(name, st, children='', el='Interactive.Div'):
    if children == '':
        return f'<{el} name="{name}" style={{{style(st)}}} />'
    return f'<{el} name="{name}" style={{{style(st)}}}>{children}</{el}>'


def jtext(t):
    """JSX 文字：含 < > { } 或換行時改寫成 {"..."}，避免語法錯誤與換行被吃掉。"""
    import json
    if any(c in t for c in '<>{}\n'):
        return '{' + json.dumps(t, ensure_ascii=False) + '}'
    return t


def spans(parts, base_color):
    """[(text, color or None), ...] → 每段一個可編輯的 Interactive.Span。"""
    out = []
    for i, (t, c) in enumerate(parts):
        out.append(f'<Interactive.Span name="文字片段 {i + 1}" style={{{{color: {js(c or base_color)}, whiteSpace: \'pre\'}}}}>{jtext(t)}</Interactive.Span>')
    return ''.join(out)


def text(name, x, y, txt, size=48, color=INK, weight=400, font=SANS, align='left', width=None, extra=None):
    st = {'position': 'absolute', 'left': x, 'top': y, 'fontFamily': font, 'fontSize': size,
          'fontWeight': weight, 'color': color, 'textAlign': align}
    if width is not None:
        st['width'] = width
    if extra:
        st.update(extra)
    children = spans(txt, color) if isinstance(txt, list) else jtext(txt)
    return tag(name, st, children)


def box(name, x, y, w, h, extra=None, children='', radius=18, bg=CARD):
    st = {'position': 'absolute', 'left': x, 'top': y, 'width': w, 'height': h,
          'borderRadius': radius, 'backgroundColor': bg}
    if extra:
        st.update(extra)
    return tag(name, st, children)


def centered(extra=None):
    st = {'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}
    if extra:
        st.update(extra)
    return st


def ring(name, x, y, w, h, color, dur, width=5, radius=18, pad=8):
    """聚焦框：淡入、放大一點、結尾淡出。"""
    return box(name, x - pad, y - pad, w + 2 * pad, h + 2 * pad, radius=radius + 4, bg='transparent', extra={
        'borderWidth': width, 'borderStyle': 'solid', 'borderColor': color,
        'opacity': raw(kf([0, 12, dur - 12, dur], [0, 1, 1, 0])),
        'scale': raw(kf([0, 12], ['1.08', '1'], 'scale')),
    })


class Scene:
    def __init__(self, comp, title, duration, header):
        self.comp = comp
        self.title = title
        self.duration = duration
        self.header = header
        self.components = []
        self.timeline = []
        self.names = set()

    def add(self, track, frm, dur, body, uses_frame=True):
        """新增一條軌道。body 是一個或多個 JSX 元素（字串或字串清單）。"""
        assert frm + dur <= self.duration, (track, frm, dur, self.duration)
        cname = f'El{len(self.components) + 1:02d}'
        if isinstance(body, (list, tuple)):
            body = '<>' + ''.join(body) + '</>'
        head = '  const frame = useCurrentFrame();\n' if uses_frame and 'frame' in body else ''
        self.components.append(f'// {track}\nconst {cname}: React.FC = () => {{\n{head}  return {body};\n}};\n')
        self.timeline.append((track, frm, dur, cname))

    def source(self, frm, dur, ids):
        self.add(f'來源標籤 {ids}', frm, dur, tag('來源文字', {
            'position': 'absolute', 'right': 48, 'bottom': 36, 'fontFamily': SANS, 'fontSize': 24, 'color': MUTED,
        }, f'來源 {ids}'), uses_frame=False)

    def render(self):
        const = self.comp.upper()
        out = [f'// {self.title}\n{self.header}\n//\n'
               '// 結構說明：每個畫面元素是一個獨立的 <Sequence>（時間軸上一條軌道）；\n'
               '// 元素裡的關鍵影格從元素開始算起；軌道越下面的畫在越上層。詳見 video/README.md。\n'
               "import {AbsoluteFill, Easing, Img, Interactive, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';\n"
               "import '../theme';\n\n"
               f'export const {const}_DURATION = {self.duration}; // {self.duration / 30:.1f} 秒 @ 30fps\n']
        out.extend(self.components)
        out.append(f'export const {self.comp}: React.FC = () => {{\n  return (\n    <AbsoluteFill>')
        out.append(f'      <Interactive.Div name="背景" from={{0}} durationInFrames={{{self.duration}}} '
                   f"style={{{{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, backgroundColor: '{BG}'}}}} />")
        for track, frm, dur, cname in self.timeline:
            out.append(f'      <Sequence name="{track}" from={{{frm}}} durationInFrames={{{dur}}}>\n        <{cname} />\n      </Sequence>')
        out.append('    </AbsoluteFill>\n  );\n};\n')
        return '\n'.join(out)
