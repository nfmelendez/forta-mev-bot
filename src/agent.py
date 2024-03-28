from forta_agent import Finding, FindingType, FindingSeverity, TransactionEvent, BlockEvent, EntityType
import pickle
import logging
import sys
from typing import List
from flatten_json import flatten
import time
from itertools import groupby
from typing import Dict, List


EXPIRATION_WINDOW_SECONDS = 24*60*60 # a day

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

CACHE = {}

try:
    from src.schemas.mev_block import MevBlock
    from src.classifiers.event import EventLogClassifier
    from src.swaps import get_swaps
    from src.sandwiches import get_sandwiches
    from src.schemas.sandwiches import Sandwich
    from src.arbitrages import get_arbitrages
    from src.schemas.arbitrages import Arbitrage
    from src.schemas.swaps import Swap
    from src.liquidations import get_liquidations
    from src.schemas.liquidations import Liquidation
    from src.flashloans import get_flashloans
    from src.block_builder import get_block_builder
    from src.schemas.block_builder import BlockBuilder
    from src.config.constants import DUMP_BLOCK
except ModuleNotFoundError:
    from schemas.mev_block import MevBlock
    from classifiers.event import EventLogClassifier
    from swaps import get_swaps
    from sandwiches import get_sandwiches
    from schemas.sandwiches import Sandwich
    from arbitrages import get_arbitrages
    from schemas.arbitrages import Arbitrage
    from schemas.swaps import Swap
    from liquidations import get_liquidations
    from schemas.liquidations import Liquidation
    from flashloans import get_flashloans
    from block_builder import get_block_builder
    from schemas.block_builder import BlockBuilder
    from config.constants import DUMP_BLOCK

