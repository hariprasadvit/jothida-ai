"""
Marriage Matching (Thirumana Porutham) Calculator
Implements traditional 10 Porutham system with Vedic rules
"""

from datetime import datetime
from typing import Dict, List, Optional
from app.services.ephemeris import EphemerisService, NAKSHATRAS, RASIS
from app.services.jathagam_generator import JathagamGenerator


# Nakshatra index to name mapping for lookups
NAKSHATRA_INDEX = {n["tamil"]: i for i, n in enumerate(NAKSHATRAS)}
RASI_INDEX = {r["tamil"]: i for i, r in enumerate(RASIS)}

# Gana (Character) classification
NAKSHATRA_GANA = {
    # Deva (Divine) - indices 0, 4, 6, 7, 12, 13, 16, 21, 26
    "deva": [0, 4, 6, 7, 12, 13, 16, 21, 26],
    # Manushya (Human) - indices 1, 2, 5, 10, 11, 14, 19, 20, 24
    "manushya": [1, 2, 5, 10, 11, 14, 19, 20, 24],
    # Rakshasa (Demon) - indices 3, 8, 9, 15, 17, 18, 22, 23, 25
    "rakshasa": [3, 8, 9, 15, 17, 18, 22, 23, 25],
}

# Yoni (Animal) classification
NAKSHATRA_YONI = {
    0: ("Horse", "Male"), 1: ("Elephant", "Male"), 2: ("Sheep", "Female"),
    3: ("Serpent", "Female"), 4: ("Dog", "Female"), 5: ("Cat", "Female"),
    6: ("Cat", "Male"), 7: ("Sheep", "Male"), 8: ("Cat", "Male"),
    9: ("Rat", "Male"), 10: ("Rat", "Female"), 11: ("Cow", "Male"),
    12: ("Buffalo", "Female"), 13: ("Tiger", "Female"), 14: ("Buffalo", "Male"),
    15: ("Tiger", "Male"), 16: ("Deer", "Female"), 17: ("Deer", "Male"),
    18: ("Dog", "Male"), 19: ("Monkey", "Male"), 20: ("Mongoose", "Male"),
    21: ("Monkey", "Female"), 22: ("Lion", "Male"), 23: ("Horse", "Female"),
    24: ("Lion", "Female"), 25: ("Cow", "Female"), 26: ("Elephant", "Female"),
}

# Yoni compatibility matrix (animal enemies)
YONI_ENEMIES = {
    "Horse": "Buffalo", "Elephant": "Lion", "Sheep": "Monkey",
    "Serpent": "Mongoose", "Dog": "Deer", "Cat": "Rat",
    "Tiger": "Cow", "Buffalo": "Horse", "Lion": "Elephant",
    "Monkey": "Sheep", "Mongoose": "Serpent", "Deer": "Dog",
    "Rat": "Cat", "Cow": "Tiger"
}

# Rajju classification (body parts)
NAKSHATRA_RAJJU = {
    "pada": [0, 6, 7, 13, 14, 20, 21],      # Feet
    "kati": [1, 5, 8, 12, 15, 19, 22, 26],  # Waist
    "nabhi": [2, 4, 9, 11, 16, 18, 23, 25], # Navel
    "kanta": [3, 10, 17, 24],               # Neck
    "siro": []                              # Head
}

# Nadi classification (temperament)
NAKSHATRA_NADI = {
    "aadi": [0, 3, 6, 9, 12, 15, 18, 21, 24],      # Vata
    "madhya": [1, 4, 7, 10, 13, 16, 19, 22, 25],   # Pitta
    "antya": [2, 5, 8, 11, 14, 17, 20, 23, 26],    # Kapha
}

# Vedha (Obstruction) pairs
VEDHA_PAIRS = [
    (0, 17), (1, 16), (2, 15), (3, 14), (4, 13), (5, 12),
    (6, 21), (7, 20), (8, 19), (9, 18), (22, 26), (23, 25)
]


