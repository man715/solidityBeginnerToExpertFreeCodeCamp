from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpfulScripts import getAccount, deployMocks, LOCALBLOCKCHAINENVIRONMENTS

def deployFundMe():
   account = getAccount() 
   # pass the price feed address to our fundme contract
   
   if network.show_active() not in LOCALBLOCKCHAINENVIRONMENTS:
       priceFeedAddress = config["networks"][network.show_active()]["eth_usd_price_feed"]
   else:
       deployMocks()
       priceFeedAddress = MockV3Aggregator[-1].address

   fundMe = FundMe.deploy(priceFeedAddress, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify"))
   print(f"Contract deployed to {fundMe.address}")

   return fundMe

def main():
    deployFundMe()
