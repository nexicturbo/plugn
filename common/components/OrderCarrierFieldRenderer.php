<?php

namespace common\components;

use yii\helpers\Html;
use yii\helpers\Url;

class OrderCarrierFieldRenderer
{
    public static function trackingLink($url)
    {
        if ($url === null || $url === '') {
            return null;
        }

        $scheme = strtolower((string) parse_url($url, PHP_URL_SCHEME));
        if (!in_array($scheme, ['http', 'https'], true)) {
            return Html::encode($url);
        }

        return Html::a(Html::encode($url), Url::to($url, true), [
            'target' => '_blank',
            'rel' => 'noopener noreferrer',
        ]);
    }
}
