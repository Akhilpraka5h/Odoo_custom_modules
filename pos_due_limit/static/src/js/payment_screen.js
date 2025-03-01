import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { _t } from "@web/core/l10n/translation";
import { WarningDialog } from "@web/core/errors/error_dialogs";

patch(PaymentScreen.prototype, {
 async validateOrder() {
   const partner = this.currentOrder.get_partner();
   if (partner) {
     console.log(partner.name);
     if (partner.available_credit === undefined) {
       partner.available_credit = partner.credit_balance;
     }
     console.log(partner.available_credit, "available_credit");

     let totalCustomerAccountPayment = 0;
     for (const method of this.currentOrder.payment_ids) {
       console.log(method.get_amount(), method.payment_method_id.name);
       if (method.payment_method_id.name == "Customer Account") {
         totalCustomerAccountPayment += method.get_amount();
       }
     }

     if (totalCustomerAccountPayment > partner.available_credit) {
       this.dialog.add(WarningDialog, {
         title: _t("Not Enough Credit"),
         message: _t("Please Pay the Existing Bills or Increase Credit Limit"),
       });
       return;
     }

     partner.available_credit -= totalCustomerAccountPayment;
     console.log("Updated balance_credit:", partner.available_credit);
     super.validateOrder();
   } else {
     super.validateOrder();
   }
 },
});
