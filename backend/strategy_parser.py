import re
from typing import Dict

class StrategyParser:
    def parse_description(self, description: str) -> Dict:
        strategy = {}
        if not description:
            return {
                "sma_short": 20,
                "sma_long": 50,
                "rsi_period": 14,
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "stop_loss": 0.02,
                "take_profit": 0.04
            }
        description_lower = description.lower()
        sma_short_match = re.search(r'sma\s*(\d+)\s*et\s*(\d+)|moving\s*average\s*(\d+)\s*(\d+)', description_lower)
        if sma_short_match:
            groups = sma_short_match.groups()
            strategy["sma_short"] = int(groups[0] or groups[2] or 20)
            strategy["sma_long"] = int(groups[1] or groups[3] or 50)
        else:
            strategy["sma_short"] = 20
            strategy["sma_long"] = 50
        rsi_match = re.search(r'rsi\s*(\d+)', description_lower)
        if rsi_match:
            strategy["rsi_period"] = int(rsi_match.group(1))
        else:
            strategy["rsi_period"] = 14
        sl_match = re.search(r'stop\s*loss\s*(\d+(?:\.\d+)?)%?', description_lower)
        if sl_match:
            strategy["stop_loss"] = float(sl_match.group(1)) / 100
        else:
            strategy["stop_loss"] = 0.02
        tp_match = re.search(r'take\s*profit\s*(\d+(?:\.\d+)?)%?', description_lower)
        if tp_match:
            strategy["take_profit"] = float(tp_match.group(1)) / 100
        else:
            strategy["take_profit"] = 0.04
        if "oversold" in description_lower:
            os_match = re.search(r'oversold\s*(\d+)', description_lower)
            if os_match:
                strategy["rsi_oversold"] = int(os_match.group(1))
            else:
                strategy["rsi_oversold"] = 30
        else:
            strategy["rsi_oversold"] = 30
        if "overbought" in description_lower:
            ob_match = re.search(r'overbought\s*(\d+)', description_lower)
            if ob_match:
                strategy["rsi_overbought"] = int(ob_match.group(1))
            else:
                strategy["rsi_overbought"] = 70
        else:
            strategy["rsi_overbought"] = 70
        return strategy
