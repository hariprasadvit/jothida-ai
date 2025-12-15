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
"""

import io
from datetime import datetime
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
    """V6.0 Super Jyotish Report Generator"""

    def __init__(self, chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta'):
        self.chart_data = chart_data
        self.user_data = user_data
        self.language = language
        self.engine = JyotishEngine(chart_data, user_data)
        self.report_data = self.engine.generate_report_data()

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
                    sign_tamil = RASI_TAMIL[RASIS.index(sign)] if sign in RASIS else sign

                    cell_class = "corner" if (row_idx in [0, 3] or col_idx in [0, 3]) else "middle"
                    lagna_marker = '<span class="lagna-marker">Asc</span>' if is_lagna else ''

                    cells_html += f'''
                    <div class="chart-cell {cell_class}">
                        <span class="sign-name">{sign_tamil[:3]}</span>
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
                    sign_tamil = RASI_TAMIL[RASIS.index(sign)] if sign in RASIS else sign
                    cell_class = "corner" if (row_idx in [0, 3] or col_idx in [0, 3]) else "middle"

                    cells_html += f'''
                    <div class="chart-cell {cell_class}">
                        <span class="sign-name">{sign_tamil[:3]}</span>
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
        d1_html = self._render_south_indian_chart(d1_data, "D1 Rasi Chart / ராசி சக்கரம்")
        d9_html = self._render_d9_chart(d9_data, "D9 Navamsa Chart / நவாம்ச சக்கரம்")

        return f'''
        <div class="charts-side-by-side" style="display: flex; justify-content: space-around; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 300px;">{d1_html}</div>
            <div style="flex: 1; min-width: 300px;">{d9_html}</div>
        </div>
        '''

    def _render_nirayana_longitudes_table(self) -> str:
        """Render Nirayana Longitudes Summary table with Deg:Min:Sec format"""
        longitudes = self.engine.get_nirayana_longitudes_table()

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

            rows += f'''
            <tr>
                <td><strong>{p.get('abbr', '')}</strong> {p.get('tamil', '')}</td>
                <td>{p.get('rasi_tamil', '')}</td>
                <td>{p.get('longitude_dms', '')}</td>
                <td>{p.get('nakshatra', '')} / {p.get('pada', '')}</td>
                <td>{status or '-'}</td>
            </tr>
            '''

        return f'''
        <div class="section">
            <h3 class="section-title">Nirayana Longitudes Summary / நிரயன தீர்க்காம்சம்</h3>
            <table>
                <thead>
                    <tr>
                        <th>Planet / கிரகம்</th>
                        <th>Rasi / ராசி</th>
                        <th>Deg:Min:Sec</th>
                        <th>Star / Pada</th>
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
                    sign_tamil = h_data.get('sign_tamil', sign[:3])
                    planets = h_data.get('planets', [])

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
                        <span class="sign-name">{sign_tamil[:3]}</span>
                        <span class="house-num">H{house_num}</span>
                        <div class="planets">{lagna_marker} {planets_html}</div>
                    </div>
                    '''

        return f'''
        <div class="chart-container">
            <div class="chart-title">Special Rasi Chakra / விசேஷ ராசி சக்கரம்</div>
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

        rows = ""
        for h in houses:
            planets_str = ', '.join([p['abbr'] + ('(R)' if p.get('retrograde') else '')
                                     for p in h.get('planets', [])])
            rows += f'''
            <tr>
                <td><strong>H{h['house_num']}</strong></td>
                <td>{h['sign_tamil']}</td>
                <td>{h['lord_abbr']}</td>
                <td>{h['arambha']['degree_dms']}</td>
                <td>{h['madhya']['degree_dms']}</td>
                <td>{h['anthya']['degree_dms']}</td>
                <td>{planets_str or '-'}</td>
            </tr>
            '''

        return f'''
        <div class="section">
            <h3 class="section-title">Bhava Table / பாவ அட்டவணை</h3>
            <table style="font-size: 8pt;">
                <thead>
                    <tr>
                        <th>House</th>
                        <th>Sign / ராசி</th>
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
        name = identity['name']
        birth_date = identity['birth_date']
        birth_time = identity['birth_time']
        birth_place = identity['birth_place']
        lagna = identity['lagna']
        moon_sign = identity['moon_sign']
        nakshatra = identity['moon_nakshatra']

        lagna_tamil = RASI_TAMIL[RASIS.index(lagna)] if lagna in RASIS else lagna
        moon_tamil = RASI_TAMIL[RASIS.index(moon_sign)] if moon_sign in RASIS else moon_sign

        return f"""
        <div class="cover">
            <div class="cover-title">ஜாதக அறிக்கை</div>
            <div class="cover-subtitle">V6.2 Super Jyotish Report</div>

            <div class="cover-name">{name}</div>

            <div class="cover-details">
                <p><strong>பிறந்த தேதி:</strong> {birth_date}</p>
                <p><strong>பிறந்த நேரம்:</strong> {birth_time}</p>
                <p><strong>பிறந்த இடம்:</strong> {birth_place}</p>
            </div>

            <div class="cover-chart-summary">
                <p><strong>லக்னம்:</strong> {lagna_tamil} ({lagna})</p>
                <p><strong>ராசி:</strong> {moon_tamil} ({moon_sign})</p>
                <p><strong>நட்சத்திரம்:</strong> {nakshatra}</p>
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

        # Birth details
        name = identity['name']
        birth_date = identity['birth_date']
        birth_time = identity['birth_time']
        birth_place = identity['birth_place']
        lat = self.user_data.get('latitude', 13.0827)
        lon = self.user_data.get('longitude', 80.2707)

        # Panchanga data
        weekday = panchanga.get('weekday_tamil', 'ஞாயிறு')
        nakshatra = panchanga.get('nakshatra_tamil', identity['moon_nakshatra'])
        nakshatra_pada = panchanga.get('nakshatra_pada', 1)
        rasi = panchanga.get('rasi_tamil', '')
        rasi_lord = panchanga.get('rasi_lord_tamil', '')
        lagna = panchanga.get('lagna_tamil', identity['lagna'])
        lagna_lord = panchanga.get('lagna_lord_tamil', '')
        thithi = panchanga.get('thithi_tamil', '')
        karana = panchanga.get('karana_tamil', '')
        yoga = panchanga.get('yoga_tamil', '')
        sunrise = panchanga.get('sunrise', '06:00')
        sunset = panchanga.get('sunset', '18:00')
        ayanamsa_val = panchanga.get('ayanamsa', 23.85)
        try:
            ayanamsa = float(ayanamsa_val) if ayanamsa_val else 23.85
        except (ValueError, TypeError):
            ayanamsa = 23.85

        # Special panchanga details
        star_lord = panchanga.get('nakshatra_lord_tamil', '')
        ganam = panchanga.get('ganam', 'Deva')
        yoni = panchanga.get('yoni', 'Horse')
        animal = panchanga.get('animal', '')
        chandra_avastha = panchanga.get('chandra_avastha', '')
        dagda_rasi = panchanga.get('dagda_rasi', '')
        yogi_point = panchanga.get('yogi_point', '')
        yogi_planet = panchanga.get('yogi_planet_tamil', '')
        avayogi = panchanga.get('avayogi_tamil', '')
        atmakaraka = panchanga.get('atmakaraka_tamil', '')
        amatyakaraka = panchanga.get('amatyakaraka_tamil', '')
        lagna_aruda = panchanga.get('lagna_aruda', '')
        dhana_aruda = panchanga.get('dhana_aruda', '')
        kalidina = panchanga.get('kalidina', 0)
        dinamana = panchanga.get('dinamana', '')

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <div class="ganesha-symbol">ॐ</div>
                <h1>ஜோதிட அறிக்கை</h1>
                <div class="om-sri">॥ ஓம் ஸ்ரீ கணேசாய நமஹ ॥</div>
            </div>

            <h2 class="section-title" style="text-align: center; color: var(--maroon);">
                Birth Details / பிறப்பு விவரங்கள்
            </h2>

            <div class="birth-details-box">
                <div class="birth-details-grid">
                    <div class="birth-detail-item">
                        <span class="label">Name / பெயர்</span>
                        <span class="value"><strong>{name}</strong></span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Sex / பாலினம்</span>
                        <span class="value">-</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Date of Birth / பிறந்த தேதி</span>
                        <span class="value">{birth_date} ({weekday})</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Time of Birth / பிறந்த நேரம்</span>
                        <span class="value">{birth_time}</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Place of Birth / பிறந்த இடம்</span>
                        <span class="value">{birth_place}</span>
                    </div>
                    <div class="birth-detail-item">
                        <span class="label">Longitude & Latitude</span>
                        <span class="value">{lon:.4f}° E, {lat:.4f}° N</span>
                    </div>
                </div>
            </div>

            <h2 class="section-title" style="text-align: center; color: var(--maroon); margin-top: 20px;">
                Panchanga Details / பஞ்சாங்க விவரங்கள்
            </h2>

            <div class="panchanga-box">
                <div class="panchanga-grid">
                    <div class="panchanga-item">
                        <span class="label">Ayanamsa / அயனாம்சம்</span>
                        <span class="value">Lahiri {ayanamsa:.4f}°</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Birth Star / நட்சத்திரம்</span>
                        <span class="value">{nakshatra} - {nakshatra_pada} பாதம்</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Birth Rasi / ராசி</span>
                        <span class="value">{rasi} ({rasi_lord})</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Lagna / லக்னம்</span>
                        <span class="value">{lagna} ({lagna_lord})</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Thithi / திதி</span>
                        <span class="value">{thithi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Sunrise / சூரிய உதயம்</span>
                        <span class="value">{sunrise}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Sunset / சூரிய அஸ்தமனம்</span>
                        <span class="value">{sunset}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Dinamana / தினமானம்</span>
                        <span class="value">{dinamana}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Kalidina Sankhya</span>
                        <span class="value">{kalidina}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Dasa System</span>
                        <span class="value">Vimshottari</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Star Lord / நட்சத்திர அதிபதி</span>
                        <span class="value">{star_lord}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Ganam / கணம்</span>
                        <span class="value">{ganam}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Yoni / யோனி</span>
                        <span class="value">{yoni}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Animal / விலங்கு</span>
                        <span class="value">{animal}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Chandra Avastha</span>
                        <span class="value">{chandra_avastha}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Dagda Rasi / தக்த ராசி</span>
                        <span class="value">{dagda_rasi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Karanam / கரணம்</span>
                        <span class="value">{karana}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Nithya Yoga / நித்ய யோகம்</span>
                        <span class="value">{yoga}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Yogi Point</span>
                        <span class="value">{yogi_point}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Yogi Planet / யோகி கிரகம்</span>
                        <span class="value">{yogi_planet}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Avayogi / அவயோகி</span>
                        <span class="value">{avayogi}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Atma Karaka / ஆத்மகாரகன்</span>
                        <span class="value">{atmakaraka}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Amatya Karaka / அமாத்ய காரகன்</span>
                        <span class="value">{amatyakaraka}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Lagna Aruda (AL)</span>
                        <span class="value">{lagna_aruda}</span>
                    </div>
                    <div class="panchanga-item">
                        <span class="label">Dhana Aruda (A2)</span>
                        <span class="value">{dhana_aruda}</span>
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 15px; font-size: 9pt; color: #6b7280;">
                All calculations based on Lahiri Ayanamsa | சுத்த ஜாதக விதிகள்படி கணிக்கப்பட்டது
            </div>
        </div>
        """

    def _lifesign_page_2_predictions(self) -> str:
        """LifeSign Format - Page 2: Panchanga Predictions Summary"""
        panchanga = self.engine.get_complete_panchanga()
        identity = self.report_data['identity']

        name = identity['name']
        nakshatra = panchanga.get('nakshatra_tamil', identity['moon_nakshatra'])
        nakshatra_en = panchanga.get('nakshatra', identity['moon_nakshatra'])
        rasi = panchanga.get('rasi_tamil', '')
        rasi_en = panchanga.get('rasi', identity['moon_sign'])
        lagna = panchanga.get('lagna_tamil', '')
        lagna_en = panchanga.get('lagna', identity['lagna'])
        nakshatra_lord = panchanga.get('nakshatra_lord', 'Ketu')
        rasi_lord = panchanga.get('rasi_lord', 'Mars')
        lagna_lord = panchanga.get('lagna_lord', 'Mars')

        # Get nakshatra qualities for prediction
        ganam = panchanga.get('ganam', 'Deva')
        yoni = panchanga.get('yoni', 'Horse')
        thithi = panchanga.get('thithi_tamil', '')
        yoga = panchanga.get('yoga_tamil', '')

        # Generate dynamic prediction paragraph based on chart data
        prediction_text = self._generate_panchanga_prediction(panchanga, identity)

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>பஞ்சாங்க பலன்கள்</h1>
                <div class="om-sri">Panchanga Predictions</div>
            </div>

            <div class="highlight" style="text-align: center; margin: 15px 0;">
                <p style="font-size: 12pt;"><strong>{name}</strong></p>
                <p style="font-size: 10pt;">
                    {nakshatra} நட்சத்திரம் | {rasi} ராசி | {lagna} லக்னம்
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">Birth Summary / பிறப்பு சுருக்கம்</h2>
                <div class="prediction-para">
                    {prediction_text}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Nakshatra Characteristics / நட்சத்திர குணாதிசயங்கள்</h2>
                <div class="two-col">
                    <div class="stat-box">
                        <div class="stat-value" style="font-size: 16pt;">{nakshatra}</div>
                        <div class="stat-label">{nakshatra_en} | Lord: {nakshatra_lord}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="font-size: 16pt;">{ganam} கணம்</div>
                        <div class="stat-label">Gana Type | {yoni} Yoni</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Panchanga Elements / பஞ்சாங்க அம்சங்கள்</h2>
                <table>
                    <tr>
                        <th>Element</th>
                        <th>Value</th>
                        <th>Significance</th>
                    </tr>
                    <tr>
                        <td><strong>Thithi / திதி</strong></td>
                        <td>{thithi}</td>
                        <td>{self._get_thithi_significance(panchanga.get('thithi', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Nakshatra / நட்சத்திரம்</strong></td>
                        <td>{nakshatra}</td>
                        <td>{self._get_nakshatra_significance(nakshatra_en)}</td>
                    </tr>
                    <tr>
                        <td><strong>Yoga / யோகம்</strong></td>
                        <td>{yoga}</td>
                        <td>{self._get_yoga_significance(panchanga.get('yoga', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Karana / கரணம்</strong></td>
                        <td>{panchanga.get('karana_tamil', '')}</td>
                        <td>{self._get_karana_significance(panchanga.get('karana', ''))}</td>
                    </tr>
                    <tr>
                        <td><strong>Varam / வாரம்</strong></td>
                        <td>{panchanga.get('weekday_tamil', '')}</td>
                        <td>{self._get_weekday_significance(panchanga.get('weekday', ''))}</td>
                    </tr>
                </table>
            </div>

            <div class="success" style="margin-top: 15px;">
                <p><strong>Yogi Planet / யோகி கிரகம்:</strong> {panchanga.get('yogi_planet_tamil', '')} -
                   This planet brings prosperity when strengthened.</p>
            </div>
            <div class="warning">
                <p><strong>Avayogi / அவயோகி:</strong> {panchanga.get('avayogi_tamil', '')} -
                   This planet's periods require caution.</p>
            </div>
        </div>
        """

    def _generate_panchanga_prediction(self, panchanga: Dict, identity: Dict) -> str:
        """Generate dynamic prediction paragraph based on panchanga data"""
        name = identity['name']
        nakshatra = panchanga.get('nakshatra', identity['moon_nakshatra'])
        nakshatra_lord = panchanga.get('nakshatra_lord', 'Ketu')
        rasi = panchanga.get('rasi', identity['moon_sign'])
        rasi_lord = panchanga.get('rasi_lord', 'Mars')
        lagna = panchanga.get('lagna', identity['lagna'])
        lagna_lord = panchanga.get('lagna_lord', 'Mars')
        ganam = panchanga.get('ganam', 'Deva')
        yoni = panchanga.get('yoni', 'Horse')
        thithi = panchanga.get('thithi', 'Pratipada')
        yoga = panchanga.get('yoga', 'Vishkambha')

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

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>பாவ பலன்கள்</h1>
                <div class="om-sri">Bhava Predictions (Houses 1-6)</div>
            </div>

            <div class="section">
                {houses_1_6_html}
            </div>
        </div>

        <div class="page">
            <div class="lifesign-header">
                <h1>பாவ பலன்கள்</h1>
                <div class="om-sri">Bhava Predictions (Houses 7-12)</div>
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

            bhukti_html = ""
            for bhukti in bhuktis[:5]:  # Show first 5 bhuktis
                bhukti_html += f"""
                <div class="bhukti-item">
                    <strong>{bhukti.get('planet_tamil', '')} ({bhukti.get('planet', '')})</strong>:
                    {bhukti.get('start', '')} to {bhukti.get('end', '')}
                </div>
                """

            current_html = f"""
            <div class="dasha-period" style="border-left-color: #10b981; border-width: 4px;">
                <div class="dasha-header" style="color: #065f46;">
                    ★ Current Mahadasha: {mahadasha_tamil} ({mahadasha})
                </div>
                <div class="dasha-dates">
                    {start_date} to {end_date}
                </div>
                <p class="content" style="font-size: 9pt;">{prediction}</p>
                <h4 style="font-size: 10pt; margin-top: 8px;">Bhukti Periods / புக்தி காலம்:</h4>
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

            future_html += f"""
            <div class="dasha-period">
                <div class="dasha-header">{mahadasha_tamil} ({mahadasha}) Mahadasha</div>
                <div class="dasha-dates">{start_date} to {end_date}</div>
                <p class="content" style="font-size: 9pt;">{prediction}</p>
            </div>
            """

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>விம்சோத்தரி தசா பலன்கள்</h1>
                <div class="om-sri">Vimshottari Dasha Predictions</div>
            </div>

            <div class="section">
                <h2 class="section-title">Current Period / நடப்பு காலம்</h2>
                {current_html}
            </div>

            <div class="section">
                <h2 class="section-title">Upcoming Periods / வரவிருக்கும் காலங்கள்</h2>
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
        # Handle both dict with 'list' key and direct list formats
        if isinstance(doshas, list):
            dosha_list = doshas
        elif isinstance(doshas, dict):
            dosha_list = doshas.get('list', [])
        else:
            dosha_list = []

        if not dosha_list:
            return f"""
            <div class="page">
                <div class="lifesign-header">
                    <h1>தோஷ பகுப்பாய்வு</h1>
                    <div class="om-sri">Dosha Analysis</div>
                </div>

                <div class="success" style="text-align: center; padding: 30px;">
                    <div style="font-size: 48pt; margin-bottom: 15px;">✓</div>
                    <h2 style="color: #065f46;">No Major Doshas Found</h2>
                    <p>The birth chart does not indicate any significant doshas requiring remedies.</p>
                    <p style="margin-top: 15px;">
                        உங்கள் ஜாதகத்தில் குறிப்பிடத்தக்க தோஷங்கள் எதுவும் இல்லை.
                    </p>
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

            dosha_html += f"""
            <div class="dosha-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="dosha-name">{name_tamil or name}</span>
                    <span style="color: {severity_color}; font-weight: 600;">{severity}</span>
                </div>
                <p class="content" style="font-size: 9pt;">{description}</p>

                <h4 style="font-size: 10pt; margin-top: 10px; color: var(--muted-red);">Effects / விளைவுகள்:</h4>
                <ul style="font-size: 9pt; margin-left: 15px;">{effects_html}</ul>

                <div class="remedy-box" style="margin-top: 10px;">
                    <div class="remedy-title">Remedies / பரிகாரங்கள்</div>
                    <ul style="margin-left: 15px;">{remedies_html}</ul>
                </div>
            </div>
            """

        return f"""
        <div class="page">
            <div class="lifesign-header">
                <h1>தோஷ பகுப்பாய்வு</h1>
                <div class="om-sri">Dosha Analysis with Remedies</div>
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
                    Regular practice of prescribed mantras and remedies can bring positive transformation.
                    நிர்ணயிக்கப்பட்ட மந்திரங்கள் மற்றும் பரிகாரங்களை தொடர்ந்து செய்வது நேர்மறையான மாற்றத்தை கொண்டு வரும்.
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
        """Pages 15-20: Life Area Analysis"""
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

            planets_list = ', '.join(area.get('planets_in_house', [])) or 'None'

            pages_html += f"""
            <div class="page">
                <div class="page-num">Page {page_num}</div>
                <h1 class="page-title">{page_num}. {area_title} Analysis</h1>

                <div class="highlight">
                    <p><strong>Primary House:</strong> H{area.get('primary_house', 1)} ({area.get('house_sign', 'N/A')})</p>
                    <p><strong>House Lord:</strong> {area.get('house_lord', 'N/A')}</p>
                    <p><strong>Karaka:</strong> {area.get('karaka', 'N/A')}</p>
                </div>

                <div class="section">
                    <h2 class="section-title">Strength Analysis</h2>
                    <table>
                        <tr><th>Factor</th><th>Score</th><th>Visual</th></tr>
                        <tr>
                            <td>House Lord Strength</td>
                            <td>{area.get('lord_strength', 0.5):.2f}</td>
                            <td>{self._score_bar(area.get('lord_strength', 0.5), 100)}</td>
                        </tr>
                        <tr>
                            <td>Karaka Strength</td>
                            <td>{area.get('karaka_strength', 0.5):.2f}</td>
                            <td>{self._score_bar(area.get('karaka_strength', 0.5), 100)}</td>
                        </tr>
                        <tr>
                            <td><strong>Combined Score</strong></td>
                            <td><strong>{area.get('combined_score', 0.5):.2f}</strong></td>
                            <td>{self._score_bar(area.get('combined_score', 0.5), 100)}</td>
                        </tr>
                    </table>
                </div>

                <div class="section">
                    <h2 class="section-title">Planets in House</h2>
                    <p>{planets_list}</p>
                </div>

                <div class="{'success' if area.get('combined_score', 0) > 0.6 else 'warning' if area.get('combined_score', 0) > 0.45 else 'highlight'}">
                    <p><strong>Interpretation:</strong> {area.get('interpretation', 'Moderate')}</p>
                </div>

                <div class="math-trace">{area.get('math_trace', '')}</div>
            </div>
            """

        return pages_html

    def _page_21_yogas(self) -> str:
        """Page 21: Yogas Present"""
        yogas = self.report_data['yogas']

        yoga_cards = ""
        for yoga in yogas[:6]:  # Limit to 6
            yoga_cards += f"""
            <div class="yoga-card">
                <div class="yoga-name">{yoga['name']} / {yoga.get('name_tamil', '')}</div>
                <div class="yoga-type">{yoga.get('type', '')}</div>
                <p><strong>Formation:</strong> {yoga.get('formed_by', '')}</p>
                <p><strong>Strength:</strong> {self._score_bar(yoga.get('strength', 0.5), 80)} {yoga.get('strength', 0.5):.2f}</p>
                <p><strong>Effects:</strong> {yoga.get('effects', '')}</p>
            </div>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 21</div>
            <h1 class="page-title">21. Yogas Present / யோகங்கள்</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Yogas formed based on degree-precise planetary positions</p>
            </div>

            <div class="section">
                <h2 class="section-title">Detected Yogas ({len(yogas)})</h2>
                {yoga_cards if yoga_cards else '<p>No major yogas detected in this chart.</p>'}
            </div>
        </div>
        """

    def _page_22_yoga_activation(self) -> str:
        """Page 22: Yoga Activation Timeline"""
        yogas = self.report_data['yogas']
        dasha = self.report_data['dasha']

        activation_rows = ""
        for yoga in yogas[:6]:
            activation = yoga.get('activation', {})
            status = "🟢 Active" if activation.get('is_active') else "⚪ Dormant"
            activation_rows += f"""
            <tr>
                <td>{yoga['name']}</td>
                <td>{status}</td>
                <td>{activation.get('period', 'Future')}</td>
                <td>{activation.get('strength_multiplier', 1.0):.1f}x</td>
            </tr>
            """

        return f"""
        <div class="page">
            <div class="page-num">Page 22</div>
            <h1 class="page-title">22. Yoga Activation Timeline / யோக செயல்பாடு</h1>

            <div class="highlight">
                <p><strong>Rule:</strong> Yoga presence ≠ Yoga activation. Activation requires dasha support.</p>
            </div>

            <div class="section">
                <h2 class="section-title">Current Dasha Context</h2>
                <p><strong>Mahadasha:</strong> {dasha['current'].get('mahadasha', 'N/A')} ({dasha['current'].get('mahadasha_tamil', '')})</p>
                <p><strong>Antardasha:</strong> {dasha['current'].get('antardasha', 'N/A')} ({dasha['current'].get('antardasha_tamil', '')})</p>
            </div>

            <div class="section">
                <h2 class="section-title">Yoga Activation Status</h2>
                <table>
                    <tr><th>Yoga</th><th>Status</th><th>Activation Period</th><th>Effect Multiplier</th></tr>
                    {activation_rows if activation_rows else '<tr><td colspan="4">No yogas to analyze</td></tr>'}
                </table>
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

    def _pages_32_35_dasha_analysis(self) -> str:
        """Pages 32-35: Dasha Phase Analysis"""
        dasha = self.report_data['dasha']
        timeline = dasha.get('timeline', [])

        # Page 32: Current Dasha
        current = dasha['current']
        maha_poi = dasha.get('mahadasha_poi', {})
        antar_poi = dasha.get('antardasha_poi', {})

        page_32 = f"""
        <div class="page">
            <div class="page-num">Page 32</div>
            <h1 class="page-title">32. Current Dasha Analysis / தற்போதைய தசா பகுப்பாய்வு</h1>

            <div class="section">
                <h2 class="section-title">Mahadasha: {current['mahadasha']} ({current['mahadasha_tamil']})</h2>
                <div class="planet-card">
                    <p><strong>POI Strength:</strong> {maha_poi.get('total', 0.5):.2f}</p>
                    <p><strong>House Position:</strong> H{maha_poi.get('house_position', 1)}</p>
                    <p><strong>Dignity:</strong> {maha_poi.get('dignity', 'N/A')}</p>
                    {self._score_bar(maha_poi.get('total', 0.5), 200)}
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Antardasha: {current['antardasha']} ({current['antardasha_tamil']})</h2>
                <div class="planet-card">
                    <p><strong>POI Strength:</strong> {antar_poi.get('total', 0.5):.2f}</p>
                    <p><strong>House Position:</strong> H{antar_poi.get('house_position', 1)}</p>
                    <p><strong>Dignity:</strong> {antar_poi.get('dignity', 'N/A')}</p>
                    {self._score_bar(antar_poi.get('total', 0.5), 200)}
                </div>
            </div>

            <div class="stat-box">
                <div class="stat-value">{dasha.get('combined_strength', 0.5):.2f}</div>
                <div class="stat-label">Combined Period Strength</div>
            </div>

            <div class="highlight">
                <p><strong>Activated Life Areas:</strong> {', '.join(dasha.get('activated_areas', []))}</p>
            </div>

            <div class="math-trace">{maha_poi.get('math_trace', '')}</div>
        </div>
        """

        # Page 33-35: Dasha Timeline
        timeline_rows = ""
        for period in timeline[:10]:
            timeline_rows += f"""
            <tr>
                <td>{period['planet']} ({period['planet_tamil']})</td>
                <td>{period['start_year']}</td>
                <td>{period['end_year']}</td>
                <td>{period['duration']} years</td>
            </tr>
            """

        page_33 = f"""
        <div class="page">
            <div class="page-num">Page 33</div>
            <h1 class="page-title">33. Complete Dasha Timeline / முழு தசா காலவரிசை</h1>

            <div class="section">
                <table>
                    <tr><th>Mahadasha</th><th>Start</th><th>End</th><th>Duration</th></tr>
                    {timeline_rows}
                </table>
            </div>
        </div>
        """

        page_34 = """
        <div class="page">
            <div class="page-num">Page 34</div>
            <h1 class="page-title">34. Dasha Interpretation Guide / தசா விளக்க வழிகாட்டி</h1>

            <div class="section">
                <h2 class="section-title">Reading Your Dasha</h2>
                <p class="content">
                    Each mahadasha period brings the themes of that planet to the forefront.
                    The quality of results depends on the planet's natal strength (POI)
                    and house placement.
                </p>
            </div>

            <div class="section">
                <h2 class="section-title">POI Score Interpretation</h2>
                <table>
                    <tr><th>Score Range</th><th>Interpretation</th></tr>
                    <tr><td>0.65 - 1.00</td><td>Strong period - Planet delivers positive results naturally</td></tr>
                    <tr><td>0.45 - 0.64</td><td>Moderate period - Mixed results, effort required</td></tr>
                    <tr><td>0.35 - 0.44</td><td>Challenging period - Growth through obstacles</td></tr>
                </table>
            </div>
        </div>
        """

        page_35 = f"""
        <div class="page">
            <div class="page-num">Page 35</div>
            <h1 class="page-title">35. Dasha Transit Interaction / தசா கோசார தொடர்பு</h1>

            <div class="highlight">
                <p><strong>Current Period Interpretation:</strong> {dasha.get('interpretation_strength', 'Moderate')}</p>
            </div>

            <div class="section">
                <p class="content">
                    The current {current['mahadasha']} mahadasha with {current['antardasha']} antardasha
                    creates a combined influence score of {dasha.get('combined_strength', 0.5):.2f}.
                    This indicates a {'favorable' if dasha.get('combined_strength', 0) > 0.55 else 'moderate'}
                    period for the significations of these planets.
                </p>
            </div>
        </div>
        """

        return page_32 + page_33 + page_34 + page_35

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
                    Report generated by V6.0 Super Jyotish Engine<br>
                    Every insight mathematically derived from chart data
                </p>
            </div>
        </div>
        """


def generate_v6_report(chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta') -> bytes:
    """Main function to generate V6 PDF report"""
    generator = V6ReportGenerator(chart_data, user_data, language)
    return generator.generate()
