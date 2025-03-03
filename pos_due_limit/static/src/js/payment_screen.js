import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PaymentScreen.prototype, {
  async validateOrder() {
    const partner = this.currentOrder.get_partner();
    if (partner) {
      if (partner.available_credit === undefined) {
        partner.available_credit = partner.credit_balance;
      }
      let totalCustomerAccountPayment = 0;
      for (const method of this.currentOrder.payment_ids) {
        if (method.payment_method_id.name == "Customer Account") {
          totalCustomerAccountPayment += method.get_amount();
        }
      }
      if (totalCustomerAccountPayment > partner.available_credit) {
        this.dialog.add(AlertDialog, {
          body: _t("Please Pay the Existing Bills or Increase Credit Limit"),
        });
        return;
      }
      partner.available_credit -= totalCustomerAccountPayment;
      super.validateOrder();
    } else {
      super.validateOrder();
    }
  },
});
