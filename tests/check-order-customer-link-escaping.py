#!/usr/bin/env python3
from pathlib import Path


views = [
    Path("backend/views/order/draft.php"),
    Path("backend/views/order/abandoned-checkout.php"),
]

unsafe = "Html::a($data->customer->customer_name"
safe = "Html::a(Html::encode($data->customer->customer_name)"

for view in views:
    source = view.read_text()
    if unsafe in source:
        raise SystemExit(f"{view}: customer link text is still unescaped")
    if safe not in source:
        raise SystemExit(f"{view}: expected encoded customer link text guard")

print("Order customer link escaping guard passed.")
