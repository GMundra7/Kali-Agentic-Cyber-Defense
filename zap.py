from zapv2 import ZAPv2
import time

ZAP_ADDRESS = "http://localhost:8080"

def run_zap_scan(target: str):
    try:
        zap = ZAPv2(apikey='', proxies={
            'http': ZAP_ADDRESS,
            'https': ZAP_ADDRESS
        })

        url = f"http://{target}"

        # Spider only (fast)
        spider_id = zap.spider.scan(url)
        while int(zap.spider.status(spider_id)) < 100:
            time.sleep(2)

        # Fetch alerts from spider findings
        all_alerts = zap.core.alerts(baseurl=url)

        seen = set()
        filtered = []
        for alert in all_alerts:
            name = alert.get("name")
            risk = alert.get("risk")
            if name not in seen and risk in ["High", "Medium"]:
                seen.add(name)
                filtered.append({
                    "name": name,
                    "risk": risk,
                    "url": alert.get("url"),
                    "description": alert.get("description", "")[:200]
                })

        return filtered if filtered else "No medium/high vulnerabilities found"

    except Exception as e:
        return f"ZAP Error: {str(e)}"