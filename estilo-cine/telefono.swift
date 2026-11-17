// Candidatos a pantalla de celular (rectángulos) en cada cuadro, con Vision. El que sí es se elige en Python (oscuro, sigue al anterior).
// Uso: bin/telefono <carpeta de cuadros> <desde n> <hasta n>  → por cuadro: "n  x0 y0 x1 y1 x2 y2 x3 y3 conf | ..." (px, 0 = arriba;
// esquinas: arriba-izq, arriba-der, abajo-der, abajo-izq)
import Foundation
import Vision
import ImageIO

let a = CommandLine.arguments
let dir = a[1], n0 = Int(a[2])!, n1 = Int(a[3])!
for n in n0...n1 {
  let f = dir + "/" + String(format: "%05d.jpg", n)
  guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: f) as CFURL, nil),
        let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
  let W = Double(img.width), H = Double(img.height)
  let r = VNDetectRectanglesRequest()
  r.minimumAspectRatio = 0.3; r.maximumAspectRatio = 0.7; r.minimumSize = 0.06; r.maximumObservations = 12
  r.quadratureTolerance = 25; r.minimumConfidence = 0.3
  try? VNImageRequestHandler(cgImage: img, options: [:]).perform([r])
  var out: [String] = []
  for o in r.results ?? [] {
    let pts = [o.topLeft, o.topRight, o.bottomRight, o.bottomLeft].map { String(format: "%.1f %.1f", Double($0.x) * W, (1 - Double($0.y)) * H) }
    out.append(pts.joined(separator: " ") + String(format: " %.2f", o.confidence))
  }
  print("\(n) " + out.joined(separator: " | ")); fflush(stdout)
}
