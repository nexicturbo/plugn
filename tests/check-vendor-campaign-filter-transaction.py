#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
controller = root / "backend/controllers/VendorCampaignController.php"
source = controller.read_text()

assert "$filtersSaved = true;" in source
assert "$filtersSaved = false;" in source
assert "Yii::$app->request->post('CampaignFilter', [])" in source
assert "foreach ($cf->getFirstErrors() as $error)" in source
assert "foreach ($model->getFirstErrors() as $error)" in source
assert "if ($filtersSaved) {\n                    $transaction->commit();" in source
assert "if ($transaction->isActive) {\n                $transaction->rollBack();" in source
assert "$transaction->rollBack();\n                        break;" not in source

commit_index = source.index("$transaction->commit();")
redirect_index = source.index("return $this->redirect(['view', 'id' => $model->campaign_uuid]);")
rollback_index = source.index("if ($transaction->isActive)")

assert commit_index < redirect_index < rollback_index

print("Vendor campaign filter transaction guard passed.")
