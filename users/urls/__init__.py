from .wallet_urls import wallet_url_patterns
from .payment_urls import payment_url_patterns
from .user_urls import user_url_patterns

urlpatterns = wallet_url_patterns + payment_url_patterns + user_url_patterns
