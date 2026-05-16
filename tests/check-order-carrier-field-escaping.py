from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORDER_VIEWS = [
    ROOT / "backend/views/order/view.php",
    ROOT / "frontend/views/order/view.php",
]


def assert_contains(content: str, needle: str, path: Path) -> None:
    assert needle in content, f"{path} is missing {needle!r}"


def assert_not_contains(content: str, needle: str, path: Path) -> None:
    assert needle not in content, f"{path} still contains unsafe pattern {needle!r}"


for view_path in ORDER_VIEWS:
    content = view_path.read_text(encoding="utf-8")

    assert_contains(content, "Html::encode($url)", view_path)
    assert_contains(content, "parse_url($url, PHP_URL_SCHEME)", view_path)
    assert_contains(content, "in_array($scheme, ['http', 'https'], true)", view_path)
    assert_contains(content, "'rel' => 'noopener noreferrer'", view_path)
    assert_contains(content, "Html::encode($data->armada_order_status)", view_path)
    assert_contains(content, "Html::encode($data->mashkor_order_number)", view_path)
    assert_contains(
        content,
        "Html::encode(Yii::$app->mashkorDelivery->getOrderStatus($data->mashkor_order_status))",
        view_path,
    )
    assert_contains(content, "Html::encode($data->mashkor_driver_phone)", view_path)

    assert_not_contains(content, "Html::a($data->armada_tracking_link", view_path)
    assert_not_contains(content, "Html::a($data->armada_delivery_code", view_path)
    assert_not_contains(content, "Html::a($data->mashkor_tracking_link", view_path)
    assert_not_contains(
        content,
        ". $data->armada_order_status .",
        view_path,
    )
    assert_not_contains(
        content,
        "? $data->mashkor_order_number : null",
        view_path,
    )
    assert_not_contains(
        content,
        ". Yii::$app->mashkorDelivery->getOrderStatus($data->mashkor_order_status) .",
        view_path,
    )
    assert_not_contains(
        content,
        "? $data->mashkor_driver_phone : null",
        view_path,
    )

print("order carrier field escaping guard passed")
