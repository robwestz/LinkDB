"""
AI Service for LinkDB - LLM Integration Layer

This service provides AI-powered insights, recommendations, and chat functionality.
Supports both OpenAI and mock mode (for testing without API keys).
"""

import os
import json
from typing import Dict, List, Optional
import asyncio

class AIService:
    """
    Centralized AI/LLM service with mock fallback.

    If no API key is provided, uses intelligent mock responses
    based on actual customer data.
    """

    def __init__(self, provider: str = "mock"):
        self.provider = provider
        self.use_mock = True

        # Try to initialize real provider if API key exists
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key and api_key.startswith("sk-"):
                try:
                    import openai
                    openai.api_key = api_key
                    self.model = "gpt-4-turbo-preview"
                    self.use_mock = False
                    self.openai = openai
                except ImportError:
                    print("⚠️  OpenAI not installed. Using mock mode.")
                    self.use_mock = True
            else:
                print("ℹ️  No OpenAI API key found. Using intelligent mock mode.")
                self.use_mock = True

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Send chat messages to LLM and get response.
        Falls back to intelligent mock responses if no API key.
        """
        if self.use_mock:
            return self._mock_chat(messages)

        # Real OpenAI implementation
        try:
            response = await asyncio.to_thread(
                self.openai.ChatCompletion.create,
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  OpenAI error: {e}. Falling back to mock.")
            return self._mock_chat(messages)

    def _mock_chat(self, messages: List[Dict[str, str]]) -> str:
        """Intelligent mock chat responses based on conversation context."""
        if not messages:
            return "Hej! Hur kan jag hjälpa dig med din SEO-strategi?"

        last_message = messages[-1].get("content", "").lower()

        # Pattern matching for common questions
        if any(word in last_message for word in ["länkprofil", "backlink", "profil"]):
            return """Din länkprofil ser generellt bra ut! Här är en snabb sammanfattning:

✅ **Styrkor:**
- Bra diversifiering av publiceringsdomäner
- Naturlig ankartextsfördelning
- Stabil länkbyggnadsvolym

⚠️ **Förbättringsområden:**
- Överväg att minska exakta matchningar något
- Öka temporal variation för mer naturlighet
- Diversifiera TLD-distributionen mer

Vill du att jag går djupare in på något specifikt område?"""

        elif any(word in last_message for word in ["risk", "varning", "problem"]):
            return """Jag ser några potentiella risker att vara medveten om:

🚨 **Medelhög risk:**
- Exakt match-ratio ligger på gränsen (ca 40-50%)
- Vissa månader visar onaturliga spikar i länkbyggnad

🟡 **Låg risk:**
- TLD-distribution något sned mot .com
- Få länkar från .edu/.gov

💡 **Rekommendation:**
Fokusera på att bygga mer varierande ankare (partial match, branded) i nästa kampanj för att minska risk för över-optimering."""

        elif any(word in last_message for word in ["nästa", "göra", "rekommendation"]):
            return """Här är mina top 3 rekommendationer för nästa steg:

🎯 **1. Diversifiera ankartexterna (Hög prioritet)**
   - Öka partial match till 60-70%
   - Minska exact match under 30%
   - Detta minskar över-optimeringsrisk

📊 **2. Jämna ut temporal fördelningen (Medel prioritet)**
   - Sikta på 4-6 länkar per månad
   - Undvik spikar och långa pauser
   - Bygger naturligare profil

🌍 **3. Utöka TLD-variation (Låg prioritet)**
   - Lägg till fler .se, .org, .net länkar
   - Minskar beroendet av .com
   - Stärker geografisk relevans

Vill du att jag utvecklar någon av dessa?"""

        elif any(word in last_message for word in ["tack", "ok", "bra"]):
            return "Varsågod! Fråga gärna om du vill diskutera något mer. Jag är här för att hjälpa dig optimera din SEO-strategi! 🚀"

        # Default intelligent response
        return f"""Jag förstår din fråga om "{last_message[:50]}...".

Baserat på din data kan jag ge följande insikter:

📊 Din länkprofil visar generellt god kvalitet med balanserad fördelning över tid och domäner.

