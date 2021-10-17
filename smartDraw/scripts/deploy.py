from brownue import draw
from scripts._functions import get_account, get_contract

def deployDraw():
    account = get_account(_id="metamask2")
    _draw = draw.deploy(get_contract())

def main():
    deployDraw()
