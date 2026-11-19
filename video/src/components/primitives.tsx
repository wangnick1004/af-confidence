import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

// 0→1 的柔和進場，從第 start 格開始
export const useEnter = (start: number, durationInFrames = 20) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - start, fps, config: theme.spring, durationInFrames});
};

// 在 [from, to] 這段時間內可見，前後各有淡入淡出
export const useWindow = (from: number, to: number, fade = 12) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [from, from + fade, to - fade, to], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// 畫面下方的一句話字幕：一次只出現一句
export const Caption: React.FC<{from: number; to: number; children: React.ReactNode}> = ({
  from,
  to,
  children,
}) => {
  const o = useWindow(from, to);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 150,
        textAlign: 'center',
        fontFamily: theme.font.sans,
        fontSize: 54,
        fontWeight: 700,
        color: theme.color.ink,
        opacity: o,
        transform: `translateY(${(1 - o) * 16}px)`,
      }}
    >
      {children}
    </div>
  );
};

// 右下角的來源標籤，方便校對（正式版可關掉）
export const SourceTag: React.FC<{ids: string}> = ({ids}) => (
  <div
    style={{
      position: 'absolute',
      right: 48,
      bottom: 36,
      fontFamily: theme.font.sans,
      fontSize: 24,
      color: theme.color.muted,
    }}
  >
    來源 {ids}
  </div>
);
