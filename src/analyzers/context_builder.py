from typing import Dict, Any
from src.models.alert import UnifiedAlert
from src.threat_intel.virustotal import VirusTotalClient
from src.threat_intel.abuseipdb import AbuseIPDBClient
from src.threat_intel.indicators import file_hash, public_ip
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ContextBuilder:
    def __init__(self):
        self.vt_client = VirusTotalClient()
        self.abuse_client = AbuseIPDBClient()

    async def build_context(self, alert: UnifiedAlert) -> Dict[str, Any]:
        context = {
            "threat_intel": {},
            "historical": [],  # TODO: Implement historical lookup from DB
        }

        # Enrich IP addresses (public only: never send internal IPs to third parties)
        source_ip = public_ip(alert.source_ip)
        if alert.source_ip and not source_ip:
            logger.info("Skipping threat intel for non-public or invalid source_ip")
        if source_ip:
            vt_ip = await self.vt_client.get_ip_report(source_ip)
            abuse_ip = await self.abuse_client.check_ip(source_ip)

            if vt_ip:
                context["threat_intel"]["source_ip_vt"] = vt_ip
            if abuse_ip:
                context["threat_intel"]["source_ip_abuse"] = abuse_ip

        # Enrich File Hashes
        digest = file_hash(alert.file_hash)
        if alert.file_hash and not digest:
            logger.info("Skipping threat intel for malformed file_hash")
        if digest:
            vt_hash = await self.vt_client.get_file_report(digest)
            if vt_hash:
                context["threat_intel"]["file_hash_vt"] = vt_hash

        return context
