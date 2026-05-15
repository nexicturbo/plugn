#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
view = ROOT / "backend/views/payment-failed/index.php"
source = view.read_text()

unsafe = re.compile(r"Html::a\s*\(\s*\$model->restaurant->name\b")
safe = re.compile(
    r"Html::a\s*\(\s*Html::encode\s*\(\s*\$model->restaurant->name\s*\)"
)

if unsafe.search(source):
    raise SystemExit("payment-failed index still renders raw restaurant names in links")

if not safe.search(source):
    raise SystemExit("payment-failed index does not encode restaurant link text")

print("Payment-failed index restaurant link text is encoded.")
