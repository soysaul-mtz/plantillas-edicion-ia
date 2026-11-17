// Apertura de la boca de la persona a cámara, cuadro por cuadro (Vision), para saber quién habla (ella o alguien fuera de cuadro).
// Uso: bin/boca video.mov [paso=0.0333] [desde] [hasta]  → una línea por muestra: "t apertura" (alto de labios internos / ancho de la cara; -1 sin cara)
import Foundation
import AVFoundation
import Vision

let a = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let paso = a.count > 2 ? Double(a[2])! : 1.0 / 30
let dur = a.count > 4 ? Double(a[4])! : CMTimeGetSeconds(asset.duration)
let gen = AVAssetImageGenerator(asset: asset); gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
gen.maximumSize = CGSize(width: 1080, height: 1920)
var t = a.count > 3 ? Double(a[3])! : 0.0
while t < dur {
  var v = -1.0
  if let img = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil) {
    let req = VNDetectFaceLandmarksRequest()
    try? VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
    if let c = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }), let lab = c.landmarks?.innerLips {
      let p = lab.normalizedPoints.map { Double($0.y) }
      v = (p.max()! - p.min()!) * Double(c.boundingBox.height) / Double(c.boundingBox.width)
    }
  }
  print(String(format: "%.3f %.4f", t, v)); fflush(stdout)
  t += paso
}
