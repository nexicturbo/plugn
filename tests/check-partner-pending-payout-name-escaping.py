#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
view = ROOT / "partner/views/partner-payout/pending.php"
source = view.read_text()

unsafe = re.compile(
    r"<td>\s*<\?=\s*\$payment->restaurant->name\s*\?>\s*</td>",
    re.MULTILINE,
)
safe = re.compile(
    r"<td>\s*<\?=\s*Html::encode\s*\(\s*\$payment->restaurant->name\s*\)\s*\?>\s*</td>",
    re.MULTILINE,
)

if unsafe.search(source):
    raise SystemExit("partner pending payout table still prints raw restaurant names")

if not safe.search(source):
    raise SystemExit("partner pending payout table does not encode restaurant names")

print("Partner pending payout restaurant names are encoded.")
