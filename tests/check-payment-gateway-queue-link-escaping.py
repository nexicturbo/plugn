#!/usr/bin/env python3
from pathlib import Path


view = Path("backend/views/payment-gateway-queue/view.php")
source = view.read_text()

unsafe = "Html::a($data->restaurant->name"
safe = "Html::a(Html::encode($data->restaurant->name)"

if unsafe in source:
    raise SystemExit(f"{view}: restaurant link text is still unescaped")

if safe not in source:
    raise SystemExit(f"{view}: expected encoded restaurant link text guard")

print("Payment gateway queue restaurant link escaping guard passed.")
