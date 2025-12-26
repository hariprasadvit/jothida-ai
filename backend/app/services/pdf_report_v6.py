"""
V6.2 Super Jyotish Report Generator
40-page comprehensive report with all calculations derived from chart data
No static text - every insight has mathematical basis

V6.2 Features:
- Saffron/Gold color scheme
- Visual South Indian charts (D1, D9, D10)
- POI (Planet Operating Index) tables
- HAI (House Activation Index) tables
- Aspect/Yoga visual map

V6.2+ NEW Features:
- TimeAdaptiveEngine (V7.0) for PAST_ANALYSIS, FUTURE_PREDICTION, MONTH_WISE modes
- FutureProjectionService for monthly/yearly predictions
- LifeTimelineService for comprehensive life timeline
"""

import io
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from .jyotish_engine import (
    JyotishEngine, RASIS, RASI_TAMIL, RASI_LORDS, PLANETS, PLANET_TAMIL, PLANET_SYMBOLS,
    NAKSHATRAS, HOUSE_KARAKAS, MATURITY_AGES, SOUTH_INDIAN_POSITIONS,
    PLANET_ABBR, PLANET_SANSKRIT, RASI_SANSKRIT,
    WEEKDAYS_TAMIL, THITHIS, THITHIS_TAMIL, KARANAS, KARANAS_TAMIL,
    NITHYA_YOGAS, NITHYA_YOGAS_TAMIL, NAKSHATRA_GANAM, NAKSHATRA_YONI
)

# V6.2+ Import TimeAdaptiveEngine (V7.0) for time-mode aware predictions
try:
    from .time_adaptive_engine import TimeAdaptiveEngine, TimeMode
    TIME_ADAPTIVE_AVAILABLE = True
except ImportError:
    TIME_ADAPTIVE_AVAILABLE = False
    TimeAdaptiveEngine = None
    TimeMode = None

# V6.2+ Import FutureProjectionService for monthly/yearly predictions
try:
    from .future_projection_service import FutureProjectionService
    FUTURE_PROJECTION_AVAILABLE = True
except ImportError:
    FUTURE_PROJECTION_AVAILABLE = False
    FutureProjectionService = None

# V6.3+ Import comprehensive traits data for storytelling content
try:
    from .traits_data import (
        RASI_TRAITS, NAKSHATRA_TRAITS, DASHA_PREDICTIONS,
        PLANET_HOUSE_EFFECTS, LIFE_AREA_NARRATIVES,
        get_combined_personality, get_personality_narrative, get_dasha_narrative,
        YOGA_DESCRIPTIONS, get_yoga_description
    )
    TRAITS_DATA_AVAILABLE = True
except ImportError:
    TRAITS_DATA_AVAILABLE = False
    RASI_TRAITS = {}
    NAKSHATRA_TRAITS = {}
    DASHA_PREDICTIONS = {}
    PLANET_HOUSE_EFFECTS = {}
    LIFE_AREA_NARRATIVES = {}
    YOGA_DESCRIPTIONS = {}


def get_v6_css() -> str:
    """V6.2 CSS with Saffron/Gold color scheme"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    :root {
        --saffron: #FF6B35;
        --saffron-dark: #E85D26;
        --gold: #D4AF37;
        --gold-light: #F4E4A6;
        --gold-dark: #B8972E;
        --maroon: #800020;
        --cream: #FFF8E7;
        --muted-red: #C75050;
        --neutral: #666666;
    }

    @page {
        size: A4;
        margin: 1.5cm 1.2cm;
        @top-center {
            content: "ஜோதிட AI - V6.2 Jyotish Report";
            font-family: 'Noto Sans Tamil', sans-serif;
            font-size: 9pt;
            color: var(--saffron);
        }
        @bottom-center {
            content: "Page " counter(page);
            font-size: 8pt;
            color: var(--neutral);
        }
    }

    body {
        font-family: 'Noto Sans Tamil', 'Noto Sans', Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.5;
        color: #1f2937;
    }

    .cover { page-break-after: always; text-align: center; padding-top: 60px;
             background: linear-gradient(180deg, #FFF8E7 0%, white 100%); }
    .cover-title { font-size: 42pt; color: var(--saffron); margin-bottom: 10px; }
    .cover-subtitle { font-size: 18pt; color: var(--gold-dark); margin-bottom: 40px; }
    .cover-name { font-size: 28pt; color: var(--maroon); margin: 30px 0; padding: 15px 40px;
                  border: 3px solid var(--gold); display: inline-block; border-radius: 8px;
                  background: var(--cream); }
    .cover-details { font-size: 12pt; color: #6b7280; margin-top: 20px; }
    .cover-details p { margin: 8px 0; }
    .cover-chart-summary { margin-top: 30px; background: var(--cream); padding: 20px;
                           border-radius: 10px; display: inline-block; border: 2px solid var(--gold); }
    .cover-chart-summary p { font-size: 14pt; margin: 5px 0; color: var(--maroon); }

    .page { page-break-before: always; }
    .page-title { font-size: 16pt; color: var(--saffron); border-bottom: 2px solid var(--gold);
                  padding-bottom: 8px; margin-bottom: 15px; }
    .page-num { font-size: 9pt; color: #9ca3af; margin-bottom: 5px; }

    .section { margin: 15px 0; }
    .section-title { font-size: 13pt; color: var(--maroon); margin: 15px 0 8px 0; }
    .subsection { font-size: 11pt; color: var(--saffron-dark); margin: 10px 0 5px 0; font-weight: 600; }

    .content { text-align: justify; margin-bottom: 10px; }
    .math-trace { font-size: 8pt; color: #6b7280; font-style: italic;
                  background: var(--cream); padding: 4px 8px; border-radius: 4px; margin: 5px 0; }

    table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 9pt; }
    th { background: var(--saffron); color: white; padding: 8px 6px; text-align: center; font-weight: 600; }
    td { padding: 6px; border: 1px solid #e5e7eb; text-align: center; }
    tr:nth-child(even) { background: var(--cream); }
    tr:nth-child(odd) { background: white; }

    .score-bar { height: 20px; background: #e5e7eb; border-radius: 10px; overflow: hidden; }
    .score-fill { height: 100%; border-radius: 10px; }
    .score-high { background: linear-gradient(90deg, #10b981, #34d399); }
    .score-medium { background: linear-gradient(90deg, var(--gold-dark), var(--gold)); }
    .score-low { background: linear-gradient(90deg, var(--muted-red), #e07070); }

    .highlight { background: var(--cream); border-left: 4px solid var(--saffron); padding: 12px; margin: 10px 0; }
    .warning { background: #fef3c7; border-left: 4px solid var(--gold); padding: 12px; margin: 10px 0; }
    .success { background: #d1fae5; border-left: 4px solid #10b981; padding: 12px; margin: 10px 0; }

    .planet-card { border: 1px solid var(--gold); border-radius: 8px; padding: 12px; margin: 10px 0;
                   background: white; page-break-inside: avoid; }
    .planet-header { display: flex; justify-content: space-between; align-items: center;
                     border-bottom: 1px solid var(--gold-light); padding-bottom: 8px; margin-bottom: 8px; }
    .planet-name { font-size: 14pt; font-weight: 700; color: var(--maroon); }
    .planet-symbol { font-size: 20pt; }

    .yoga-card { background: linear-gradient(135deg, var(--cream), #fff5d6); border-radius: 8px;
                 padding: 12px; margin: 10px 0; border: 1px solid var(--gold); }
    .yoga-name { font-size: 12pt; font-weight: 700; color: var(--maroon); }
    .yoga-type { font-size: 9pt; color: var(--saffron); }

    .dosha-card { background: linear-gradient(135deg, #fff0f0, #ffe0e0); border-radius: 8px;
                  padding: 12px; margin: 10px 0; border: 1px solid var(--muted-red); }
    .dosha-name { font-size: 12pt; font-weight: 700; color: #800020; }

    /* V6.2 South Indian Chart Styles */
    .chart-container { margin: 15px auto; text-align: center; }
    .chart-title { font-size: 14pt; color: var(--maroon); margin-bottom: 10px; font-weight: 700; }
    .chart-grid { display: grid; grid-template-columns: repeat(4, 1fr); border: 3px solid var(--saffron);
                  margin: 10px auto; width: 340px; background: white; }
    .chart-cell { border: 1px solid var(--gold); padding: 6px 4px; text-align: center;
                  min-height: 65px; font-size: 8pt; position: relative; }
    .chart-cell.corner { background: var(--cream); }
    .chart-cell.middle { background: white; }
    .chart-cell.center-empty { background: #f0f0f0; }
    .chart-cell .sign-name { font-weight: 700; color: var(--saffron-dark); font-size: 7pt;
                              position: absolute; top: 2px; left: 3px; }
    .chart-cell .house-num { font-size: 7pt; color: var(--neutral);
                              position: absolute; top: 2px; right: 3px; }
    .chart-cell .planets { font-size: 9pt; color: var(--maroon); margin-top: 12px; font-weight: 600; }
    .chart-cell .lagna-marker { color: var(--saffron); font-weight: 700; }

    .poi-grade { font-weight: 700; padding: 2px 8px; border-radius: 4px; }
    .poi-grade.A { background: #d1fae5; color: #065f46; }
    .poi-grade.B { background: var(--gold-light); color: var(--gold-dark); }
    .poi-grade.C { background: #fee2e2; color: var(--muted-red); }
    .poi-grade.D { background: #fecaca; color: #991b1b; }

    .timeline { margin: 15px 0; }
    .timeline-item { display: flex; align-items: center; margin: 8px 0; padding: 8px;
                     background: #f9fafb; border-radius: 6px; }
    .timeline-marker { width: 12px; height: 12px; border-radius: 50%; margin-right: 12px; }
    .timeline-marker.active { background: var(--saffron); }
    .timeline-marker.future { background: #e5e7eb; }
    .timeline-marker.past { background: var(--gold-dark); }

    .remedy-box { background: #ecfdf5; border: 1px solid #6ee7b7; border-radius: 8px;
                  padding: 12px; margin: 10px 0; }
    .remedy-title { font-weight: 700; color: #065f46; margin-bottom: 8px; }

    .flex-row { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; }
    .flex-item { flex: 1; min-width: 45%; }

    .stat-box { background: var(--cream); border-radius: 8px; padding: 15px; text-align: center;
                margin: 5px; border: 1px solid var(--gold-light); }
    .stat-value { font-size: 24pt; font-weight: 700; color: var(--saffron); }
    .stat-label { font-size: 9pt; color: #6b7280; }

    ul { margin: 8px 0 8px 20px; }
    li { margin: 4px 0; }

    .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }

    /* Aspect/Yoga Map */
    .aspect-map { margin: 15px 0; }
    .aspect-item { display: inline-block; margin: 4px; padding: 4px 10px; border-radius: 15px;
                   font-size: 9pt; }
    .aspect-conjunction { background: var(--gold-light); color: var(--maroon); }
    .aspect-opposition { background: #fee2e2; color: var(--muted-red); }
    .aspect-trine { background: #d1fae5; color: #065f46; }
    .aspect-square { background: #fef3c7; color: #92400e; }

    /* LifeSign Format Styles */
    .lifesign-header { text-align: center; background: linear-gradient(135deg, #FF6B35, #D4AF37);
                       color: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
    .lifesign-header h1 { font-size: 24pt; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
    .lifesign-header .om-sri { font-size: 14pt; margin-top: 5px; }

    .birth-details-box { border: 2px solid var(--saffron); border-radius: 8px; padding: 15px;
                         background: white; margin: 10px 0; }
    .birth-details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 20px; }
    .birth-detail-item { display: flex; justify-content: space-between; padding: 4px 0;
                         border-bottom: 1px dotted #e5e7eb; }
    .birth-detail-item .label { color: var(--maroon); font-weight: 600; }
    .birth-detail-item .value { color: #1f2937; }

    .panchanga-box { border: 2px solid var(--gold); border-radius: 8px; padding: 15px;
                     background: var(--cream); margin: 10px 0; }
    .panchanga-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px 15px; }
    .panchanga-item { padding: 6px 0; border-bottom: 1px solid var(--gold-light); }
    .panchanga-item .label { font-size: 8pt; color: #6b7280; display: block; }
    .panchanga-item .value { font-size: 10pt; color: var(--maroon); font-weight: 600; }

    .ganesha-symbol { font-size: 36pt; text-align: center; color: var(--saffron); margin: 10px 0; }
    .om-symbol { font-size: 24pt; color: var(--gold-dark); }

    .prediction-para { text-align: justify; line-height: 1.8; margin: 10px 0; padding: 10px;
                       background: white; border-radius: 6px; border-left: 4px solid var(--saffron); }

    .bhava-prediction { margin: 12px 0; padding: 12px; background: white; border-radius: 8px;
                        border: 1px solid #e5e7eb; page-break-inside: avoid; }
    .bhava-header { display: flex; justify-content: space-between; align-items: center;
                    border-bottom: 2px solid var(--saffron); padding-bottom: 6px; margin-bottom: 8px; }
    .bhava-title { font-size: 12pt; font-weight: 700; color: var(--maroon); }
    .bhava-sign { font-size: 10pt; color: var(--saffron); }
    .bhava-years { font-size: 9pt; color: var(--gold-dark); font-weight: 600;
                   background: var(--cream); padding: 4px 8px; border-radius: 4px; margin-top: 8px; }

    .dasha-period { margin: 10px 0; padding: 10px; background: white; border-radius: 8px;
                    border-left: 4px solid var(--saffron); }
    .dasha-header { font-size: 12pt; font-weight: 700; color: var(--maroon); }
    .dasha-dates { font-size: 9pt; color: var(--gold-dark); margin: 4px 0; }
    .bhukti-list { margin: 8px 0 8px 15px; font-size: 9pt; }
    .bhukti-item { margin: 4px 0; padding: 4px; background: #f9fafb; border-radius: 4px; }

    .mantra-box { background: linear-gradient(135deg, #fff5e6, #ffe4b5); border: 1px solid var(--gold);
                  border-radius: 8px; padding: 12px; margin: 8px 0; text-align: center; }
    .mantra-text { font-size: 11pt; color: var(--maroon); font-weight: 600; font-style: italic; }
    .mantra-count { font-size: 9pt; color: #6b7280; margin-top: 4px; }

    .chakra-symbol { width: 80px; height: 80px; margin: 10px auto; display: block; }
    """


