#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
view = ROOT / "backend/views/payment-failed/index.php"
source = view.read_text()

unsafe = "Html::a($model->restaurant->name"
safe = "Html::a(Html::encode($model->restaurant->name)"

if unsafe in source:
    raise SystemExit("payment-failed index still renders raw restaurant names in links")

if safe not in source:
    raise SystemExit("payment-failed index does not encode restaurant link text")

print("Payment-failed index restaurant link text is encoded.")
