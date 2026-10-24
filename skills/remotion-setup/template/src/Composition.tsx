import { Video } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/Inter";
import { ALL_FORMATS, Input, UrlSource } from "mediabunny";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Composition,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const { fontFamily } = loadFont("normal", { weights: ["400", "800"] });

const FPS = 30;

export type ReelProps = {
  // Cut video inside public/, e.g. "footage/my-video_cut.mp4". Leave empty for the placeholder slate.
  src: string;
  title: string;
  accent: string;
};

const calculateMetadata: CalculateMetadataFunction<ReelProps> = async ({
  props,
}) => {
  if (!props.src) {
    return { durationInFrames: 5 * FPS };
  }
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(staticFile(props.src)),
  });
  const seconds = await input.computeDuration();
  return { durationInFrames: Math.max(1, Math.ceil(seconds * FPS)) };
};

export const MyComposition = () => {
  return (
    <Composition
      id="Reel"
      component={Reel}
      durationInFrames={5 * FPS}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={{ src: "", title: "Drop a cut video in public/footage", accent: "#3B7BFF" }}
      calculateMetadata={calculateMetadata}
    />
  );
};

export const Reel: React.FC<ReelProps> = ({ src, title, accent }) => {
  if (src) {
    return (
      <AbsoluteFill style={{ backgroundColor: "black" }}>
        <Video src={staticFile(src)} />
      </AbsoluteFill>
    );
  }
  return <Slate title={title} accent={accent} />;
};

const Slate: React.FC<{ title: string; accent: string }> = ({
  title,
  accent,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 } });
  const y = interpolate(enter, [0, 1], [40, 0]);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0B0B0F",
        justifyContent: "center",
        alignItems: "center",
        fontFamily,
      }}
    >
      <div
        style={{
          opacity: enter,
          transform: `translateY(${y}px)`,
          textAlign: "center",
          padding: 80,
        }}
      >
        <div
          style={{
            color: accent,
            fontSize: 44,
            fontWeight: 800,
            letterSpacing: 6,
            textShadow: `0 0 40px ${accent}`,
          }}
        >
          REMOTION STUDIO
        </div>
        <div
          style={{ color: "#F4F4F6", fontSize: 64, fontWeight: 800, marginTop: 24 }}
        >
          {title}
        </div>
        <div style={{ color: "#8A8A99", fontSize: 36, marginTop: 24 }}>
          1080 × 1920 · 30 fps
        </div>
      </div>
    </AbsoluteFill>
  );
};