class MEVBot:

    last_block:MevBlock = MevBlock()
    classifier = EventLogClassifier()

    def reset_cache(self):
        CACHE.clear()

    def utility_provide_handle_transaction(self, transaction_event: TransactionEvent):
        output = open(transaction_event.hash + '.pkl', 'wb')
        pickle.dump(transaction_event, output)
        return []
    
    def provide_handle_transaction(self, transaction_event: TransactionEvent) -> List[Finding]:
        result = []

        self.last_block.transactions.append(transaction_event)
        classified_event = self.classifier.classify([transaction_event])

        swaps = get_swaps(classified_event)
        flashloans = get_flashloans(classified_event)
        block_builder = get_block_builder(self.last_block.block.block.miner, self.last_block.block.network)
        arbitrages = get_arbitrages(list(swaps), list(flashloans))
        result += self.create_arbitrage_finding(arbitrages, block_builder)

        liquidations = get_liquidations(classified_event)
        result += self.create_liquidation_finding(liquidations, block_builder)


        return result
    
    def real_handle_transaction(self, transaction_event: TransactionEvent) -> List[Finding]:
        return self.provide_handle_transaction(transaction_event)
    
    def create_liquidation_finding(self, liquidations: List[Liquidation], block_builder: BlockBuilder) -> List[Finding]:
        results:List[Finding] = []
        block_builder_name = "None"
        if (block_builder):
            block_builder_name = block_builder.name
        alert_id = "MEV-LIQUIDATION-BOT-IDENTIFIED"
        for liquidation in liquidations:

            key = f"{liquidation.block_number}:{liquidation.transaction_hash}:{liquidation.log_index}"

            liquidator_bot_owner = liquidation.bot_owner
            
            cacheKey = f"{alert_id}:{liquidation.liquidator_user}:{liquidator_bot_owner}"

            expire_time_s = CACHE.get(cacheKey)
            now_s =  time.time()
            if expire_time_s != None and expire_time_s > now_s:
                logging.info(f"Alert is cached {cacheKey}")
                logging.info("Liquidation Finding: " + liquidation.model_dump_json())
                continue
            else:
                CACHE[cacheKey] = now_s + EXPIRATION_WINDOW_SECONDS

            labels = [
                        {
                            "entityType": EntityType.Address,
                            "entity": liquidation.liquidator_user,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                "description" : "Debt liquidation bot"
                            }
                        },
                        {
                            "entityType": EntityType.Address,
                            "entity": liquidator_bot_owner,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                "description": "Debt liquidation bot owner"
                            }
                        },
                    ]
            
            
            evidence = {
                "evidence": {
                        "debt_token_address" : liquidation.debt_token_address,
                        "debt_purchase_amount": liquidation.debt_purchase_amount,
                        "received_token_address": liquidation.received_token_address,
                        "received_amount": liquidation.received_amount,
                        "receive_a_token": liquidation.receive_a_token
                }
            }

            f = Finding(
                {
                    "name": "Liquidation MEV bot identified",
                    "description": f"{liquidation.liquidator_user} is a MEV bot doing liquidation controlled by {liquidator_bot_owner}",
                    "alert_id": alert_id,
                    "type": FindingType.Info,
                    "severity": FindingSeverity.Info,
                    "protocol": liquidation.protocol,
                    "metadata": {
                        "liquidator_bot": liquidation.liquidator_user,
                        "liquidator_bot_owner": liquidator_bot_owner,
                        "liquidated_user" : liquidation.liquidated_user,
                        "block_builder_name": block_builder_name,
                        **flatten(evidence, '.')
                    },
                    "unique_key": key,
                    "labels": labels
                }
            )

            logging.info("Liquidation Finding: " + liquidation.model_dump_json())
            results.append(f)
        return results

    def create_arbitrage_finding(self, arbitrages: List[Arbitrage], block_builder: BlockBuilder) -> List[Finding]:

        if (len(arbitrages) == 0):
            return []
        
        results:List[Finding] = []
        alert_id = "MEV-ARBITRAGE-BOT-IDENTIFIED"

        cacheKey = f"{alert_id}:{arbitrages[0].account_address}:{arbitrages[0].swaps[0].owner_address}"
        expire_time_s = CACHE.get(cacheKey)
        now_s =  time.time()
        if expire_time_s != None and expire_time_s > now_s:
            logging.info(f"Alert is cached {cacheKey}")
            return []
        else:
            CACHE[cacheKey] = now_s + EXPIRATION_WINDOW_SECONDS



        block_builder_name = "None"
        if (block_builder):
            block_builder_name = block_builder.name

        for arbitrage in arbitrages:
            mev_bot_owner_address = arbitrage.swaps[0].owner_address

            
            assets = [
                # Remove 'token_id' key if its value is -1; otherwise, keep the item unchanged
                {k: v for k, v in asset.items() if k != 'token_id' or asset['token_id'] != -1}
                for asset in [
                    {
                    'address': swap.token_in_address, 
                    'token_id' : swap.token_in_id 
                    } for swap in arbitrage.swaps
                ]
            ]

            asset_types =  list(dict.fromkeys(map(lambda x : "NFT" if 'token_id' in x else "TOKEN", assets)))

            evidence = {
                    "start_amount": arbitrage.start_amount,
                    "end_amount": arbitrage.end_amount,
                }
            
            flashloan = arbitrage.flashloan
            
            if (flashloan):
                evidence["flashloan"] = {
                    "asset" : flashloan.asset,
                    "amount": flashloan.amount,
                    "protocol": flashloan.protocol
                }
            
            metadata = {
                "block_builder": block_builder_name,
                "mev_bot_address": arbitrage.account_address,
                "mev_bot_owner_address": mev_bot_owner_address,
                "profit_token_address": arbitrage.profit_token_address,
                "profit_amount": arbitrage.profit_amount,
                "flashloan": flashloan != None, 
                "assets": assets,
                "asset_types": "-".join(asset_types),
                "evidence": evidence
            }

            key = f"{arbitrage.block_number}:{arbitrage.transaction_hash}:{arbitrage.account_address}"
            
            labels = [
                        {
                            "entityType": EntityType.Address,
                            "entity": arbitrage.account_address,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                 "description": "Arbitrage Bot",
                            }
                        },
                        {
                            "entityType": EntityType.Address,
                            "entity": mev_bot_owner_address,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                 "description": "Arbitrage Bot Owner EOA",
                            }
                        }
                    ]
            
            f = Finding(
                {
                    "name": "Arbitrage MEV bot identified",
                    "description": f"{arbitrage.account_address} is a MEV bot doing arbitrage owned by {mev_bot_owner_address}",
                    "alert_id": alert_id,
                    "type": FindingType.Info,
                    "severity": FindingSeverity.Info,
                    "protocol": arbitrage.swaps[0].protocol,
                    "metadata": flatten(metadata, '.'),
                    "unique_key": key,
                    "labels": labels
                }
            )

            logging.info("Arbitrage Finding: " + arbitrage.model_dump_json())
            results.append(f)

        return results

    def generate_swap_metadata(self, swap:Swap) -> dict:
         return {
                    "transaction_hash": swap.transaction_hash,
                    "transaction_position": swap.transaction_position,
                    "log_index": swap.log_index,
                    "contract_address": swap.contract_address,
                    "from_address": swap.from_address,
                    "to_address": swap.to_address,
                    "token_in_address": swap.token_in_address,
                    "token_in_amount": swap.token_in_amount,
                    "token_out_address": swap.token_out_address,
                    "token_out_amount": swap.token_out_amount,
                    "protocol": swap.protocol
                }
             
    
    def create_sandwich_finding(self, sandwiches: List[Sandwich], block_builder:BlockBuilder) -> List[Finding]:
        results:List[Finding] = []
        alert_id ="MEV-SANDWICH-BOT-IDENTIFIED"
        block_Builder_name = "None"
        if block_builder != None:
            block_Builder_name = block_builder.name

        # for sandwich of more than 1 victim
        def get_swap_by_front_and_back_transaction_hash(
            sands: List[Sandwich],
        ) -> Dict[str, List[Sandwich]]:
            get_transaction_hash = lambda e: e.frontrun_swap.transaction_hash + e.backrun_swap.transaction_hash
            return {
                transaction_hash: list(sands)
                for transaction_hash, sands in groupby(
                    sorted(sands, key=get_transaction_hash),
                    key=get_transaction_hash,
                )
            }

        grouped_sandwitches = get_swap_by_front_and_back_transaction_hash(sandwiches)
        for _, sandwiches in grouped_sandwitches.items():
            sandwich = sandwiches[0]
            cacheKey = f"{alert_id}:{sandwich.sandwicher_address}:{sandwich.frontrun_swap.owner_address}"
            expire_time_s = CACHE.get(cacheKey)
            now_s =  time.time()
            if expire_time_s != None and expire_time_s > now_s:
                logging.info(f"Alert is cached {cacheKey}")
                logging.info("Sandwich Finding: " + sandwich.model_dump_json())
                continue
            else:
                CACHE[cacheKey] = now_s + EXPIRATION_WINDOW_SECONDS

            swaps_transaction_hash = [swap.transaction_hash for inner_sandwich in sandwiches for swap in inner_sandwich.sandwiched_swaps ]

            assets = [swap.token_in_address for inner_sandwich in sandwiches for swap in inner_sandwich.sandwiched_swaps ]
            assets += [swap.token_out_address for inner_sandwich in sandwiches for swap in inner_sandwich.sandwiched_swaps]

            profits = {}
            for sand in sandwiches:
                if sand.profit_token_address in profits:
                    profits[sand.profit_token_address] += sand.profit_amount
                else:
                    profits[sand.profit_token_address] = sand.profit_amount
            profits_data = []
            for k,v in profits.items():
                profits_data += [{ 'profit_token_address': k, 'profit_amount':v }]

            metadata = {
                        "block_builder": block_Builder_name,
                        "sandwicher_address": sandwich.sandwicher_address,
                        "sandwicher_owner_address": sandwich.frontrun_swap.owner_address,
                        "profits": profits_data,
                        "assets": ", ".join(list(set(assets))),
                        "evidence": {
                            "frontrun_transaction": sandwich.frontrun_swap.transaction_hash,
                            "backrun_transaction": sandwich.backrun_swap.transaction_hash,
                            "list_sandwich_transactions": ", ".join(swaps_transaction_hash)
                        }
                    }
            
            key = f"{sandwich.block_number}:{sandwich.frontrun_swap.transaction_hash}:{sandwich.frontrun_swap.transaction_position}"
            labels = [
                        {
                            "entityType": EntityType.Address,
                            "entity": sandwich.sandwicher_address,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                "description": "Sandwicher"
                            }
                        },
                        {
                            "entityType": EntityType.Address,
                            "entity": sandwich.frontrun_swap.owner_address,
                            "label": "MEV",
                            "confidence": 1,
                            "metadata": {
                                "description": "Sandwicher Owner EOA"
                            }
                        }

            ]
            
            f = Finding(
                {
                    "name": "Sandwitch MEV bot identified",
                    "description": f"{sandwich.sandwicher_address} is a MEV bot doing sandwich owned by {sandwich.frontrun_swap.owner_address}",
                    "alert_id": "MEV-SANDWICH-BOT-IDENTIFIED",
                    "type": FindingType.Info,
                    "severity": FindingSeverity.Info,
                    "protocol": sandwich.frontrun_swap.protocol,
                    "metadata": flatten(metadata, '.'),
                    "unique_key": key,
                    "labels": labels
                }
            )
            logging.info("Sandwich Finding: " + sandwich.model_dump_json())
            results.append(f)
        return results


