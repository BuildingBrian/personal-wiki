"""Capture the three required Obsidian screenshots from the running Obsidian app.

Obsidian is an Electron app. Started with --remote-debugging-port it exposes the standard Chrome DevTools
interface, which can run Obsidian's own commands (open a note, open the graph) and ask the window to render
itself to a PNG. The pictures are Obsidian's real window contents, not a mock-up.

Start Obsidian:   /Applications/Obsidian.app/Contents/MacOS/Obsidian --remote-debugging-port=9222 &
Then run:         python scripts/obsidian_shots.py "<note title>"
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
OPEN = """
for (const leaf of app.workspace.getLeavesOfType('graph')) leaf.detach();
const wanted = %s;
const file = app.vault.getAbstractFileByPath(wanted) || app.metadataCache.getFirstLinkpathDest(wanted, '');
if (!file) return 'NOT FOUND: ' + wanted;
await app.workspace.getLeaf(false).openFile(file);
const leaf = app.workspace.getMostRecentLeaf();
const state = leaf.getViewState();
state.state = Object.assign({}, state.state, {mode: 'preview'});
await leaf.setViewState(state);
return leaf.view.file ? leaf.view.file.path : null;
"""
GRAPH = """
await app.commands.executeCommandById('graph:open');
await new Promise(r => setTimeout(r, 6000));
const leaf = app.workspace.getLeavesOfType('graph')[0];
return leaf ? JSON.stringify({filter: leaf.view.dataEngine ? leaf.view.dataEngine.getOptions().search : null,
                              nodes: leaf.view.renderer && leaf.view.renderer.nodes ? leaf.view.renderer.nodes.length : null}) : null;
"""


UNRESOLVED = """
const out = {};
for (const [source, targets] of Object.entries(app.metadataCache.unresolvedLinks)) {
  if ((source.startsWith('wiki/') || source === 'index.md') && Object.keys(targets).length) out[source] = Object.keys(targets);
}
return JSON.stringify(out);
"""


async def main(note):
    targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=5))
    target = next(t for t in targets if t["type"] == "page" and "obsidian.md" in t["url"])
    page = Page(await websocket_connect(target["webSocketDebuggerUrl"], max_message_size=200 * 1024 * 1024))
    await page.call("Emulation.setDeviceMetricsOverride", width=1500, height=1500, deviceScaleFactor=2, mobile=False)
    print("vault:", await page.js("return app.vault.getName() + ' · ' + app.vault.getMarkdownFiles().length + ' markdown files'"))
    await page.js(SETUP)
    print("opened:", await page.js(OPEN % json.dumps(note)))
    await asyncio.sleep(2)
    await page.shot("1-open-note-with-sources.png")
    print("opened:", await page.js(OPEN % json.dumps("index.md")))
    await asyncio.sleep(2)
    await page.shot("2-index-and-page-list.png")
    await page.call("Emulation.setDeviceMetricsOverride", width=1500, height=1000, deviceScaleFactor=2, mobile=False)
    print("unresolved links inside wiki/ and index.md, as Obsidian sees them:", await page.js(UNRESOLVED))
    print("graph:", await page.js(GRAPH))
    await page.shot("3-graph-view.png")
    await page.call("Emulation.clearDeviceMetricsOverride")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "index"))
