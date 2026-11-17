// Ojos de la persona en cada cuadro (Vision), para quitar ojeras en piel.py.
// Uso: bin/ojos <carpeta de cuadros .jpg>  → una línea por cuadro: "n  ix0 ix1 iy0 iy1  dx0 dx1 dy0 dy1" (px, 0 = arriba;
// ojo izquierdo y derecho de la imagen) o "n -1" si no hay cara
import Foundation
import Vision
import ImageIO

let dir = CommandLine.arguments[1]
let fs = (try! FileManager.default.contentsOfDirectory(atPath: dir)).filter { $0.hasSuffix(".jpg") }.sorted()
for f in fs {
  let n = Int(f.prefix(5))!
  guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: dir + "/" + f) as CFURL, nil),
        let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("\(n) -1"); continue }
  let W = Double(img.width), H = Double(img.height)
  let req = VNDetectFaceLandmarksRequest()
  try? VNImageRequestHandler(cgImage: img, options: [:]).perform([req])
  guard let cara = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }), let lm = cara.landmarks,
        let a = lm.leftEye, let b = lm.rightEye else { print("\(n) -1"); continue }
  func caja(_ r: VNFaceLandmarkRegion2D) -> [Double] {
    let p = r.pointsInImage(imageSize: CGSize(width: W, height: H)).map { (Double($0.x), H - Double($0.y)) }
    return [p.map { $0.0 }.min()!, p.map { $0.0 }.max()!, p.map { $0.1 }.min()!, p.map { $0.1 }.max()!]
  }
  let ojos = [caja(a), caja(b)].sorted { $0[0] < $1[0] }
  print("\(n) " + (ojos[0] + ojos[1]).map { String(format: "%.1f", $0) }.joined(separator: " "))
}
