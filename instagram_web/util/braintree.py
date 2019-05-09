import braintree
from config import BT_MERCHANT_KEY, BT_PRIVATE_KEY, BT_PUBLIC_KEY


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id=BT_MERCHANT_KEY,
        public_key=BT_PUBLIC_KEY,
        private_key=BT_PRIVATE_KEY)
)


def generate_client_token():
    return gateway.client_token.generate()


def complete_transaction():
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settelement": True
        }
    })