class MatchingCalculator:
    """
    Calculate marriage compatibility using traditional 10 Porutham system
    """

    def __init__(self, ephemeris: Optional[EphemerisService] = None):
        self.ephemeris = ephemeris
        if ephemeris:
            self.jathagam_generator = JathagamGenerator(ephemeris)

    def calculate_full_matching(self, bride, groom) -> Dict:
        """Calculate complete matching with all 10 poruthams"""
        # Generate birth charts
        bride_chart = self.jathagam_generator.generate(bride)
        groom_chart = self.jathagam_generator.generate(groom)

        # Get Moon positions (primary for matching)
        bride_moon = bride_chart["moon_sign"]
        groom_moon = groom_chart["moon_sign"]

        bride_nakshatra_idx = NAKSHATRA_INDEX.get(bride_moon["nakshatra"], 0)
        groom_nakshatra_idx = NAKSHATRA_INDEX.get(groom_moon["nakshatra"], 0)
        bride_rasi_idx = RASI_INDEX.get(bride_moon["rasi_tamil"], 0)
        groom_rasi_idx = RASI_INDEX.get(groom_moon["rasi_tamil"], 0)

        # Calculate all poruthams
        poruthams = self._calculate_all_poruthams(
            bride_nakshatra_idx, groom_nakshatra_idx,
            bride_rasi_idx, groom_rasi_idx
        )

        # Calculate overall score
        total_score = sum(p["score"] for p in poruthams)
        max_score = sum(p["max_score"] for p in poruthams)
        overall_score = (total_score / max_score) * 100

        # Check doshas
        doshas = self._check_doshas(bride_chart, groom_chart)

        # Compatibility radar data
        compatibility_radar = {
            "emotional": self._calculate_category_score(poruthams, ["Ganam", "Rasi"]),
            "physical": self._calculate_category_score(poruthams, ["Yoni"]),
            "financial": self._calculate_category_score(poruthams, ["Mahendra", "Stree Deergha"]),
            "family": self._calculate_category_score(poruthams, ["Rasi Adhipathi", "Vasiyam"]),
            "health": self._calculate_category_score(poruthams, ["Rajju", "Nadi"]),
            "spiritual": self._calculate_category_score(poruthams, ["Dinam", "Vedha"]),
        }

        # Generate AI verdict
        ai_verdict = self._generate_verdict(overall_score, poruthams, doshas)

        # Recommendations
        recommendations = self._generate_recommendations(poruthams, doshas)

        return {
            "overall_score": round(overall_score, 1),
            "overall_status": self._get_status(overall_score),
            "ai_verdict": ai_verdict,
            "poruthams": poruthams,
            "doshas": doshas,
            "compatibility_radar": compatibility_radar,
            "future_timeline": self._generate_timeline(overall_score),
            "recommendations": recommendations,
            "bride_details": {
                "name": bride.name,
                "nakshatra": bride_moon["nakshatra"],
                "rasi": bride_moon["rasi_tamil"]
            },
            "groom_details": {
                "name": groom.name,
                "nakshatra": groom_moon["nakshatra"],
                "rasi": groom_moon["rasi_tamil"]
            }
        }

    def quick_check(self, bride_nakshatra: str, bride_rasi: str,
                    groom_nakshatra: str, groom_rasi: str) -> Dict:
        """Quick matching without full birth details"""
        bride_nak_idx = NAKSHATRA_INDEX.get(bride_nakshatra, 0)
        groom_nak_idx = NAKSHATRA_INDEX.get(groom_nakshatra, 0)
        bride_rasi_idx = RASI_INDEX.get(bride_rasi, 0)
        groom_rasi_idx = RASI_INDEX.get(groom_rasi, 0)

        poruthams = self._calculate_all_poruthams(
            bride_nak_idx, groom_nak_idx,
            bride_rasi_idx, groom_rasi_idx
        )

        total_score = sum(p["score"] for p in poruthams)
        max_score = sum(p["max_score"] for p in poruthams)
        overall_score = (total_score / max_score) * 100

        return {
            "overall_score": round(overall_score, 1),
            "overall_status": self._get_status(overall_score),
            "matched_count": sum(1 for p in poruthams if p["score"] >= p["max_score"] * 0.6),
            "poruthams": poruthams
        }

    def _calculate_all_poruthams(self, bride_nak: int, groom_nak: int,
                                  bride_rasi: int, groom_rasi: int) -> List[Dict]:
        """Calculate all 10 poruthams"""
        poruthams = []

        # 1. Dinam (Day) Porutham
        poruthams.append(self._calc_dinam(bride_nak, groom_nak))

        # 2. Ganam (Temperament) Porutham
        poruthams.append(self._calc_ganam(bride_nak, groom_nak))

        # 3. Mahendra Porutham
        poruthams.append(self._calc_mahendra(bride_nak, groom_nak))

        # 4. Stree Deergha Porutham
        poruthams.append(self._calc_stree_deergha(bride_nak, groom_nak))

        # 5. Yoni Porutham
        poruthams.append(self._calc_yoni(bride_nak, groom_nak))

        # 6. Rasi Porutham
        poruthams.append(self._calc_rasi(bride_rasi, groom_rasi))

        # 7. Rasi Adhipathi Porutham
        poruthams.append(self._calc_rasi_adhipathi(bride_rasi, groom_rasi))

        # 8. Vasiyam Porutham
        poruthams.append(self._calc_vasiyam(bride_rasi, groom_rasi))

        # 9. Rajju Porutham
        poruthams.append(self._calc_rajju(bride_nak, groom_nak))

        # 10. Vedha Porutham
        poruthams.append(self._calc_vedha(bride_nak, groom_nak))

        return poruthams

    def _calc_dinam(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Dinam Porutham - Day compatibility"""
        # Count from bride's nakshatra to groom's
        count = (groom_nak - bride_nak) % 27 + 1

        # Good if count divides by 9 gives 2, 4, 6, 8, 9
        remainder = count % 9
        is_good = remainder in [2, 4, 6, 8, 0]

        score = 100 if is_good else 30

        return {
            "name": "Dinam",
            "tamil_name": "தினம்",
            "english_name": "Day",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "நாளாந்த வாழ்க்கை இணக்கம் - தம்பதிகளின் அன்றாட வாழ்வில் ஒற்றுமை",
            "ai_insight": "தினப் பொருத்தம் நல்லது" if is_good else "தினப் பொருத்தம் குறைவு"
        }

    def _calc_ganam(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Ganam Porutham - Character compatibility"""
        bride_gana = self._get_gana(bride_nak)
        groom_gana = self._get_gana(groom_nak)

        # Same gana: 100%, Deva-Manushya: 70%, Manushya-Rakshasa: 50%
        # Deva-Rakshasa: 30%
        if bride_gana == groom_gana:
            score = 100
        elif {bride_gana, groom_gana} == {"deva", "manushya"}:
            score = 70
        elif {bride_gana, groom_gana} == {"manushya", "rakshasa"}:
            score = 50
        else:
            score = 30

        return {
            "name": "Ganam",
            "tamil_name": "கணம்",
            "english_name": "Temperament",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "குணநலன் பொருத்தம் - தேவ, மனுஷ, ராட்சச கணங்களின் இணக்கம்",
            "ai_insight": f"மணமகள்: {bride_gana}, மணமகன்: {groom_gana}"
        }

    def _calc_mahendra(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Mahendra Porutham - Prosperity"""
        count = (groom_nak - bride_nak) % 27 + 1

        # Good if count is 4, 7, 10, 13, 16, 19, 22, 25
        good_counts = [4, 7, 10, 13, 16, 19, 22, 25]
        is_good = count in good_counts

        score = 100 if is_good else 40

        return {
            "name": "Mahendra",
            "tamil_name": "மகேந்திரம்",
            "english_name": "Prosperity",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "செல்வம் & சந்ததி - குடும்ப வளர்ச்சி மற்றும் செழிப்பு",
            "ai_insight": None
        }

    def _calc_stree_deergha(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Stree Deergha Porutham - Longevity"""
        count = (groom_nak - bride_nak) % 27 + 1

        # Good if groom's nakshatra is at least 13 away from bride's
        is_good = count >= 13

        score = 100 if is_good else (count / 13) * 100

        return {
            "name": "Stree Deergha",
            "tamil_name": "ஸ்திரி தீர்க்கம்",
            "english_name": "Longevity",
            "score": round(score),
            "max_score": 100,
            "status": self._get_status(score),
            "description": "நீடித்த மகிழ்ச்சி - மனைவியின் நீண்ட ஆயுளும் சுமங்கலித்வமும்",
            "ai_insight": None
        }

    def _calc_yoni(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Yoni Porutham - Physical compatibility"""
        bride_yoni = NAKSHATRA_YONI[bride_nak]
        groom_yoni = NAKSHATRA_YONI[groom_nak]

        bride_animal = bride_yoni[0]
        groom_animal = groom_yoni[0]

        # Same animal: 100%
        # Enemy animals: 0%
        # Different but not enemy: 50%
        if bride_animal == groom_animal:
            score = 100
        elif YONI_ENEMIES.get(bride_animal) == groom_animal or \
             YONI_ENEMIES.get(groom_animal) == bride_animal:
            score = 20
        else:
            score = 60

        return {
            "name": "Yoni",
            "tamil_name": "யோனி",
            "english_name": "Physical",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "உடல் & உணர்வு இணக்கம் - தம்பதிகளின் உடல் மற்றும் மன ஒற்றுமை",
            "ai_insight": f"மணமகள் யோனி: {bride_animal}, மணமகன் யோனி: {groom_animal}"
        }

    def _calc_rasi(self, bride_rasi: int, groom_rasi: int) -> Dict:
        """Calculate Rasi Porutham - Mental compatibility"""
        count = (groom_rasi - bride_rasi) % 12 + 1

        # 2, 6, 8, 12 from bride's rasi: Not good
        # 7 (opposite) is excellent
        if count == 7:
            score = 100
        elif count in [2, 6, 8, 12]:
            score = 30
        else:
            score = 70

        return {
            "name": "Rasi",
            "tamil_name": "ராசி",
            "english_name": "Mental",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "மன இணக்கம் - சந்திரனின் ராசி அடிப்படையிலான மன பொருத்தம்",
            "ai_insight": None
        }

    def _calc_rasi_adhipathi(self, bride_rasi: int, groom_rasi: int) -> Dict:
        """Calculate Rasi Adhipathi Porutham - Lord compatibility"""
        # Rasi lords
        lords = [4, 2, 3, 1, 0, 3, 2, 4, 5, 6, 6, 5]  # Mars, Venus, Mercury, Moon, Sun...

        bride_lord = lords[bride_rasi]
        groom_lord = lords[groom_rasi]

        # Friends: same lord or friendly lords
        friends = {
            0: [1, 5],      # Sun: Moon, Jupiter
            1: [0, 3],      # Moon: Sun, Mercury
            2: [0, 1, 5],   # Venus: Sun, Moon, Jupiter
            3: [0, 2, 6],   # Mercury: Sun, Venus, Saturn
            4: [0, 1, 5],   # Mars: Sun, Moon, Jupiter
            5: [0, 1, 4],   # Jupiter: Sun, Moon, Mars
            6: [3, 2],      # Saturn: Mercury, Venus
        }

        if bride_lord == groom_lord:
            score = 100
        elif groom_lord in friends.get(bride_lord, []):
            score = 80
        else:
            score = 40

        return {
            "name": "Rasi Adhipathi",
            "tamil_name": "ராசி அதிபதி",
            "english_name": "Lord Compatibility",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "குடும்ப நல்வாழ்வு - ராசி அதிபதிகளின் நட்பு பொருத்தம்",
            "ai_insight": None
        }

    def _calc_vasiyam(self, bride_rasi: int, groom_rasi: int) -> Dict:
        """Calculate Vasiyam Porutham - Attraction"""
        # Vasiya rasis for each rasi
        vasiya = {
            0: [4, 8],      # Aries: Leo, Sagittarius
            1: [2, 6],      # Taurus: Cancer, Libra
            2: [5],         # Gemini: Virgo
            3: [7, 10],     # Cancer: Scorpio, Aquarius
            4: [6],         # Leo: Libra
            5: [2, 11],     # Virgo: Gemini, Pisces
            6: [5],         # Libra: Virgo
            7: [3],         # Scorpio: Cancer
            8: [11],        # Sagittarius: Pisces
            9: [0, 10],     # Capricorn: Aries, Aquarius
            10: [0],        # Aquarius: Aries
            11: [9],        # Pisces: Capricorn
        }

        # Check if mutually vasiya or one-way
        bride_vasiya = groom_rasi in vasiya.get(bride_rasi, [])
        groom_vasiya = bride_rasi in vasiya.get(groom_rasi, [])

        if bride_vasiya and groom_vasiya:
            score = 100
        elif bride_vasiya or groom_vasiya:
            score = 70
        else:
            score = 40

        return {
            "name": "Vasiyam",
            "tamil_name": "வசியம்",
            "english_name": "Attraction",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "ஈர்ப்பு & கவர்ச்சி - தம்பதிகளுக்கிடையே ஈர்ப்பு சக்தி",
            "ai_insight": None
        }

    def _calc_rajju(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Rajju Porutham - Mangalya strength (CRITICAL)"""
        bride_rajju = self._get_rajju(bride_nak)
        groom_rajju = self._get_rajju(groom_nak)

        # Same rajju is bad (except siro)
        if bride_rajju == groom_rajju and bride_rajju != "siro":
            score = 20
        else:
            score = 100

        return {
            "name": "Rajju",
            "tamil_name": "ரஜ்ஜு",
            "english_name": "Mangalya",
            "score": score,
            "max_score": 100,
            "status": "critical" if score < 50 else self._get_status(score),
            "description": "மங்கல பலம் - மிக முக்கியம், கணவனின் நீண்ட ஆயுளை குறிக்கிறது",
            "ai_insight": "ரஜ்ஜு தோஷம் - பரிகாரம் அவசியம்" if score < 50 else None
        }

    def _calc_vedha(self, bride_nak: int, groom_nak: int) -> Dict:
        """Calculate Vedha Porutham - Obstruction"""
        # Check if the pair is in vedha pairs
        is_vedha = (bride_nak, groom_nak) in VEDHA_PAIRS or \
                   (groom_nak, bride_nak) in VEDHA_PAIRS

        score = 20 if is_vedha else 100

        return {
            "name": "Vedha",
            "tamil_name": "வேதை",
            "english_name": "Obstruction",
            "score": score,
            "max_score": 100,
            "status": self._get_status(score),
            "description": "தடைகள் நீக்கம் - வாழ்க்கையில் தடைகள் இல்லாமல் இருப்பது",
            "ai_insight": "வேதை தோஷம் உள்ளது" if is_vedha else None
        }

    def _get_gana(self, nakshatra_idx: int) -> str:
        """Get gana for nakshatra"""
        for gana, indices in NAKSHATRA_GANA.items():
            if nakshatra_idx in indices:
                return gana
        return "manushya"

    def _get_rajju(self, nakshatra_idx: int) -> str:
        """Get rajju for nakshatra"""
        for rajju, indices in NAKSHATRA_RAJJU.items():
            if nakshatra_idx in indices:
                return rajju
        return "nabhi"

    def _get_status(self, score: float) -> str:
        """Get status string from score"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "warning"
        return "critical"

    def _check_doshas(self, bride_chart: Dict, groom_chart: Dict) -> List[Dict]:
        """Check for various doshas"""
        doshas = []

        # Simplified Mangal Dosha check (Mars in 1, 4, 7, 8, 12)
        def has_mangal_dosha(chart):
            for planet in chart["planets"]:
                if planet["planet"] == "Mars":
                    # Check house position (simplified)
                    return planet["strength"] < 40
            return False

        bride_mangal = has_mangal_dosha(bride_chart)
        groom_mangal = has_mangal_dosha(groom_chart)

        doshas.append({
            "name": "Mangal Dosha",
            "tamil_name": "செவ்வாய் தோஷம்",
            "bride_has": bride_mangal,
            "groom_has": groom_mangal,
            "is_compatible": bride_mangal == groom_mangal,  # Both have or both don't
            "remedy": "குஜ தோஷ சாந்தி பூஜை" if bride_mangal != groom_mangal else None
        })

        # Nadi Dosha
        bride_nadi = self._get_nadi(bride_chart)
        groom_nadi = self._get_nadi(groom_chart)
        same_nadi = bride_nadi == groom_nadi

        doshas.append({
            "name": "Nadi Dosha",
            "tamil_name": "நாடி தோஷம்",
            "bride_has": same_nadi,
            "groom_has": same_nadi,
            "is_compatible": not same_nadi,
            "remedy": "நாடி தோஷ நிவாரண பூஜை" if same_nadi else None
        })

        return doshas

    def _get_nadi(self, chart: Dict) -> str:
        """Get nadi from chart"""
        nakshatra = chart["moon_sign"]["nakshatra"]
        nak_idx = NAKSHATRA_INDEX.get(nakshatra, 0)
        for nadi, indices in NAKSHATRA_NADI.items():
            if nak_idx in indices:
                return nadi
        return "madhya"

    def _calculate_category_score(self, poruthams: List[Dict], names: List[str]) -> float:
        """Calculate average score for category"""
        relevant = [p for p in poruthams if p["name"] in names]
        if not relevant:
            return 50
        return sum(p["score"] for p in relevant) / len(relevant)

    def _generate_verdict(self, score: float, poruthams: List[Dict], doshas: List[Dict]) -> str:
        """Generate AI verdict"""
        critical = [p for p in poruthams if p["status"] == "critical"]
        dosha_issues = [d for d in doshas if not d["is_compatible"]]

        if score >= 70 and not critical:
            return "நல்ல பொருத்தம் - திருமணத்திற்கு சிறந்தது"
        elif score >= 50:
            issues = ", ".join([p["tamil_name"] for p in critical])
            return f"சாதாரண பொருத்தம் - {issues} கவனிக்கவும்"
        else:
            return "குறைவான பொருத்தம் - ஜோதிடரை கலந்தாலோசிக்கவும்"

    def _generate_recommendations(self, poruthams: List[Dict], doshas: List[Dict]) -> List[str]:
        """Generate recommendations"""
        recs = []

        critical = [p for p in poruthams if p["status"] == "critical"]
        for p in critical:
            if p["name"] == "Rajju":
                recs.append("ரஜ்ஜு தோஷத்திற்கு நவக்கிரக ஹோமம் செய்யவும்")
            elif p["name"] == "Vedha":
                recs.append("வேதை தோஷத்திற்கு சாந்தி பூஜை செய்யவும்")

        for d in doshas:
            if not d["is_compatible"] and d["remedy"]:
                recs.append(d["remedy"])

        if not recs:
            recs.append("எந்த பரிகாரமும் தேவையில்லை - நல்ல பொருத்தம்")

        return recs

    def _generate_timeline(self, score: float) -> List[Dict]:
        """Generate future timeline predictions"""
        import datetime
        current_year = datetime.datetime.now().year

        timeline = [
            {"year": str(current_year + 1), "event": "திருமணம்", "type": "positive", "score": int(score)},
        ]

        if score >= 70:
            timeline.extend([
                {"year": str(current_year + 2), "event": "குழந்தை யோகம்", "type": "positive", "score": 78},
                {"year": str(current_year + 4), "event": "வீடு யோகம்", "type": "positive", "score": 85},
            ])
        else:
            timeline.extend([
                {"year": str(current_year + 2), "event": "சனி பெயர்ச்சி", "type": "warning", "score": 45},
            ])

        return timeline

    @staticmethod
    def get_porutham_info(name: str) -> Dict:
        """Get detailed info about a porutham"""
        info = {
            "Dinam": {
                "name": "தினம்",
                "importance": "நாளாந்த வாழ்க்கை",
                "description": "இது தம்பதிகளின் அன்றாட வாழ்க்கையில் ஒற்றுமையை குறிக்கிறது.",
                "calculation": "மணமகளின் நட்சத்திரத்திலிருந்து மணமகனின் நட்சத்திரம் வரை எண்ணி 9ஆல் வகுக்க வேண்டும்."
            },
            "Ganam": {
                "name": "கணம்",
                "importance": "குணநலன்",
                "description": "தேவ, மனுஷ, ராட்சச என்ற மூன்று கணங்களின் பொருத்தம்.",
                "calculation": "ஒரே கணம் சிறந்தது. தேவ-மனுஷ நல்லது."
            }
        }
        return info.get(name, {"name": name, "description": "விவரம் கிடைக்கவில்லை"})
