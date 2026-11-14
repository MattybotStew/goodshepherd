// Renders pages in WKWebView (Safari's engine), runs a measurement script, saves full-page PNGs.
// usage: wkrun <measure.js> <outdir> <width> <url> [<url>...]
import AppKit
import WebKit

final class Runner: NSObject, WKNavigationDelegate {
    let js: String, outDir: String, width: CGFloat
    var urls: [String]
    var web: WKWebView!
    var window: NSWindow!
    var current = ""
    var navDone: CheckedContinuation<Void, Never>?

    init(js: String, outDir: String, width: CGFloat, urls: [String]) {
        self.js = js; self.outDir = outDir; self.width = width; self.urls = urls
        super.init()
        let cfg = WKWebViewConfiguration()
        cfg.websiteDataStore = .nonPersistent()
        web = WKWebView(frame: NSRect(x: 0, y: 0, width: width, height: 900), configuration: cfg)
        web.navigationDelegate = self
        web.customUserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.2 Safari/605.1.15"
        window = NSWindow(contentRect: NSRect(x: -20000, y: 0, width: width, height: 900), styleMask: [.borderless], backing: .buffered, defer: false)
        window.contentView = web
        window.orderBack(nil)
    }
    func webView(_ w: WKWebView, didFinish n: WKNavigation!) { navDone?.resume(); navDone = nil }
    func webView(_ w: WKWebView, didFail n: WKNavigation!, withError e: Error) { print("\(Int(width)) \(current) NAVFAIL \(e.localizedDescription)"); navDone?.resume(); navDone = nil }
    func webView(_ w: WKWebView, didFailProvisionalNavigation n: WKNavigation!, withError e: Error) { print("\(Int(width)) \(current) NAVFAIL \(e.localizedDescription)"); navDone?.resume(); navDone = nil }

    @MainActor func run() async {
        for u in urls {
            current = u
            await withCheckedContinuation { c in navDone = c; web.load(URLRequest(url: URL(string: u)!)) }
            try? await Task.sleep(nanoseconds: 2_000_000_000)
            do {
                let r = try await web.callAsyncJavaScript(js, arguments: [:], in: nil, contentWorld: .page)
                let path = URL(string: u)!.path
                print(String(format: "%-5d %-36@ %@", Int(width), path as NSString, (r as? String ?? "") as NSString))
            } catch { print("\(Int(width)) \(u) JSERR \(error)") }
            // full-page snapshot
            if let hAny = try? await web.evaluateJavaScript("document.documentElement.scrollHeight"), let h = hAny as? Double {
                let cfg = WKSnapshotConfiguration()
                web.setFrameSize(NSSize(width: width, height: min(h, 16000)))
                try? await Task.sleep(nanoseconds: 700_000_000)
                cfg.rect = NSRect(x: 0, y: 0, width: width, height: min(h, 16000))
                cfg.afterScreenUpdates = true
                if let img = try? await web.takeSnapshot(configuration: cfg),
                   let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
                   let png = rep.representation(using: .png, properties: [:]) {
                    let name = URL(string: u)!.path.replacingOccurrences(of: "/", with: "_")
                    try? png.write(to: URL(fileURLWithPath: "\(outDir)/\(Int(width))\(name).png"))
                }
                web.setFrameSize(NSSize(width: width, height: 900))
            }
            try? await Task.sleep(nanoseconds: 1_500_000_000)
        }
        fflush(stdout); exit(0)
    }
}

setvbuf(stdout, nil, _IOLBF, 0)
let a = CommandLine.arguments
let js = try! String(contentsOfFile: a[1], encoding: .utf8)
let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let runner = Runner(js: js, outDir: a[2], width: CGFloat(Double(a[3])!), urls: Array(a[4...]))
Task { @MainActor in await runner.run() }
app.run()
