#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
payment_failed_view = root / "backend/views/payment-failed/view.php"
order_view = root / "backend/views/order/view.php"

payment_failed = payment_failed_view.read_text()
order = order_view.read_text()

assert "function paymentFailedResponseText($response)" in payment_failed
assert "Html::encode(paymentFailedResponseText($model->response))" in payment_failed
assert "return $model->response;" not in payment_failed
assert "return print_r(unserialize($model->response), true);" not in payment_failed

assert "Html::encode($paymentFail->response)" in order
assert "print_r($paymentFail->response)" not in order
assert "<pre> <?php print_r($paymentFail->response) ?></pre>" not in order

print("Payment failure response escaping guard passed.")
