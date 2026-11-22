# Local File Tool Test Kit

Generate synthetic fixtures and check the result of a browser file workflow without using private data. The Python 3 generator uses only the standard library and no network.

```sh
python3 generate_fixtures.py fixtures
```

Use a fresh directory each time: the generator refuses to overwrite existing fixtures.

## Test cases

| Case | Procedure | Expected result |
| --- | --- | --- |
| Merge PDFs | In [ClearPDF Merge](https://www.openclawhirehuman.com/tools/merge-pdf) or [BentoPDF](https://www.bentopdf.com/merge-pdf), add `page-a.pdf` then `page-b.pdf`, combine and open the download. Repeat in reverse. | Exactly two pages, in the chosen order: PAGE A then PAGE B, and vice versa. |
| Compress PNG | Open `color-grid.png` in [Squoosh](https://squoosh.app/) or [FujinAI Image Compressor](https://www.fujindeai.com/tools/compress-image), fix output format and quality, and disable resizing. Save the output. | Visible color grid and 192 × 128 dimensions. Record the actual saved byte count. Smaller output is not a guarantee. |

## Check file handling

After loading the tool, clear the browser Network log, keep all request types visible, select the fixture, run the task, and download. Check request bodies and WebSocket traffic where applicable. Repeat with network disabled after dependencies have loaded. An offline success is evidence for those conditions only. A failure does not prove upload: a codec or script may still need to load. Do not publish raw logs containing headers or cookies.

Record the exact tool URL, test date, browser version, settings, output dimensions or PDF page order, and network observations. Say “No file transfer observed in this run” rather than asserting platform-wide privacy. The initial synthetic PDF and PNG generation was checked locally; the tool checks above are procedures, not claims that every linked tool was run.

Disclosure: repository maintainers are affiliated with ClearPDF and FujinAI. The same checks apply to all tools.
