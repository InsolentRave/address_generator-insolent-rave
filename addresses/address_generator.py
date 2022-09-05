from django.conf import settings
from hdwallet import BIP32HDWallet, BIP44HDWallet
from hdwallet.symbols import BTC, ETH, LTC, TRX

from .errors import AddressPathError, NotSupportedCurrency, PrivateKeyError


# Factories for each symbol to create basic wallet object:
symbol_to_wallet_factory = {
    'BTC': lambda: BIP32HDWallet(symbol=BTC),
    'ETH': lambda: BIP44HDWallet(symbol=ETH),
    'LTC': lambda: BIP32HDWallet(symbol=LTC),
    'TRX': lambda: BIP32HDWallet(symbol=TRX),
}


def generate_address(symbol, path):
    """
    Generates the address from a currency symbol and a path.
    """
    try:
        wallet = symbol_to_wallet_factory[symbol]()
    except KeyError:
        raise NotSupportedCurrency(symbol)

    set_private_key(wallet, path)
    # Generate the address from the child private key
    return wallet.address()


def set_private_key(wallet, path):
    """
    Sets the child private key of the wallet based on the key path.
    """
    try:
        # Sets the master private key of the wallet:
        wallet.from_xprivate_key(xprivate_key=settings.ZEPLY_XPRIVATE_KEY, strict=True)

    except ValueError as exc:
        raise PrivateKeyError(exc)

    try:
        # Selects the child private key for generating the address based on the path:
        wallet.from_path(path)
    except Exception as exc:
        raise AddressPathError(exc)
