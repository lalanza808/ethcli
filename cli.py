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

@cli.command('create_wallet')
def create_wallet():
    m = generate_mnemonic()
    k = get_eth_account(m, 0, 0)
    click.echo(f'Mnemonic: {m}')
    click.echo(f'Privkey: {k[1]}')
    click.echo(f'Pubkey: {k[0]}')

def get_eth_account(mnemonic_seed:str, address_index:int=0, account_index:int=0):
    bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=mnemonic_seed, language="english", passphrase=None
    )
    bip44_hdwallet.clean_derivation()
    bip44_derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=account_index, change=False, address=address_index
    )
    bip44_hdwallet.from_path(path=bip44_derivation)
    public_address = bip44_hdwallet.address()
    private_key = '0x' + bip44_hdwallet.private_key()
    bip44_hdwallet.clean_derivation()
    return (public_address, private_key)

if __name__ == '__main__':
    cli()


# connect to ETH provider
# generate list of N addresses stemming from a root private key
# sign and send transactions to network across N addresses
