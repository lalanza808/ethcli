import click
from hdwallet import BIP44HDWallet
from hdwallet.utils import generate_mnemonic
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation


@click.group()
def cli():
    pass

@cli.command('show_eth_address')
@click.argument('wallet_index')
@click.argument('mnemonic_seed', nargs=-1)
def show_eth_address(wallet_index, mnemonic_seed):
    mnemonic_seed = " ".join(mnemonic_seed)
    click.echo(get_eth_account(wallet_index, mnemonic_seed)[0])

@cli.command('show_eth_pkey')
@click.argument('wallet_index')
@click.argument('mnemonic_seed', nargs=-1)
def show_eth_pkey(wallet_index, mnemonic_seed):
    mnemonic_seed = " ".join(mnemonic_seed)
    click.echo(get_eth_account(wallet_index, mnemonic_seed)[1])

@cli.command('generate_seed')
def generate_seed():
    m = generate_mnemonic()
    click.echo(m)

def get_eth_account(account_index, mnemonic_seed:str):
    bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=mnemonic_seed, language="english", passphrase=None
    )
    bip44_hdwallet.clean_derivation()
    bip44_derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=account_index
    )
    bip44_hdwallet.from_path(path=bip44_derivation)
    public_address = bip44_hdwallet.address()
    private_key = '0x' + bip44_hdwallet.private_key()
    bip44_hdwallet.clean_derivation()
    return (public_address, private_key)

if __name__ == '__main__':
    cli()