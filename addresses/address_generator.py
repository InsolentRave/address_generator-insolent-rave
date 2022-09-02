from django.conf import settings
from hdwallet import BIP32HDWallet, BIP44HDWallet
from hdwallet.symbols import BTC, ETH, LTC, TRX

from .errors import AddressPathError, NotSupportedCurrency, PrivateKeyError

symbol_to_wallet_factory = {
    'BTC': lambda: BIP32HDWallet(symbol=BTC),
    'ETH': lambda: BIP44HDWallet(symbol=ETH),
    'LTC': lambda: BIP32HDWallet(symbol=LTC),
    'TRX': lambda: BIP32HDWallet(symbol=TRX),
}


def generate_address(symbol, path):
    try:
        wallet = symbol_to_wallet_factory[symbol]()
    except KeyError:
        raise NotSupportedCurrency(symbol)

    set_path(wallet, path)
    return wallet.address()


def set_path(wallet, path):
    try:
        wallet.from_xprivate_key(xprivate_key=settings.ZEPLY_XPRIVATE_KEY, strict=True)

    except ValueError as exc:
        raise PrivateKeyError(exc)

    try:
        wallet.from_path(path)
    except Exception as exc:
        raise AddressPathError(exc)
