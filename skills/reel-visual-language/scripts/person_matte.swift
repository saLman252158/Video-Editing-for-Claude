// Person matte for "text behind the speaker" (macOS 12+, Apple Vision, no installs).
// Writes one grayscale PNG per frame (white = person) to <outdir>/m_00001.png ...
// Usage: swiftc -O person_matte.swift -o person_matte && ./person_matte in.mp4 outdir [quality: fast|balanced|accurate]
import AVFoundation
import Vision
import CoreImage
import Foundation

let args = CommandLine.arguments
guard args.count >= 3 else { print("usage: person_matte in.mp4 outdir [fast|balanced|accurate]"); exit(1) }
let outDir = URL(fileURLWithPath: args[2])
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let track = asset.tracks(withMediaType: .video)[0]
let reader = try! AVAssetReader(asset: asset)
let output = AVAssetReaderTrackOutput(track: track, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
reader.add(output); reader.startReading()

let req = VNGeneratePersonSegmentationRequest()
req.qualityLevel = (args.count > 3 ? args[3] : "accurate") == "fast" ? .fast : ((args.count > 3 && args[3] == "balanced") ? .balanced : .accurate)
req.outputPixelFormat = kCVPixelFormatType_OneComponent8
let ctx = CIContext()
let gray = CGColorSpaceCreateDeviceGray()
var n = 0
while let sb = output.copyNextSampleBuffer(), let px = CMSampleBufferGetImageBuffer(sb) {
  n += 1
  let h = VNImageRequestHandler(cvPixelBuffer: px, orientation: .up)
  try? h.perform([req])
  guard let m = req.results?.first?.pixelBuffer else { continue }
  // scale the low-res mask up to the frame size
  var mask = CIImage(cvPixelBuffer: m)
  let W = CGFloat(CVPixelBufferGetWidth(px)), H = CGFloat(CVPixelBufferGetHeight(px))
  mask = mask.transformed(by: CGAffineTransform(scaleX: W / mask.extent.width, y: H / mask.extent.height))
  let url = outDir.appendingPathComponent(String(format: "m_%05d.png", n))
  try! ctx.writePNGRepresentation(of: mask, to: url, format: .L8, colorSpace: gray)
}
print("frames:", n)
