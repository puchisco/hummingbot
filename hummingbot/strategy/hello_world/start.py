from typing import (
    List,
    Tuple,
)
from hummingbot.strategy.hello_world.hello_world_config_map import hello_world_config_map
from hummingbot.client.settings import EXAMPLE_PAIRS
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple

from hummingbot.strategy.hello_world import HelloWorldStrategy

def start(self):
    try:
        market = hello_world_config_map.get("market").value.lower()
        asset_trading_pair = hello_world_config_map.get("asset_trading_pair").value

        try:
            trading_pair = EXAMPLE_PAIRS.get(market).replace("-", "_")
            self._notify(f"trading_pair: {trading_pair}")     
            assets: Tuple[str, str] = self._initialize_market_assets(market, [trading_pair])[0]
            self._notify(f"Market: {market}")
            self._notify(f"list(assets): {str(assets)}")


        except ValueError as e:
            self._notify(str(e))
            return

        market_names: List[Tuple[str, List[str]]] = [(market, [trading_pair])]

        
        self._initialize_wallet(token_trading_pairs=list(set(assets)))
        self._initialize_markets(market_names)
        self.assets = set(assets)

        maker_data = [self.markets[market], trading_pair] + list(assets)
        self.market_trading_pairs = [MarketTradingPairTuple(*maker_data)]

        strategy_logging_options = HelloWorldStrategy.OPTION_LOG_ALL

        self.strategy = HelloWorldStrategy(market_infos=[MarketTradingPairTuple(*maker_data)],
                                           asset_trading_pair=asset_trading_pair,
                                           logging_options=strategy_logging_options)
    except Exception as e:
        self._notify(str(e))
        self.logger().error("Unknown error during initialization.", exc_info=True)