mev_bot = MEVBot()

def handle_transaction(transaction_event: TransactionEvent) -> list:
    return mev_bot.real_handle_transaction(transaction_event)

def handle_block(block_event: BlockEvent):
    findings = []
    if mev_bot.last_block.number == 0:
        mev_bot.last_block = MevBlock(block=block_event)
        mev_bot.last_block.number = block_event.block_number
        return []

    _dump_block(mev_bot.last_block)

    logging.info(f"Looking for sandwich in block: {mev_bot.last_block.number} network: {mev_bot.last_block.block.network}")
    classified_events = mev_bot.classifier.classify(mev_bot.last_block.transactions)
    swaps = get_swaps(classified_events)
    block_builder = get_block_builder(mev_bot.last_block.block.block.miner, mev_bot.last_block.block.network)
    sandwiches = get_sandwiches(mev_bot.last_block.block.network, list(swaps))
    findings = mev_bot.create_sandwich_finding(sandwiches, block_builder)
    mev_bot.last_block = MevBlock(block=block_event)
    mev_bot.last_block.number = block_event.block_number
    return findings

def _dump_block(last_block: MevBlock):
    if DUMP_BLOCK:
        output = open( str(last_block.number) + '.pkl', 'wb')
        pickle.dump(last_block, output)
        logging.info("save witn number of transactions " + str(len(last_block.transactions)))

