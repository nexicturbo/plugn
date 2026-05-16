<?php

use yii\helpers\Html;
use yii\widgets\DetailView;

/* @var $this yii\web\View */
/* @var $model common\models\PaymentFailed */

$this->title = $model->payment_failed_uuid;
$this->params['breadcrumbs'][] = ['label' => Yii::t('app', 'Payment Faileds'), 'url' => ['index']];
$this->params['breadcrumbs'][] = $this->title;
\yii\web\YiiAsset::register($this);

function tryUnserializePaymentFailedResponse($response, &$decoded) {
    if (!is_string($response)) {
        return false;
    }

    set_error_handler(function ($severity, $message, $file, $line) {
        throw new ErrorException($message, 0, $severity, $file, $line);
    });

    try {
        $decoded = unserialize($response, ['allowed_classes' => false]);
        return $decoded !== false || $response === 'b:0;';
    } catch (Throwable $e) {
        $decoded = null;
        return false;
    } finally {
        restore_error_handler();
    }
}

function paymentFailedResponseText($response) {
    if (tryUnserializePaymentFailedResponse($response, $decoded)) {
        return print_r($decoded, true);
    }

    return (string) $response;
}

?>
<div class="payment-failed-view">

    <h1><?= Html::encode($this->title) ?></h1>

    <p>
        <?= Html::a(Yii::t('app', 'Update'), ['update', 'id' => $model->payment_failed_uuid], ['class' => 'btn btn-primary']) ?>
        <?= Html::a(Yii::t('app', 'Delete'), ['delete', 'id' => $model->payment_failed_uuid], [
            'class' => 'btn btn-danger',
            'data' => [
                'confirm' => Yii::t('app', 'Are you sure you want to delete this item?'),
                'method' => 'post',
            ],
        ]) ?>
    </p>

    <?= DetailView::widget([
        'model' => $model,
        'attributes' => [
            'payment_failed_uuid',

            [
                'attribute' => 'payment_uuid',
                "format" => "raw",
                'value' => function ($model) {

                    return Html::a($model->payment_uuid, \yii\helpers\Url::to(['payment/view', 'id' => $model->payment_uuid]), [
                        "target" => "_blank"
                    ]);
                }
            ],

            [
                'attribute' => 'order_uuid',
                "format" => "raw",
                'value' => function ($model) {
                    return Html::a($model->order_uuid, \yii\helpers\Url::to(['order/view', 'id' => $model->order_uuid]), [
                        "target" => "_blank"
                    ]);
                }
            ],
            'customer_id',
            [
                'attribute' => 'restaurantName',
                "format" => "raw",
                'value' => function ($model) {
                    if($model->restaurant) {
                        return Html::a($model->restaurant->name, \yii\helpers\Url::to(['restaurant/view', 'id' => $model->order->restaurant_uuid]), [
                            "target" => "_blank"
                        ]);
                    }
                }
            ],
            [
                'attribute' => 'response',
                "format" => "raw",
                'value' => function ($model) {
                    return Html::tag('pre', Html::encode(paymentFailedResponseText($model->response)), [
                        'class' => 'payment-failed-response',
                    ]);
                }
            ],
            'created_at',
            'updated_at',
        ],
    ]) ?>

</div>