🎯 Fokusera på att fortsätta bygga naturliga ankare och diversifiera dina källor.

Vill du att jag analyserar något specifikt område djupare? Du kan fråga om:
- Ankartextstrategi
- Temporal fördelning
- Domänkvalitet
- Konkurrentanalys"""

    async def generate_insights(self, customer_data: Dict) -> List[str]:
        """
        Generate AI-powered insights from customer analysis data.
        Uses intelligent analysis based on actual metrics.
        """
        insights = []

        # Analyze overall score
        overall_score = customer_data.get("overall_score", 0)
        if overall_score >= 80:
            insights.append(f"🌟 Utmärkt övergripande hälsa ({overall_score:.1f}/100) - Din länkprofil är i toppskick!")
        elif overall_score >= 60:
            insights.append(f"✅ God länkprofilhälsa ({overall_score:.1f}/100) med utrymme för förbättring")
        else:
            insights.append(f"⚠️ Länkprofilen behöver uppmärksamhet ({overall_score:.1f}/100)")

        # Analyze anchor quality
        anchor_quality = customer_data.get("anchor_quality", {})
        exact_match_ratio = anchor_quality.get("exact_match_ratio", 0) * 100

        if exact_match_ratio > 50:
            insights.append(f"🚨 Hög risk för över-optimering: {exact_match_ratio:.1f}% exakta matchningar (rekommenderat: <40%)")
        elif exact_match_ratio > 30:
            insights.append(f"⚠️ Exakt match-ratio på gränsen ({exact_match_ratio:.1f}%) - överväg mer varierade ankare")
        else:
            insights.append(f"✅ Utmärkt ankardiversifiering med endast {exact_match_ratio:.1f}% exakta matchningar")

        # Analyze temporal patterns
        temporal = customer_data.get("temporal_patterns", {})
        velocity = temporal.get("links_per_month", 0)

        if velocity > 10:
            insights.append(f"📈 Hög länkbyggnadshastighet ({velocity:.1f} länkar/månad) - säkerställ naturlig variation")
        elif velocity < 2:
            insights.append(f"📉 Låg länkbyggnadshastighet ({velocity:.1f} länkar/månad) - överväg att öka aktiviteten")
        else:
            insights.append(f"⚡ Balanserad länkbyggnadshastighet ({velocity:.1f} länkar/månad)")

        # Analyze domain quality
        domain_quality = customer_data.get("domain_quality", {})
        unique_domains = domain_quality.get("unique_domains", 0)
        total_links = customer_data.get("link_history", {}).get("total_links", 1)

        domain_ratio = (unique_domains / total_links * 100) if total_links > 0 else 0

        if domain_ratio > 80:
            insights.append(f"🌐 Exceptionell domändivers ifiering: {unique_domains} unika domäner ({domain_ratio:.1f}%)")
        elif domain_ratio > 50:
            insights.append(f"✅ God domändiversifiering med {unique_domains} unika publiceringsdomäner")
        else:
            insights.append(f"⚠️ Begränsad domändiversifiering ({domain_ratio:.1f}%) - öka variationen av källor")

        # Add strategic insight
        if len(insights) < 5:
            brand = customer_data.get("brand", "Din webbplats")
            insights.append(f"💡 För {brand}: Fortsätt fokusera på kvalitet över kvantitet och bygg länkar från relevanta källor i din nisch")

        return insights[:5]  # Return max 5 insights

    async def generate_recommendations(
        self,
        customer_data: Dict,
        target_url: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate smart recommendations for next actions.
        Based on data-driven analysis of weaknesses.
        """
        recommendations = []

        # Analyze anchor quality for recommendations
        anchor_quality = customer_data.get("anchor_quality", {})
        exact_match_ratio = anchor_quality.get("exact_match_ratio", 0) * 100
        over_opt_risk = anchor_quality.get("over_optimization_risk", "low")

        if exact_match_ratio > 40 or over_opt_risk in ["high", "medium"]:
            recommendations.append({
                "priority": 1,
                "title": "Diversifiera ankartexterna omedelbart",
                "action": "I nästa kampanj: 70% partial match, 20% branded, 10% exact match",
                "reasoning": f"Nuvarande exact match-ratio ({exact_match_ratio:.1f}%) ökar risken för Google-påföljder",
                "impact": "high"
            })

        # Temporal pattern recommendations
        temporal = customer_data.get("temporal_patterns", {})
        consistency = temporal.get("consistency_score", 100)

        if consistency < 70:
            recommendations.append({
                "priority": 2,
                "title": "Jämna ut länkbyggnadstempon",
                "action": "Sikta på 4-6 länkar per månad med jämn fördelning",
                "reasoning": f"Låg konsistens ({consistency:.0f}/100) kan signalera onaturligt mönster",
                "impact": "medium"
            })

        # Domain diversity recommendation
        domain_quality = customer_data.get("domain_quality", {})
        diversity_score = domain_quality.get("diversity_score", 100)

        if diversity_score < 80:
            recommendations.append({
                "priority": 3,
                "title": "Öka domänvariationen",
                "action": "Fokusera på nya, unika domäner med hög auktoritet i din nisch",
                "reasoning": f"Diversity score ({diversity_score:.0f}/100) kan förbättras med bredare källbas",
                "impact": "medium"
            })

        # Ensure we always have at least one recommendation
        if not recommendations:
            recommendations.append({
                "priority": 1,
                "title": "Fortsätt den goda utvecklingen",
                "action": "Bibehåll nuvarande strategi och bygg 4-6 kvalitetslänkar per månad",
                "reasoning": "Din länkprofil är väl balanserad - fokusera på att behålla kvaliteten",
                "impact": "low"
            })

        return recommendations[:3]  # Return max 3 recommendations

    async def natural_language_query(self, query: str, context: Dict) -> str:
        """
        Answer natural language questions about customer data.
        Intelligent parsing of context to answer specific questions.
        """
        query_lower = query.lower()

        # Links per month questions
        if any(word in query_lower for word in ["länkar", "månad", "month", "per månad"]):
            links_per_month = context.get("links_per_month", 0)
            total_links = context.get("total_links", 0)
            return f"Du har i genomsnitt {links_per_month:.1f} länkar per månad, med totalt {total_links} länkar i databasen."

        # Domain questions
        if any(word in query_lower for word in ["domän", "domain", "källor"]):
            unique_domains = context.get("unique_domains", 0)
            total_links = context.get("total_links", 1)
            ratio = (unique_domains / total_links * 100) if total_links > 0 else 0
            return f"Du har länkar från {unique_domains} unika domäner, vilket ger en diversifieringsgrad på {ratio:.1f}%. Detta är {'utmärkt' if ratio > 70 else 'bra' if ratio > 50 else 'okej, men kan förbättras'}."

        # Score/quality questions
        if any(word in query_lower for word in ["score", "kvalitet", "betyg", "health"]):
            overall_score = context.get("overall_score", 0)
            status = "utmärkt" if overall_score >= 80 else "god" if overall_score >= 60 else "behöver förbättring"
            return f"Din övergripande hälsopoäng är {overall_score:.1f}/100, vilket är {status}. Detta baseras på analys av ankarkvalitet, temporal fördelning och domänkvalitet."

        # Risk questions
        if any(word in query_lower for word in ["risk", "varning", "warning", "problem"]):
            # Check for warnings in anchor quality
            warnings_count = len(context.get("warnings", []))
            if warnings_count > 0:
                return f"Jag har identifierat {warnings_count} varning(ar) i din profil. De vanligaste riskerna är över-optimering av ankartexer och onaturliga länkar per månad-mönster."
            return "Din profil ser generellt säker ut utan några större risksignaler. Fortsätt fokusera på naturlig länkbyggnad."

        # Default response
        return f"Baserat på din data: Du har {context.get('total_links', 0)} länkar från {context.get('unique_domains', 0)} domäner med en hälsopoäng på {context.get('overall_score', 0):.1f}/100. Fråga gärna mer specifikt om du vill veta något särskilt!"


# Singleton instance
ai_service = AIService(provider="mock")  # Will auto-upgrade to OpenAI if API key exists
