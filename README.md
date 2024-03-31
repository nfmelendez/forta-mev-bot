# MEV Bot detector

## Description

This bot detects MEV bots that uses different strategies to extract value from a protocol by adding, removing or reordening transactions in a block 

## Supported Chains

- All EVM compatible chains

## Checkout the MEV alerts

[MEV bot Forta Explorer](https://app.forta.network/bot/0x5bb675492f3accba1d35e7f59f584b6fae11df919f13223f3056a69dc5686b4b)


## Supported Strategies

### Sandwich

 A Sandwich MEV strategy involves strategically placing buy and sell orders around a victim transaction in order to profit from the price movement that the victim transaction generates.

#### Steps to capture value:
1. Search for a swap with high slippage, will be the victim transaction
2. Using AMM formula predict the price after transaction
3. Create a Flashbot bundle, add a buy transaction first, then in the middle copy the victim transaction and after the sell transaction. All the price manipulation must not superate the slippage that the victim configured
4. Profit will be the difference between buy cheap and sell expensive. 

#### Alert

- MEV-SANDWICH-BOT-IDENTIFIED
    - Fired when a sandwich attack is executed: exist an attack front and back transaction and a victim sandwich transactions.
    - Severity: "Info"
    - Type: "Info"
    - Metadata:
        - `sandwicher_address`: attacker address 
        - `block_builder`: Name of the block builder(ex Flashbots) or None 
        -  `profits`: it s a list of
            - `profit_amount`: Profit amount extracted by the attacker
            - `profit_token_address`: Profit asset
        - `assets`: list of assets involved in the sandwich
        - `flashloan`: true if arbitrage used a flashloan
        - `evidence`
          - `frontrun_transaction`: Attacker transaction in front of the victim
          - `backrun_transaction`: Attacker transaction back of the victim
          - `list_sandwich_transactions`: victims's sandwiched transaction
          - `flashloan`: if a flashloan exist, describe asset, amount and protocol


#### Labels
- Sandwicher
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The Sandwicher contract address
    - `confidence`:  1
    - `metadata`:
        - `description`: Sandwicher contract 


- Sandwicher Owner
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The Sandwicher Owner address
    - `confidence`:  1
    - `metadata`:
        - `description`: Sandwicher Owner 


### Arbitrage

 A Arbitrage is exploiting price differences of the same or similar assets in same or different venues

#### Steps to capture value:
1. Search for an asset price discrepancy in different or same venue
2. Buy cheap in one place and sell in another in order to profit


#### Alert
- MEV-ARBITRAGE-BOT-IDENTIFIED
    - Fired when a arbitrage is executed doing swaps of token in one or many exchanges in order to profit from the price difference
    - Severity: "Info"
    - Type: "Info"
    - Metadata:
        - `mev_bot_address`: Arbitrage MEV bot address 
        - `mev_bot_owner_address`: Owner EOA of the Arbitrage bot 
        - `block_builder`: Name of the block builder(ex Flashbots) or None 
        - `profit_amount`: Profit amount extracted by the attacker
        - `profit_token_address`: Profit asset
        - `assets`: list of assets involved in the arbitrage, can be tokens or NFTs with their token id
        - `asset_types`: which type of assets are involved in the arbitrage, cab be: TOKEN, NFT or TOKEN-NFT
        - `evidence`
          - `start_amount`: Amount of profit token when started the swap chain
          - `end_amount`: Amount of profit token when finished the swap chain


#### Labels
- Arbitrage Bot
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The Arbitrage bot contract address
    - `confidence`:  1
    - `metadata`:
        - `description`: Arbitrage Bot contract 


- Arbitrage Bot Owner
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The arbitrage bot Owner address
    - `confidence`:  1
    - `metadata`:
        - `description`: Arbitrage bot Owner 




### Liquidation

 Are bots that monitor the heal factor of debts, if one bad is detected it repays and profit from the collateral. 

#### Steps to capture value:
1. Search for a debt with bad health factor
2. Flashloan debt asset (not mandatory)
3. Liquidate the bad debt position in exchange for collateral asset
4. Swap part (or all if you want profit in debt asset) of collateral asset to repay flashLoan(if the case apply).
5. The remaining asset is profit
 


#### Alert
- MEV-LIQUIDATION-BOT-IDENTIFIED
    - Fired when a liquidation of debt is detected
    - Severity: "Info"
    - Type: "Info"
    - Metadata:
        - `liquidator_bot`: Arbitrage MEV bot address 
        - `liquidator_bot_owner`: Owner EOA of the Arbitrage bot 
        - `liquidated_user`: Name of the block builder(ex Flashbots) or None 
        - `block_builder_name`: Profit amount extracted by the attacker
        - `evidence`
          - `debt_token_address`: Profit asset
          - `debt_purchase_amount`: list of assets involved in the arbitrage
          - `received_token_address`: list of assets involved in the arbitrage
          - `received_amount`: list of assets involved in the arbitrage
          - `receive_a_token`: list of assets involved in the arbitrage


#### Labels
- Liquidation Bot
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The Liquidation bot contract address
    - `confidence`:  1
    - `metadata`:
        - `description`: Liquidation Bot contract 


- Liquidation Bot Owner
    - `entityType`: EntityType.Address
    - `label`: MEV
    - `entity`: The liquidation bot owner address
    - `confidence`:  1
    - `metadata`:
        - `description`: Liquidation bot owner 