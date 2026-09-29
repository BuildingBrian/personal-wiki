"""Capture the three required Obsidian screenshots from the running Obsidian app.

Obsidian is an Electron app. Started with --remote-debugging-port it exposes the standard Chrome DevTools
interface, which can run Obsidian's own commands (open a note, open the graph) and ask the window to render
itself to a PNG. The pictures are Obsidian's real window contents, not a mock-up.

Start Obsidian:   /Applications/Obsidian.app/Contents/MacOS/Obsidian --remote-debugging-port=9222 &
Then run:         python scripts/obsidian_shots.py "<note path>" "<related note title>" "<Source#Heading>"
Needs the 'tornado' package (any Jupyter environment has it).
"""
import asyncio
import base64
import json
import sys
import urllib.request
from pathlib import Path

from tornado.websocket import websocket_connect

OUT = Path(__file__).resolve().parents[1] / "evidence" / "obsidian"
PORT = 9222


class Page:
    def __init__(self, ws):
        self.ws, self.n = ws, 0

    async def call(self, method, **params):
        self.n += 1
        mine = self.n
        await self.ws.write_message(json.dumps({"id": mine, "method": method, "params": params}))
        while True:
            message = json.loads(await self.ws.read_message())
            if message.get("id") == mine:
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message.get("result", {})

    async def js(self, expression):
        result = await self.call("Runtime.evaluate", expression=f"(async () => {{ {expression} }})()",
                                 awaitPromise=True, returnByValue=True)
        if result.get("exceptionDetails"):
            raise RuntimeError(result["exceptionDetails"].get("exception", {}).get("description", "js error"))
        return result.get("result", {}).get("value")

    async def shot(self, name):
        data = await self.call("Page.captureScreenshot", format="png")
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / name
        path.write_bytes(base64.b64decode(data["data"]))
        print(f"saved {path.relative_to(OUT.parents[1])} ({path.stat().st_size // 1024} KB)")


SETUP = """
app.workspace.leftSplit.expand();
app.workspace.rightSplit.collapse();
await app.commands.executeCommandById('file-explorer:open');
const explorer = app.workspace.getLeavesOfType('file-explorer')[0];
if (explorer && explorer.view.tree && explorer.view.tree.setCollapseAll) explorer.view.tree.setCollapseAll(false);
"""
SHOW = """
// Open a file in the main tab, in reading view (or live preview for long originals), optionally at a heading.
const link = %s, source = %s, mode = %s;
const [name, heading] = link.split('#');
const file = app.vault.getAbstractFileByPath(name) || app.metadataCache.getFirstLinkpathDest(name, source);
if (!file) return 'NOT FOUND: ' + link;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const leaf = app.workspace.getMostRecentLeaf(app.workspace.rootSplit) || app.workspace.getLeaf(true);
await leaf.openFile(file, {state: {mode: mode, source: false}, eState: heading ? {subpath: '#' + heading} : {}});
app.workspace.setActiveLeaf(leaf, {focus: true});
await sleep(2500);
if (heading) { leaf.view.setEphemeralState({subpath: '#' + heading}); await sleep(3000); }
const seen = leaf.view.containerEl.innerText.replace(/\\s+/g, ' ').trim();
return file.path + (heading ? '#' + heading : '') + '  [' + seen.length + ' characters visible]';
"""
GRAPH = """
const plugin = app.internalPlugins.plugins.graph.instance;
Object.assign(plugin.options, {search: 'path:wiki/', showAttachments: false, showTags: false, showOrphans: true,
                               textFadeMultiplier: -3, nodeSizeMultiplier: 1.5, linkDistance: 260, repelStrength: 16,
                               'collapse-filter': false, 'collapse-color-groups': false, 'collapse-display': true});
await app.commands.executeCommandById('graph:open');
await new Promise(r => setTimeout(r, 7000));
const leaf = app.workspace.getLeavesOfType('graph')[0];
if (!leaf) return null;
const renderer = leaf.view.renderer;
renderer.zoomTo(0.78);
await new Promise(r => setTimeout(r, 2000));
renderer.setPan(renderer.panX - 330, renderer.panY + 40);      // keep the graph clear of the filter panel
await new Promise(r => setTimeout(r, 2000));
return JSON.stringify({filter: leaf.view.dataEngine.getOptions().search, attachments: leaf.view.dataEngine.getOptions().showAttachments,
                       nodes: Object.keys(leaf.view.renderer.nodeLookup || {}).length || (leaf.view.renderer.nodes || []).length});
"""


UNRESOLVED = """
const out = {};
for (const [source, targets] of Object.entries(app.metadataCache.unresolvedLinks)) {
  if ((source.startsWith('wiki/') || source === 'index.md') && Object.keys(targets).length) out[source] = Object.keys(targets);
}
return JSON.stringify(out);
"""


async def main(note, related, source_link):
    targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=5))
    target = next(t for t in targets if t["type"] == "page" and "obsidian.md" in t["url"])
    page = Page(await websocket_connect(target["webSocketDebuggerUrl"], max_message_size=200 * 1024 * 1024))
    tall = dict(width=1500, height=1560, deviceScaleFactor=2, mobile=False)
    wide = dict(width=1500, height=1000, deviceScaleFactor=2, mobile=False)

    async def capture(name, size, link, source="", mode="preview"):
        await page.call("Emulation.setDeviceMetricsOverride", **size)
        print("opened:", await page.js(SHOW % (json.dumps(link), json.dumps(source), json.dumps(mode))))
        await page.call("Page.bringToFront")
        await asyncio.sleep(1.5)
        await page.shot(name)

    print("vault:", await page.js("return app.vault.getName() + ' · ' + app.vault.getMarkdownFiles().length + ' markdown files'"))
    await page.js(SETUP)
    await capture("1-open-note-with-sources.png", tall, note)
    await capture("2-index-and-page-list.png", tall, "index.md")
    unresolved = await page.js(UNRESOLVED)
    print("unresolved links inside wiki/ and index.md, as Obsidian sees them:", unresolved)
    (OUT / "obsidian-unresolved-links.json").write_text(unresolved + "\n", encoding="utf-8")
    if related:
        await capture("4-related-note.png", tall, related, note)
    if source_link:
        await capture("5-original-source-passage.png", wide, source_link, related or note, "source")
    await page.call("Emulation.setDeviceMetricsOverride", **wide)
    print("graph:", await page.js(GRAPH))
    await page.call("Page.bringToFront")
    await asyncio.sleep(1.5)
    await page.shot("3-graph-view.png")
    await page.call("Emulation.clearDeviceMetricsOverride")


if __name__ == "__main__":
    args = sys.argv[1:] + [None, None, None]
    asyncio.run(main(args[0] or "index.md", args[1], args[2]))