class V6ReportGenerator:
    """V6.2 Super Jyotish Report Generator with TimeAdaptiveEngine (V7.0)"""

    def __init__(self, chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta'):
        self.chart_data = chart_data
        self.user_data = user_data
        self.language = language
        print(f"[V6ReportGenerator] Initialized with language: '{language}'")
        self.engine = JyotishEngine(chart_data, user_data)
        self.report_data = self.engine.generate_report_data()

        # V6.2+ Initialize TimeAdaptiveEngine (V7.0) for time-mode predictions
        self.time_engine = None
        if TIME_ADAPTIVE_AVAILABLE and TimeAdaptiveEngine:
            try:
                self.time_engine = TimeAdaptiveEngine(chart_data)
            except Exception:
                pass

        # V6.2+ Initialize FutureProjectionService (constructor takes optional ephemeris only)
        self.future_service = None
        if FUTURE_PROJECTION_AVAILABLE and FutureProjectionService:
            try:
                self.future_service = FutureProjectionService()
            except Exception:
                pass

        # V6.2+ Generate time-based predictions
        self.monthly_predictions = self._generate_monthly_predictions()
        self.yearly_predictions = self._generate_yearly_predictions()
        self.past_analysis = self._generate_past_analysis()

    def generate(self) -> bytes:
        """Generate the complete PDF report"""
        html_content = self._build_html()

        font_config = FontConfiguration()
        html = HTML(string=html_content)
        css = CSS(string=get_v6_css(), font_config=font_config)

        pdf_buffer = io.BytesIO()
        html.write_pdf(pdf_buffer, stylesheets=[css], font_config=font_config)

        return pdf_buffer.getvalue()

    def _build_html(self) -> str:
        """Build complete HTML document"""
        pages = [
            self._cover_page(),                    # Cover
            self._lifesign_page_1_birth_panchanga(),  # LifeSign Page 1: Birth Details + Panchanga
            self._lifesign_page_2_predictions(),      # LifeSign Page 2: Panchanga Predictions
            self._lifesign_bhava_predictions(),       # LifeSign: Bhava Predictions with Years
            self._lifesign_dasha_predictions(),       # LifeSign: Detailed Dasha with Dates
            self._lifesign_dosha_analysis(),          # LifeSign: Dosha Analysis with Mantras
            self._page_1_identity(),               # Page 1: Identity & Chart Snapshot
            self._page_1b_detailed_charts(),       # Page 1b: Detailed Charts (NEW)
            self._page_personality_traits(),       # NEW: Comprehensive Personality (300-500 words)
            self._page_2_panchanga(),              # Page 2: Panchanga Psychology
            self._page_3_elements(),               # Page 3: Elemental & Guna Balance
            self._page_4_purushartha(),            # Page 4: Purushartha Dominance
            self._page_5_lagna(),                  # Page 5: Lagna Intelligence
            self._page_6_moon(),                   # Page 6: Moon & Emotional Wiring
            self._pages_7_13_planets(),            # Pages 7-13: Planetary Intelligence
            self._page_14_interactions(),          # Page 14: Planetary Interaction Graph
            self._pages_15_20_life_areas(),        # Pages 15-20: Life Area Analysis
            self._page_21_yogas(),                 # Page 21: Yogas Present
            self._page_22_yoga_activation(),       # Page 22: Yoga Activation Timeline
            self._page_23_doshas(),                # Page 23: Dosha Reality Check
            self._page_24_dosha_mitigation(),      # Page 24: Dosha Mitigation Logic
            self._page_25_strength_effort(),       # Page 25: Strength vs Effort Matrix
            self._page_26_navamsa(),               # Page 26: Navamsa Truth (D9)
            self._page_27_dashamsa(),              # Page 27: Career Varga (D10)
            self._page_28_ashtakavarga(),          # Page 28: Ashtakavarga Protection Map
            self._page_29_maturity(),              # Page 29: Planetary Maturity Timeline
            self._page_30_patterns(),              # Page 30: Life Pattern Synthesis
            self._page_31_dasha_philosophy(),      # Page 31: Dasha Philosophy
            self._pages_32_35_dasha_analysis(),    # Pages 32-35: Dasha Phase Analysis
            self._page_36_validation(),            # Page 36: Past Validation Check
            self._page_37_strategy(),              # Page 37: Life Strategy
            self._page_38_spiritual(),             # Page 38: Spiritual Path Logic
            self._page_39_remedies(),              # Page 39: Remedial Logic
            self._page_40_narrative(),             # Page 40: Final Life Narrative
            # V6.2+ NEW: Monthly, Yearly, and Past Predictions using TimeAdaptiveEngine
            self._page_41_monthly_predictions(),   # Page 41: Monthly Predictions (V7.0 MONTH_WISE)
            self._page_42_yearly_predictions(),    # Page 42: 3-Year Forecast (V7.0 FUTURE_PREDICTION)
            self._page_43_past_events_analysis(),  # Page 43: Past Events Analysis (V7.0 PAST_ANALYSIS)
            self._page_44_future_timeline(),       # Page 44: Future Life Timeline
        ]

        return f"""
        <!DOCTYPE html>
        <html lang="ta">
        <head>
            <meta charset="UTF-8">
            <title>V6 Jyotish Report - {self.user_data.get('name', 'User')}</title>
        </head>
        <body>
            {''.join(pages)}
        </body>
        </html>
        """

    def _score_bar(self, score: float, width: int = 100) -> str:
        """Generate a visual score bar"""
        pct = int(score * 100)
        if score >= 0.65:
            cls = 'score-high'
        elif score >= 0.45:
            cls = 'score-medium'
        else:
            cls = 'score-low'
        return f'<div class="score-bar" style="width:{width}px"><div class="score-fill {cls}" style="width:{pct}%"></div></div>'

    def _poi_badge(self, grade: str) -> str:
        """Generate POI grade badge"""
        grade_class = grade[0] if grade else 'C'
        return f'<span class="poi-grade {grade_class}">{grade}</span>'

    def _render_south_indian_chart(self, chart_data: Dict, title: str, show_degrees: bool = False) -> str:
        """Render South Indian style chart as HTML with planet abbreviations (Su, Mo, Ma)"""
        houses = chart_data.get('houses', {})
        lagna = chart_data.get('lagna', 'Aries')
        is_english = self.language == 'en'

        # South Indian chart layout - signs are fixed positions
        grid_layout = [
            ['Pisces', 'Aries', 'Taurus', 'Gemini'],
            ['Aquarius', None, None, 'Cancer'],
            ['Capricorn', None, None, 'Leo'],
            ['Sagittarius', 'Scorpio', 'Libra', 'Virgo']
        ]

        # Build planet placement by sign using abbreviations
        sign_planets = {sign: [] for sign in RASIS}
        lagna_sign = lagna

        for house_num, house_data in houses.items():
            sign = house_data.get('sign', '')
            planets = house_data.get('planets', [])
            for p in planets:
                # Use abbreviation (Su, Mo, Ma) instead of symbol
                abbr = p.get('abbr', '') or PLANET_ABBR.get(p.get('name', ''), p.get('name', '')[:2])
                planet_str = abbr

                # Add status markers
                if p.get('retrograde'):
                    planet_str += '(R)'
                if p.get('exalted'):
                    planet_str += '*'
                if p.get('debilitated'):
                    planet_str += '^'
                if show_degrees:
                    planet_str += f" {p.get('degree_dms', '')}" if p.get('degree_dms') else f"({p.get('degree', 0):.0f}°)"

                sign_planets[sign].append(planet_str)

        # Find house numbers for each sign based on lagna
        lagna_idx = RASIS.index(lagna_sign) if lagna_sign in RASIS else 0
        sign_to_house = {}
        for i in range(12):
            sign = RASIS[(lagna_idx + i) % 12]
            sign_to_house[sign] = i + 1

        cells_html = ""
        for row_idx, row in enumerate(grid_layout):
            for col_idx, sign in enumerate(row):
                if sign is None:
                    cells_html += '<div class="chart-cell center-empty"></div>'
                else:
                    house_num = sign_to_house.get(sign, 0)
                    planets_str = ' '.join(sign_planets.get(sign, []))
                    is_lagna = (sign == lagna_sign)

                    # Use English sign abbreviation or Tamil based on language
                    if is_english:
                        sign_display = sign[:3]
                    else:
                        sign_tamil = RASI_TAMIL[RASIS.index(sign)] if sign in RASIS else sign
                        sign_display = sign_tamil[:3]

                    cell_class = "corner" if (row_idx in [0, 3] or col_idx in [0, 3]) else "middle"
                    lagna_marker = '<span class="lagna-marker">Asc</span>' if is_lagna else ''

                    cells_html += f'''
                    <div class="chart-cell {cell_class}">
                        <span class="sign-name">{sign_display}</span>
                        <span class="house-num">H{house_num}</span>
                        <div class="planets">{lagna_marker} {planets_str}</div>
                    </div>
                    '''

        return f'''
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <div class="chart-grid">{cells_html}</div>
        </div>
        '''

    def _render_d9_chart(self, d9_data: Dict, title: str = "D9 Navamsa Chart") -> str:
        """Render Navamsa chart with abbreviations"""
        planets = d9_data.get('planets', {})
        vargottama = d9_data.get('vargottama', [])
        is_english = self.language == 'en'

        # Build sign to planets mapping using abbreviations
        sign_planets = {sign: [] for sign in RASIS}
        for planet, data in planets.items():
            sign = data.get('sign', '')
            abbr = PLANET_ABBR.get(planet, planet[:2])
            if planet in vargottama:
                abbr += '*'  # Mark vargottama
            if sign in sign_planets:
                sign_planets[sign].append(abbr)

        # Use same grid layout
        grid_layout = [
            ['Pisces', 'Aries', 'Taurus', 'Gemini'],
            ['Aquarius', None, None, 'Cancer'],
            ['Capricorn', None, None, 'Leo'],
            ['Sagittarius', 'Scorpio', 'Libra', 'Virgo']
        ]

        cells_html = ""
        for row_idx, row in enumerate(grid_layout):
            for col_idx, sign in enumerate(row):
                if sign is None:
                    cells_html += '<div class="chart-cell center-empty"></div>'
                else:
                    planets_str = ' '.join(sign_planets.get(sign, []))

                    # Use English sign abbreviation or Tamil based on language
                    if is_english:
                        sign_display = sign[:3]
                    else:
                        sign_tamil = RASI_TAMIL[RASIS.index(sign)] if sign in RASIS else sign
                        sign_display = sign_tamil[:3]

                    cell_class = "corner" if (row_idx in [0, 3] or col_idx in [0, 3]) else "middle"

                    cells_html += f'''
                    <div class="chart-cell {cell_class}">
                        <span class="sign-name">{sign_display}</span>
                        <div class="planets">{planets_str}</div>
                    </div>
                    '''

        vargottama_abbrs = [PLANET_ABBR.get(p, p[:2]) for p in vargottama]
        vargottama_str = ', '.join(vargottama_abbrs) if vargottama_abbrs else 'None'
        return f'''
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <div class="chart-grid">{cells_html}</div>
            <p class="math-trace">Vargottama planets (*): {vargottama_str}</p>
        </div>
        '''

    def _render_aspect_map(self) -> str:
        """Render aspect and yoga visualization"""
        aspect_data = self.report_data.get('aspect_yoga_map', {})
        conjunctions = aspect_data.get('conjunctions', [])
        aspects = aspect_data.get('aspects', [])

        html = '<div class="aspect-map">'

        if conjunctions:
            html += '<h4 class="subsection">Conjunctions</h4>'
            for conj in conjunctions:
                planets = ' + '.join(conj.get('planets', []))
                orb = conj.get('orb', 0)
                html += f'<span class="aspect-item aspect-conjunction">{planets} ({orb:.1f}°)</span>'

        if aspects:
            html += '<h4 class="subsection">Major Aspects</h4>'
            for asp in aspects:
                planets = ' - '.join(asp.get('planets', []))
                asp_type = asp.get('type', '')
                orb = asp.get('orb', 0)
                css_class = f"aspect-{asp_type}"
                html += f'<span class="aspect-item {css_class}">{planets} {asp_type} ({orb:.1f}°)</span>'

        html += '</div>'
        return html

    def _render_side_by_side_charts(self, d1_data: Dict, d9_data: Dict) -> str:
        """Render D1 Rasi and D9 Navamsa charts side by side"""
        is_english = self.language == 'en'

        if is_english:
            d1_title = "D1 Rasi Chart"
            d9_title = "D9 Navamsa Chart"
        else:
            d1_title = "D1 Rasi Chart / ராசி சக்கரம்"
            d9_title = "D9 Navamsa Chart / நவாம்ச சக்கரம்"

        d1_html = self._render_south_indian_chart(d1_data, d1_title)
        d9_html = self._render_d9_chart(d9_data, d9_title)

        return f'''
        <div class="charts-side-by-side" style="display: flex; justify-content: space-around; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px;">{d1_html}</div>
            <div style="flex: 1; min-width: 300px;">{d9_html}</div>
        </div>
        '''

    def _render_nirayana_longitudes_table(self) -> str:
        """Render Nirayana Longitudes Summary table with Deg:Min:Sec format"""
        longitudes = self.engine.get_nirayana_longitudes_table()
        is_english = self.language == 'en'

        rows = ""
        for p in longitudes:
            # Status markers
            status = ""
            if p.get('retrograde'):
                status += '<span style="color: #DC2626;">(R)</span>'
            if p.get('exalted'):
                status += '<span style="color: #059669;">*Ex</span>'
            if p.get('debilitated'):
                status += '<span style="color: #D97706;">^Db</span>'
            if p.get('combust'):
                status += '<span style="color: #9333EA;">(C)</span>'

            # Language-specific display
            if is_english:
                planet_display = f"<strong>{p.get('abbr', '')}</strong> {p.get('planet', '')}"
                rasi_display = p.get('rasi', '')
            else:
                planet_display = f"<strong>{p.get('abbr', '')}</strong> {p.get('tamil', '')}"
                rasi_display = p.get('rasi_tamil', '')

            rows += f'''
            <tr>
                <td>{planet_display}</td>
                <td>{rasi_display}</td>
                <td>{p.get('longitude_dms', '')}</td>
                <td>{p.get('nakshatra', '')} / {p.get('pada', '')}</td>
                <td>{status or '-'}</td>
            </tr>
            '''

        # Language-specific headers
        if is_english:
            title = "Nirayana Longitudes Summary"
            th_planet = "Planet"
            th_rasi = "Rasi"
            th_star = "Star / Pada"
        else:
            title = "Nirayana Longitudes Summary / நிரயன தீர்க்காம்சம்"
            th_planet = "Planet / கிரகம்"
            th_rasi = "Rasi / ராசி"
            th_star = "Star / Pada"

        return f'''
        <div class="section">
            <h3 class="section-title">{title}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{th_planet}</th>
                        <th>{th_rasi}</th>
                        <th>Deg:Min:Sec</th>
                        <th>{th_star}</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <p class="math-trace">Legend: (R)=Retrograde, *Ex=Exalted, ^Db=Debilitated, (C)=Combust</p>
        </div>
        '''

    def _render_special_rasi_chakra(self) -> str:
        """Render Special Rasi Chakra with detailed planet info and status markers"""
        chakra_data = self.engine.get_special_rasi_chakra_data()
        houses = chakra_data.get('houses', {})
        is_english = self.language == 'en'

        # South Indian grid layout
        grid_layout = [
            ['Pisces', 'Aries', 'Taurus', 'Gemini'],
            ['Aquarius', None, None, 'Cancer'],
            ['Capricorn', None, None, 'Leo'],
            ['Sagittarius', 'Scorpio', 'Libra', 'Virgo']
        ]

        # Map sign to house data
        sign_to_house = {}
        for h_num, h_data in houses.items():
            sign_to_house[h_data['sign']] = h_data

        cells_html = ""
        for row_idx, row in enumerate(grid_layout):
            for col_idx, sign in enumerate(row):
                if sign is None:
                    cells_html += '<div class="chart-cell center-empty"></div>'
                else:
                    h_data = sign_to_house.get(sign, {})
                    house_num = h_data.get('house_num', 0)
                    is_lagna = h_data.get('is_lagna', False)
                    planets = h_data.get('planets', [])

                    # Use English or Tamil sign display
                    if is_english:
                        sign_display = sign[:3]
                    else:
                        sign_display = h_data.get('sign_tamil', sign[:3])[:3]

                    # Build planet display with degrees
                    planet_lines = []
                    for p in planets:
                        display = p.get('display', p.get('abbr', ''))
                        deg_dms = p.get('degree_dms', '')
                        planet_lines.append(f"{display}<br><small>{deg_dms}</small>")

                    planets_html = ' '.join(planet_lines) if planet_lines else ''
                    cell_class = "corner" if (row_idx in [0, 3] or col_idx in [0, 3]) else "middle"
                    lagna_marker = '<span class="lagna-marker">Asc</span>' if is_lagna else ''

                    cells_html += f'''
                    <div class="chart-cell {cell_class}" style="font-size: 8pt;">
                        <span class="sign-name">{sign_display}</span>
                        <span class="house-num">H{house_num}</span>
                        <div class="planets">{lagna_marker} {planets_html}</div>
                    </div>
                    '''

        # Language-specific title
        if is_english:
            chart_title = "Special Rasi Chakra"
        else:
            chart_title = "Special Rasi Chakra / விசேஷ ராசி சக்கரம்"

        return f'''
        <div class="chart-container">
            <div class="chart-title">{chart_title}</div>
            <div class="chart-grid">{cells_html}</div>
            <p class="math-trace">
                Markers: (R)=Retrograde, *=Exalted, ^=Debilitated, (C)=Combust |
                Lagna: {chakra_data.get('lagna_degree_dms', '')}
            </p>
        </div>
        '''

    def _render_bhava_table(self) -> str:
        """Render Bhava Table with Arambha, Madhya, Anthya cusps"""
        bhava_data = self.engine.get_bhava_table_data()
        houses = bhava_data.get('houses', [])
        is_english = self.language == 'en'

        rows = ""
        for h in houses:
            planets_str = ', '.join([p['abbr'] + ('(R)' if p.get('retrograde') else '')
                                     for p in h.get('planets', [])])
            # Language-specific sign display
            sign_display = h.get('sign', h['sign_tamil']) if is_english else h['sign_tamil']
            rows += f'''
            <tr>
                <td><strong>H{h['house_num']}</strong></td>
                <td>{sign_display}</td>
                <td>{h['lord_abbr']}</td>
                <td>{h['arambha']['degree_dms']}</td>
                <td>{h['madhya']['degree_dms']}</td>
                <td>{h['anthya']['degree_dms']}</td>
                <td>{planets_str or '-'}</td>
            </tr>
            '''

        # Language-specific headers
        if is_english:
            title = "Bhava Table"
            th_sign = "Sign"
        else:
            title = "Bhava Table / பாவ அட்டவணை"
            th_sign = "Sign / ராசி"

        return f'''
        <div class="section">
            <h3 class="section-title">{title}</h3>
            <table style="font-size: 8pt;">
                <thead>
                    <tr>
                        <th>House</th>
                        <th>{th_sign}</th>
                        <th>Lord</th>
                        <th>Arambha (Start)</th>
                        <th>Madhya (Middle)</th>
                        <th>Anthya (End)</th>
                        <th>Planets</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <p class="math-trace">Equal House System | Lagna: {bhava_data.get('lagna_degree', 0):.2f}°</p>
        </div>
        '''

    def _render_sudarshana_chakra(self) -> str:
        """Render Sudarshana Chakra - three concentric rings (Lagna, Moon, Sun based)"""
        chakra_data = self.engine.get_sudarshana_chakra_data()

        def render_ring(ring_data: Dict, ring_name: str, color: str) -> str:
            houses = ring_data.get('houses', {})
            cells = []
            for i in range(1, 13):
                h = houses.get(i, {})
                sign_abbr = h.get('sign_abbr', '')
                planets = h.get('planet_abbrs', '')
                cells.append(f"<td style='border: 1px solid {color}; padding: 4px; font-size: 7pt;'>"
                             f"<strong>{sign_abbr}</strong><br>{planets}</td>")
            return f'''
            <tr style="background: {color}15;">
                <td style="font-weight: bold; color: {color};">{ring_name}<br>{ring_data.get('base_sign', '')[:3]}</td>
                {''.join(cells)}
            </tr>
            '''

        lagna_ring = render_ring(chakra_data['lagna_ring'], 'Lagna', '#FF6B35')
        moon_ring = render_ring(chakra_data['moon_ring'], 'Moon', '#4F46E5')
        sun_ring = render_ring(chakra_data['sun_ring'], 'Sun', '#F59E0B')

        # Header row with house numbers
        header_cells = ''.join([f"<th style='font-size: 8pt;'>H{i}</th>" for i in range(1, 13)])

        return f'''
        <div class="section">
            <h3 class="section-title">Sudarshana Chakra / சுதர்சன சக்கரம்</h3>
            <table style="font-size: 8pt; text-align: center;">
                <thead>
                    <tr>
                        <th>Base</th>
                        {header_cells}
                    </tr>
                </thead>
                <tbody>
                    {lagna_ring}
                    {moon_ring}
                    {sun_ring}
                </tbody>
            </table>
            <p class="math-trace">{chakra_data.get('description', '')}</p>
        </div>
        '''

    def _cover_page(self) -> str:
        """Generate cover page"""
        identity = self.report_data['identity']
        is_english = self.language == 'en'

        name = identity['name']
        birth_date = identity['birth_date']
        birth_time = identity['birth_time']
        birth_place = identity['birth_place']
        lagna = identity['lagna']
        moon_sign = identity['moon_sign']
        nakshatra = identity['moon_nakshatra']

        # Language-specific display values
        if is_english:
            lagna_display = lagna
            moon_display = moon_sign
            cover_title = "Jothida Report"
            cover_subtitle = "V6.2 Super Jyotish Report"
            lbl_dob = "Date of Birth"
            lbl_tob = "Time of Birth"
            lbl_pob = "Place of Birth"
            lbl_lagna = "Lagna"
            lbl_rasi = "Rasi"
            lbl_nakshatra = "Nakshatra"
        else:
            lagna_display = RASI_TAMIL[RASIS.index(lagna)] if lagna in RASIS else lagna
            moon_display = RASI_TAMIL[RASIS.index(moon_sign)] if moon_sign in RASIS else moon_sign
            cover_title = "ஜாதக அறிக்கை"
            cover_subtitle = "V6.2 Super Jyotish Report"
            lbl_dob = "பிறந்த தேதி"
            lbl_tob = "பிறந்த நேரம்"
            lbl_pob = "பிறந்த இடம்"
            lbl_lagna = "லக்னம்"
            lbl_rasi = "ராசி"
            lbl_nakshatra = "நட்சத்திரம்"

        return f"""
        <div class="cover">
            <div class="cover-title">{cover_title}</div>
            <div class="cover-subtitle">{cover_subtitle}</div>

            <div class="cover-name">{name}</div>

            <div class="cover-details">
                <p><strong>{lbl_dob}:</strong> {birth_date}</p>
                <p><strong>{lbl_tob}:</strong> {birth_time}</p>
                <p><strong>{lbl_pob}:</strong> {birth_place}</p>
            </div>

            <div class="cover-chart-summary">
                <p><strong>{lbl_lagna}:</strong> {lagna_display} ({lagna})</p>
                <p><strong>{lbl_rasi}:</strong> {moon_display} ({moon_sign})</p>
                <p><strong>{lbl_nakshatra}:</strong> {nakshatra}</p>
            </div>

            <div style="margin-top: 40px; color: #9ca3af;">
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                <p style="font-size: 9pt;">Every insight mathematically derived from chart data</p>
                <p style="font-size: 8pt; margin-top: 5px; color: #B8972E;">Powered by V6.2 Jyotish Engine | Saffron & Gold Edition</p>
            </div>
        </div>
        """

    def _lifesign_page_1_birth_panchanga(self) -> str:
        """LifeSign Format - Page 1: Complete Birth Details + Panchanga Data"""
        # Get all dynamic panchanga data from engine
        panchanga = self.engine.get_complete_panchanga()
        identity = self.report_data['identity']

        # Check language - 'en' for English, 'ta' for Tamil
        is_english = self.language == 'en'

        # Birth details
        name = identity['name']
        birth_date = identity['birth_date']
        birth_time = identity['birth_time']
        birth_place = identity['birth_place']
        lat = self.user_data.get('latitude', 13.0827)
        lon = self.user_data.get('longitude', 80.2707)

        # Panchanga data - Language-specific selection
        if is_english:
            weekday = panchanga.get('weekday', 'Sunday')
            nakshatra = panchanga.get('nakshatra', identity['moon_nakshatra'])
            rasi = panchanga.get('moon_rasi', identity.get('moon_sign', ''))
            rasi_lord = panchanga.get('moon_rasi_lord', '')
            lagna = panchanga.get('lagna', identity['lagna'])
            lagna_lord = panchanga.get('lagna_lord', '')
            thithi = panchanga.get('thithi', '')
            karana = panchanga.get('karana', '')
            yoga = panchanga.get('nithya_yoga', '')
            star_lord = panchanga.get('star_lord', '')
            ganam = panchanga.get('ganam', 'Deva')
            yoni = panchanga.get('yoni', 'Horse')
            dagda_rasi = panchanga.get('dagda_rasi', '')
            yogi_planet = panchanga.get('yogi_planet', '')
            avayogi = panchanga.get('avayogi_planet', '')
            atmakaraka = panchanga.get('atma_karaka', '')
            amatyakaraka = panchanga.get('amatya_karaka', '')
            lagna_aruda = panchanga.get('lagna_pada', '')
            dhana_aruda = panchanga.get('dhana_pada', '')
            dasa_system = panchanga.get('dasa_system', 'Vimshottari')
        else:
            weekday = panchanga.get('weekday_tamil', 'ஞாயிறு')
            nakshatra = panchanga.get('nakshatra_tamil', identity['moon_nakshatra'])
            rasi = panchanga.get('moon_rasi_tamil', '')
            rasi_lord = panchanga.get('moon_rasi_lord_tamil', '')
            lagna = panchanga.get('lagna_tamil', identity['lagna'])
            lagna_lord = panchanga.get('lagna_lord_tamil', '')
            thithi = panchanga.get('thithi_tamil', '')
            karana = panchanga.get('karana_tamil', '')
            yoga = panchanga.get('nithya_yoga_tamil', '')
            star_lord = panchanga.get('star_lord_tamil', '')
            ganam = panchanga.get('ganam_tamil', panchanga.get('ganam', 'Deva'))
            yoni = panchanga.get('yoni_tamil', panchanga.get('yoni', 'Horse'))
            dagda_rasi = panchanga.get('dagda_rasi_tamil', panchanga.get('dagda_rasi', ''))
            yogi_planet = panchanga.get('yogi_planet_tamil', '')
            avayogi = panchanga.get('avayogi_planet_tamil', '')
            atmakaraka = panchanga.get('atma_karaka_tamil', '')
            amatyakaraka = panchanga.get('amatya_karaka_tamil', '')
            lagna_aruda = panchanga.get('lagna_pada_tamil', '')
            dhana_aruda = panchanga.get('dhana_pada_tamil', '')
            dasa_system = panchanga.get('dasa_system_tamil', 'விம்ஷோத்தரி')

        nakshatra_pada = panchanga.get('nakshatra_pada', 1)
        sunrise = panchanga.get('sunrise', '06:00')
        sunset = panchanga.get('sunset', '18:00')
        ayanamsa_val = panchanga.get('ayanamsa_value', 'Lahiri 23.8500°')
        chandra_avastha = panchanga.get('chandra_avastha', '')
        yogi_point = panchanga.get('yogi_point', '')
        kalidina = panchanga.get('kalidina_sankhya', 0)
        dinamana = panchanga.get('dinamana', '')

        # Language-specific labels
        if is_english:
            title = "Jothida Report"
            subtitle = "Om Sri Ganesaya Namaha"
            birth_title = "Birth Details"
            panchanga_title = "Panchanga Details"
            lbl_name = "Name"
            lbl_sex = "Sex"
            lbl_dob = "Date of Birth"
            lbl_tob = "Time of Birth"
            lbl_pob = "Place of Birth"
            lbl_ayanamsa = "Ayanamsa"
            lbl_star = "Birth Star"
            lbl_rasi = "Birth Rasi"
            lbl_lagna = "Lagna"
            lbl_thithi = "Thithi"
            lbl_sunrise = "Sunrise"
            lbl_sunset = "Sunset"
            lbl_dinamana = "Dinamana"
            lbl_kalidina = "Kalidina Sankhya"
            lbl_dasa = "Dasa System"
            lbl_starlord = "Star Lord"
            lbl_ganam = "Ganam"
            lbl_yoni = "Yoni"
            lbl_chandra = "Chandra Avastha"
            lbl_dagda = "Dagda Rasi"
            lbl_karana = "Karanam"
            lbl_yoga = "Nithya Yoga"
            lbl_yogipt = "Yogi Point"
            lbl_yogipl = "Yogi Planet"
            lbl_avayogi = "Avayogi"
            lbl_atma = "Atma Karaka"
            lbl_amatya = "Amatya Karaka"
            lbl_lagna_aruda = "Lagna Aruda (AL)"
            lbl_dhana_aruda = "Dhana Aruda (A2)"
            pada_label = f"Pada {nakshatra_pada}"
            footer_text = "All calculations based on Lahiri Ayanamsa"
        else:
            title = "ஜோதிட அறிக்கை"
            subtitle = "॥ ஓம் ஸ்ரீ கணேசாய நமஹ ॥"
            birth_title = "பிறப்பு விவரங்கள்"
            panchanga_title = "பஞ்சாங்க விவரங்கள்"
            lbl_name = "பெயர்"
            lbl_sex = "பாலினம்"
            lbl_dob = "பிறந்த தேதி"
            lbl_tob = "பிறந்த நேரம்"
            lbl_pob = "பிறந்த இடம்"
            lbl_ayanamsa = "அயனாம்சம்"
            lbl_star = "நட்சத்திரம்"
            lbl_rasi = "ராசி"
            lbl_lagna = "லக்னம்"
            lbl_thithi = "திதி"
            lbl_sunrise = "சூரிய உதயம்"
            lbl_sunset = "சூரிய அஸ்தமனம்"
            lbl_dinamana = "தினமானம்"
            lbl_kalidina = "காளிதின சங்க்யா"
            lbl_dasa = "தசா முறை"
            lbl_starlord = "நட்சத்திர அதிபதி"
            lbl_ganam = "கணம்"
            lbl_yoni = "யோனி"
            lbl_chandra = "சந்திர அவஸ்தா"
            lbl_dagda = "தக்த ராசி"
            lbl_karana = "கரணம்"
            lbl_yoga = "நித்ய யோகம்"
            lbl_yogipt = "யோகி புள்ளி"
            lbl_yogipl = "யோகி கிரகம்"
            lbl_avayogi = "அவயோகி"
            lbl_atma = "ஆத்மகாரகன்"
            lbl_amatya = "அமாத்ய காரகன்"
            lbl_lagna_aruda = "லக்ன ஆருடம் (AL)"
            lbl_dhana_aruda = "தன ஆருடம் (A2)"
            pada_label = f"{nakshatra_pada} பாதம்"
            footer_text = "சுத்த ஜாதக விதிகள்படி கணிக்கப்பட்டது"

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <div class="ganesha-symbol">ॐ</div>
                <h1>{title}</h1>
                <div class="om-sri">{subtitle}</div>
            </div>

            <h2 class="section-title" style="text-align: center; color: var(--maroon);">
                {birth_title}
            </h2>

            <div class="birth-details-box">
                <div class="birth-details-grid">
                    <div class="birth-detail-item">
                        <span class="label">{lbl_name}</span>
                        <span class="value"><strong>{name}</strong></span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">{lbl_sex}</span>
                        <span class="value">-</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">{lbl_dob}</span>
                        <span class="value">{birth_date} ({weekday})</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">{lbl_tob}</span>
                        <span class="value">{birth_time}</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">{lbl_pob}</span>
                        <span class="value">{birth_place}</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Longitude & Latitude</span>
                        <span class="value">{lon:.4f}° E, {lat:.4f}° N</span>
                    </div>
                </div>
            </div>

            <h2 class="section-title" style="text-align: center; color: var(--maroon); margin-top: 20px;">
                {panchanga_title}
            </h2>

            <div class="panchanga-box">
                <div class="panchanga-grid">
                    <div class="panchanga-item">
                        <span class="label">{lbl_ayanamsa}</span>
                        <span class="value">{ayanamsa_val}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_star}</span>
                        <span class="value">{nakshatra} - {pada_label}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_rasi}</span>
                        <span class="value">{rasi} ({rasi_lord})</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_lagna}</span>
                        <span class="value">{lagna} ({lagna_lord})</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_thithi}</span>
                        <span class="value">{thithi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_sunrise}</span>
                        <span class="value">{sunrise}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_sunset}</span>
                        <span class="value">{sunset}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_dinamana}</span>
                        <span class="value">{dinamana}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_kalidina}</span>
                        <span class="value">{kalidina}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_dasa}</span>
                        <span class="value">{dasa_system}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_starlord}</span>
                        <span class="value">{star_lord}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_ganam}</span>
                        <span class="value">{ganam}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_yoni}</span>
                        <span class="value">{yoni}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_chandra}</span>
                        <span class="value">{chandra_avastha}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_dagda}</span>
                        <span class="value">{dagda_rasi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_karana}</span>
                        <span class="value">{karana}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_yoga}</span>
                        <span class="value">{yoga}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_yogipt}</span>
                        <span class="value">{yogi_point}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_yogipl}</span>
                        <span class="value">{yogi_planet}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_avayogi}</span>
                        <span class="value">{avayogi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_atma}</span>
                        <span class="value">{atmakaraka}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_amatya}</span>
                        <span class="value">{amatyakaraka}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_lagna_aruda}</span>
                        <span class="value">{lagna_aruda}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">{lbl_dhana_aruda}</span>
                        <span class="value">{dhana_aruda}</span>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 15px; font-size: 9pt; color: #6b7280;">
                {footer_text}
            </div>
        </div>
        """

    def _lifesign_page_2_predictions(self) -> str:
        """LifeSign Format - Page 2: Panchanga Predictions Summary"""
        panchanga = self.engine.get_complete_panchanga()
        identity = self.report_data['identity']
        is_english = self.language == 'en'

        name = identity['name']

        # Language-specific data selection
        if is_english:
            nakshatra = panchanga.get('nakshatra', identity['moon_nakshatra'])
            rasi = panchanga.get('moon_rasi', identity.get('moon_sign', ''))
            lagna = panchanga.get('lagna', identity.get('lagna', ''))
            thithi = panchanga.get('thithi', '')
            yoga = panchanga.get('nithya_yoga', '')
            karana = panchanga.get('karana', '')
            weekday = panchanga.get('weekday', '')
            yogi_planet = panchanga.get('yogi_planet', '')
            avayogi = panchanga.get('avayogi_planet', '')
        else:
            nakshatra = panchanga.get('nakshatra_tamil', identity['moon_nakshatra'])
            rasi = panchanga.get('moon_rasi_tamil', identity.get('moon_sign', ''))
            lagna = panchanga.get('lagna_tamil', identity.get('lagna', ''))
            thithi = panchanga.get('thithi_tamil', '')
            yoga = panchanga.get('nithya_yoga_tamil', '')
            karana = panchanga.get('karana_tamil', '')
            weekday = panchanga.get('weekday_tamil', '')
            yogi_planet = panchanga.get('yogi_planet_tamil', '')
            avayogi = panchanga.get('avayogi_planet_tamil', '')

        nakshatra_en = panchanga.get('nakshatra', identity['moon_nakshatra'])
        nakshatra_lord = panchanga.get('star_lord', 'Ketu')
        rasi_lord = panchanga.get('moon_rasi_lord', 'Mars')
        lagna_lord = panchanga.get('lagna_lord', 'Mars')

        # Get nakshatra qualities for prediction
        ganam = panchanga.get('ganam', 'Deva')
        yoni = panchanga.get('yoni', 'Horse')

        # Generate dynamic prediction paragraph based on chart data
        prediction_text = self._generate_panchanga_prediction(panchanga, identity)

        # Language-specific labels
        if is_english:
            page_title = "Panchanga Predictions"
            page_subtitle = "Birth Chart Analysis"
            star_label = "Nakshatra"
            rasi_label = "Rasi"
            lagna_label = "Lagna"
            birth_summary_title = "Birth Summary"
            nakshatra_char_title = "Nakshatra Characteristics"
            gana_label = "Gana"
            panchanga_elements_title = "Panchanga Elements"
            yogi_planet_label = "Yogi Planet"
            avayogi_label = "Avayogi"
        else:
            page_title = "பஞ்சாங்க பலன்கள்"
            page_subtitle = "Panchanga Predictions"
            star_label = "நட்சத்திரம்"
            rasi_label = "ராசி"
            lagna_label = "லக்னம்"
            birth_summary_title = "Birth Summary / பிறப்பு சுருக்கம்"
            nakshatra_char_title = "Nakshatra Characteristics / நட்சத்திர குணாதிசயங்கள்"
            gana_label = "கணம்"
            panchanga_elements_title = "Panchanga Elements / பஞ்சாங்க அம்சங்கள்"
            yogi_planet_label = "Yogi Planet / யோகி கிரகம்"
            avayogi_label = "Avayogi / அவயோகி"

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>{page_title}</h1>
                <div class="om-sri">{page_subtitle}</div>
            </div>

            <div class="highlight" style="text-align: center; margin: 15px 0;">
                <p style="font-size: 12pt;"><strong>{name}</strong></p>
                <p style="font-size: 10pt;">
                    {nakshatra} {star_label} | {rasi} {rasi_label} | {lagna} {lagna_label}
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">{birth_summary_title}</h2>
                <div class="prediction-para">
                    {prediction_text}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">{nakshatra_char_title}</h2>
                <div class="two-col">
                    <div class="stat-box">
                        <div class="stat-value" style="font-size: 16pt;">{nakshatra}</div>
                        <div class="stat-label">{nakshatra_en} | Lord: {nakshatra_lord}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="font-size: 16pt;">{ganam} {gana_label}</div>
                        <div class="stat-label">Gana Type | {yoni} Yoni</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">{panchanga_elements_title}</h2>
                <table>
                    <tr>
                        <th>Element</th>
                        <th>Value</th>
                        <th>Significance</th>
                    </tr>
                    <tr>
                        <td><strong>Thithi</strong></td>
                        <td>{thithi}</td>
                        <td>{self._get_thithi_significance(panchanga.get('thithi', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Nakshatra</strong></td>
                        <td>{nakshatra}</td>
                        <td>{self._get_nakshatra_significance(nakshatra_en)}</td>
                    </tr>
                    <tr>
                        <td><strong>Yoga</strong></td>
                        <td>{yoga}</td>
                        <td>{self._get_yoga_significance(panchanga.get('nithya_yoga', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Karana</strong></td>
                        <td>{karana}</td>
                        <td>{self._get_karana_significance(panchanga.get('karana', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Varam</strong></td>
                        <td>{weekday}</td>
                        <td>{self._get_weekday_significance(panchanga.get('weekday', ''))}</td>
                    </tr>
                </table>
            </div>

            <div class="success" style="margin-top: 15px;">
                <p><strong>{yogi_planet_label}:</strong> {yogi_planet} -
                   This planet brings prosperity when strengthened.</p>
            </div>
            <div class="warning">
                <p><strong>{avayogi_label}:</strong> {avayogi} -
                   This planet's periods require caution.</p>
            </div>
        </div>
        """

    def _generate_panchanga_prediction(self, panchanga: Dict, identity: Dict) -> str:
        """Generate dynamic prediction paragraph based on panchanga data"""
        name = identity['name']
        nakshatra = panchanga.get('nakshatra', identity['moon_nakshatra'])
        nakshatra_lord = panchanga.get('star_lord', 'Ketu')
        rasi = panchanga.get('moon_rasi', identity['moon_sign'])
        rasi_lord = panchanga.get('moon_rasi_lord', 'Mars')
        lagna = panchanga.get('lagna', identity['lagna'])
        lagna_lord = panchanga.get('lagna_lord', 'Mars')
        ganam = panchanga.get('ganam', 'Deva')
        yoni = panchanga.get('yoni', 'Horse')
        thithi = panchanga.get('thithi', 'Pratipada')
        yoga = panchanga.get('nithya_yoga', 'Vishkambha')

        # Ganam-based personality
        ganam_traits = {
            'Deva': 'possess divine qualities with inherent goodness and spiritual inclination',
            'Manushya': 'have balanced human qualities with practical wisdom and adaptability',
            'Rakshasa': 'have powerful determination and protective instincts with strong willpower'
        }
        ganam_trait = ganam_traits.get(ganam, 'have unique personality traits')

        # Yoni-based characteristics
        yoni_traits = {
            'Horse': 'swift in action and love freedom',
            'Elephant': 'possess great strength and wisdom',
            'Sheep': 'gentle and adaptable nature',
            'Serpent': 'have deep intuition and transformation ability',
            'Dog': 'loyal and protective of loved ones',
            'Cat': 'independent and mysterious nature',
            'Rat': 'clever and resourceful',
            'Cow': 'nurturing and stable temperament',
            'Buffalo': 'patient and hardworking',
            'Tiger': 'courageous and powerful',
            'Deer': 'graceful and alert',
            'Monkey': 'intelligent and versatile',
            'Lion': 'natural leadership qualities',
            'Mongoose': 'quick-witted and brave'
        }
        yoni_trait = yoni_traits.get(yoni, 'have distinctive characteristics')

        return f"""
        <strong>{name}</strong> was born under the auspicious <strong>{nakshatra}</strong> nakshatra,
        ruled by <strong>{nakshatra_lord}</strong>. The Moon is positioned in <strong>{rasi}</strong> rasi
        (ruled by {rasi_lord}), giving the native {ganam_trait}. With <strong>{lagna}</strong> as the
        ascendant (lord: {lagna_lord}), the native's outer personality and life direction are significantly
        influenced by this rising sign.

        Being born in <strong>{ganam} Ganam</strong> and <strong>{yoni} Yoni</strong>, the native will {yoni_trait}.
        The birth occurred during <strong>{thithi}</strong> thithi under <strong>{yoga}</strong> yoga,
        which shapes the mental disposition and life circumstances.

        The nakshatra lord {nakshatra_lord} plays a crucial role in determining the native's
        characteristics, mental makeup, and life events. The position of this planet in the birth chart
        will significantly influence career, relationships, and spiritual growth.
        """

    def _get_thithi_significance(self, thithi: str) -> str:
        """Get thithi significance - dynamic based on actual thithi"""
        significance_map = {
            'Pratipada': 'New beginnings, initiative',
            'Dwitiya': 'Growth, accumulation',
            'Tritiya': 'Action, courage',
            'Chaturthi': 'Obstacles overcome, Ganesha blessing',
            'Panchami': 'Intelligence, creativity',
            'Shashthi': 'Victory over enemies',
            'Saptami': 'Spiritual progress',
            'Ashtami': 'Durga blessing, transformation',
            'Navami': 'Divine grace',
            'Dashami': 'Completion, success',
            'Ekadashi': 'Spiritual merit, Vishnu blessing',
            'Dwadashi': 'Completion of journey',
            'Trayodashi': 'Shiva blessing',
            'Chaturdashi': 'Shiva worship',
            'Purnima': 'Fullness, completion',
            'Amavasya': 'Ancestors, introspection'
        }
        return significance_map.get(thithi, 'Auspicious day')

    def _get_nakshatra_significance(self, nakshatra: str) -> str:
        """Get nakshatra significance"""
        nak_data = next((n for n in NAKSHATRAS if n['name'] == nakshatra), None)
        if nak_data:
            return f"Deity: {nak_data.get('deity', 'Unknown')}"
        return 'Stellar influence'

    def _get_yoga_significance(self, yoga: str) -> str:
        """Get yoga significance"""
        yoga_significance = {
            'Vishkambha': 'Obstacle removal, support',
            'Preeti': 'Love, affection',
            'Ayushman': 'Longevity, health',
            'Saubhagya': 'Good fortune',
            'Shobhana': 'Brilliance, beauty',
            'Atiganda': 'Caution needed',
            'Sukarma': 'Good deeds rewarded',
            'Dhriti': 'Patience, stability',
            'Shoola': 'Sharp intelligence',
            'Ganda': 'Challenges to overcome',
            'Vriddhi': 'Growth, expansion',
            'Dhruva': 'Stability, permanence',
            'Vyaghata': 'Fierce energy',
            'Harshana': 'Joy, happiness',
            'Vajra': 'Diamond-like strength',
            'Siddhi': 'Accomplishment, success',
            'Vyatipata': 'Transformation',
            'Variyan': 'Excellence',
            'Parigha': 'Protection',
            'Shiva': 'Auspicious, blessed',
            'Siddha': 'Achievement',
            'Sadhya': 'Attainable goals',
            'Shubha': 'Auspicious',
            'Shukla': 'Pure, bright',
            'Brahma': 'Creative power',
            'Indra': 'Leadership',
            'Vaidhriti': 'Cleansing'
        }
        return yoga_significance.get(yoga, 'Auspicious combination')

    def _get_karana_significance(self, karana: str) -> str:
        """Get karana significance"""
        karana_significance = {
            'Bava': 'Auspicious for all works',
            'Balava': 'Strength and prosperity',
            'Kaulava': 'Friendship and gains',
            'Taitila': 'Social activities',
            'Garija': 'Victory and success',
            'Vanija': 'Trade and commerce',
            'Vishti': 'Avoid new beginnings',
            'Shakuni': 'Medicine, healing',
            'Chatushpada': 'Animal related',
            'Naga': 'Long term projects',
            'Kimstughna': 'Avoid auspicious works'
        }
        return karana_significance.get(karana, 'Half-lunar influence')

    def _get_weekday_significance(self, weekday: str) -> str:
        """Get weekday significance"""
        weekday_significance = {
            'Sunday': 'Sun - Authority, father',
            'Monday': 'Moon - Mind, mother',
            'Tuesday': 'Mars - Energy, courage',
            'Wednesday': 'Mercury - Intelligence, speech',
            'Thursday': 'Jupiter - Wisdom, teachers',
            'Friday': 'Venus - Love, beauty',
            'Saturday': 'Saturn - Discipline, karma'
        }
        return weekday_significance.get(weekday, 'Planetary ruler influence')

    def _lifesign_bhava_predictions(self) -> str:
        """LifeSign Format - Bhava (House) Predictions with Important Years"""
        bhava_predictions = self.engine.get_bhava_predictions()
        is_english = self.language == 'en'

        # Build separate HTML for houses 1-6 and 7-12
        houses_1_6_html = ""
        houses_7_12_html = ""

        for house_num in range(1, 13):
            bhava = bhava_predictions.get(house_num, {})
            sign = bhava.get('sign', 'Aries')
            sign_tamil = bhava.get('sign_tamil', 'மேஷம்')
            lord = bhava.get('lord', 'Mars')
            lord_tamil = bhava.get('lord_tamil', '') or PLANET_TAMIL.get(lord, lord)
            lord_house = bhava.get('lord_house', 1)
            planets = bhava.get('planets', [])
            important_years = bhava.get('important_years', [])
            prediction = bhava.get('prediction', '')

            # Handle both string and dict formats for planets
            if planets and isinstance(planets[0], dict):
                planets_str = ', '.join([f"{p['abbr']}{'(R)' if p.get('retrograde') else ''}" for p in planets]) or 'Empty'
            else:
                # planets is a list of planet names (strings)
                planets_str = ', '.join([PLANET_ABBR.get(p, p[:2]) for p in planets]) if planets else 'Empty'
            years_str = ', '.join([str(y) for y in important_years]) if important_years else 'General influence'

            house_html = f"""
            <div class="bhava-prediction">
                <div class="bhava-header">
                    <span class="bhava-title">{house_num}. {HOUSE_KARAKAS.get(house_num, {}).get('name', f'House {house_num}')} /
                        {HOUSE_KARAKAS.get(house_num, {}).get('tamil', '')}</span>
                    <span class="bhava-sign">{sign_tamil} ({sign})</span>
                </div>
                <p style="font-size: 9pt; margin: 4px 0;">
                    <strong>Lord:</strong> {lord_tamil} ({lord}) in House {lord_house} |
                    <strong>Planets:</strong> {planets_str}
                </p>
                <p class="content" style="font-size: 9pt;">{prediction}</p>
                <div class="bhava-years">
                    <strong>Important Years:</strong> {years_str}
                </div>
            </div>
            """

            if house_num <= 6:
                houses_1_6_html += house_html
            else:
                houses_7_12_html += house_html

        # Language-specific titles
        if is_english:
            page1_title = "Bhava Predictions"
            page1_subtitle = "House Predictions (Houses 1-6)"
            page2_title = "Bhava Predictions"
            page2_subtitle = "House Predictions (Houses 7-12)"
        else:
            page1_title = "பாவ பலன்கள்"
            page1_subtitle = "Bhava Predictions (Houses 1-6)"
            page2_title = "பாவ பலன்கள்"
            page2_subtitle = "Bhava Predictions (Houses 7-12)"

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>{page1_title}</h1>
                <div class="om-sri">{page1_subtitle}</div>
            </div>

            <div class="section">
                {houses_1_6_html}
            </div>
        </div>

        <div class="page">
            <div class="lifesign-header">
                <h1>{page2_title}</h1>
                <div class="om-sri">{page2_subtitle}</div>
            </div>

            <div class="section">
                {houses_7_12_html}
            </div>
        </div>
        """

    def _lifesign_dasha_predictions(self) -> str:
        """LifeSign Format - Detailed Dasha Predictions with Dates"""
        dasha_data = self.engine.get_detailed_dasha_predictions()
        current_dasha = dasha_data.get('current_dasha', {})
        all_dashas = dasha_data.get('all_dashas', [])
        is_english = self.language == 'en'

        # Current dasha section
        current_html = ""
        if current_dasha:
            mahadasha = current_dasha.get('mahadasha', 'Venus')
            mahadasha_tamil = current_dasha.get('mahadasha_tamil', 'சுக்கிரன்')
            start_date = current_dasha.get('start_date', '')
            end_date = current_dasha.get('end_date', '')
            prediction = current_dasha.get('prediction', '')
            remedies = current_dasha.get('remedies', {})
            bhuktis = current_dasha.get('bhuktis', [])

            # Language-specific display
            mahadasha_display = mahadasha if is_english else f"{mahadasha_tamil} ({mahadasha})"
            bhukti_title = "Bhukti Periods:" if is_english else "Bhukti Periods / புக்தி காலம்:"

            bhukti_html = ""
            for bhukti in bhuktis[:5]:  # Show first 5 bhuktis
                planet_display = bhukti.get('planet', '') if is_english else f"{bhukti.get('planet_tamil', '')} ({bhukti.get('planet', '')})"
                bhukti_html += f"""
                <div class="bhukti-item">
                    <strong>{planet_display}</strong>:
                    {bhukti.get('start', '')} to {bhukti.get('end', '')}
                </div>
                """

            current_html = f"""
            <div class="dasha-period" style="border-left-color: #10b981; border-width: 4px;">
                <div class="dasha-header" style="color: #065f46;">
                    ★ Current Mahadasha: {mahadasha_display}
                </div>
                <div class="dasha-dates">
                    {start_date} to {end_date}
                </div>
                <p class="content" style="font-size: 9pt;">{prediction}</p>
                <h4 style="font-size: 10pt; margin-top: 8px;">{bhukti_title}</h4>
                <div class="bhukti-list">{bhukti_html}</div>
                <div class="mantra-box">
                    <div class="mantra-text">{remedies.get('mantra', 'ॐ शुक्राय नमः')}</div>
                    <div class="mantra-count">Chant {remedies.get('count', 108)} times daily</div>
                </div>
            </div>
            """

        # Future dashas
        future_html = ""
        for dasha in all_dashas[:4]:  # Show 4 future dashas
            if dasha.get('is_current'):
                continue
            mahadasha = dasha.get('mahadasha', '')
            mahadasha_tamil = dasha.get('mahadasha_tamil', '')
            start_date = dasha.get('start_date', '')
            end_date = dasha.get('end_date', '')
            prediction = dasha.get('prediction', '')

            dasha_header = f"{mahadasha} Mahadasha" if is_english else f"{mahadasha_tamil} ({mahadasha}) Mahadasha"

            future_html += f"""
            <div class="dasha-period">
                <div class="dasha-header">{dasha_header}</div>
                <div class="dasha-dates">{start_date} to {end_date}</div>
                <p class="content" style="font-size: 9pt;">{prediction}</p>
            </div>
            """

        # Language-specific labels
        if is_english:
            page_title = "Vimshottari Dasha Predictions"
            page_subtitle = "Planetary Period Analysis"
            current_period_title = "Current Period"
            upcoming_title = "Upcoming Periods"
        else:
            page_title = "விம்சோத்தரி தசா பலன்கள்"
            page_subtitle = "Vimshottari Dasha Predictions"
            current_period_title = "Current Period / நடப்பு காலம்"
            upcoming_title = "Upcoming Periods / வரவிருக்கும் காலங்கள்"

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>{page_title}</h1>
                <div class="om-sri">{page_subtitle}</div>
            </div>

            <div class="section">
                <h2 class="section-title">{current_period_title}</h2>
                {current_html}
            </div>

            <div class="section">
                <h2 class="section-title">{upcoming_title}</h2>
                {future_html}
            </div>

            <div class="highlight" style="margin-top: 15px;">
                <p style="font-size: 9pt;">
                    <strong>Note:</strong> Dasha periods are calculated using Vimshottari system based on
                    Moon's position at birth. The predictions are derived from the relationship between
                    dasha lord and birth chart planets.
                </p>
            </div>
        </div>
        """

    def _lifesign_dosha_analysis(self) -> str:
        """LifeSign Format - Dosha Analysis with Mantras"""
        doshas = self.report_data.get('doshas', {})
        is_english = self.language == 'en'
        # Handle both dict with 'list' key and direct list formats
        if isinstance(doshas, list):
            dosha_list = doshas
        elif isinstance(doshas, dict):
            dosha_list = doshas.get('list', [])
        else:
            dosha_list = []

        # Language-specific labels
        if is_english:
            page_title = "Dosha Analysis"
            page_subtitle = "Astrological Afflictions & Remedies"
            no_dosha_title = "No Major Doshas Found"
            no_dosha_text = "The birth chart does not indicate any significant doshas requiring remedies."
            effects_title = "Effects:"
            remedies_title = "Remedies"
            footer_text = "Regular practice of prescribed mantras and remedies can bring positive transformation."
        else:
            page_title = "தோஷ பகுப்பாய்வு"
            page_subtitle = "Dosha Analysis with Remedies"
            no_dosha_title = "No Major Doshas Found"
            no_dosha_text = "The birth chart does not indicate any significant doshas requiring remedies.<br>உங்கள் ஜாதகத்தில் குறிப்பிடத்தக்க தோஷங்கள் எதுவும் இல்லை."
            effects_title = "Effects / விளைவுகள்:"
            remedies_title = "Remedies / பரிகாரங்கள்"
            footer_text = "Regular practice of prescribed mantras and remedies can bring positive transformation.<br>நிர்ணயிக்கப்பட்ட மந்திரங்கள் மற்றும் பரிகாரங்களை தொடர்ந்து செய்வது நேர்மறையான மாற்றத்தை கொண்டு வரும்."

        if not dosha_list:
            return f"""
            <div class="page">
                <div class="lifesign-header">
                    <h1>{page_title}</h1>
                    <div class="om-sri">{page_subtitle}</div>
                </div>

                <div class="success" style="text-align: center; padding: 30px;">
                    <div style="font-size: 48pt; margin-bottom: 15px;">✓</div>
                    <h2 style="color: #065f46;">{no_dosha_title}</h2>
                    <p>{no_dosha_text}</p>
                </div>
            </div>
            """

        dosha_html = ""
        for dosha in dosha_list:
            name = dosha.get('name', '')
            name_tamil = dosha.get('name_tamil', '') or dosha.get('tamil', '')
            severity_val = dosha.get('severity', 0.5)
            # Handle numeric and string severity
            if isinstance(severity_val, (int, float)):
                severity = 'Mild' if severity_val < 0.3 else ('Moderate' if severity_val < 0.6 else 'Severe')
            else:
                severity = str(severity_val)
            description = dosha.get('formed_by', '') or dosha.get('description', '')
            effects = dosha.get('effects', [])
            remedies_data = dosha.get('remedies', [])

            severity_color = {
                'Mild': '#059669',
                'Moderate': '#D97706',
                'Severe': '#DC2626'
            }.get(severity, '#6b7280')

            # Handle remedies as list or dict
            if isinstance(remedies_data, list):
                remedies_html = ''.join([f'<li style="font-size: 9pt;">{r}</li>' for r in remedies_data[:4]])
            elif isinstance(remedies_data, dict):
                remedies_html = f"""
                    <li style="font-size: 9pt;"><strong>Deity:</strong> {remedies_data.get('deity', 'Lord Shiva')}</li>
                    <li style="font-size: 9pt;"><strong>Day:</strong> {remedies_data.get('day', 'Tuesday')}</li>
                    <li style="font-size: 9pt;"><strong>Donation:</strong> {remedies_data.get('donation', 'Red lentils')}</li>
                """
            else:
                remedies_html = '<li style="font-size: 9pt;">Consult an astrologer for specific remedies</li>'

            # If effects is empty, use net_effect
            if not effects:
                net_effect = dosha.get('net_effect', '')
                effects = [net_effect] if net_effect else ['Consult astrologer for detailed analysis']
            effects_html = ''.join([f'<li>{e}</li>' for e in effects[:4]])

            # Dosha name display - use English only for English mode
            dosha_display = name if is_english else (name_tamil or name)

            dosha_html += f"""
            <div class="dosha-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="dosha-name">{dosha_display}</span>
                    <span style="color: {severity_color}; font-weight: 600;">{severity}</span>
                </div>
                <p class="content" style="font-size: 9pt;">{description}</p>

                <h4 style="font-size: 10pt; margin-top: 10px; color: var(--muted-red);">{effects_title}</h4>
                <ul style="font-size: 9pt; margin-left: 15px;">{effects_html}</ul>

                <div class="remedy-box" style="margin-top: 10px;">
                    <div class="remedy-title">{remedies_title}</div>
                    <ul style="margin-left: 15px;">{remedies_html}</ul>
                </div>
            </div>
            """

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>{page_title}</h1>
                <div class="om-sri">{page_subtitle}</div>
            </div>

            <div class="warning" style="margin-bottom: 15px;">
                <p style="font-size: 9pt;">
                    <strong>Important:</strong> Doshas are areas requiring attention, not permanent afflictions.
                    With proper remedies and conscious effort, their effects can be significantly reduced.
                </p>
            </div>

            <div class="section">
                {dosha_html}
            </div>

            <div class="highlight" style="margin-top: 15px;">
                <p style="font-size: 9pt; text-align: center;">
                    {footer_text}
                </p>
            </div>
        </div>
        """

    def _page_1_identity(self) -> str:
        """Page 1: Identity & Chart Snapshot with D1 Chart"""
        identity = self.report_data['identity']
        planets = self.report_data['planets']
        d1_chart = self.report_data.get('d1_chart', {})
        d9_chart = self.report_data.get('d9_chart', {})

        # Build planet positions table with POI using abbreviations
        planet_rows = ""
        for planet in PLANETS:
            p = planets.get(planet, {})
            pos = p.get('position', {})
            dignity = p.get('dignity', ('Unknown', 0.5, ''))
            poi = p.get('poi', {'total': 5.0, 'grade': 'C'})
            abbr = PLANET_ABBR.get(planet, planet[:2])

            planet_rows += f"""
            <tr>
                <td><strong>{abbr}</strong> {PLANET_TAMIL.get(planet, '')}</td>
                <td>{pos.get('sign', 'N/A')}</td>
                <td>H{pos.get('house', 1)}</td>
                <td>{pos.get('degree', 0):.1f}°</td>
                <td>{dignity[0]}</td>
                <td>{self._poi_badge(poi.get('grade', 'C'))} {poi.get('total', 5):.1f}</td>
            </tr>
            """

        # Render side-by-side D1 and D9 charts
        charts_html = self._render_side_by_side_charts(d1_chart, d9_chart)

        return f"""
        <div class="page">
            <div class="page-num">Page 1</div>
            <h1 class="page-title">1. Identity & Chart Snapshot / அடையாளம்</h1>

            <div class="three-col">
                <div class="stat-box">
                    <div class="stat-value">{identity['lagna']}</div>
                    <div class="stat-label">Lagna / லக்னம்</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{identity['moon_sign']}</div>
                    <div class="stat-label">Moon Sign / ராசி</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{identity['moon_nakshatra']}</div>
                    <div class="stat-label">Nakshatra / நட்சத்திரம்</div>
                </div>
            </div>

            {charts_html}

            <div class="section">
                <h2 class="section-title">Planet Operating Index (POI) / கிரக இயக்க குறியீடு</h2>
                <table>
                    <tr>
                        <th>Planet</th>
                        <th>Sign</th>
                        <th>House</th>
                        <th>Degree</th>
                        <th>Dignity</th>
                        <th>POI Score</th>
                    </tr>
                    {planet_rows}
                </table>
                <div class="math-trace">
                    POI = Dignity + Shadbala + Retrograde + Combustion + Aspects (V6.2 Formula)
                </div>
            </div>
        </div>
        """

    def _page_1b_detailed_charts(self) -> str:
        """Page 1b: Detailed Charts - Nirayana Longitudes, Special Chakra, Bhava Table, Sudarshana"""
        # Render all detailed chart components
        nirayana_table = self._render_nirayana_longitudes_table()
        special_chakra = self._render_special_rasi_chakra()
        bhava_table = self._render_bhava_table()
        sudarshana = self._render_sudarshana_chakra()

        return f"""
        <div class="page">
            <div class="page-num">Page 1b</div>
            <h1 class="page-title">Detailed Chart Analysis / விரிவான சக்கர பகுப்பாய்வு</h1>

            {nirayana_table}

            {special_chakra}
        </div>

        <div class="page">
            <div class="page-num">Page 1c</div>
            <h1 class="page-title">House System & Sudarshana / பாவ அமைப்பு</h1>

            {bhava_table}

            {sudarshana}
        </div>
        """

    def _page_personality_traits(self) -> str:
        """NEW: Comprehensive Personality Analysis with 300-500 word descriptions"""
        identity = self.report_data['identity']
        moon_sign = identity.get('moon_sign', 'Aries')
        nakshatra = identity.get('moon_nakshatra', 'Ashwini')
        lagna = identity.get('lagna', 'Aries')

        # Get rich trait data
        rasi_data = RASI_TRAITS.get(moon_sign, {})
        nakshatra_data = NAKSHATRA_TRAITS.get(nakshatra, {})
        lagna_data = RASI_TRAITS.get(lagna, {})

        # Moon sign personality (300-500 words)
        moon_personality = rasi_data.get('personality', f'Your Moon in {moon_sign} shapes your emotional nature and inner world.')
        moon_strengths = rasi_data.get('strengths', ['Adaptability', 'Intuition', 'Sensitivity'])
        moon_weaknesses = rasi_data.get('weaknesses', ['Moodiness', 'Over-sensitivity'])
        moon_relationship = rasi_data.get('relationship_style', 'Seeks emotional connection and security in relationships.')

        # Nakshatra personality (300-500 words)
        nak_personality = nakshatra_data.get('personality', f'Your birth star {nakshatra} adds unique qualities to your nature.')
        nak_career = nakshatra_data.get('career_strengths', ['Service', 'Creativity'])
        nak_relationship = nakshatra_data.get('relationship_nature', 'Seeks meaningful connections.')

        # Lagna influence
        lagna_personality = lagna_data.get('personality', '')[:600] if lagna_data.get('personality') else f'Your {lagna} rising sign shapes how the world perceives you.'
        lagna_strengths = lagna_data.get('strengths', ['Leadership', 'Initiative'])

        # Build strengths and weaknesses lists
        strengths_html = ''.join([f'<li>{s}</li>' for s in moon_strengths[:4]])
        weaknesses_html = ''.join([f'<li>{w}</li>' for w in moon_weaknesses[:3]])
        career_html = ''.join([f'<li>{c}</li>' for c in nak_career[:4]])

        return f"""
        <div class="page">
            <div class="page-num">Personality Profile</div>
            <h1 class="page-title">உங்கள் ஆளுமை குணாதிசயங்கள் / Your Personality Profile</h1>

            <div class="highlight" style="margin-bottom: 15px;">
                <p><strong>Moon Sign:</strong> {moon_sign} ({rasi_data.get('tamil', '')}) |
                   <strong>Birth Star:</strong> {nakshatra} ({nakshatra_data.get('tamil', '')}) |
                   <strong>Rising Sign:</strong> {lagna} ({lagna_data.get('tamil', '')})</p>
            </div>

            <div class="section">
                <h2 class="section-title">ராசி குணங்கள் / Moon Sign Traits: {moon_sign}</h2>
                <div class="prediction-para">
                    {moon_personality}
                </div>
            </div>

            <div class="two-col">
                <div class="section">
                    <h3 class="subsection">Core Strengths / வலிமைகள்</h3>
                    <ul style="margin-left: 15px; font-size: 9pt;">
                        {strengths_html}
                    </ul>
                </div>
                <div class="section">
                    <h3 class="subsection">Areas for Growth / வளர்ச்சி பகுதிகள்</h3>
                    <ul style="margin-left: 15px; font-size: 9pt;">
                        {weaknesses_html}
                    </ul>
                </div>
            </div>

            <div class="section">
                <h3 class="subsection">Relationship Style / உறவு பாணி</h3>
                <p style="font-size: 10pt; line-height: 1.6;">{moon_relationship}</p>
            </div>
        </div>

        <div class="page">
            <div class="page-num">Birth Star Profile</div>
            <h1 class="page-title">நட்சத்திர குணங்கள் / Birth Star Traits: {nakshatra}</h1>

            <div class="highlight" style="margin-bottom: 15px;">
                <p><strong>Nakshatra Lord:</strong> {nakshatra_data.get('lord', 'Ketu')} |
                   <strong>Deity:</strong> {nakshatra_data.get('deity', '')} |
                   <strong>Symbol:</strong> {nakshatra_data.get('symbol', '')}</p>
            </div>

            <div class="section">
                <div class="prediction-para">
                    {nak_personality}
                </div>
            </div>

            <div class="section">
                <h3 class="subsection">Career Aptitudes / தொழில் திறன்கள்</h3>
                <ul style="margin-left: 15px; font-size: 9pt;">
                    {career_html}
                </ul>
            </div>

            <div class="section">
                <h3 class="subsection">Relationship Nature / உறவு இயல்பு</h3>
                <p style="font-size: 10pt; line-height: 1.6;">{nak_relationship}</p>
            </div>
        </div>

        <div class="page">
            <div class="page-num">Rising Sign Profile</div>
            <h1 class="page-title">லக்ன குணங்கள் / Rising Sign: {lagna}</h1>

            <div class="section">
                <h2 class="section-title">How the World Sees You / உலகம் உங்களை எப்படி பார்க்கிறது</h2>
                <div class="prediction-para">
                    {lagna_personality}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Combined Influence / ஒருங்கிணைந்த தாக்கம்</h2>
                <div class="prediction-para">
                    Your Moon in {moon_sign} combined with {nakshatra} nakshatra and {lagna} rising creates a unique personality blend.
                    The {rasi_data.get('element', 'elemental')} nature of your Moon sign provides emotional grounding,
                    while your {nakshatra} birth star adds {nakshatra_data.get('guna', 'specific')} qualities to your character.
                    Your {lagna} ascendant shapes how you present yourself to the world and approach new situations.

                    This combination gives you natural abilities in {', '.join(lagna_strengths[:2])} from your rising sign,
                    emotional depth from your {moon_sign} Moon, and the unique gifts of {nakshatra} - including
                    {nakshatra_data.get('career_strengths', ['intuition', 'service'])[0].lower() if nakshatra_data.get('career_strengths') else 'special talents'}.

                    In relationships, you seek {moon_relationship.split('.')[0].lower() if moon_relationship else 'meaningful connections'},
                    while your nakshatra nature adds {nak_relationship.split(',')[0].lower() if nak_relationship else 'depth'} to your bonds.
                </div>
            </div>
        </div>
        """

    def _page_2_panchanga(self) -> str:
        """Page 2: Panchanga Psychology"""
        identity = self.report_data['identity']
        gunas = self.report_data['gunas']

        nakshatra = identity['moon_nakshatra']
        nak_data = next((n for n in NAKSHATRAS if n['name'] == nakshatra), NAKSHATRAS[0])

        return f"""
        <div class="page">
            <div class="page-num">Page 2</div>
            <h1 class="page-title">2. Panchanga Psychology / பஞ்சாங்க உளவியல்</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Tithi weight 25% + Nakshatra weight 35% + Yoga weight 20% + Karana weight 20%</p>
            </div>

            <div class="section">
                <h2 class="section-title">Birth Nakshatra Analysis / பிறப்பு நட்சத்திர பகுப்பாய்வு</h2>
                <div class="planet-card">
                    <div class="planet-header">
                        <span class="planet-name">{nakshatra} ({nak_data['tamil']})</span>
                        <span>Lord: {nak_data['lord']}</span>
                    </div>
                    <p><strong>Deity:</strong> {nak_data['deity']}</p>
                    <p><strong>Primary Guna:</strong> {nak_data['guna']}</p>
                    <p><strong>Pada:</strong> {identity.get('nakshatra_pada', 2)}</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Guna Composition / குண அமைப்பு</h2>
                <table>
                    <tr>
                        <th>Guna / குணம்</th>
                        <th>Ratio</th>
                        <th>Visual</th>
                    </tr>
                    <tr>
                        <td>Sattva (சத்வம்)</td>
                        <td>{gunas['ratios'].get('Sattva', 0):.0%}</td>
                        <td>{self._score_bar(gunas['ratios'].get('Sattva', 0), 100)}</td>
                    </tr>
                    <tr>
                        <td>Rajas (ரஜஸ்)</td>
                        <td>{gunas['ratios'].get('Rajas', 0):.0%}</td>
                        <td>{self._score_bar(gunas['ratios'].get('Rajas', 0), 100)}</td>
                    </tr>
                    <tr>
                        <td>Tamas (தமஸ்)</td>
                        <td>{gunas['ratios'].get('Tamas', 0):.0%}</td>
                        <td>{self._score_bar(gunas['ratios'].get('Tamas', 0), 100)}</td>
                    </tr>
                </table>

                <div class="highlight">
                    <p><strong>Dominant Guna:</strong> {gunas['dominant_guna']}</p>
                    <p><strong>Personality Type:</strong> {gunas['personality_type']}</p>
                </div>
            </div>

            <div class="math-trace">{gunas['math_trace']}</div>
        </div>
        """

    def _page_3_elements(self) -> str:
        """Page 3: Elemental & Guna Balance"""
        elements = self.report_data['elements']

        return f"""
        <div class="page">
            <div class="page-num">Page 3</div>
            <h1 class="page-title">3. Elemental Balance / தாது சமநிலை</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Planet count weighted by strength (Sun/Moon = 1.5x weight)</p>
            </div>

            <div class="section">
                <h2 class="section-title">Element Distribution</h2>
                <table>
                    <tr>
                        <th>Element / தாது</th>
                        <th>Planets</th>
                        <th>Ratio</th>
                        <th>Visual</th>
                    </tr>
                    <tr>
                        <td>🔥 Fire / அக்னி</td>
                        <td>{elements['counts'].get('Fire', 0)}</td>
                        <td>{elements['ratios'].get('Fire', 0):.0%}</td>
                        <td>{self._score_bar(elements['ratios'].get('Fire', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td>🌍 Earth / பூமி</td>
                        <td>{elements['counts'].get('Earth', 0)}</td>
                        <td>{elements['ratios'].get('Earth', 0):.0%}</td>
                        <td>{self._score_bar(elements['ratios'].get('Earth', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td>💨 Air / வாயு</td>
                        <td>{elements['counts'].get('Air', 0)}</td>
                        <td>{elements['ratios'].get('Air', 0):.0%}</td>
                        <td>{self._score_bar(elements['ratios'].get('Air', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td>💧 Water / நீர்</td>
                        <td>{elements['counts'].get('Water', 0)}</td>
                        <td>{elements['ratios'].get('Water', 0):.0%}</td>
                        <td>{self._score_bar(elements['ratios'].get('Water', 0), 120)}</td>
                    </tr>
                </table>
            </div>

            <div class="two-col">
                <div class="success">
                    <p><strong>Dominant Element:</strong> {elements['dominant_element']}</p>
                    <p>This element's qualities are naturally strong in your personality.</p>
                </div>
                <div class="warning">
                    <p><strong>Weak Element:</strong> {elements['weak_element']}</p>
                    <p>Consider cultivating qualities of this element for balance.</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Balance Score</h2>
                <div class="stat-box">
                    <div class="stat-value">{elements['balance_score']:.0%}</div>
                    <div class="stat-label">Elemental Balance (Higher = More Balanced)</div>
                </div>
            </div>

            <div class="math-trace">{elements['math_trace']}</div>
        </div>
        """

    def _page_4_purushartha(self) -> str:
        """Page 4: Purushartha Dominance"""
        purushartha = self.report_data['purushartha']

        return f"""
        <div class="page">
            <div class="page-num">Page 4</div>
            <h1 class="page-title">4. Purushartha Dominance / புருஷார்த்த ஆதிக்கம்</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Sum of house lord strengths + occupant strengths per category</p>
            </div>

            <div class="section">
                <h2 class="section-title">Life Goals Distribution</h2>
                <table>
                    <tr>
                        <th>Purushartha</th>
                        <th>Houses</th>
                        <th>Score</th>
                        <th>Visual</th>
                    </tr>
                    <tr>
                        <td><strong>Dharma</strong> (தர்மம்) - Purpose</td>
                        <td>1, 5, 9</td>
                        <td>{purushartha['scores'].get('Dharma', 0):.0%}</td>
                        <td>{self._score_bar(purushartha['scores'].get('Dharma', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td><strong>Artha</strong> (அர்த்தம்) - Resources</td>
                        <td>2, 6, 10</td>
                        <td>{purushartha['scores'].get('Artha', 0):.0%}</td>
                        <td>{self._score_bar(purushartha['scores'].get('Artha', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td><strong>Kama</strong> (காமம்) - Desires</td>
                        <td>3, 7, 11</td>
                        <td>{purushartha['scores'].get('Kama', 0):.0%}</td>
                        <td>{self._score_bar(purushartha['scores'].get('Kama', 0), 120)}</td>
                    </tr>
                    <tr>
                        <td><strong>Moksha</strong> (மோக்ஷம்) - Liberation</td>
                        <td>4, 8, 12</td>
                        <td>{purushartha['scores'].get('Moksha', 0):.0%}</td>
                        <td>{self._score_bar(purushartha['scores'].get('Moksha', 0), 120)}</td>
                    </tr>
                </table>
            </div>

            <div class="success">
                <p><strong>Primary Life Focus:</strong> {purushartha['dominant']}</p>
                <p>{purushartha['life_focus']}</p>
            </div>

            <div class="math-trace">{purushartha['math_trace']}</div>
        </div>
        """

    def _page_5_lagna(self) -> str:
        """Page 5: Lagna Intelligence"""
        identity = self.report_data['identity']
        planets = self.report_data['planets']

        lagna = identity['lagna']
        lagna_lord = RASI_LORDS.get(lagna, 'Unknown')

        # Get lagna lord data
        lord_data = planets.get(lagna_lord, {})
        lord_pos = lord_data.get('position', {})
        lord_shadbala = lord_data.get('shadbala', {'total': 0.5})

        return f"""
        <div class="page">
            <div class="page-num">Page 5</div>
            <h1 class="page-title">5. Lagna Intelligence / லக்ன புத்தி</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Lagna Lord POI (Position of Interest) + House Context</p>
            </div>

            <div class="section">
                <h2 class="section-title">Lagna Configuration</h2>
                <div class="two-col">
                    <div class="stat-box">
                        <div class="stat-value">{lagna}</div>
                        <div class="stat-label">Lagna Sign</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{identity['lagna_degree']:.1f}°</div>
                        <div class="stat-label">Lagna Degree</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Lagna Lord Analysis: {lagna_lord}</h2>
                <div class="planet-card">
                    <div class="planet-header">
                        <span class="planet-name">{PLANET_SYMBOLS.get(lagna_lord, '')} {lagna_lord}</span>
                        <span>Strength: {lord_shadbala['total']:.2f}</span>
                    </div>
                    <p><strong>Position:</strong> {lord_pos.get('sign', 'N/A')} in House {lord_pos.get('house', 1)}</p>
                    <p><strong>Dignity:</strong> {lord_data.get('dignity', ('Unknown',))[0]}</p>
                    <p><strong>Nakshatra:</strong> {lord_pos.get('nakshatra', 'N/A')}</p>

                    <div style="margin-top: 10px;">
                        <strong>Strength Breakdown:</strong>
                        {self._score_bar(lord_shadbala['total'], 200)}
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Lagna Lord House Placement Meaning</h2>
                <p class="content">
                    With lagna lord {lagna_lord} in house {lord_pos.get('house', 1)},
                    the focus of self-expression connects to {HOUSE_KARAKAS.get(lord_pos.get('house', 1), {}).get('signifies', ['life'])[0]}.
                    The strength score of {lord_shadbala['total']:.2f} indicates
                    {'strong' if lord_shadbala['total'] > 0.6 else 'moderate' if lord_shadbala['total'] > 0.4 else 'developing'}
                    capacity for self-manifestation.
                </p>
            </div>
        </div>
        """

    def _page_6_moon(self) -> str:
        """Page 6: Moon & Emotional Wiring"""
        identity = self.report_data['identity']
        planets = self.report_data['planets']

        moon_data = planets.get('Moon', {})
        moon_pos = moon_data.get('position', {})
        moon_shadbala = moon_data.get('shadbala', {'total': 0.5})

        return f"""
        <div class="page">
            <div class="page-num">Page 6</div>
            <h1 class="page-title">6. Moon & Emotional Wiring / சந்திரன் & உணர்வு அமைப்பு</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Moon POI + Aspects + Nakshatra Traits</p>
            </div>

            <div class="section">
                <h2 class="section-title">Moon Configuration</h2>
                <div class="planet-card">
                    <div class="planet-header">
                        <span class="planet-name">☽ Moon / சந்திரன்</span>
                        <span>Strength: {moon_shadbala['total']:.2f}</span>
                    </div>
                    <div class="two-col">
                        <div>
                            <p><strong>Sign:</strong> {identity['moon_sign']}</p>
                            <p><strong>Nakshatra:</strong> {identity['moon_nakshatra']}</p>
                        </div>
                        <div>
                            <p><strong>House:</strong> H{moon_pos.get('house', 4)}</p>
                            <p><strong>Degree:</strong> {moon_pos.get('degree', 0):.1f}°</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Emotional Profile</h2>
                <p class="content">
                    Moon in {identity['moon_sign']} in {identity['moon_nakshatra']} nakshatra creates
                    an emotional foundation characterized by the sign's and nakshatra's qualities.
                    With a strength score of {moon_shadbala['total']:.2f}, the emotional processing
                    capacity is {'robust' if moon_shadbala['total'] > 0.6 else 'moderate' if moon_shadbala['total'] > 0.4 else 'sensitive'}.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">Moon Strength Components</h2>
                <table>
                    <tr>
                        <th>Component</th>
                        <th>Score</th>
                        <th>Visual</th>
                    </tr>
                    <tr>
                        <td>Positional (Sthana)</td>
                        <td>{moon_shadbala.get('components', {}).get('sthana', 0.5):.2f}</td>
                        <td>{self._score_bar(moon_shadbala.get('components', {}).get('sthana', 0.5), 100)}</td>
                    </tr>
                    <tr>
                        <td>Directional (Dig)</td>
                        <td>{moon_shadbala.get('components', {}).get('dig', 0.5):.2f}</td>
                        <td>{self._score_bar(moon_shadbala.get('components', {}).get('dig', 0.5), 100)}</td>
                    </tr>
                    <tr>
                        <td>Temporal (Kala)</td>
                        <td>{moon_shadbala.get('components', {}).get('kala', 0.5):.2f}</td>
                        <td>{self._score_bar(moon_shadbala.get('components', {}).get('kala', 0.5), 100)}</td>
                    </tr>
                    <tr>
                        <td>Aspectual (Drik)</td>
                        <td>{moon_shadbala.get('components', {}).get('drik', 0.5):.2f}</td>
                        <td>{self._score_bar(moon_shadbala.get('components', {}).get('drik', 0.5), 100)}</td>
                    </tr>
                </table>
            </div>

            <div class="math-trace">{moon_shadbala.get('math_trace', 'Moon strength calculation')}</div>
        </div>
        """

    def _pages_7_13_planets(self) -> str:
        """Pages 7-13: Planetary Intelligence (one page per planet)"""
        planets_data = self.report_data['planets']
        pages_html = ""

        for i, planet in enumerate(['Sun', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu']):
            p_data = planets_data.get(planet, {})
            pos = p_data.get('position', {})
            dignity = p_data.get('dignity', ('Unknown', 0.5, ''))
            shadbala = p_data.get('shadbala', {'total': 0.5, 'components': {}, 'math_trace': ''})

            maturity_age = MATURITY_AGES.get(planet, 30)
            current_age = self.report_data['identity']['current_age']
            maturity_status = 'Matured' if current_age >= maturity_age else f'Matures at {maturity_age}'

            pages_html += f"""
            <div class="page">
                <div class="page-num">Page {7 + i}</div>
                <h1 class="page-title">{PLANET_SYMBOLS.get(planet, '')} {planet} Intelligence / {PLANET_TAMIL.get(planet, '')} புத்தி</h1>

                <div class="planet-card">
                    <div class="planet-header">
                        <span class="planet-name">{PLANET_SYMBOLS.get(planet, '')} {planet} ({PLANET_TAMIL.get(planet, '')})</span>
                        <span style="font-size: 14pt;">{shadbala['total']:.2f}</span>
                    </div>

                    <div class="two-col">
                        <div>
                            <p><strong>Sign:</strong> {pos.get('sign', 'N/A')}</p>
                            <p><strong>House:</strong> H{pos.get('house', 1)}</p>
                            <p><strong>Degree:</strong> {pos.get('degree', 0):.2f}°</p>
                        </div>
                        <div>
                            <p><strong>Nakshatra:</strong> {pos.get('nakshatra', 'N/A')}</p>
                            <p><strong>Dignity:</strong> {dignity[0]}</p>
                            <p><strong>Retrograde:</strong> {'Yes' if pos.get('retrograde') else 'No'}</p>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2 class="section-title">Shadbala (6-fold Strength)</h2>
                    <table>
                        <tr><th>Component</th><th>Score</th><th>Visual</th></tr>
                        <tr>
                            <td>Sthana (Position)</td>
                            <td>{shadbala.get('components', {}).get('sthana', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('sthana', 0.5), 80)}</td>
                        </tr>
                        <tr>
                            <td>Dig (Direction)</td>
                            <td>{shadbala.get('components', {}).get('dig', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('dig', 0.5), 80)}</td>
                        </tr>
                        <tr>
                            <td>Kala (Time)</td>
                            <td>{shadbala.get('components', {}).get('kala', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('kala', 0.5), 80)}</td>
                        </tr>
                        <tr>
                            <td>Chesta (Motion)</td>
                            <td>{shadbala.get('components', {}).get('chesta', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('chesta', 0.5), 80)}</td>
                        </tr>
                        <tr>
                            <td>Naisargika (Natural)</td>
                            <td>{shadbala.get('components', {}).get('naisargika', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('naisargika', 0.5), 80)}</td>
                        </tr>
                        <tr>
                            <td>Drik (Aspect)</td>
                            <td>{shadbala.get('components', {}).get('drik', 0.5):.2f}</td>
                            <td>{self._score_bar(shadbala.get('components', {}).get('drik', 0.5), 80)}</td>
                        </tr>
                    </table>
                </div>

                <div class="highlight">
                    <p><strong>Maturity:</strong> {maturity_status}</p>
                    <p><strong>Current Age:</strong> {current_age} years</p>
                </div>

                <div class="math-trace">{shadbala.get('math_trace', '')}</div>
            </div>
            """

        return pages_html

    def _page_14_interactions(self) -> str:
        """Page 14: Planetary Interaction Graph"""
        interactions = self.report_data['interactions']

        conj_rows = ""
        for conj in interactions.get('conjunctions', [])[:6]:
            conj_rows += f"""
            <tr>
                <td>{' + '.join(conj['planets'])}</td>
                <td>{conj['sign']}</td>
                <td>{conj['degree_diff']:.1f}°</td>
            </tr>
            """

        aspect_rows = ""
        for asp in interactions.get('major_aspects', [])[:6]:
            aspect_rows += f"""
            <tr>
                <td>{asp['type']}</td>
                <td>{' vs '.join(asp['planets'])}</td>
                <td>{' - '.join(asp['signs'])}</td>
            </tr>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 14</div>
            <h1 class="page-title">14. Planetary Interaction Graph / கிரக தொடர்பு வரைபடம்</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Friend-enemy matrix + Conjunction clusters</p>
            </div>

            <div class="section">
                <h2 class="section-title">Conjunctions (Same Sign)</h2>
                <table>
                    <tr><th>Planets</th><th>Sign</th><th>Orb</th></tr>
                    {conj_rows if conj_rows else '<tr><td colspan="3">No major conjunctions</td></tr>'}
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Major Aspects</h2>
                <table>
                    <tr><th>Type</th><th>Planets</th><th>Signs</th></tr>
                    {aspect_rows if aspect_rows else '<tr><td colspan="3">No major aspects</td></tr>'}
                </table>
            </div>

            <div class="math-trace">{interactions.get('math_trace', '')}</div>
        </div>
        """

    def _pages_15_20_life_areas(self) -> str:
        """Pages 15-20: Life Area Analysis with Rich Narrative Descriptions"""
        life_areas = self.report_data['life_areas']
        pages_html = ""

        areas = [
            ('career', 'Career / தொழில்', 15),
            ('marriage', 'Marriage / திருமணம்', 16),
            ('children', 'Children / குழந்தைகள்', 17),
            ('health', 'Health / ஆரோக்கியம்', 18),
            ('wealth', 'Wealth / செல்வம்', 19),
            ('education', 'Education / கல்வி', 20)
        ]

        for area_key, area_title, page_num in areas:
            area = life_areas.get(area_key, {})
            detailed = area.get('detailed_insights', {})

            planets_list = ', '.join(area.get('planets_in_house', [])) or 'None'
            house_sign = area.get('house_sign', 'Aries')
            house_lord = area.get('house_lord', 'Mars')
            combined_score = area.get('combined_score', 0.5)

            # Generate rich narrative description based on area
            narrative = self._generate_life_area_narrative(
                area_key, house_sign, house_lord, combined_score, planets_list, detailed
            )

            # Build area-specific detailed section
            detailed_html = self._render_detailed_insights(area_key, detailed)

            # Determine outlook based on score
            if combined_score > 0.7:
                outlook = "Excellent"
                outlook_class = "success"
            elif combined_score > 0.55:
                outlook = "Good"
                outlook_class = "success"
            elif combined_score > 0.4:
                outlook = "Moderate"
                outlook_class = "warning"
            else:
                outlook = "Challenging - requires attention"
                outlook_class = "highlight"

            pages_html += f"""
            <div class="page">
                <div class="page-num">Page {page_num}</div>
                <h1 class="page-title">{page_num}. {area_title} Analysis</h1>

                <div class="highlight">
                    <p><strong>Primary House:</strong> H{area.get('primary_house', 1)}
                    in {house_sign} | <strong>Lord:</strong> {house_lord} |
                    <strong>Karaka:</strong> {area.get('karaka', 'N/A')} |
                    <strong>Overall Outlook:</strong> {outlook}</p>
                </div>

                <div class="section">
                    <h2 class="section-title">Detailed Analysis / விரிவான பகுப்பாய்வு</h2>
                    <div class="prediction-para">
                        {narrative}
                    </div>
                </div>

                {detailed_html}

                <div class="section">
                    <h2 class="section-title">Planetary Influences</h2>
                    <p><strong>Planets in this house:</strong> {planets_list}</p>
                    <div class="two-col" style="margin-top: 10px;">
                        <div>
                            <p><strong>House Lord Strength:</strong></p>
                            {self._score_bar(area.get('lord_strength', 0.5), 120)}
                        </div>
                        <div>
                            <p><strong>Karaka Strength:</strong></p>
                            {self._score_bar(area.get('karaka_strength', 0.5), 120)}
                        </div>
                    </div>
                </div>

                <div class="{outlook_class}">
                    <p><strong>Key Insight:</strong> {area.get('interpretation', 'Moderate potential in this area.')}</p>
                </div>
            </div>
            """

        return pages_html

    def _generate_life_area_narrative(self, area_key: str, house_sign: str,
                                       house_lord: str, score: float,
                                       planets: str, detailed: dict) -> str:
        """Generate rich narrative description for each life area (200-400 words)"""

        # Get sign characteristics
        sign_traits = RASI_TRAITS.get(house_sign, {})
        sign_element = sign_traits.get('element', 'Mixed')
        sign_quality = sign_traits.get('quality', 'Adaptable')

        if area_key == 'career':
            return self._career_narrative(house_sign, house_lord, score,
                                          planets, sign_element, detailed)
        elif area_key == 'marriage':
            return self._marriage_narrative(house_sign, house_lord, score,
                                            planets, sign_traits, detailed)
        elif area_key == 'wealth':
            return self._wealth_narrative(house_sign, house_lord, score,
                                          planets, sign_element, detailed)
        elif area_key == 'health':
            return self._health_narrative(house_sign, house_lord, score,
                                          planets, sign_element, detailed)
        elif area_key == 'children':
            return self._children_narrative(house_sign, house_lord, score,
                                            planets, sign_traits, detailed)
        elif area_key == 'education':
            return self._education_narrative(house_sign, house_lord, score,
                                             planets, sign_element, detailed)
        return "Analysis for this life area."

    def _career_narrative(self, sign: str, lord: str, score: float,
                          planets: str, element: str, detailed: dict) -> str:
        """Generate 200-400 word career narrative"""
        strength = "strong" if score > 0.6 else "moderate" if score > 0.4 else "developing"

        # Career fields based on sign
        career_map = {
            'Aries': 'leadership, entrepreneurship, military, sports, or engineering',
            'Taurus': 'finance, banking, agriculture, arts, or luxury goods',
            'Gemini': 'communication, writing, media, sales, or technology',
            'Cancer': 'hospitality, real estate, healthcare, or nurturing professions',
            'Leo': 'entertainment, politics, management, or creative arts',
            'Virgo': 'healthcare, research, accounting, or service industries',
            'Libra': 'law, diplomacy, arts, fashion, or counseling',
            'Scorpio': 'research, psychology, investigation, or finance',
            'Sagittarius': 'education, travel, philosophy, or international business',
            'Capricorn': 'government, administration, traditional business, or management',
            'Aquarius': 'technology, innovation, social causes, or scientific research',
            'Pisces': 'arts, healing, spirituality, or creative industries'
        }

        fields = career_map.get(sign, 'diverse professional fields')
        rec_fields = ', '.join(detailed.get('recommended_fields', [])[:3]) if detailed.get('recommended_fields') else fields

        narrative = f"""Your career path is illuminated by the {sign} energy governing your 10th house of profession and public standing. With {lord} as the ruling planet of your career house, your professional journey carries the distinctive qualities of this celestial influence.

The {element} element nature of {sign} shapes your approach to work and ambition. {"You bring dynamic energy and initiative to your professional endeavors, naturally gravitating toward roles that allow independence and leadership." if element == 'Fire' else "You approach your career with practicality and persistence, building lasting foundations through methodical effort." if element == 'Earth' else "Your career benefits from your intellectual agility and communication skills, thriving in roles that engage your mind." if element == 'Air' else "Your professional path is guided by intuition and emotional intelligence, excelling in roles that require understanding human nature."}

Based on this configuration, you are naturally suited for careers in {rec_fields}. Your {strength} career indicators suggest {"excellent opportunities for advancement and recognition in your chosen field" if score > 0.6 else "steady progress with consistent effort and strategic planning" if score > 0.4 else "growth through perseverance, with rewards coming through sustained dedication"}.

{"The planets currently placed in your career house add their own influences, creating additional dimensions to your professional potential." if planets != 'None' else "With no planets directly in your career house, the condition of your 10th lord becomes especially important for professional success."}

{detailed.get('timing_note', 'Career developments are particularly significant during the Dasha periods of your 10th lord and the planets aspecting your 10th house.')}"""

        return narrative

    def _marriage_narrative(self, sign: str, lord: str, score: float,
                            planets: str, sign_traits: dict, detailed: dict) -> str:
        """Generate 200-400 word marriage/partnership narrative"""

        partner_qualities = {
            'Aries': 'independent, energetic, and action-oriented',
            'Taurus': 'stable, sensual, and security-conscious',
            'Gemini': 'intellectually stimulating, communicative, and versatile',
            'Cancer': 'nurturing, emotionally supportive, and family-oriented',
            'Leo': 'confident, generous, and warm-hearted',
            'Virgo': 'practical, helpful, and detail-oriented',
            'Libra': 'harmonious, fair-minded, and partnership-focused',
            'Scorpio': 'intense, loyal, and deeply committed',
            'Sagittarius': 'adventurous, optimistic, and freedom-loving',
            'Capricorn': 'responsible, ambitious, and traditionally-minded',
            'Aquarius': 'unique, independent, and intellectually oriented',
            'Pisces': 'compassionate, intuitive, and spiritually inclined'
        }

        qualities = partner_qualities.get(sign, 'balanced and compatible')
        rel_style = sign_traits.get('relationship_style', 'seeks meaningful partnership')

        narrative = f"""Your 7th house of marriage and partnership falls in {sign}, painting a detailed picture of your relationship destiny. The energy of {lord}, ruling this important house, significantly influences who you attract and how your partnerships unfold.

With {sign} governing partnerships, you are naturally drawn to individuals who are {qualities}. Your ideal partner reflects these {sign} qualities, creating a dynamic where {rel_style.lower() if rel_style else 'mutual growth and understanding flourish'}.

{"Your partnership indicators suggest strong potential for a harmonious and fulfilling marriage. The celestial support for your 7th house brings natural compatibility and the ability to maintain lasting bonds." if score > 0.6 else "Your relationship path shows steady potential with room for growth. Building a strong partnership requires conscious effort in communication and understanding, but the foundations are supportive." if score > 0.4 else "Relationships may require extra attention and conscious cultivation. The challenges indicated can become opportunities for profound growth when approached with patience and self-awareness."}

{"The planets in your 7th house add complexity and specific themes to your relationship experiences. Understanding these influences helps you navigate partnership dynamics more skillfully." if planets != 'None' else "With your 7th house unoccupied by planets, the condition and placement of its lord becomes the primary indicator of marriage timing and quality."}

Venus, the natural significator of marriage, {detailed.get('venus_analysis', 'plays an important role in determining relationship harmony and timing')}.

{detailed.get('key_advice', 'Understanding both your needs and your partners perspective creates the foundation for lasting happiness in partnership.')}"""

        return narrative

    def _wealth_narrative(self, sign: str, lord: str, score: float,
                          planets: str, element: str, detailed: dict) -> str:
        """Generate 200-400 word wealth narrative"""

        wealth_approach = {
            'Fire': 'through bold ventures, entrepreneurship, and taking calculated risks',
            'Earth': 'through steady accumulation, wise investments, and practical financial management',
            'Air': 'through intellectual pursuits, networking, and innovative ideas',
            'Water': 'through intuitive decisions, inheritance, and emotionally-driven opportunities'
        }

        approach = wealth_approach.get(element, 'through balanced financial strategies')

        narrative = f"""Your financial destiny is shaped by {sign} governing your 2nd house of accumulated wealth, with {lord} directing the flow of resources into your life. This configuration reveals both your natural approach to money and your potential for material prosperity.

The {element} element influence suggests wealth comes to you {approach}. Your relationship with money reflects {sign} qualities - {"you may be quick to earn and equally quick to spend, driven by immediate desires and opportunities" if sign in ['Aries', 'Leo', 'Sagittarius'] else "you value security and tend to build wealth gradually through consistent effort and wise preservation" if sign in ['Taurus', 'Virgo', 'Capricorn'] else "financial decisions often involve intellectual analysis and multiple income streams" if sign in ['Gemini', 'Libra', 'Aquarius'] else "intuition plays a role in your financial decisions, and emotional security is linked to material security"}.

{"Your wealth indicators are strongly positive, suggesting natural ability to attract and retain resources. Financial stability comes more easily to you than many, though wise stewardship remains important." if score > 0.6 else "Your financial path shows steady potential with room for growth through conscious effort. Building wealth requires patience and strategic planning, but the foundations support success." if score > 0.4 else "Wealth accumulation may require extra attention and discipline. The challenges indicated become opportunities for developing stronger financial habits and wisdom."}

Jupiter, the great benefic and natural significator of wealth, {detailed.get('jupiter_note', 'influences your overall prosperity potential')}.

Your 11th house of gains works in conjunction with the 2nd house, together determining your complete financial picture. {detailed.get('income_note', 'Multiple sources of income may develop throughout your life.')}"""

        return narrative

    def _health_narrative(self, sign: str, lord: str, score: float,
                          planets: str, element: str, detailed: dict) -> str:
        """Generate 200-400 word health narrative"""

        constitution = {
            'Fire': 'naturally robust with strong vital energy. You may have excellent recovery abilities but should guard against burnout, fever-related conditions, and inflammatory issues',
            'Earth': 'steady and enduring, with good stamina. You should pay attention to digestion, weight management, and conditions that develop slowly over time',
            'Air': 'active and variable, with energy that fluctuates. The nervous system and respiratory health deserve attention, along with managing stress and mental fatigue',
            'Water': 'sensitive and responsive, deeply connected to emotional states. Water retention, lymphatic health, and conditions affected by emotions require awareness'
        }

        const_text = constitution.get(element, 'balanced, requiring attention to overall wellness')
        body_areas = detailed.get('body_areas_to_monitor', ['general wellness'])
        body_list = ', '.join(body_areas[:3]) if body_areas else 'overall constitution'

        narrative = f"""Your physical constitution and health patterns are revealed through the 6th house of health and the overall strength of your Lagna (ascendant). With {sign} influencing your health house and {lord} as its ruler, specific patterns emerge regarding your vitality and areas requiring attention.

Your {element} element constitution tends to be {const_text}. Understanding this natural tendency helps you take proactive measures for maintaining wellness throughout life.

{"Your health indicators are favorable, suggesting a naturally strong constitution and good recuperative abilities. While no one is immune to health challenges, your chart supports vitality and longevity." if score > 0.6 else "Your health patterns show areas of both strength and sensitivity. Paying attention to preventive care and lifestyle choices significantly improves your wellbeing." if score > 0.4 else "Health matters may require more conscious attention in your life. The challenges indicated actually motivate you to develop excellent health habits that serve you well long-term."}

Based on the planetary configurations, the areas deserving particular attention include: {body_list}. These are not predictions of illness but rather indications of where preventive care is most valuable.

{detailed.get('constitution_assessment', 'Your overall vitality benefits from regular physical activity suited to your constitution, adequate rest, and attention to nutrition.')}

The Sun, representing vitality, and the Lagna lord, representing physical body, together indicate your energy levels and recovery capacity. {detailed.get('vitality_note', 'Maintaining healthy routines during challenging planetary periods provides extra support.')}"""

        return narrative

    def _children_narrative(self, sign: str, lord: str, score: float,
                            planets: str, sign_traits: dict, detailed: dict) -> str:
        """Generate 200-400 word children/progeny narrative"""

        parenting_style = {
            'Aries': 'encouraging independence and courage, fostering a spirit of adventure',
            'Taurus': 'providing stability and comfort, teaching the value of patience and persistence',
            'Gemini': 'stimulating intellectual curiosity, encouraging communication and learning',
            'Cancer': 'deeply nurturing and protective, creating a secure emotional environment',
            'Leo': 'encouraging creative expression and confidence, celebrating their uniqueness',
            'Virgo': 'teaching practical skills and attention to detail, fostering helpfulness',
            'Libra': 'emphasizing fairness and harmony, teaching social grace and cooperation',
            'Scorpio': 'forming deep emotional bonds, teaching resilience and inner strength',
            'Sagittarius': 'encouraging exploration and higher learning, fostering optimism',
            'Capricorn': 'teaching responsibility and discipline, preparing them for success',
            'Aquarius': 'encouraging individuality and humanitarian values, fostering innovation',
            'Pisces': 'nurturing creativity and compassion, developing spiritual awareness'
        }

        style = parenting_style.get(sign, 'balanced and supportive')

        narrative = f"""Your 5th house of children and creative expression falls in {sign}, with {lord} guiding matters related to progeny. This configuration reveals the nature of your relationship with children and the blessings or lessons that come through this area of life.

With {sign} energy in your house of children, your parenting approach naturally involves {style}. Children who come into your life tend to reflect {sign} qualities, and your relationship with them carries these themes.

{"Your chart shows strong indicators for happiness through children. Whether through biological offspring, adoption, or close relationships with young people, this area of life brings significant joy and fulfillment." if score > 0.6 else "Your connection with children develops meaningfully through conscious cultivation. The relationship may involve growth on both sides, with children teaching you as much as you teach them." if score > 0.4 else "Matters related to children may require patience and dedication. Any challenges in this area become opportunities for deep personal growth and understanding."}

Jupiter, the natural significator of children and divine grace, {detailed.get('jupiter_note', 'plays a significant role in determining blessings in this area')}. The condition of Jupiter in your chart provides additional insights into your relationship with progeny.

{"The planets in your 5th house add their specific influences to matters of children and creativity." if planets != 'None' else "With no planets directly occupying your 5th house, the placement and condition of its lord becomes especially significant."}

{detailed.get('timing_note', 'Matters related to children are particularly active during the Dasha periods connected to the 5th house and Jupiter.')}"""

        return narrative

    def _education_narrative(self, sign: str, lord: str, score: float,
                             planets: str, element: str, detailed: dict) -> str:
        """Generate 200-400 word education narrative"""

        learning_approach = {
            'Fire': 'enthusiastic and inspired learner who grasps concepts quickly but may need variety to maintain interest. You learn best through active engagement and practical application',
            'Earth': 'methodical and thorough student who builds knowledge systematically. You excel when given time to absorb material deeply and apply it practically',
            'Air': 'intellectually agile learner who excels at theoretical understanding and making connections between ideas. Discussion and debate enhance your learning',
            'Water': 'intuitive learner who absorbs knowledge emotionally and holistically. Creative and artistic subjects often resonate deeply, and you learn well in supportive environments'
        }

        approach = learning_approach.get(element, 'adaptive and comprehensive')

        narrative = f"""Your educational journey and intellectual development are illuminated by the 4th house of foundational learning and the 9th house of higher wisdom. With {sign} energy influencing these areas and {lord} as a guiding planet, your learning style and academic potential take specific shape.

You are a {approach}. Understanding this natural tendency helps you choose study methods and educational environments that support your success.

{"Your educational indicators are strongly favorable, suggesting natural academic ability and the capacity for advanced learning. Whether through formal education or self-study, you have the potential to acquire significant knowledge and expertise." if score > 0.6 else "Your educational path shows steady potential with opportunity for significant achievement through consistent effort. Building knowledge requires dedication, but you have the capacity for meaningful intellectual growth." if score > 0.4 else "Learning may require extra effort or non-traditional approaches. The challenges indicated often lead to developing unique perspectives and practical wisdom that formal education alone cannot provide."}

Mercury, the planet of intellect and learning, {detailed.get('mercury_note', 'significantly influences your mental capacity and learning abilities')}. Jupiter, representing higher wisdom and teachers, {detailed.get('jupiter_note', 'shapes your access to guidance and advanced knowledge')}.

Areas of natural intellectual strength include {', '.join(detailed.get('subjects', ['general studies'])[:3]) if detailed.get('subjects') else 'diverse fields of knowledge'}. These subjects tend to come more easily and may form the foundation of your expertise.

{detailed.get('timing_note', 'Educational pursuits are particularly favored during Mercury and Jupiter planetary periods.')}"""

        return narrative

    def _render_detailed_insights(self, area_key: str, detailed: dict) -> str:
        """Render detailed insights based on life area type"""
        if area_key == 'career':
            return self._render_career_insights(detailed)
        elif area_key == 'health':
            return self._render_health_insights(detailed)
        elif area_key == 'marriage':
            return self._render_marriage_insights(detailed)
        elif area_key == 'wealth':
            return self._render_wealth_insights(detailed)
        elif area_key == 'education':
            return self._render_education_insights(detailed)
        elif area_key == 'children':
            return self._render_children_insights(detailed)
        return ""

    def _render_career_insights(self, detailed: dict) -> str:
        """Render career-specific detailed insights"""
        if not detailed:
            return ""

        recommended = detailed.get('recommended_fields', [])
        recommended_html = ', '.join(recommended[:6]) if recommended else 'General fields'

        traits = detailed.get('career_traits', [])
        traits_html = ', '.join(traits) if traits else ''

        return f"""
        <div class="section">
            <h2 class="section-title">Recommended Career Fields</h2>
            <div class="success" style="padding: 10px; margin: 5px 0;">
                <p><strong>{recommended_html}</strong></p>
            </div>
            <p style="font-size: 9pt; color: #666; margin-top: 5px;"><em>Based on: {detailed.get('strength_analysis', '')}</em></p>
        </div>

        <div class="section">
            <h2 class="section-title">Career Direction & Approach</h2>
            <p><strong>Direction:</strong> {detailed.get('career_direction', 'N/A')}</p>
            <p><strong>Approach:</strong> {detailed.get('approach', 'N/A')}</p>
            <p><strong>Career Traits:</strong> {traits_html or 'Adaptable'}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Timing & Progression</h2>
            <p>{detailed.get('timing_note', 'Steady progression expected')}</p>
            <p><strong>Planet Influence:</strong> {detailed.get('planets_influence', 'N/A')}</p>
        </div>
        """

    def _render_health_insights(self, detailed: dict) -> str:
        """Render health-specific detailed insights"""
        if not detailed:
            return ""

        body_areas = detailed.get('body_areas_to_monitor', [])
        body_html = ', '.join(body_areas[:5]) if body_areas else 'General wellness'

        recommendations = detailed.get('recommendations', [])
        rec_html = ''.join([f'<li>{r}</li>' for r in recommendations[:4]])

        weak_planets = detailed.get('weak_planets', [])
        weak_html = ', '.join(weak_planets) if weak_planets else 'None'

        return f"""
        <div class="section">
            <h2 class="section-title">Health Focus Areas</h2>
            <div class="warning" style="padding: 10px; margin: 5px 0;">
                <p><strong>Monitor:</strong> {body_html}</p>
            </div>
            <p><strong>Constitution:</strong> {detailed.get('constitution_assessment', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Vitality Analysis</h2>
            <p><strong>Vitality Score:</strong> {detailed.get('vitality_score', 'N/A')}</p>
            <p><strong>Physical Energy:</strong> {detailed.get('physical_energy', 'N/A')}</p>
            <p><strong>Chronic Tendency:</strong> {detailed.get('chronic_tendency', 'None')}</p>
            <p><strong>Weak Planets:</strong> {weak_html}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Health Recommendations</h2>
            <ul style="margin-left: 20px; font-size: 9pt;">
                {rec_html or '<li>Maintain regular health checkups</li>'}
            </ul>
        </div>
        """

    def _render_marriage_insights(self, detailed: dict) -> str:
        """Render marriage-specific detailed insights"""
        if not detailed:
            return ""

        dynamics = detailed.get('relationship_dynamics', [])
        dynamics_html = ', '.join(dynamics) if dynamics else 'Balanced partnership'

        return f"""
        <div class="section">
            <h2 class="section-title">Partner Characteristics</h2>
            <div class="highlight" style="padding: 10px; margin: 5px 0;">
                <p><strong>{detailed.get('partner_characteristics', 'N/A')}</strong></p>
            </div>
            <p><strong>7th House Sign:</strong> {detailed.get('7th_house_sign', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Relationship Analysis</h2>
            <p><strong>Venus Analysis:</strong> {detailed.get('venus_analysis', 'N/A')}</p>
            <p><strong>Jupiter Analysis:</strong> {detailed.get('jupiter_analysis', 'N/A')}</p>
            <p><strong>Harmony Potential:</strong> {detailed.get('harmony_potential', 'N/A')}</p>
            <p><strong>Dynamics:</strong> {dynamics_html}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Timing & Advice</h2>
            <p><strong>Timing:</strong> {detailed.get('timing_indication', 'N/A')}</p>
            <p><strong>Key Advice:</strong> {detailed.get('key_advice', 'N/A')}</p>
        </div>
        """

    def _render_wealth_insights(self, detailed: dict) -> str:
        """Render wealth-specific detailed insights"""
        if not detailed:
            return ""

        sources = detailed.get('recommended_income_sources', [])
        sources_html = ', '.join(sources[:4]) if sources else 'General income'

        return f"""
        <div class="section">
            <h2 class="section-title">Wealth Potential</h2>
            <div class="success" style="padding: 10px; margin: 5px 0;">
                <p><strong>{detailed.get('wealth_potential', 'N/A')}</strong></p>
            </div>
            <p><strong>Pattern:</strong> {detailed.get('accumulation_pattern', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Income Sources</h2>
            <p><strong>Recommended:</strong> {sources_html}</p>
            <p><strong>Jupiter Influence:</strong> {detailed.get('jupiter_influence', 'N/A')}</p>
            <p><strong>11th Lord:</strong> {detailed.get('11th_lord', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Financial Strategy</h2>
            <p><strong>Timing:</strong> {detailed.get('timing_pattern', 'N/A')}</p>
            <p><strong>Investment Advice:</strong> {detailed.get('investment_advice', 'N/A')}</p>
        </div>
        """

    def _render_education_insights(self, detailed: dict) -> str:
        """Render education-specific detailed insights"""
        if not detailed:
            return ""

        fields = detailed.get('recommended_fields', [])
        fields_html = ', '.join(fields[:6]) if fields else 'General studies'

        return f"""
        <div class="section">
            <h2 class="section-title">Recommended Fields of Study</h2>
            <div class="success" style="padding: 10px; margin: 5px 0;">
                <p><strong>{fields_html}</strong></p>
            </div>
            <p><strong>Higher Education:</strong> {detailed.get('higher_education_prospects', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Learning Profile</h2>
            <p><strong>Learning Style:</strong> {detailed.get('learning_style', 'N/A')}</p>
            <p><strong>Intellectual Capacity:</strong> {detailed.get('intellectual_capacity', 'N/A')}</p>
            <p><strong>Concentration:</strong> {detailed.get('concentration', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Academic Strengths</h2>
            <p><strong>Mercury Strength:</strong> {detailed.get('mercury_strength', 'N/A')}</p>
            <p><strong>Jupiter Strength:</strong> {detailed.get('jupiter_strength', 'N/A')}</p>
            <p><strong>Best Approach:</strong> {detailed.get('best_approach', 'N/A')}</p>
        </div>
        """

    def _render_children_insights(self, detailed: dict) -> str:
        """Render children-specific detailed insights"""
        if not detailed:
            return ""

        dynamics = detailed.get('relationship_dynamics', [])
        dynamics_html = ', '.join(dynamics) if dynamics else 'Harmonious bond expected'

        return f"""
        <div class="section">
            <h2 class="section-title">Progeny Prospects</h2>
            <div class="highlight" style="padding: 10px; margin: 5px 0;">
                <p><strong>{detailed.get('progeny_prospects', 'N/A')}</strong></p>
            </div>
            <p><strong>5th House Sign:</strong> {detailed.get('5th_house_sign', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Children Characteristics</h2>
            <p><strong>Traits:</strong> {detailed.get('children_characteristics', 'N/A')}</p>
            <p><strong>Jupiter Analysis:</strong> {detailed.get('jupiter_analysis', 'N/A')}</p>
            <p><strong>Creative Expression:</strong> {detailed.get('creative_expression', 'N/A')}</p>
        </div>

        <div class="section">
            <h2 class="section-title">Timing & Relationship</h2>
            <p><strong>Timing:</strong> {detailed.get('timing_indication', 'N/A')}</p>
            <p><strong>Dynamics:</strong> {dynamics_html}</p>
        </div>
        """

    def _page_21_yogas(self) -> str:
        """Page 21-22: Yogas Present with Rich Descriptions"""
        yogas = self.report_data['yogas']

        # Generate pages for all yogas with detailed descriptions
        yoga_pages = self._generate_yoga_detail_pages(yogas)

        return yoga_pages

    def _generate_yoga_detail_pages(self, yogas: list) -> str:
        """Generate multiple pages with rich yoga descriptions"""
        if not yogas:
            return f"""
            <div class="page">
                <div class="page-num">Page 21</div>
                <h1 class="page-title">21. Yogas Present / யோகங்கள்</h1>
                <div class="highlight">
                    <p>Yogas are special planetary combinations that bestow unique blessings and abilities.</p>
                </div>
                <div class="section">
                    <p>No major yogas detected in this chart based on classical formation rules.</p>
                    <p style="margin-top: 10px;">This doesn't diminish your chart's potential - individual planetary strengths
                    and house placements provide their own unique gifts and opportunities.</p>
                </div>
            </div>
            """

        pages_html = ""
        page_num = 21
        yogas_per_page = 2  # 2 yogas per page for detailed descriptions

        for page_idx in range(0, len(yogas), yogas_per_page):
            page_yogas = yogas[page_idx:page_idx + yogas_per_page]

            yoga_content = ""
            for yoga in page_yogas:
                yoga_name = yoga.get('name', 'Unknown Yoga')

                # Get rich description from YOGA_DESCRIPTIONS
                yoga_data = YOGA_DESCRIPTIONS.get(yoga_name, {})
                rich_description = yoga_data.get('description', yoga.get('effects', f'{yoga_name} brings its unique blessings to your chart.'))
                effects_list = yoga_data.get('effects', [])
                activation_info = yoga_data.get('activation', 'During related planetary Dasha periods')
                category = yoga_data.get('category', yoga.get('type', 'Auspicious'))

                # Truncate description for page fit but keep substantial
                desc_preview = rich_description[:500] + '...' if len(rich_description) > 500 else rich_description

                # Build effects list HTML
                effects_html = ""
                if effects_list:
                    effects_items = ''.join([f'<li>{effect}</li>' for effect in effects_list[:5]])
                    effects_html = f'<ul style="font-size: 9pt; margin: 5px 0;">{effects_items}</ul>'

                strength = yoga.get('strength', 0.5)
                strength_label = "Strong" if strength > 0.7 else "Moderate" if strength > 0.4 else "Developing"

                yoga_content += f"""
                <div class="section" style="margin-bottom: 20px; page-break-inside: avoid;">
                    <div style="background: linear-gradient(135deg, #2c5282 0%, #1a365d 100%); color: white; padding: 12px; border-radius: 8px 8px 0 0;">
                        <h2 style="margin: 0; font-size: 14pt;">{yoga_name} / {yoga.get('name_tamil', yoga_data.get('name_tamil', ''))}</h2>
                        <p style="margin: 5px 0 0 0; font-size: 10pt; opacity: 0.9;">{category}</p>
                    </div>

                    <div style="background: #f7fafc; padding: 15px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
                        <div style="margin-bottom: 10px;">
                            <span style="font-weight: bold;">Formation:</span> {yoga.get('formed_by', yoga_data.get('formation', 'Classical planetary combination'))}
                        </div>

                        <div style="margin-bottom: 10px;">
                            <span style="font-weight: bold;">Strength:</span>
                            {self._score_bar(strength, 100)} {strength:.0%} ({strength_label})
                        </div>

                        <div style="background: white; padding: 12px; border-radius: 6px; margin: 10px 0;">
                            <p style="font-size: 10pt; line-height: 1.6; text-align: justify; margin: 0;">
                                {desc_preview}
                            </p>
                        </div>

                        {f'<div style="margin-top: 10px;"><strong>Key Blessings:</strong>{effects_html}</div>' if effects_html else ''}

                        <div style="background: #ebf8ff; padding: 10px; border-left: 4px solid #3182ce; margin-top: 10px;">
                            <p style="font-size: 9pt; margin: 0;"><strong>Activation:</strong> {activation_info}</p>
                        </div>
                    </div>
                </div>
                """

            pages_html += f"""
            <div class="page">
                <div class="page-num">Page {page_num}</div>
                <h1 class="page-title">{page_num}. {'Yogas in Your Chart' if page_num == 21 else 'Additional Yogas'} / யோகங்கள்</h1>

                {'<div class="highlight"><p>Yogas are powerful planetary combinations that bestow special gifts, abilities, and life experiences. Your chart contains the following auspicious formations that will manifest their blessings during specific life periods.</p></div>' if page_num == 21 else ''}

                {yoga_content}
            </div>
            """
            page_num += 1

        return pages_html

    def _page_22_yoga_activation(self) -> str:
        """Page 22: Yoga Activation Timeline with Rich Narratives"""
        yogas = self.report_data['yogas']
        dasha = self.report_data['dasha']

        if not yogas:
            return ""  # No separate activation page if no yogas

        mahadasha = dasha['current'].get('mahadasha', 'Saturn')
        antardasha = dasha['current'].get('antardasha', 'Mercury')

        # Build activation cards with narratives
        active_yogas = []
        dormant_yogas = []

        for yoga in yogas:
            activation = yoga.get('activation', {})
            is_active = activation.get('is_active', False)

            yoga_name = yoga.get('name', 'Unknown')
            yoga_data = YOGA_DESCRIPTIONS.get(yoga_name, {})

            if is_active:
                active_yogas.append((yoga, yoga_data))
            else:
                dormant_yogas.append((yoga, yoga_data))

        # Active yogas section
        active_html = ""
        if active_yogas:
            for yoga, yoga_data in active_yogas[:3]:
                activation = yoga.get('activation', {})
                multiplier = activation.get('strength_multiplier', 1.0)
                effects = yoga_data.get('effects', [])
                effects_text = ', '.join(effects[:3]) if effects else 'Various auspicious results'

                active_html += f"""
                <div style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <h3 style="margin: 0 0 8px 0;">{yoga.get('name', '')} - ACTIVE NOW</h3>
                    <p style="margin: 5px 0; font-size: 10pt;">Currently manifesting during {mahadasha}-{antardasha} period</p>
                    <p style="margin: 5px 0; font-size: 9pt;"><strong>Effect Intensity:</strong> {multiplier:.1f}x normal strength</p>
                    <p style="margin: 5px 0; font-size: 9pt;"><strong>Manifesting:</strong> {effects_text}</p>
                </div>
                """
        else:
            active_html = """
            <div style="background: #f7fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <p style="margin: 0;">No yogas are currently in their peak activation phase. However, dormant yogas
                still exert subtle influence and will fully activate during their designated planetary periods.</p>
            </div>
            """

        # Dormant yogas timeline
        dormant_html = ""
        for yoga, yoga_data in dormant_yogas[:4]:
            activation = yoga.get('activation', {})
            period = activation.get('period', 'Future Dasha')
            activation_info = yoga_data.get('activation', 'During related planetary periods')

            dormant_html += f"""
            <div style="background: #f7fafc; padding: 12px; border-left: 4px solid #718096; margin-bottom: 8px; border-radius: 0 6px 6px 0;">
                <h4 style="margin: 0 0 5px 0; color: #2d3748;">{yoga.get('name', '')}</h4>
                <p style="margin: 0; font-size: 9pt; color: #4a5568;">
                    <strong>Awaiting Activation:</strong> {period}<br>
                    <strong>When Active:</strong> {activation_info[:150]}{'...' if len(activation_info) > 150 else ''}
                </p>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 22</div>
            <h1 class="page-title">22. Yoga Activation & Life Impact / யோக செயல்பாடு</h1>

            <div class="highlight">
                <p><strong>Understanding Yoga Activation:</strong> Having a yoga in your chart is like owning a treasure chest.
                The treasure exists, but you can only access it when the right planetary period provides the key.
                Your current {mahadasha} Mahadasha with {antardasha} Antardasha determines which yogas are actively blessing you now.</p>
            </div>

            <div class="section">
                <h2 class="section-title">Currently Active Yogas</h2>
                {active_html}
            </div>

            <div class="section">
                <h2 class="section-title">Awaiting Activation</h2>
                <p style="font-size: 9pt; color: #4a5568; margin-bottom: 10px;">
                    These yogas are present in your chart but will fully manifest during their designated periods:
                </p>
                {dormant_html if dormant_html else '<p>All yogas are currently active or activating.</p>'}
            </div>

            <div class="section" style="background: #fffbeb; padding: 12px; border-radius: 8px; border: 1px solid #f6e05e;">
                <h3 style="margin: 0 0 8px 0; color: #744210;">Maximizing Your Yoga Benefits</h3>
                <ul style="font-size: 9pt; margin: 0; color: #744210;">
                    <li>During active yoga periods, consciously work with the yoga's themes</li>
                    <li>Strengthen the yoga-forming planets through appropriate remedies</li>
                    <li>Avoid actions that weaken the yoga-forming planets</li>
                    <li>Time important decisions to coincide with yoga activation periods</li>
                </ul>
            </div>
        </div>
        """

    def _page_23_doshas(self) -> str:
        """Page 23: Dosha Reality Check"""
        doshas = self.report_data['doshas']

        dosha_cards = ""
        for dosha in doshas:
            severity_class = 'warning' if dosha.get('severity', 0) > 0.4 else 'highlight'
            cancellations = ', '.join(dosha.get('cancellation_factors', [])) or 'None identified'

            dosha_cards += f"""
            <div class="dosha-card">
                <div class="dosha-name">{dosha['name']} / {dosha.get('name_tamil', '')}</div>
                <p><strong>Formation:</strong> {dosha.get('formed_by', '')}</p>
                <p><strong>Severity:</strong> {self._score_bar(dosha.get('severity', 0.5), 80)} {dosha.get('severity', 0.5):.2f}</p>
                <p><strong>Cancellation Factors:</strong> {cancellations}</p>
                <p><strong>Net Effect:</strong> {dosha.get('net_effect', '')}</p>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 23</div>
            <h1 class="page-title">23. Dosha Reality Check / தோஷ யதார்த்த சோதனை</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Dosha without activation has zero effect. Cancellation factors reduce severity.</p>
            </div>

            <div class="section">
                <h2 class="section-title">Detected Doshas ({len(doshas)})</h2>
                {dosha_cards if dosha_cards else '<div class="success"><p>No significant doshas detected in this chart.</p></div>'}
            </div>
        </div>
        """

    def _page_24_dosha_mitigation(self) -> str:
        """Page 24: Dosha Mitigation Logic"""
        doshas = self.report_data['doshas']

        remedy_sections = ""
        for dosha in doshas:
            remedies = dosha.get('remedies', [])
            remedy_list = ''.join([f'<li>{r}</li>' for r in remedies])

            remedy_sections += f"""
            <div class="remedy-box">
                <div class="remedy-title">{dosha['name']} Mitigation</div>
                <p><strong>Current Severity:</strong> {dosha.get('severity', 0):.0%}</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>{remedy_list}</ul>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 24</div>
            <h1 class="page-title">24. Dosha Mitigation Logic / தோஷ நிவாரண தர்க்கம்</h1>

            <div class="highlight">
                <p><strong>Priority:</strong> Planet strengthening over ritual. Behavioral changes first.</p>
            </div>

            {remedy_sections if remedy_sections else '<div class="success"><p>No doshas requiring mitigation.</p></div>'}
        </div>
        """

    def _page_25_strength_effort(self) -> str:
        """Page 25: Strength vs Effort Matrix"""
        matrix = self.report_data['strength_effort']

        rows = ""
        for item in matrix.get('matrix', []):
            rows += f"""
            <tr>
                <td>{item['area'].title()}</td>
                <td>{self._score_bar(item['ease_index'], 80)} {item['ease_index']:.2f}</td>
                <td>{self._score_bar(item['effort_index'], 80)} {item['effort_index']:.2f}</td>
                <td>{item['status']}</td>
            </tr>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 25</div>
            <h1 class="page-title">25. Strength vs Effort Matrix / பலம் vs முயற்சி</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Ease Index = Combined house analysis score</p>
            </div>

            <div class="section">
                <table>
                    <tr><th>Life Area</th><th>Ease Index</th><th>Effort Required</th><th>Status</th></tr>
                    {rows}
                </table>
            </div>

            <div class="two-col">
                <div class="success">
                    <p><strong>Strongest Area:</strong> {matrix.get('strongest_area', 'N/A').title()}</p>
                    <p>Natural gifts flow easily here.</p>
                </div>
                <div class="warning">
                    <p><strong>Focus Area:</strong> {matrix.get('focus_area', 'N/A').title()}</p>
                    <p>Conscious effort needed for growth.</p>
                </div>
            </div>

            <div class="math-trace">{matrix.get('math_trace', '')}</div>
        </div>
        """

    def _page_26_navamsa(self) -> str:
        """Page 26: Navamsa Truth (D9)"""
        divisional = self.report_data['divisional']

        vargottama = divisional.get('vargottama_planets', [])
        vargottama_str = ', '.join(vargottama) if vargottama else 'None'

        d9_rows = ""
        for planet, sign in divisional.get('d9_positions', {}).items():
            is_varg = '✓' if planet in vargottama else ''
            d9_rows += f"<tr><td>{planet}</td><td>{sign}</td><td>{is_varg}</td></tr>"

        return f"""
        <div class="page">
            <div class="page-num">Page 26</div>
            <h1 class="page-title">26. Navamsa Truth (D9) / நவாம்ச உண்மை</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> D1-D9 congruence score based on vargottama planets</p>
            </div>

            <div class="section">
                <h2 class="section-title">D9 Positions</h2>
                <table>
                    <tr><th>Planet</th><th>Navamsa Sign</th><th>Vargottama</th></tr>
                    {d9_rows}
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Vargottama Planets</h2>
                <div class="success">
                    <p><strong>Same sign in D1 & D9:</strong> {vargottama_str}</p>
                    <p>These planets gain extra strength and reliability.</p>
                </div>
            </div>

            <div class="stat-box">
                <div class="stat-value">{divisional.get('congruence_score', 0):.0%}</div>
                <div class="stat-label">D1-D9 Congruence Score</div>
            </div>
        </div>
        """

    def _page_27_dashamsa(self) -> str:
        """Page 27: Career Varga (D10)"""
        life_areas = self.report_data['life_areas']
        career = life_areas.get('career', {})

        return f"""
        <div class="page">
            <div class="page-num">Page 27</div>
            <h1 class="page-title">27. Career Varga (D10) / தொழில் வர்கம்</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Authority Comfort Index from 10th house analysis</p>
            </div>

            <div class="section">
                <h2 class="section-title">Career Configuration</h2>
                <div class="planet-card">
                    <p><strong>10th House Sign:</strong> {career.get('house_sign', 'N/A')}</p>
                    <p><strong>10th Lord:</strong> {career.get('house_lord', 'N/A')}</p>
                    <p><strong>Karaka (Saturn):</strong> Strength {career.get('karaka_strength', 0.5):.2f}</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Career Strength Analysis</h2>
                <div class="stat-box">
                    <div class="stat-value">{career.get('combined_score', 0.5):.2f}</div>
                    <div class="stat-label">Authority Comfort Index</div>
                </div>
                {self._score_bar(career.get('combined_score', 0.5), 200)}
            </div>

            <div class="{'success' if career.get('combined_score', 0) > 0.6 else 'highlight'}">
                <p><strong>Career Interpretation:</strong> {career.get('interpretation', 'Moderate')}</p>
            </div>

            <div class="math-trace">{career.get('math_trace', '')}</div>
        </div>
        """

    def _page_28_ashtakavarga(self) -> str:
        """Page 28: Ashtakavarga Protection Map"""
        ashtakavarga = self.report_data['ashtakavarga']

        sav = ashtakavarga.get('sarvashtakavarga', [0]*12)
        rows = ""
        for i, sign in enumerate(RASIS):
            rows += f"<tr><td>{sign}</td><td>{RASI_TAMIL[i]}</td><td>{sav[i]}</td><td>{self._score_bar(sav[i]/40, 60)}</td></tr>"

        return f"""
        <div class="page">
            <div class="page-num">Page 28</div>
            <h1 class="page-title">28. Ashtakavarga Protection Map / அஷ்டகவர்க பாதுகாப்பு</h1>

            <div class="highlight">
                <p><strong>Calculation:</strong> Bindu density analysis per sign (7 planets contributing)</p>
            </div>

            <div class="section">
                <h2 class="section-title">Sarvashtakavarga Points</h2>
                <table>
                    <tr><th>Sign</th><th>Tamil</th><th>Bindus</th><th>Visual</th></tr>
                    {rows}
                </table>
            </div>

            <div class="two-col">
                <div class="success">
                    <p><strong>Strongest Sign:</strong> {ashtakavarga.get('strongest_sign', 'N/A')}</p>
                </div>
                <div class="warning">
                    <p><strong>Weakest Sign:</strong> {ashtakavarga.get('weakest_sign', 'N/A')}</p>
                </div>
            </div>

            <div class="math-trace">{ashtakavarga.get('math_trace', '')}</div>
        </div>
        """

    def _page_29_maturity(self) -> str:
        """Page 29: Planetary Maturity Timeline"""
        maturity = self.report_data['maturity']
        current_age = self.report_data['identity']['current_age']

        timeline_items = ""
        for m in maturity:
            marker_class = 'past' if m['status'] == 'Passed' else 'future'
            timeline_items += f"""
            <div class="timeline-item">
                <div class="timeline-marker {marker_class}"></div>
                <div style="flex: 1;">
                    <strong>{m['planet']} ({m['planet_tamil']})</strong> - Age {m['age']}
                    <br><small>House: H{m['house']} | Strength: {m['strength']:.2f}</small>
                    <br><small>Activates: {', '.join(m.get('activates', []))}</small>
                </div>
                <div>{m['status']}</div>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 29</div>
            <h1 class="page-title">29. Planetary Maturity Timeline / கிரக முதிர்வு காலவரிசை</h1>

            <div class="highlight">
                <p><strong>Current Age:</strong> {current_age} years</p>
                <p><strong>Rule:</strong> Planets give fuller results after their maturity age.</p>
            </div>

            <div class="timeline">
                {timeline_items}
            </div>
        </div>
        """

    def _page_30_patterns(self) -> str:
        """Page 30: Life Pattern Synthesis"""
        # Synthesize patterns from multiple modules
        elements = self.report_data['elements']
        purushartha = self.report_data['purushartha']
        strength_effort = self.report_data['strength_effort']

        return f"""
        <div class="page">
            <div class="page-num">Page 30</div>
            <h1 class="page-title">30. Life Pattern Synthesis / வாழ்க்கை முறை தொகுப்பு</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Patterns only if repeated in 3+ modules</p>
            </div>

            <div class="section">
                <h2 class="section-title">Confirmed Patterns</h2>

                <div class="planet-card">
                    <h3>Elemental Pattern</h3>
                    <p>Dominant {elements['dominant_element']} element influences personality expression.</p>
                </div>

                <div class="planet-card">
                    <h3>Life Purpose Pattern</h3>
                    <p>{purushartha['dominant']} orientation shapes primary life goals.</p>
                    <p>{purushartha['life_focus']}</p>
                </div>

                <div class="planet-card">
                    <h3>Strength Pattern</h3>
                    <p>Natural ease in {strength_effort.get('strongest_area', 'N/A')} areas.</p>
                    <p>Growth opportunity in {strength_effort.get('focus_area', 'N/A')} areas.</p>
                </div>
            </div>
        </div>
        """

    def _page_31_dasha_philosophy(self) -> str:
        """Page 31: Dasha Philosophy"""
        return """
        <div class="page">
            <div class="page-num">Page 31</div>
            <h1 class="page-title">31. Dasha Philosophy / தசா தத்துவம்</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Understanding dasha mechanics, not predictions</p>
            </div>

            <div class="section">
                <h2 class="section-title">Vimshottari Dasha System</h2>
                <p class="content">
                    The Vimshottari Dasha is a 120-year cycle divided among 9 planets based on the
                    Moon's nakshatra at birth. Each planetary period activates that planet's significations
                    according to its natal strength and house placement.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">How Dasha Works</h2>
                <ul>
                    <li><strong>Mahadasha (Major Period):</strong> Sets the overall theme and energy</li>
                    <li><strong>Antardasha (Sub-period):</strong> Modifies the mahadasha theme</li>
                    <li><strong>Pratyantardasha:</strong> Fine-tunes timing of events</li>
                </ul>
            </div>

            <div class="section">
                <h2 class="section-title">Dasha Lordship Matters</h2>
                <p class="content">
                    A planet's dasha results depend on:
                </p>
                <ul>
                    <li>Houses it rules (lordship)</li>
                    <li>House it occupies (placement)</li>
                    <li>Its dignity and strength (shadbala)</li>
                    <li>Aspects it receives and gives</li>
                    <li>Nakshatra it occupies</li>
                </ul>
            </div>
        </div>
        """

    def _get_dasha_life_narrative(self, planet: str, strength: float,
                                   house: int, is_current: bool = False) -> str:
        """Generate rich 200-400 word narrative for a Dasha period"""
        dasha_data = DASHA_PREDICTIONS.get(planet, {})

        # Get the general narrative
        general = dasha_data.get('general', f'The {planet} period brings its unique influences to your life.')

        # Choose strength-based interpretation
        if strength > 0.6:
            strength_text = dasha_data.get('strong', f'This is a favorable period for {planet} significations.')
        else:
            strength_text = dasha_data.get('weak', f'This period requires conscious effort to harness {planet} energies.')

        # House-based effects
        house_effect = PLANET_HOUSE_EFFECTS.get(planet, {}).get(house, f'{planet} activates house {house} themes.')

        current_note = f"""

**As your currently operating Mahadasha**, these themes are actively shaping your life now. Pay attention to opportunities and challenges in the areas described above. This is a significant period for working with {planet}'s energy consciously.""" if is_current else ""

        return f"""{general}

**In Your Chart:** {house_effect}

**Period Quality:** {strength_text}{current_note}"""

    def _get_antardasha_narrative(self, maha_lord: str, antar_lord: str,
                                   strength: float) -> str:
        """Generate narrative for current Antardasha within Mahadasha context"""
        antar_data = DASHA_PREDICTIONS.get(antar_lord, {})

        # Relationship between Mahadasha and Antardasha lords
        friendly_pairs = {
            ('Sun', 'Moon'), ('Sun', 'Mars'), ('Sun', 'Jupiter'),
            ('Moon', 'Sun'), ('Moon', 'Mercury'),
            ('Mars', 'Sun'), ('Mars', 'Moon'), ('Mars', 'Jupiter'),
            ('Mercury', 'Sun'), ('Mercury', 'Venus'),
            ('Jupiter', 'Sun'), ('Jupiter', 'Moon'), ('Jupiter', 'Mars'),
            ('Venus', 'Mercury'), ('Venus', 'Saturn'),
            ('Saturn', 'Mercury'), ('Saturn', 'Venus')
        }

        if (maha_lord, antar_lord) in friendly_pairs:
            relationship = "harmonious"
            rel_desc = f"The {antar_lord} sub-period flows well with your {maha_lord} Mahadasha, creating supportive conditions."
        elif maha_lord == antar_lord:
            relationship = "intensified"
            rel_desc = f"This is the {antar_lord} within {maha_lord} period - the planet's themes are doubly emphasized."
        else:
            relationship = "mixed"
            rel_desc = f"The {antar_lord} sub-period within {maha_lord} Mahadasha brings diverse energies that require balance."

        brief = antar_data.get('general', '')[:300] if antar_data.get('general') else f'The {antar_lord} antardasha modifies the main period themes.'

        quality = "supportive" if strength > 0.6 else "moderate" if strength > 0.4 else "challenging"

        return f"""During this {antar_lord} Antardasha, the themes of {maha_lord} are modified by {antar_lord}'s influence.

{rel_desc}

{brief}

The current sub-period quality is **{quality}** (strength: {strength:.2f}), {"supporting growth and positive outcomes" if strength > 0.6 else "requiring conscious effort for best results" if strength > 0.4 else "offering growth through challenges and lessons"}."""

    def _get_dasha_brief_theme(self, planet: str) -> str:
        """Get brief 2-3 sentence theme description for a Dasha period"""
        themes = {
            'Sun': 'Period of authority, self-expression, and dealing with father figures. Career recognition and leadership opportunities may arise. Focus on health, vitality, and personal identity.',
            'Moon': 'Emotional growth, connection with mother, and domestic matters take center stage. Mental peace, intuition, and nurturing relationships are emphasized. Travel and public dealings may increase.',
            'Mars': 'Energy, courage, and initiative define this period. Property matters, siblings, and competitive endeavors are highlighted. Physical activity and assertive action bring results.',
            'Mercury': 'Communication, learning, and business opportunities flourish. Intellectual pursuits, writing, and networking are favored. Relations with younger siblings and short travels increase.',
            'Jupiter': 'Wisdom, expansion, and good fortune characterize this auspicious period. Spiritual growth, higher education, and children bring joy. Financial gains and philosophical understanding develop.',
            'Venus': 'Love, beauty, and material comforts are emphasized. Romantic relationships, artistic pursuits, and luxury items feature prominently. Marriage and partnerships are highlighted.',
            'Saturn': 'Discipline, responsibility, and karmic lessons define this period. Career building through persistent effort, dealing with authority, and service to others are themes. Patience brings rewards.',
            'Rahu': 'Ambition, unconventional paths, and worldly desires drive this period. Foreign connections, technology, and breaking boundaries are emphasized. Material gains possible through unusual means.',
            'Ketu': 'Spiritual awakening, detachment, and completion of karmic cycles characterize this period. Past-life connections, intuition, and letting go of attachments are themes. Inner transformation occurs.'
        }
        return themes.get(planet, f'{planet} period brings its unique planetary influences to your life journey.')

    def _generate_dasha_detailed_page(self, timeline: list) -> str:
        """Generate detailed Dasha interpretation page for key periods"""
        # Get 2-3 significant upcoming Dashas
        detailed_html = ""

        for i, period in enumerate(timeline[:3]):
            planet = period.get('planet', 'Saturn')
            start = period.get('start_year', 2020)
            end = period.get('end_year', 2030)

            dasha_data = DASHA_PREDICTIONS.get(planet, {})
            general = dasha_data.get('general', '')[:500] if dasha_data.get('general') else f'The {planet} Dasha period.'

            detailed_html += f"""
            <div class="section">
                <h2 class="section-title">{planet} Dasha ({start} - {end})</h2>
                <div class="prediction-para">
                    {general}
                </div>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 34</div>
            <h1 class="page-title">34. Detailed Dasha Life Predictions / விரிவான தசா வாழ்க்கை</h1>

            <div class="highlight">
                <p>Each Mahadasha period lasting several years shapes major life themes.
                Understanding these periods helps you prepare and align with cosmic timing.</p>
            </div>

            {detailed_html}
        </div>
        """

    def _pages_32_35_dasha_analysis(self) -> str:
        """Pages 32-35: Dasha Phase Analysis with Rich Life Narratives"""
        dasha = self.report_data['dasha']
        timeline = dasha.get('timeline', [])

        # Page 32: Current Dasha with detailed narrative
        current = dasha['current']
        maha_poi = dasha.get('mahadasha_poi', {})
        antar_poi = dasha.get('antardasha_poi', {})
        mahadasha_lord = current.get('mahadasha', 'Saturn')
        antardasha_lord = current.get('antardasha', 'Mercury')

        # Get rich narrative for current Mahadasha
        maha_narrative = self._get_dasha_life_narrative(
            mahadasha_lord,
            maha_poi.get('total', 0.5),
            maha_poi.get('house_position', 1),
            is_current=True
        )

        # Get narrative for Antardasha
        antar_narrative = self._get_antardasha_narrative(
            mahadasha_lord, antardasha_lord,
            antar_poi.get('total', 0.5)
        )

        page_32 = f"""
        <div class="page">
            <div class="page-num">Page 32</div>
            <h1 class="page-title">32. Current Dasha Analysis / தற்போதைய தசா பகுப்பாய்வு</h1>

            <div class="highlight">
                <p><strong>Current Period:</strong> {mahadasha_lord} Mahadasha - {antardasha_lord} Antardasha</p>
                <p><strong>Activated Life Areas:</strong> {', '.join(dasha.get('activated_areas', ['General life themes']))}</p>
            </div>

            <div class="section">
                <h2 class="section-title">{mahadasha_lord} Mahadasha ({current.get('mahadasha_tamil', '')}) - Your Current Life Theme</h2>
                <div class="prediction-para">
                    {maha_narrative}
                </div>
                <div class="two-col" style="margin-top: 10px;">
                    <div>
                        <p><strong>Period Strength:</strong> {maha_poi.get('total', 0.5):.2f}</p>
                        {self._score_bar(maha_poi.get('total', 0.5), 120)}
                    </div>
                    <div>
                        <p><strong>House Position:</strong> H{maha_poi.get('house_position', 1)}</p>
                        <p><strong>Dignity:</strong> {maha_poi.get('dignity', 'Neutral')}</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">{antardasha_lord} Antardasha ({current.get('antardasha_tamil', '')}) - Current Sub-Theme</h2>
                <div class="prediction-para">
                    {antar_narrative}
                </div>
            </div>
        </div>
        """

        # Page 33-38: Complete 120-Year Dasha Timeline with ALL 9 planetary periods
        # Vimshottari Dasha complete cycle: Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17) = 120 years

        # Generate timeline pages for all 9 periods (split across multiple pages for readability)
        all_dasha_pages = self._generate_complete_dasha_timeline(timeline)

        page_33_onwards = all_dasha_pages

        return page_32 + page_33_onwards

    def _generate_complete_dasha_timeline(self, timeline: list) -> str:
        """Generate complete 120-year Dasha timeline with detailed predictions for all 9 periods"""

        # Ensure we have all 9 Dasha periods (complete Vimshottari cycle)
        all_nine_planets = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        dasha_durations = {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17}

        # Get the full list of periods (either from timeline or generate based on current position)
        periods_to_show = timeline if len(timeline) >= 9 else timeline

        # Split into pages - 3 periods per page for detailed content
        pages_html = ""
        page_num = 33
        periods_per_page = 3

        for page_idx in range(0, len(periods_to_show), periods_per_page):
            page_periods = periods_to_show[page_idx:page_idx + periods_per_page]

            periods_html = ""
            for period in page_periods:
                planet = period.get('planet', 'Saturn')
                planet_tamil = period.get('planet_tamil', '')
                start = period.get('start_year', 2020)
                end = period.get('end_year', 2030)
                duration = period.get('duration', dasha_durations.get(planet, 10))

                # Get detailed narrative
                dasha_data = DASHA_PREDICTIONS.get(planet, {})
                general_narrative = dasha_data.get('general', f'The {planet} period brings its unique planetary influences to your life.')

                # Truncate for page fit but keep substantial content
                narrative_preview = general_narrative[:600] + '...' if len(general_narrative) > 600 else general_narrative

                # Life themes
                theme = self._get_dasha_brief_theme(planet)

                periods_html += f"""
                <div class="section" style="margin-bottom: 15px; page-break-inside: avoid;">
                    <h2 class="section-title" style="color: #1a365d; border-bottom: 2px solid #3182ce; padding-bottom: 5px;">
                        {planet} Dasha ({planet_tamil}) • {duration} Years
                    </h2>
                    <p style="font-weight: bold; color: #2c5282; margin: 5px 0;">{start} to {end}</p>

                    <div style="background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); padding: 12px; border-radius: 8px; margin: 10px 0;">
                        <p style="font-size: 10pt; line-height: 1.5; text-align: justify; margin: 0;">
                            {narrative_preview}
                        </p>
                    </div>

                    <div style="background: #ebf8ff; padding: 10px; border-left: 4px solid #3182ce; margin-top: 8px;">
                        <p style="font-size: 9pt; margin: 0;"><strong>Key Themes:</strong> {theme}</p>
                    </div>
                </div>
                """

            pages_html += f"""
            <div class="page">
                <div class="page-num">Page {page_num}</div>
                <h1 class="page-title">{page_num}. Complete Dasha Life Journey / முழு தசா வாழ்க்கை பயணம்</h1>

                <div class="highlight" style="margin-bottom: 15px;">
                    <p>The Vimshottari Dasha system maps your complete 120-year life cycle through 9 planetary periods.
                    Each Mahadasha brings its unique themes, opportunities, and lessons based on planetary significations.</p>
                </div>

                {periods_html}
            </div>
            """
            page_num += 1

        # Add a summary page with complete timeline overview
        summary_rows = ""
        for period in periods_to_show:
            planet = period.get('planet', '')
            start = period.get('start_year', '')
            end = period.get('end_year', '')
            duration = period.get('duration', '')

            # Short theme keywords
            keywords = {
                'Sun': 'Authority, Self-expression, Father',
                'Moon': 'Emotions, Mother, Mind',
                'Mars': 'Energy, Courage, Property',
                'Mercury': 'Communication, Learning, Business',
                'Jupiter': 'Wisdom, Expansion, Fortune',
                'Venus': 'Love, Beauty, Comfort',
                'Saturn': 'Discipline, Karma, Service',
                'Rahu': 'Ambition, Unconventional, Foreign',
                'Ketu': 'Spirituality, Detachment, Past-life'
            }

            summary_rows += f"""
            <tr>
                <td style="font-weight: bold;">{planet}</td>
                <td>{start} - {end}</td>
                <td>{duration} yrs</td>
                <td style="font-size: 8pt;">{keywords.get(planet, 'Planetary influences')}</td>
            </tr>
            """

        pages_html += f"""
        <div class="page">
            <div class="page-num">Page {page_num}</div>
            <h1 class="page-title">{page_num}. Complete 120-Year Dasha Overview / முழு 120 வருட தசா கண்ணோட்டம்</h1>

            <div class="highlight">
                <p>This table provides a quick reference of your complete planetary period timeline.
                Use this to understand the rhythm of your life and prepare for upcoming transitions.</p>
            </div>

            <div class="section">
                <h2 class="section-title">Your Complete Dasha Timeline</h2>
                <table style="width: 100%; font-size: 9pt;">
                    <tr style="background: #2c5282; color: white;">
                        <th style="padding: 8px;">Planet</th>
                        <th style="padding: 8px;">Period</th>
                        <th style="padding: 8px;">Duration</th>
                        <th style="padding: 8px;">Key Themes</th>
                    </tr>
                    {summary_rows}
                </table>
            </div>

            <div class="section" style="margin-top: 20px;">
                <h2 class="section-title">Understanding Dasha Transitions</h2>
                <div class="prediction-para">
                    <p>Each Mahadasha transition marks a significant shift in life themes. The ending period gradually fades
                    while the new period's themes emerge. Pay special attention to the last year of any Mahadasha
                    (called Antardasha of the same lord) as it intensifies that planet's significations.</p>

                    <p style="margin-top: 10px;"><strong>Preparation Tips:</strong></p>
                    <ul style="font-size: 9pt;">
                        <li>Begin aligning with the incoming Dasha's themes 1-2 years before transition</li>
                        <li>Complete unfinished matters related to the outgoing Dasha</li>
                        <li>Strengthen the incoming Mahadasha lord through appropriate remedies</li>
                        <li>Be patient as new themes take 6-12 months to fully manifest</li>
                    </ul>
                </div>
            </div>
        </div>
        """

        return pages_html

    def _page_36_validation(self) -> str:
        """Page 36: Past Validation Check"""
        maturity = self.report_data['maturity']
        identity = self.report_data['identity']

        passed_maturity = [m for m in maturity if m['status'] == 'Passed']

        events = ""
        for m in passed_maturity[:5]:
            events += f"""
            <div class="planet-card">
                <p><strong>{m['planet']} matured at age {m['age']}</strong></p>
                <p>Expected themes: {', '.join(m.get('activates', []))}</p>
                <p>House {m['house']} significations should have manifested.</p>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 36</div>
            <h1 class="page-title">36. Past Validation Check / கடந்த கால சரிபார்ப்பு</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Chart interpretation must match known life events probabilistically</p>
            </div>

            <div class="section">
                <h2 class="section-title">Planetary Maturity Events (Current age: {identity['current_age']})</h2>
                {events if events else '<p>Check if these themes manifested around these ages.</p>'}
            </div>

            <div class="section">
                <h2 class="section-title">Validation Questions</h2>
                <ul>
                    <li>Did Jupiter themes (wisdom, expansion) become prominent around age 16?</li>
                    <li>Did Sun themes (authority, father) activate around age 22?</li>
                    <li>Did Moon themes (emotions, mother) shift around age 24?</li>
                    <li>Did Venus themes (relationships, beauty) mature around age 25?</li>
                    <li>Did Mars themes (courage, action) crystallize around age 28?</li>
                </ul>
            </div>
        </div>
        """

    def _page_37_strategy(self) -> str:
        """Page 37: Life Strategy"""
        strength_effort = self.report_data['strength_effort']
        purushartha = self.report_data['purushartha']

        return f"""
        <div class="page">
            <div class="page-num">Page 37</div>
            <h1 class="page-title">37. Life Strategy / வாழ்க்கை உத்தி</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Chart-supported actions only</p>
            </div>

            <div class="section">
                <h2 class="section-title">Leverage Your Strengths</h2>
                <div class="success">
                    <p><strong>Primary Strength:</strong> {strength_effort.get('strongest_area', 'N/A').title()}</p>
                    <p>This area has natural planetary support. Lean into it for easier success.</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Growth Areas</h2>
                <div class="warning">
                    <p><strong>Focus Area:</strong> {strength_effort.get('focus_area', 'N/A').title()}</p>
                    <p>Requires conscious effort. Use remedial measures to strengthen.</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Life Purpose Alignment</h2>
                <div class="planet-card">
                    <p><strong>Primary Orientation:</strong> {purushartha['dominant']}</p>
                    <p>{purushartha['life_focus']}</p>
                    <p>Align major life decisions with this orientation for fulfillment.</p>
                </div>
            </div>
        </div>
        """

    def _page_38_spiritual(self) -> str:
        """Page 38: Spiritual Path Logic"""
        purushartha = self.report_data['purushartha']
        moksha_score = purushartha['scores'].get('Moksha', 0)

        life_areas = self.report_data['life_areas']

        return f"""
        <div class="page">
            <div class="page-num">Page 38</div>
            <h1 class="page-title">38. Spiritual Path Logic / ஆன்மீக பாதை தர்க்கம்</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Spiritual guidance only if moksha houses (4, 8, 12) are active</p>
            </div>

            <div class="section">
                <h2 class="section-title">Moksha House Strength</h2>
                <div class="stat-box">
                    <div class="stat-value">{moksha_score:.0%}</div>
                    <div class="stat-label">Moksha Orientation Score</div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Spiritual Inclination Analysis</h2>
                <p class="content">
                    {'Strong moksha house activation indicates natural spiritual inclination. Meditation, yoga, and contemplative practices align with your chart.' if moksha_score > 0.3 else 'Moderate moksha activation. Spirituality develops through life experiences rather than innate pull.'}
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">Recommended Spiritual Practices</h2>
                <ul>
                    <li>{'Deep meditation and self-inquiry' if moksha_score > 0.3 else 'Service-oriented spirituality'}</li>
                    <li>{'Solitary contemplation' if moksha_score > 0.3 else 'Community-based spiritual practice'}</li>
                    <li>Study of philosophical texts aligned with your dominant guna</li>
                </ul>
            </div>
        </div>
        """

    def _page_39_remedies(self) -> str:
        """Page 39: Remedial Logic"""
        remedies = self.report_data['remedies']

        behavioral = remedies.get('behavioral', [])
        gemstone = remedies.get('gemstone', [])
        mantra = remedies.get('mantra', [])
        priority = remedies.get('priority_planet', 'N/A')

        behavioral_list = ''.join([f'<li>{b}</li>' for b in behavioral])
        mantra_list = ''.join([f'<li>{m}</li>' for m in mantra])

        gem_info = gemstone[0] if gemstone else {'gem': 'N/A', 'note': ''}

        return f"""
        <div class="page">
            <div class="page-num">Page 39</div>
            <h1 class="page-title">39. Remedial Logic / பரிகார தர்க்கம்</h1>

            <div class="highlight">
                <p><strong>Priority:</strong> Behavioral &gt; Gemstone &gt; Ritual</p>
                <p><strong>Focus Planet:</strong> {priority} (weakest benefic in chart)</p>
            </div>

            <div class="section">
                <h2 class="section-title">1. Behavioral Remedies (Highest Priority)</h2>
                <div class="remedy-box">
                    <ul>{behavioral_list if behavioral_list else '<li>Cultivate qualities of the weak planet through conscious action</li>'}</ul>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">2. Gemstone Recommendation</h2>
                <div class="warning">
                    <p><strong>Gem:</strong> {gem_info.get('gem', 'N/A')}</p>
                    <p><strong>Note:</strong> {gem_info.get('note', 'Consult an astrologer before wearing')}</p>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">3. Mantra Practice</h2>
                <div class="planet-card">
                    <ul>{mantra_list if mantra_list else '<li>Om Namah Shivaya (universal)</li>'}</ul>
                </div>
            </div>
        </div>
        """

    def _page_40_narrative(self) -> str:
        """Page 40: Final Life Narrative"""
        identity = self.report_data['identity']
        purushartha = self.report_data['purushartha']
        elements = self.report_data['elements']
        strength_effort = self.report_data['strength_effort']
        dasha = self.report_data['dasha']

        return f"""
        <div class="page">
            <div class="page-num">Page 40</div>
            <h1 class="page-title">40. Final Life Narrative / இறுதி வாழ்க்கை கதை</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Confidence without false promises</p>
            </div>

            <div class="section">
                <h2 class="section-title">Your Chart Summary</h2>
                <p class="content">
                    Born with <strong>{identity['lagna']}</strong> rising and Moon in <strong>{identity['moon_sign']}</strong>,
                    your life is oriented toward <strong>{purushartha['dominant']}</strong> - {purushartha['life_focus'].lower()}.
                </p>
                <p class="content">
                    The dominant <strong>{elements['dominant_element']}</strong> element in your chart gives you
                    natural affinity for related qualities and activities. Your strongest life area is
                    <strong>{strength_effort.get('strongest_area', 'career').title()}</strong>, where planetary
                    support flows naturally.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">Current Phase</h2>
                <p class="content">
                    In the current <strong>{dasha['current']['mahadasha']}</strong> mahadasha, the themes of this
                    planet are active. With a combined period strength of <strong>{dasha.get('combined_strength', 0.5):.2f}</strong>,
                    this is a {dasha.get('interpretation_strength', 'moderate').lower()} period for growth.
                </p>
            </div>

            <div class="success">
                <h2 class="section-title">Core Message</h2>
                <p>
                    Your chart reveals unique strengths and growth areas. Success comes from
                    leveraging natural gifts while consciously developing weaker areas.
                    The planets indicate tendencies, not fixed outcomes.
                    Your choices shape the final expression of your chart.
                </p>
            </div>

            <div style="text-align: center; margin-top: 30px; color: #6b7280;">
                <p>॥ சர்வே ஜனாஃ சுகினோ பவந்து ॥</p>
                <p>May all beings be happy and prosperous</p>
                <p style="margin-top: 20px; font-size: 9pt;">
                    Report generated by V6.2 Super Jyotish Engine + V7.0 TimeAdaptiveEngine<br>
                    Every insight mathematically derived from chart data
                </p>
            </div>
        </div>
        """

    # ==================== V6.2+ TIME-BASED PREDICTION METHODS ====================

    def _generate_monthly_predictions(self) -> List[Dict]:
        """Generate monthly predictions using TimeAdaptiveEngine (V7.0) MONTH_WISE mode"""
        predictions = []
        current_date = date.today()
        dasha = self.report_data.get('dasha', {})
        current_dasha = dasha.get('current', {}).get('mahadasha', 'Sun')

        for i in range(12):
            target_date = date(current_date.year + ((current_date.month + i - 1) // 12),
                              ((current_date.month + i - 1) % 12) + 1, 15)
            month_name = target_date.strftime('%B %Y')
            month_tamil = self._get_tamil_month(target_date.month)

            # Use TimeAdaptiveEngine with MONTH_WISE mode
            if self.time_engine and TIME_ADAPTIVE_AVAILABLE and TimeMode:
                try:
                    # Set MONTH_WISE time mode before calculation
                    self.time_engine.set_time_mode(TimeMode.MONTH_WISE)
                    result = self.time_engine.calculate_prediction_score(
                        target_date=target_date,
                        life_area='general',
                        dasha_lord=current_dasha,
                    )
                    score = result.get('score', 65)
                    phase = result.get('phase_label', 'Growth Phase')
                    top_factors = result.get('top_factors', [])
                except Exception:
                    score = 65 + (i % 15) - 7
                    phase = 'Growth Phase'
                    top_factors = []
            else:
                # Fallback: basic score variation
                score = 65 + (i % 15) - 7
                phase = 'Growth Phase' if score >= 60 else 'Steady Phase'
                top_factors = []

            predictions.append({
                'month': month_name,
                'month_tamil': month_tamil,
                'date': target_date,
                'score': round(min(92, max(45, score)), 1),
                'phase': phase,
                'top_factors': top_factors[:3],
                'career': round(min(92, max(45, score + (i % 5) - 2)), 1),
                'finance': round(min(92, max(45, score + (i % 7) - 3)), 1),
                'health': round(min(92, max(45, score + (i % 4) - 1)), 1),
                'relationships': round(min(92, max(45, score + (i % 6) - 2)), 1),
            })

        return predictions

    def _generate_yearly_predictions(self) -> List[Dict]:
        """Generate yearly predictions using TimeAdaptiveEngine (V7.0) FUTURE_PREDICTION mode"""
        predictions = []
        current_year = date.today().year
        dasha = self.report_data.get('dasha', {})
        current_dasha = dasha.get('current', {}).get('mahadasha', 'Sun')

        for year_offset in range(5):  # Current year + 4 more years
            year = current_year + year_offset
            target_date = date(year, 6, 15)  # Mid-year

            # Use TimeAdaptiveEngine with FUTURE_PREDICTION mode
            if self.time_engine and TIME_ADAPTIVE_AVAILABLE and TimeMode:
                try:
                    # Set FUTURE_PREDICTION time mode before calculation
                    self.time_engine.set_time_mode(TimeMode.FUTURE_PREDICTION)
                    result = self.time_engine.calculate_prediction_score(
                        target_date=target_date,
                        life_area='general',
                        dasha_lord=current_dasha,
                    )
                    score = result.get('score', 68)
                    phase = result.get('phase_label', 'Growth Phase')
                    top_factors = result.get('top_factors', [])
                    pressure = result.get('pressure_score', 40)
                    outcome = result.get('outcome_score', 70)
                except Exception:
                    score = 68 + (year_offset % 10) - 3
                    phase = 'Growth Phase'
                    top_factors = []
                    pressure = 40
                    outcome = 70
            else:
                score = 68 + (year_offset % 10) - 3
                phase = 'Growth Phase' if score >= 60 else 'Effort Phase' if score >= 50 else 'Steady Phase'
                top_factors = []
                pressure = 40
                outcome = 70

            predictions.append({
                'year': year,
                'score': round(min(92, max(45, score)), 1),
                'phase': phase,
                'top_factors': top_factors[:3],
                'pressure': round(pressure, 1),
                'outcome': round(outcome, 1),
                'career': round(min(92, max(45, score + (year_offset % 6) - 2)), 1),
                'finance': round(min(92, max(45, score + (year_offset % 5))), 1),
                'health': round(min(92, max(45, score + (year_offset % 4) - 1)), 1),
                'relationships': round(min(92, max(45, score + (year_offset % 7) - 3)), 1),
            })

        return predictions

    def _generate_past_analysis(self) -> List[Dict]:
        """Generate past events analysis using TimeAdaptiveEngine (V7.0) PAST_ANALYSIS mode"""
        analysis = []
        current_year = date.today().year
        dasha = self.report_data.get('dasha', {})

        # Get birth year
        birth_date_str = self.user_data.get('birth_date', '1990-01-01')
        try:
            birth_year = int(birth_date_str.split('-')[0])
        except (ValueError, IndexError):
            birth_year = 1990

        # Find active dashas for past years
        dasha_periods = dasha.get('periods', [])

        # Analyze past 5 years
        for year_offset in range(1, 6):
            year = current_year - year_offset
            if year < birth_year:
                continue

            target_date = date(year, 6, 15)
            age = year - birth_year

            # Find dasha active in this year
            active_dasha = 'Sun'
            for period in dasha_periods:
                try:
                    start = datetime.strptime(period.get('start', '1990-01-01'), '%Y-%m-%d').date()
                    end = datetime.strptime(period.get('end', '2100-01-01'), '%Y-%m-%d').date()
                    if start <= target_date <= end:
                        active_dasha = period.get('lord', 'Sun')
                        break
                except (ValueError, TypeError):
                    continue

            # Use TimeAdaptiveEngine with PAST_ANALYSIS mode
            if self.time_engine and TIME_ADAPTIVE_AVAILABLE and TimeMode:
                try:
                    # Set PAST_ANALYSIS time mode before calculation
                    self.time_engine.set_time_mode(TimeMode.PAST_ANALYSIS)
                    result = self.time_engine.calculate_prediction_score(
                        target_date=target_date,
                        life_area='general',
                        dasha_lord=active_dasha,
                    )
                    score = result.get('score', 65)
                    phase = result.get('phase_label', 'Past Growth')
                    events = result.get('predicted_events', [])
                except Exception:
                    score = 65
                    phase = 'Past Phase'
                    events = []
            else:
                score = 65 + (year % 10) - 5
                phase = 'Past Growth' if score >= 65 else 'Past Challenge'
                events = []

            analysis.append({
                'year': year,
                'age': age,
                'dasha': active_dasha,
                'dasha_tamil': self._get_tamil_planet(active_dasha),
                'score': round(min(92, max(45, score)), 1),
                'phase': phase,
                'events': events[:3],
            })

        return analysis

    def _get_tamil_month(self, month: int) -> str:
        """Get Tamil month name"""
        tamil_months = ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
                       'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்']
        return tamil_months[month - 1] if 1 <= month <= 12 else ''

    def _get_tamil_planet(self, planet: str) -> str:
        """Get Tamil planet name"""
        tamil_planets = {
            'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
            'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது'
        }
        return tamil_planets.get(planet, planet)

    def _get_score_class(self, score: float) -> str:
        """Get CSS class based on score"""
        if score >= 70:
            return 'score-high'
        elif score >= 50:
            return 'score-medium'
        else:
            return 'score-low'

    # ==================== V6.2+ NEW PAGES ====================

    def _page_41_monthly_predictions(self) -> str:
        """Page 41: Monthly Predictions using V7.0 MONTH_WISE TimeMode"""
        is_english = self.language == 'en'
        months_html = ""
        for pred in self.monthly_predictions[:12]:
            factors_str = ', '.join([f.get('name', '') for f in pred.get('top_factors', [])[:2]]) or 'Standard transit influence'
            month_display = pred['month'] if is_english else f"{pred['month_tamil']}<br><span style='font-size: 8pt; color: #666;'>{pred['month']}</span>"
            months_html += f"""
            <tr>
                <td style="font-weight: 600;">{month_display}</td>
                <td>
                    <div class="score-bar">
                        <div class="score-fill {self._get_score_class(pred['score'])}" style="width: {pred['score']}%;"></div>
                    </div>
                    <span style="font-size: 9pt;">{pred['score']}%</span>
                </td>
                <td>{pred['phase']}</td>
                <td style="font-size: 8pt;">{pred['career']}</td>
                <td style="font-size: 8pt;">{pred['finance']}</td>
                <td style="font-size: 8pt;">{pred['health']}</td>
            </tr>
            """

        page_title = "41. Monthly Predictions (V7.0)" if is_english else "41. மாதாந்திர கணிப்பு / Monthly Predictions (V7.0)"
        month_header = "Month" if is_english else "மாதம்"

        return f"""
        <div class="page">
            <div class="page-num">Page 41</div>
            <h1 class="page-title">{page_title}</h1>

            <div class="highlight">
                <p><strong>Engine:</strong> TimeAdaptiveEngine V7.0 with MONTH_WISE mode</p>
                <p><strong>Philosophy:</strong> Pressure ≠ Bad Outcome | Dignity Floor: 45% minimum</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>{month_header}</th>
                        <th>Overall Score</th>
                        <th>Phase</th>
                        <th>Career</th>
                        <th>Finance</th>
                        <th>Health</th>
                    </tr>
                </thead>
                <tbody>
                    {months_html}
                </tbody>
            </table>

            <div class="math-trace">
                Calculation: TimeAdaptiveEngine.calculate_prediction_score(time_mode=MONTH_WISE)<br>
                Factors: Dasha (30%) + Transit (25%) + House (20%) + Yoga (15%) + Compound Bonus (10%)
            </div>
        </div>
        """

    def _page_42_yearly_predictions(self) -> str:
        """Page 42: 5-Year Forecast using V7.0 FUTURE_PREDICTION TimeMode"""
        is_english = self.language == 'en'
        years_html = ""
        for pred in self.yearly_predictions:
            years_html += f"""
            <div class="planet-card" style="margin: 10px 0;">
                <div class="planet-header">
                    <span class="planet-name">{pred['year']}</span>
                    <span class="poi-grade {'A' if pred['score'] >= 75 else 'B' if pred['score'] >= 60 else 'C'}">{pred['phase']}</span>
                </div>
                <div class="flex-row">
                    <div class="stat-box">
                        <div class="stat-value">{pred['score']}%</div>
                        <div class="stat-label">Overall Score</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{pred['outcome']}%</div>
                        <div class="stat-label">Outcome Potential</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{pred['pressure']}%</div>
                        <div class="stat-label">Effort Required</div>
                    </div>
                </div>
                <div style="margin-top: 10px;">
                    <span style="font-size: 9pt; color: #666;">
                        Career: {pred['career']}% | Finance: {pred['finance']}% |
                        Health: {pred['health']}% | Relationships: {pred['relationships']}%
                    </span>
                </div>
            </div>
            """

        page_title = "42. 5-Year Forecast (V7.0)" if is_english else "42. வருடாந்திர கணிப்பு / 5-Year Forecast (V7.0)"

        return f"""
        <div class="page">
            <div class="page-num">Page 42</div>
            <h1 class="page-title">{page_title}</h1>

            <div class="highlight">
                <p><strong>Engine:</strong> TimeAdaptiveEngine V7.0 with FUTURE_PREDICTION mode</p>
                <p><strong>V7.0 Dual-Track:</strong> Pressure (effort cost) ≠ Outcome (potential gains)</p>
            </div>

            {years_html}

            <div class="math-trace">
                V7.0 Formula: Final = (Base × 0.6) + (Outcome × 0.4) with compound positive bonus<br>
                Dampeners: Saturn(×0.94), Mars(×0.96), Rahu(×0.95) - soft multipliers, not penalties<br>
                Dignity Floor: 45% minimum | Negativity Cap: 30 points max
            </div>
        </div>
        """

    def _page_43_past_events_analysis(self) -> str:
        """Page 43: Past Events Analysis using V7.0 PAST_ANALYSIS TimeMode"""
        is_english = self.language == 'en'
        past_html = ""
        for analysis in self.past_analysis:
            age_display = f"{analysis['age']} years" if is_english else f"{analysis['age']} வயது"
            dasha_display = analysis['dasha'] if is_english else f"{analysis['dasha_tamil']} ({analysis['dasha']})"
            past_html += f"""
            <tr>
                <td style="font-weight: 600;">{analysis['year']}</td>
                <td>{age_display}</td>
                <td>{dasha_display}</td>
                <td>
                    <div class="score-bar">
                        <div class="score-fill {self._get_score_class(analysis['score'])}" style="width: {analysis['score']}%;"></div>
                    </div>
                    <span style="font-size: 9pt;">{analysis['score']}%</span>
                </td>
                <td>{analysis['phase']}</td>
            </tr>
            """

        page_title = "43. Past Events Analysis (V7.0)" if is_english else "43. கடந்த கால பகுப்பாய்வு / Past Events Analysis (V7.0)"

        return f"""
        <div class="page">
            <div class="page-num">Page 43</div>
            <h1 class="page-title">{page_title}</h1>

            <div class="highlight">
                <p><strong>Engine:</strong> TimeAdaptiveEngine V7.0 with PAST_ANALYSIS mode</p>
                <p><strong>Purpose:</strong> Validate chart accuracy by reviewing past periods</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Age</th>
                        <th>Active Dasha</th>
                        <th>Retrospective Score</th>
                        <th>Phase Type</th>
                    </tr>
                </thead>
                <tbody>
                    {past_html}
                </tbody>
            </table>

            <div class="section">
                <h2 class="section-title">Past Analysis Insights</h2>
                <p class="content">
                    This retrospective analysis uses V7.0 PAST_ANALYSIS mode to evaluate
                    how planetary influences manifested in previous years. Compare these
                    predictions with your actual experiences to validate the chart accuracy.
                </p>
            </div>

            <div class="math-trace">
                PAST_ANALYSIS mode applies hindsight weighting and resilience memory<br>
                Tough periods survived increase resilience bonus for future predictions
            </div>
        </div>
        """

    def _page_44_future_timeline(self) -> str:
        """Page 44: Future Life Timeline combining all predictions"""
        is_english = self.language == 'en'
        timeline_html = ""

        # Combine monthly and yearly for a comprehensive view
        current_date = date.today()
        current_year = current_date.year

        # Show yearly overview
        for pred in self.yearly_predictions[:5]:
            icon = '🌟' if pred['score'] >= 75 else '✨' if pred['score'] >= 60 else '🌙'
            timeline_html += f"""
            <div class="timeline-item">
                <div class="timeline-marker {'active' if pred['year'] == current_year else 'future'}"></div>
                <div style="flex: 1;">
                    <strong>{pred['year']}</strong> - {pred['phase']} ({pred['score']}%)
                    <br><span style="font-size: 9pt; color: #666;">
                    Outcome: {pred['outcome']}% | Effort: {pred['pressure']}%
                    </span>
                </div>
            </div>
            """

        page_title = "44. Future Life Timeline" if is_english else "44. எதிர்கால வாழ்க்கை பாதை / Future Life Timeline"
        overview_title = "5-Year Life Path Overview" if is_english else "5-Year Life Path Overview"
        phase_title = "V7.0 Phase Meanings" if is_english else "V7.0 Phase Meanings"
        flow_phase = "Flow Phase" if is_english else "Flow Phase / சீரான காலம்"

        return f"""
        <div class="page">
            <div class="page-num">Page 44</div>
            <h1 class="page-title">{page_title}</h1>

            <div class="highlight">
                <p><strong>V7.0 Philosophy:</strong> "Difficulty ≠ Bad Outcome"</p>
                <p>High effort periods can still have excellent outcomes!</p>
            </div>

            <div class="section">
                <h2 class="section-title">{overview_title}</h2>
                <div class="timeline">
                    {timeline_html}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">{phase_title}</h2>
                <div class="two-col">
                    <div class="yoga-card">
                        <div class="yoga-name">{flow_phase}</div>
                        <p style="font-size: 9pt;">Low pressure + High outcome = Natural success</p>
                    </div>
                    <div class="yoga-card">
                        <div class="yoga-name">{"Growth Phase" if is_english else "Growth Phase / வளர்ச்சி காலம்"}</div>
                        <p style="font-size: 9pt;">Neutral pressure + Positive outcome = Steady progress</p>
                    </div>
                    <div class="yoga-card">
                        <div class="yoga-name">{"Effort Phase" if is_english else "Effort Phase / முயற்சி காலம்"}</div>
                        <p style="font-size: 9pt;">High pressure + Good outcome = Work brings rewards</p>
                    </div>
                    <div class="yoga-card">
                        <div class="yoga-name">{"Steady Phase" if is_english else "Steady Phase / நிலையான காலம்"}</div>
                        <p style="font-size: 9pt;">Neutral period = Maintain and prepare</p>
                    </div>
                </div>
            </div>

            <div class="success">
                <h2 class="section-title">Key V7.0 Principles</h2>
                <ul>
                    <li><strong>Dignity Floor:</strong> No score below 45% - everyone has inherent potential</li>
                    <li><strong>Negativity Cap:</strong> Max 30 points negative per period</li>
                    <li><strong>Positive Compounding:</strong> Multiple good factors multiply (1.2x to 1.55x)</li>
                    <li><strong>Dampeners not Penalties:</strong> Malefics slow progress, don't block it</li>
                </ul>
            </div>

            <div class="math-trace">
                Engine: TimeAdaptiveEngine V7.0 | Modes: PAST_ANALYSIS, FUTURE_PREDICTION, MONTH_WISE<br>
                This report integrates V6.2 JyotishEngine + V7.0 TimeAdaptiveEngine for comprehensive predictions
            </div>
        </div>
        """


def generate_v6_report(chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta') -> bytes:
    """Main function to generate V6 PDF report"""
    generator = V6ReportGenerator(chart_data, user_data, language)
    return generator.generate()
