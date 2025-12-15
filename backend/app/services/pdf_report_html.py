"""
HTML-based PDF Report Generator for Tamil Astrology
Uses WeasyPrint for proper Tamil font rendering
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Astrological Constants
RASIS = [
    {'en': 'Aries', 'ta': 'மேஷம்', 'symbol': '♈', 'lord': 'Mars', 'lord_ta': 'செவ்வாய்'},
    {'en': 'Taurus', 'ta': 'ரிஷபம்', 'symbol': '♉', 'lord': 'Venus', 'lord_ta': 'சுக்கிரன்'},
    {'en': 'Gemini', 'ta': 'மிதுனம்', 'symbol': '♊', 'lord': 'Mercury', 'lord_ta': 'புதன்'},
    {'en': 'Cancer', 'ta': 'கடகம்', 'symbol': '♋', 'lord': 'Moon', 'lord_ta': 'சந்திரன்'},
    {'en': 'Leo', 'ta': 'சிம்மம்', 'symbol': '♌', 'lord': 'Sun', 'lord_ta': 'சூரியன்'},
    {'en': 'Virgo', 'ta': 'கன்னி', 'symbol': '♍', 'lord': 'Mercury', 'lord_ta': 'புதன்'},
    {'en': 'Libra', 'ta': 'துலாம்', 'symbol': '♎', 'lord': 'Venus', 'lord_ta': 'சுக்கிரன்'},
    {'en': 'Scorpio', 'ta': 'விருச்சிகம்', 'symbol': '♏', 'lord': 'Mars', 'lord_ta': 'செவ்வாய்'},
    {'en': 'Sagittarius', 'ta': 'தனுசு', 'symbol': '♐', 'lord': 'Jupiter', 'lord_ta': 'குரு'},
    {'en': 'Capricorn', 'ta': 'மகரம்', 'symbol': '♑', 'lord': 'Saturn', 'lord_ta': 'சனி'},
    {'en': 'Aquarius', 'ta': 'கும்பம்', 'symbol': '♒', 'lord': 'Saturn', 'lord_ta': 'சனி'},
    {'en': 'Pisces', 'ta': 'மீனம்', 'symbol': '♓', 'lord': 'Jupiter', 'lord_ta': 'குரு'},
]

NAKSHATRAS = [
    {'en': 'Ashwini', 'ta': 'அசுவினி', 'lord': 'Ketu', 'lord_ta': 'கேது'},
    {'en': 'Bharani', 'ta': 'பரணி', 'lord': 'Venus', 'lord_ta': 'சுக்கிரன்'},
    {'en': 'Krittika', 'ta': 'கார்த்திகை', 'lord': 'Sun', 'lord_ta': 'சூரியன்'},
    {'en': 'Rohini', 'ta': 'ரோகிணி', 'lord': 'Moon', 'lord_ta': 'சந்திரன்'},
    {'en': 'Mrigashira', 'ta': 'மிருகசீரிடம்', 'lord': 'Mars', 'lord_ta': 'செவ்வாய்'},
    {'en': 'Ardra', 'ta': 'திருவாதிரை', 'lord': 'Rahu', 'lord_ta': 'ராகு'},
    {'en': 'Punarvasu', 'ta': 'புனர்பூசம்', 'lord': 'Jupiter', 'lord_ta': 'குரு'},
    {'en': 'Pushya', 'ta': 'பூசம்', 'lord': 'Saturn', 'lord_ta': 'சனி'},
    {'en': 'Ashlesha', 'ta': 'ஆயில்யம்', 'lord': 'Mercury', 'lord_ta': 'புதன்'},
    {'en': 'Magha', 'ta': 'மகம்', 'lord': 'Ketu', 'lord_ta': 'கேது'},
    {'en': 'Purva Phalguni', 'ta': 'பூரம்', 'lord': 'Venus', 'lord_ta': 'சுக்கிரன்'},
    {'en': 'Uttara Phalguni', 'ta': 'உத்திரம்', 'lord': 'Sun', 'lord_ta': 'சூரியன்'},
    {'en': 'Hasta', 'ta': 'அஸ்தம்', 'lord': 'Moon', 'lord_ta': 'சந்திரன்'},
    {'en': 'Chitra', 'ta': 'சித்திரை', 'lord': 'Mars', 'lord_ta': 'செவ்வாய்'},
    {'en': 'Swati', 'ta': 'சுவாதி', 'lord': 'Rahu', 'lord_ta': 'ராகு'},
    {'en': 'Vishakha', 'ta': 'விசாகம்', 'lord': 'Jupiter', 'lord_ta': 'குரு'},
    {'en': 'Anuradha', 'ta': 'அனுஷம்', 'lord': 'Saturn', 'lord_ta': 'சனி'},
    {'en': 'Jyeshtha', 'ta': 'கேட்டை', 'lord': 'Mercury', 'lord_ta': 'புதன்'},
    {'en': 'Mula', 'ta': 'மூலம்', 'lord': 'Ketu', 'lord_ta': 'கேது'},
    {'en': 'Purva Ashadha', 'ta': 'பூராடம்', 'lord': 'Venus', 'lord_ta': 'சுக்கிரன்'},
    {'en': 'Uttara Ashadha', 'ta': 'உத்திராடம்', 'lord': 'Sun', 'lord_ta': 'சூரியன்'},
    {'en': 'Shravana', 'ta': 'திருவோணம்', 'lord': 'Moon', 'lord_ta': 'சந்திரன்'},
    {'en': 'Dhanishta', 'ta': 'அவிட்டம்', 'lord': 'Mars', 'lord_ta': 'செவ்வாய்'},
    {'en': 'Shatabhisha', 'ta': 'சதயம்', 'lord': 'Rahu', 'lord_ta': 'ராகு'},
    {'en': 'Purva Bhadrapada', 'ta': 'பூரட்டாதி', 'lord': 'Jupiter', 'lord_ta': 'குரு'},
    {'en': 'Uttara Bhadrapada', 'ta': 'உத்திரட்டாதி', 'lord': 'Saturn', 'lord_ta': 'சனி'},
    {'en': 'Revati', 'ta': 'ரேவதி', 'lord': 'Mercury', 'lord_ta': 'புதன்'},
]

PLANETS = [
    {'en': 'Sun', 'ta': 'சூரியன்', 'symbol': '☉'},
    {'en': 'Moon', 'ta': 'சந்திரன்', 'symbol': '☽'},
    {'en': 'Mars', 'ta': 'செவ்வாய்', 'symbol': '♂'},
    {'en': 'Mercury', 'ta': 'புதன்', 'symbol': '☿'},
    {'en': 'Jupiter', 'ta': 'குரு', 'symbol': '♃'},
    {'en': 'Venus', 'ta': 'சுக்கிரன்', 'symbol': '♀'},
    {'en': 'Saturn', 'ta': 'சனி', 'symbol': '♄'},
    {'en': 'Rahu', 'ta': 'ராகு', 'symbol': '☊'},
    {'en': 'Ketu', 'ta': 'கேது', 'symbol': '☋'},
]

HOUSES = [
    {'num': 1, 'name': 'Lagna', 'ta': 'லக்னம்', 'signifies': 'Self, personality, physical body'},
    {'num': 2, 'name': 'Dhana', 'ta': 'தன பாவம்', 'signifies': 'Wealth, family, speech'},
    {'num': 3, 'name': 'Sahaja', 'ta': 'சகோதர பாவம்', 'signifies': 'Siblings, courage, communication'},
    {'num': 4, 'name': 'Sukha', 'ta': 'சுக பாவம்', 'signifies': 'Mother, home, happiness'},
    {'num': 5, 'name': 'Putra', 'ta': 'புத்திர பாவம்', 'signifies': 'Children, intelligence, creativity'},
    {'num': 6, 'name': 'Ari', 'ta': 'சத்ரு பாவம்', 'signifies': 'Enemies, diseases, obstacles'},
    {'num': 7, 'name': 'Kalatra', 'ta': 'களத்திர பாவம்', 'signifies': 'Marriage, partnerships'},
    {'num': 8, 'name': 'Ayur', 'ta': 'ஆயுள் பாவம்', 'signifies': 'Longevity, transformation'},
    {'num': 9, 'name': 'Dharma', 'ta': 'தர்ம பாவம்', 'signifies': 'Fortune, spirituality'},
    {'num': 10, 'name': 'Karma', 'ta': 'கர்ம பாவம்', 'signifies': 'Career, profession'},
    {'num': 11, 'name': 'Labha', 'ta': 'லாப பாவம்', 'signifies': 'Income, gains, desires'},
    {'num': 12, 'name': 'Vyaya', 'ta': 'விரய பாவம்', 'signifies': 'Expenses, liberation'},
]

DASHA_PERIODS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

DASHA_TAMIL = {
    'Ketu': 'கேது', 'Venus': 'சுக்கிரன்', 'Sun': 'சூரியன்', 'Moon': 'சந்திரன்',
    'Mars': 'செவ்வாய்', 'Rahu': 'ராகு', 'Jupiter': 'குரு', 'Saturn': 'சனி', 'Mercury': 'புதன்'
}


def get_css_styles() -> str:
    """Return CSS styles for the PDF"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;700&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    @page {
        size: A4;
        margin: 2cm 1.5cm;
        @top-center {
            content: "ஜோதிட AI - Jathagam Report";
            font-family: 'Noto Sans Tamil', sans-serif;
            font-size: 10pt;
            color: #ea580c;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 9pt;
            color: #666;
        }
        @bottom-right {
            content: "www.jothida-ai.com";
            font-size: 8pt;
            color: #999;
        }
    }

    body {
        font-family: 'Noto Sans Tamil', 'Noto Sans', Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }

    .cover-page {
        page-break-after: always;
        text-align: center;
        padding-top: 100px;
    }

    .cover-title {
        font-size: 36pt;
        color: #c2410c;
        margin-bottom: 20px;
        font-weight: bold;
    }

    .cover-subtitle {
        font-size: 24pt;
        color: #ea580c;
        margin-bottom: 40px;
    }

    .cover-name {
        font-size: 28pt;
        color: #9a3412;
        margin: 40px 0;
        padding: 20px;
        border: 3px solid #fed7aa;
        display: inline-block;
    }

    .cover-details {
        font-size: 14pt;
        color: #666;
        margin-top: 30px;
    }

    .cover-details p {
        margin: 10px 0;
    }

    .section-header {
        font-size: 18pt;
        color: #ea580c;
        border-bottom: 2px solid #fed7aa;
        padding-bottom: 8px;
        margin: 30px 0 15px 0;
        page-break-after: avoid;
    }

    .subsection-header {
        font-size: 14pt;
        color: #9a3412;
        margin: 20px 0 10px 0;
        page-break-after: avoid;
    }

    .content {
        text-align: justify;
        margin-bottom: 15px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        page-break-inside: avoid;
    }

    th {
        background-color: #ea580c;
        color: white;
        padding: 10px 8px;
        text-align: center;
        font-weight: bold;
    }

    td {
        padding: 8px;
        border: 1px solid #fed7aa;
        text-align: center;
    }

    tr:nth-child(even) {
        background-color: #fff7ed;
    }

    tr:nth-child(odd) {
        background-color: white;
    }

    .chart-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        border: 2px solid #ea580c;
        margin: 20px auto;
        width: 400px;
    }

    .chart-cell {
        border: 1px solid #ea580c;
        padding: 15px 5px;
        text-align: center;
        background-color: #fff7ed;
        min-height: 80px;
    }

    .chart-cell.center {
        background-color: white;
    }

    .chart-cell .tamil {
        font-size: 12pt;
        color: #9a3412;
        font-weight: bold;
    }

    .chart-cell .english {
        font-size: 9pt;
        color: #666;
    }

    .highlight-box {
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }

    .planet-box {
        background-color: #fef3c7;
        border-left: 4px solid #ea580c;
        padding: 10px 15px;
        margin: 10px 0;
    }

    .planet-name {
        font-weight: bold;
        color: #9a3412;
        font-size: 13pt;
    }

    ul {
        margin: 10px 0 10px 25px;
    }

    li {
        margin: 5px 0;
    }

    .toc {
        page-break-after: always;
    }

    .toc-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px dotted #ccc;
    }

    .page-break {
        page-break-before: always;
    }

    .dasha-timeline {
        margin: 20px 0;
    }

    .dasha-bar {
        display: flex;
        align-items: center;
        margin: 8px 0;
    }

    .dasha-label {
        width: 150px;
        font-weight: bold;
    }

    .dasha-years {
        flex: 1;
        background-color: #fed7aa;
        height: 25px;
        position: relative;
    }

    .remedy-section {
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }

    .remedy-title {
        color: #166534;
        font-weight: bold;
        margin-bottom: 10px;
    }
    """


class HTMLReportGenerator:
    """Generate PDF reports using HTML and WeasyPrint"""

    def __init__(self, chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta'):
        self.chart_data = chart_data
        self.user_data = user_data
        self.language = language

    def generate(self) -> bytes:
        """Generate the PDF report"""
        html_content = self._build_html()

        font_config = FontConfiguration()
        html = HTML(string=html_content)
        css = CSS(string=get_css_styles(), font_config=font_config)

        pdf_buffer = io.BytesIO()
        html.write_pdf(pdf_buffer, stylesheets=[css], font_config=font_config)

        return pdf_buffer.getvalue()

    def _build_html(self) -> str:
        """Build complete HTML document"""
        sections = [
            self._cover_page(),
            self._toc_page(),
            self._birth_details_section(),
            self._rasi_chart_section(),
            self._navamsa_chart_section(),
            self._planet_positions_section(),
            self._house_analysis_section(),
            self._nakshatra_section(),
            self._dasha_section(),
            self._yoga_section(),
            self._dosha_section(),
            self._life_predictions_section(),
            self._career_section(),
            self._marriage_section(),
            self._health_section(),
            self._wealth_section(),
            self._remedies_section(),
            self._favorable_section(),
            self._yearly_predictions_section(),
        ]

        return f"""
        <!DOCTYPE html>
        <html lang="ta">
        <head>
            <meta charset="UTF-8">
            <title>Jathagam Report - {self.user_data.get('name', 'User')}</title>
        </head>
        <body>
            {''.join(sections)}
        </body>
        </html>
        """

    def _cover_page(self) -> str:
        """Generate cover page"""
        name = self.user_data.get('name', 'User')
        birth_date = self.user_data.get('birth_date', 'N/A')
        birth_time = self.user_data.get('birth_time', 'N/A')
        birth_place = self.user_data.get('birth_place', 'N/A')

        moon_rasi = self.chart_data.get('moon_rasi', {})
        rasi_tamil = moon_rasi.get('tamil', 'N/A') if isinstance(moon_rasi, dict) else 'N/A'

        nakshatra = self.chart_data.get('nakshatra', {})
        nak_tamil = nakshatra.get('tamil', 'N/A') if isinstance(nakshatra, dict) else 'N/A'
        nak_pada = nakshatra.get('pada', 1) if isinstance(nakshatra, dict) else 1

        return f"""
        <div class="cover-page">
            <div class="cover-title">ஜாதகம்</div>
            <div class="cover-subtitle">Jathagam Report / ஜாதக அறிக்கை</div>

            <div class="cover-name">{name}</div>

            <div class="cover-details">
                <p><strong>பிறந்த தேதி / Date of Birth:</strong> {birth_date}</p>
                <p><strong>பிறந்த நேரம் / Time of Birth:</strong> {birth_time}</p>
                <p><strong>பிறந்த இடம் / Place of Birth:</strong> {birth_place}</p>
                <p><strong>ராசி / Moon Sign:</strong> {rasi_tamil}</p>
                <p><strong>நட்சத்திரம் / Nakshatra:</strong> {nak_tamil} - பாதம் {nak_pada}</p>
            </div>

            <div style="margin-top: 60px; color: #999;">
                <p>Generated by ஜோதிட AI</p>
                <p>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </div>
        """

    def _toc_page(self) -> str:
        """Generate table of contents"""
        toc_items = [
            ("1. Birth Details / பிறப்பு விவரங்கள்", "3"),
            ("2. Rasi Chart / ராசி கட்டம்", "4"),
            ("3. Navamsa Chart / நவாம்சம்", "5"),
            ("4. Planet Positions / கிரக நிலைகள்", "6"),
            ("5. House Analysis / பாவ பலன்கள்", "8"),
            ("6. Nakshatra Analysis / நட்சத்திர பலன்", "12"),
            ("7. Dasha Periods / தசா புத்தி", "14"),
            ("8. Yogas / யோகங்கள்", "17"),
            ("9. Doshas / தோஷங்கள்", "19"),
            ("10. Life Predictions / வாழ்க்கை பலன்கள்", "21"),
            ("11. Career / தொழில்", "24"),
            ("12. Marriage / திருமணம்", "27"),
            ("13. Health / ஆரோக்கியம்", "29"),
            ("14. Wealth / செல்வம்", "31"),
            ("15. Remedies / பரிகாரங்கள்", "33"),
            ("16. Favorable Periods / சுப காலங்கள்", "36"),
            ("17. Yearly Predictions / வருட பலன்கள்", "38"),
        ]

        items_html = ""
        for title, page in toc_items:
            items_html += f'<div class="toc-item"><span>{title}</span><span>{page}</span></div>'

        return f"""
        <div class="toc">
            <h1 class="section-header" style="text-align: center;">Table of Contents / உள்ளடக்கம்</h1>
            {items_html}
        </div>
        """

    def _birth_details_section(self) -> str:
        """Generate birth details section"""
        name = self.user_data.get('name', 'N/A')
        birth_date = self.user_data.get('birth_date', 'N/A')
        birth_time = self.user_data.get('birth_time', 'N/A')
        birth_place = self.user_data.get('birth_place', 'N/A')
        latitude = self.user_data.get('latitude', 'N/A')
        longitude = self.user_data.get('longitude', 'N/A')

        moon_rasi = self.chart_data.get('moon_rasi', {})
        rasi_tamil = moon_rasi.get('tamil', 'N/A') if isinstance(moon_rasi, dict) else 'N/A'
        rasi_en = moon_rasi.get('name', '') if isinstance(moon_rasi, dict) else ''

        nakshatra = self.chart_data.get('nakshatra', {})
        nak_tamil = nakshatra.get('tamil', 'N/A') if isinstance(nakshatra, dict) else 'N/A'
        nak_en = nakshatra.get('name', '') if isinstance(nakshatra, dict) else ''
        nak_pada = nakshatra.get('pada', 1) if isinstance(nakshatra, dict) else 1

        current_dasha = self.chart_data.get('current_dasha', {})
        maha_tamil = current_dasha.get('mahadasha_tamil', 'N/A') if isinstance(current_dasha, dict) else 'N/A'

        return f"""
        <div class="page-break">
            <h1 class="section-header">1. Birth Details / பிறப்பு விவரங்கள்</h1>

            <table>
                <tr>
                    <th>Detail / விவரம்</th>
                    <th>Value / மதிப்பு</th>
                    <th>Tamil / தமிழ்</th>
                </tr>
                <tr>
                    <td>Name</td>
                    <td>{name}</td>
                    <td>பெயர்</td>
                </tr>
                <tr>
                    <td>Date of Birth</td>
                    <td>{birth_date}</td>
                    <td>பிறந்த தேதி</td>
                </tr>
                <tr>
                    <td>Time of Birth</td>
                    <td>{birth_time}</td>
                    <td>பிறந்த நேரம்</td>
                </tr>
                <tr>
                    <td>Place of Birth</td>
                    <td>{birth_place}</td>
                    <td>பிறந்த இடம்</td>
                </tr>
                <tr>
                    <td>Latitude</td>
                    <td>{latitude}</td>
                    <td>அட்சரேகை</td>
                </tr>
                <tr>
                    <td>Longitude</td>
                    <td>{longitude}</td>
                    <td>தீர்க்கரேகை</td>
                </tr>
            </table>

            <h2 class="subsection-header">1.1 Astrological Summary / ஜோதிட சுருக்கம்</h2>

            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Moon Sign / ராசி</td>
                    <td>{rasi_tamil} ({rasi_en})</td>
                </tr>
                <tr>
                    <td>Nakshatra / நட்சத்திரம்</td>
                    <td>{nak_tamil} ({nak_en}) - Pada {nak_pada}</td>
                </tr>
                <tr>
                    <td>Current Mahadasha / தற்போதைய மகாதசை</td>
                    <td>{maha_tamil}</td>
                </tr>
                <tr>
                    <td>Ayanamsa</td>
                    <td>Lahiri (Chitrapaksha)</td>
                </tr>
            </table>
        </div>
        """

    def _rasi_chart_section(self) -> str:
        """Generate Rasi chart section"""
        # South Indian style chart grid
        chart_positions = [
            ('மீனம்', 'Pisces'), ('மேஷம்', 'Aries'), ('ரிஷபம்', 'Taurus'), ('மிதுனம்', 'Gemini'),
            ('கும்பம்', 'Aquarius'), ('', ''), ('', ''), ('கடகம்', 'Cancer'),
            ('மகரம்', 'Capricorn'), ('', ''), ('', ''), ('சிம்மம்', 'Leo'),
            ('தனுசு', 'Sagittarius'), ('விருச்சிகம்', 'Scorpio'), ('துலாம்', 'Libra'), ('கன்னி', 'Virgo'),
        ]

        cells_html = ""
        for i, (tamil, english) in enumerate(chart_positions):
            is_center = i in [5, 6, 9, 10]
            cell_class = "chart-cell center" if is_center else "chart-cell"
            if tamil:
                cells_html += f'''
                <div class="{cell_class}">
                    <div class="tamil">{tamil}</div>
                    <div class="english">{english}</div>
                </div>
                '''
            else:
                cells_html += f'<div class="{cell_class}"></div>'

        return f"""
        <div class="page-break">
            <h1 class="section-header">2. Rasi Chart / ராசி கட்டம்</h1>

            <p class="content">
                The Rasi chart (also known as the birth chart or natal chart) is the primary chart in Vedic astrology.
                It shows the positions of all planets at the exact moment of your birth. The chart is divided into 12 houses,
                each representing different aspects of life.
            </p>

            <h2 class="subsection-header">2.1 South Indian Style Chart / தென்னிந்திய முறை</h2>

            <div class="chart-grid">
                {cells_html}
            </div>

            <div class="highlight-box">
                <p><strong>How to Read:</strong> In the South Indian format, the 12 zodiac signs are fixed in their positions.
                Planets are placed in the sign they occupy at birth. The Lagna (Ascendant) is marked to identify the first house.
                Reading starts from Lagna and proceeds clockwise.</p>
            </div>
        </div>
        """

    def _navamsa_chart_section(self) -> str:
        """Generate Navamsa chart section"""
        chart_positions = [
            ('மீனம்', 'Pisces'), ('மேஷம்', 'Aries'), ('ரிஷபம்', 'Taurus'), ('மிதுனம்', 'Gemini'),
            ('கும்பம்', 'Aquarius'), ('', ''), ('', ''), ('கடகம்', 'Cancer'),
            ('மகரம்', 'Capricorn'), ('', ''), ('', ''), ('சிம்மம்', 'Leo'),
            ('தனுசு', 'Sagittarius'), ('விருச்சிகம்', 'Scorpio'), ('துலாம்', 'Libra'), ('கன்னி', 'Virgo'),
        ]

        cells_html = ""
        for i, (tamil, english) in enumerate(chart_positions):
            is_center = i in [5, 6, 9, 10]
            cell_class = "chart-cell center" if is_center else "chart-cell"
            if tamil:
                cells_html += f'''
                <div class="{cell_class}">
                    <div class="tamil">{tamil}</div>
                    <div class="english">{english}</div>
                </div>
                '''
            else:
                cells_html += f'<div class="{cell_class}"></div>'

        return f"""
        <div class="page-break">
            <h1 class="section-header">3. Navamsa Chart / நவாம்சம்</h1>

            <p class="content">
                The Navamsa (D-9) chart is the most important divisional chart in Vedic astrology.
                It is derived by dividing each sign into 9 equal parts of 3°20' each.
                This chart is primarily used for analyzing marriage, dharma, and the strength of planets.
            </p>

            <h2 class="subsection-header">3.1 Navamsa Chart / நவாம்ச கட்டம்</h2>

            <div class="chart-grid" style="border-color: #9a3412;">
                {cells_html}
            </div>

            <h2 class="subsection-header">3.2 Significance / முக்கியத்துவம்</h2>

            <ul>
                <li>The strength and dignity of planets (Vargottama planets gain extra strength)</li>
                <li>Marriage and spouse characteristics</li>
                <li>Spiritual inclinations and dharmic path</li>
                <li>The fruit of your actions (Karma Phala)</li>
                <li>Hidden strengths and weaknesses of planets</li>
            </ul>
        </div>
        """

    def _planet_positions_section(self) -> str:
        """Generate planet positions section"""
        planets_data = self.chart_data.get('planets', {})

        # Convert list to dict if needed (backend returns list format)
        if isinstance(planets_data, list):
            planets_dict = {}
            for p in planets_data:
                if isinstance(p, dict) and 'planet' in p:
                    planets_dict[p['planet']] = p
            planets_data = planets_dict

        rows_html = ""
        for planet in PLANETS:
            p_data = planets_data.get(planet['en'], {}) if isinstance(planets_data, dict) else {}
            sign = p_data.get('sign', p_data.get('rasi', 'Leo'))
            house = p_data.get('house', p_data.get('house_num', 1))
            degree = p_data.get('degree', p_data.get('longitude', 0))
            nakshatra = p_data.get('nakshatra', 'Ashwini')

            rows_html += f"""
            <tr>
                <td><strong>{planet['en']}</strong> ({planet['ta']})</td>
                <td>{sign}</td>
                <td>{house}</td>
                <td>{degree:.2f}°</td>
                <td>{nakshatra}</td>
            </tr>
            """

        return f"""
        <div class="page-break">
            <h1 class="section-header">4. Planet Positions / கிரக நிலைகள்</h1>

            <p class="content">
                The positions of the nine planets (Navagrahas) at the time of birth determine various aspects of life.
                Each planet has specific significations and its placement in signs and houses creates unique effects.
            </p>

            <table>
                <tr>
                    <th>Planet / கிரகம்</th>
                    <th>Sign / ராசி</th>
                    <th>House</th>
                    <th>Degree</th>
                    <th>Nakshatra</th>
                </tr>
                {rows_html}
            </table>

            <h2 class="subsection-header">4.1 Planet Significations / கிரக காரகத்துவங்கள்</h2>

            <div class="planet-box">
                <div class="planet-name">☉ Sun / சூரியன்</div>
                <p>Soul, father, authority, government, vitality, and self-expression. Its placement influences ego, willpower, and leadership.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">☽ Moon / சந்திரன்</div>
                <p>Mind, mother, emotions, nurturing, and public image. Its placement affects emotional nature and mental peace.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">♂ Mars / செவ்வாய்</div>
                <p>Energy, courage, siblings, property, and aggression. Its placement determines drive and physical strength.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">☿ Mercury / புதன்</div>
                <p>Intellect, communication, commerce, and analytical abilities. Its placement influences thinking and speech.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">♃ Jupiter / குரு</div>
                <p>Wisdom, fortune, spirituality, children, and expansion. Its placement affects luck and higher education.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">♀ Venus / சுக்கிரன்</div>
                <p>Love, marriage, beauty, luxury, and artistic talents. Its placement determines romantic life and comforts.</p>
            </div>

            <div class="planet-box">
                <div class="planet-name">♄ Saturn / சனி</div>
                <p>Karma, discipline, delays, longevity, and hardship. Its placement indicates areas requiring patience.</p>
            </div>
        </div>
        """

    def _house_analysis_section(self) -> str:
        """Generate house analysis section"""
        rows_html = ""
        for house in HOUSES:
            rows_html += f"""
            <tr>
                <td><strong>{house['num']}</strong></td>
                <td>{house['name']} ({house['ta']})</td>
                <td>{house['signifies']}</td>
            </tr>
            """

        return f"""
        <div class="page-break">
            <h1 class="section-header">5. House Analysis / பாவ பலன்கள்</h1>

            <p class="content">
                The 12 houses (Bhavas) of the horoscope represent different areas of life.
                Each house is governed by a sign and influenced by the planets placed in it.
            </p>

            <table>
                <tr>
                    <th>#</th>
                    <th>House Name / பாவம்</th>
                    <th>Significations / காரகத்துவங்கள்</th>
                </tr>
                {rows_html}
            </table>

            <h2 class="subsection-header">5.1 House Classifications / பாவ வகைகள்</h2>

            <div class="highlight-box">
                <p><strong>Kendra Houses (Angular) - 1, 4, 7, 10:</strong> Most powerful houses, planets here gain strength.</p>
                <p><strong>Trikona Houses (Trine) - 1, 5, 9:</strong> Most auspicious houses for fortune and dharma.</p>
                <p><strong>Dusthana Houses - 6, 8, 12:</strong> Challenging houses, but can give hidden benefits.</p>
                <p><strong>Upachaya Houses - 3, 6, 10, 11:</strong> Houses of growth, malefics do well here.</p>
            </div>
        </div>
        """

    def _nakshatra_section(self) -> str:
        """Generate nakshatra section"""
        nakshatra = self.chart_data.get('nakshatra', {})
        nak_tamil = nakshatra.get('tamil', 'அசுவினி') if isinstance(nakshatra, dict) else 'அசுவினி'
        nak_en = nakshatra.get('name', 'Ashwini') if isinstance(nakshatra, dict) else 'Ashwini'
        nak_pada = nakshatra.get('pada', 1) if isinstance(nakshatra, dict) else 1

        rows_html = ""
        for i, nak in enumerate(NAKSHATRAS, 1):
            rows_html += f"""
            <tr>
                <td>{i}</td>
                <td>{nak['en']}</td>
                <td>{nak['ta']}</td>
                <td>{nak['lord_ta']}</td>
            </tr>
            """

        return f"""
        <div class="page-break">
            <h1 class="section-header">6. Nakshatra Analysis / நட்சத்திர பலன்</h1>

            <p class="content">
                Nakshatras are the 27 lunar mansions in Vedic astrology. Your birth nakshatra is determined by
                the Moon's position and reveals deep personality traits and life patterns.
            </p>

            <div class="highlight-box">
                <p><strong>Your Nakshatra:</strong> {nak_tamil} ({nak_en})</p>
                <p><strong>Pada:</strong> {nak_pada}</p>
            </div>

            <h2 class="subsection-header">6.1 Personality Traits / ஆளுமை பண்புகள்</h2>

            <ul>
                <li>Quick-witted and intelligent with good decision-making abilities</li>
                <li>Natural healing abilities and interest in medicine</li>
                <li>Adventurous spirit with love for travel and exploration</li>
                <li>Independent nature with leadership qualities</li>
                <li>Honest and straightforward in dealings</li>
            </ul>

        </div>

        <div class="page-break">
            <h2 class="subsection-header">6.2 Complete Nakshatra Reference / முழு நட்சத்திர பட்டியல்</h2>

            <table style="font-size: 9pt;">
                <tr>
                    <th>#</th>
                    <th>English</th>
                    <th>Tamil / தமிழ்</th>
                    <th>Lord / அதிபதி</th>
                </tr>
                {rows_html}
            </table>
        </div>
        """

    def _dasha_section(self) -> str:
        """Generate dasha section"""
        current_dasha = self.chart_data.get('current_dasha', {})
        maha = current_dasha.get('mahadasha', 'Jupiter') if isinstance(current_dasha, dict) else 'Jupiter'
        maha_tamil = current_dasha.get('mahadasha_tamil', 'குரு') if isinstance(current_dasha, dict) else 'குரு'
        antar = current_dasha.get('antardasha', 'Venus') if isinstance(current_dasha, dict) else 'Venus'
        antar_tamil = current_dasha.get('antardasha_tamil', 'சுக்கிரன்') if isinstance(current_dasha, dict) else 'சுக்கிரன்'

        # Generate dasha timeline
        birth_year = 1990
        try:
            birth_date_str = self.user_data.get('birth_date', '1990-01-01')
            birth_year = int(birth_date_str.split('-')[0])
        except:
            pass

        dasha_order = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

        timeline_rows = ""
        current_year = birth_year
        for dasha in dasha_order:
            duration = DASHA_PERIODS[dasha]
            end_year = current_year + duration
            tamil = DASHA_TAMIL[dasha]
            timeline_rows += f"""
            <tr>
                <td>{dasha} ({tamil})</td>
                <td>{current_year}</td>
                <td>{end_year}</td>
                <td>{duration} years</td>
            </tr>
            """
            current_year = end_year

        return f"""
        <div class="page-break">
            <h1 class="section-header">7. Dasha Periods / தசா புத்தி</h1>

            <p class="content">
                The Vimshottari Dasha system is the most widely used planetary period system in Vedic astrology.
                It spans 120 years and divides life into planetary periods ruled by different planets.
            </p>

            <h2 class="subsection-header">7.1 Current Dasha / தற்போதைய தசை</h2>

            <table>
                <tr>
                    <th>Period Type</th>
                    <th>Planet / கிரகம்</th>
                    <th>Duration</th>
                </tr>
                <tr>
                    <td>Mahadasha (Major)</td>
                    <td>{maha} ({maha_tamil})</td>
                    <td>{DASHA_PERIODS.get(maha, 16)} years</td>
                </tr>
                <tr>
                    <td>Antardasha (Sub)</td>
                    <td>{antar} ({antar_tamil})</td>
                    <td>Varies</td>
                </tr>
            </table>

            <h2 class="subsection-header">7.2 Complete Dasha Timeline / முழு தசா காலவரிசை</h2>

            <table>
                <tr>
                    <th>Mahadasha</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Duration</th>
                </tr>
                {timeline_rows}
            </table>
        </div>
        """

    def _yoga_section(self) -> str:
        """Generate yoga section"""
        return """
        <div class="page-break">
            <h1 class="section-header">8. Yogas / யோகங்கள்</h1>

            <p class="content">
                Yogas are special planetary combinations that produce specific results.
                They can be benefic (Raja Yogas) or challenging (Daridra Yogas).
            </p>

            <h2 class="subsection-header">8.1 Benefic Yogas / சுப யோகங்கள்</h2>

            <div class="highlight-box">
                <p><strong>Gajakesari Yoga:</strong> Jupiter in Kendra from Moon. Brings fame, wealth, and wisdom.</p>
            </div>

            <div class="highlight-box">
                <p><strong>Budhaditya Yoga:</strong> Sun and Mercury conjunction. Excellent for intelligence and communication.</p>
            </div>

            <div class="highlight-box">
                <p><strong>Chandra-Mangala Yoga:</strong> Moon and Mars conjunction. Provides wealth through self-effort.</p>
            </div>

            <h2 class="subsection-header">8.2 Raja Yogas / ராஜ யோகங்கள்</h2>

            <p class="content">
                Raja Yogas are formed when lords of Kendra and Trikona houses are connected.
                These yogas bestow power, position, and prosperity.
            </p>

            <ul>
                <li><strong>Dharma-Karmadhipati Yoga:</strong> 9th and 10th lord connection - Success in profession</li>
                <li><strong>Lakshmi Yoga:</strong> Venus in own/exalted sign in Kendra - Wealth and luxury</li>
                <li><strong>Saraswati Yoga:</strong> Jupiter, Venus, Mercury in Kendra/Trikona - Learning and arts</li>
            </ul>
        </div>
        """

    def _dosha_section(self) -> str:
        """Generate dosha section"""
        return """
        <div class="page-break">
            <h1 class="section-header">9. Doshas / தோஷங்கள்</h1>

            <p class="content">
                Doshas are afflictions in the birth chart that may create challenges in specific life areas.
                Understanding doshas helps in taking remedial measures.
            </p>

            <h2 class="subsection-header">9.1 Mangal Dosha / செவ்வாய் தோஷம்</h2>

            <div class="highlight-box">
                <p><strong>Definition:</strong> Mars in 1st, 4th, 7th, 8th, or 12th house from Lagna, Moon, or Venus.</p>
                <p><strong>Effects:</strong> May cause delays or challenges in marriage.</p>
                <p><strong>Remedies:</strong> Mangal Shanti puja, wearing Red Coral after consultation, marrying after 28 years.</p>
            </div>

            <h2 class="subsection-header">9.2 Kaal Sarpa Dosha / கால சர்ப தோஷம்</h2>

            <div class="highlight-box">
                <p><strong>Definition:</strong> All planets hemmed between Rahu and Ketu.</p>
                <p><strong>Effects:</strong> Struggles and obstacles in various life areas.</p>
                <p><strong>Remedies:</strong> Rahu-Ketu Shanti, Naag Puja, visiting Kaal Sarpa temples.</p>
            </div>

            <h2 class="subsection-header">9.3 Pitra Dosha / பித்ரு தோஷம்</h2>

            <div class="highlight-box">
                <p><strong>Definition:</strong> Sun afflicted by Rahu/Ketu, or 9th house affliction.</p>
                <p><strong>Effects:</strong> Ancestral karma affecting current life.</p>
                <p><strong>Remedies:</strong> Shraddha ceremonies, Tarpan, serving elderly.</p>
            </div>
        </div>
        """

    def _life_predictions_section(self) -> str:
        """Generate life predictions section"""
        return """
        <div class="page-break">
            <h1 class="section-header">10. Life Predictions / வாழ்க்கை பலன்கள்</h1>

            <p class="content">
                Based on the comprehensive analysis of your birth chart, the following life predictions
                are derived. These are general indications that may manifest differently based on
                current planetary transits and personal karma.
            </p>

            <h2 class="subsection-header">10.1 Personality & Character / ஆளுமை</h2>
            <p class="content">
                You possess a dynamic personality with natural leadership abilities. Your intellectual capacity
                is strong, and you have good analytical skills. There's an inherent desire to achieve something
                significant in life. You are generally honest and straightforward in your dealings.
            </p>

            <h2 class="subsection-header">10.2 Education & Learning / கல்வி</h2>
            <p class="content">
                Your chart indicates good potential for education, especially in analytical and technical subjects.
                Higher education is favored, and you may pursue multiple degrees or certifications.
                Research work and specialized studies are indicated.
            </p>

            <h2 class="subsection-header">10.3 Family Life / குடும்ப வாழ்க்கை</h2>
            <p class="content">
                Family relationships will be generally harmonious. You may take significant responsibilities
                for family members. The relationship with mother is particularly strong and nurturing.
                Property matters through family channels look favorable.
            </p>

            <h2 class="subsection-header">10.4 Social Life / சமூக வாழ்க்கை</h2>
            <p class="content">
                You will have a good social circle with influential friends. Your networking abilities
                will help in career advancement. Social recognition is indicated, especially in later years.
            </p>
        </div>
        """

    def _career_section(self) -> str:
        """Generate career section"""
        return """
        <div class="page-break">
            <h1 class="section-header">11. Career & Profession / தொழில்</h1>

            <p class="content">
                Career analysis is based on the 10th house (Karma Bhava), its lord, planets in the 10th house,
                and aspects to it. The 2nd, 6th, and 11th houses are also considered for comprehensive career prediction.
            </p>

            <h2 class="subsection-header">11.1 Suitable Professions / பொருத்தமான தொழில்கள்</h2>

            <table>
                <tr>
                    <th>Field / துறை</th>
                    <th>Suitability</th>
                    <th>Remarks</th>
                </tr>
                <tr>
                    <td>IT & Technology</td>
                    <td>Highly Suitable</td>
                    <td>Mercury's influence supports technical work</td>
                </tr>
                <tr>
                    <td>Finance & Banking</td>
                    <td>Suitable</td>
                    <td>Saturn's placement supports systematic work</td>
                </tr>
                <tr>
                    <td>Teaching & Academia</td>
                    <td>Highly Suitable</td>
                    <td>Jupiter's aspect favors knowledge sharing</td>
                </tr>
                <tr>
                    <td>Government Service</td>
                    <td>Suitable</td>
                    <td>Sun's placement indicates authority positions</td>
                </tr>
                <tr>
                    <td>Business & Commerce</td>
                    <td>Moderately Suitable</td>
                    <td>Mercury supports trade activities</td>
                </tr>
                <tr>
                    <td>Healthcare</td>
                    <td>Suitable</td>
                    <td>Sun and Moon combination supports healing</td>
                </tr>
            </table>

            <h2 class="subsection-header">11.2 Career Timeline / தொழில் காலவரிசை</h2>

            <ul>
                <li><strong>Age 21-28:</strong> Foundation building period. Focus on skill development.</li>
                <li><strong>Age 28-35:</strong> Career growth phase. Promotions and recognition likely.</li>
                <li><strong>Age 35-45:</strong> Peak career period. Leadership roles indicated.</li>
                <li><strong>Age 45+:</strong> Consolidation and mentoring phase.</li>
            </ul>
        </div>
        """

    def _marriage_section(self) -> str:
        """Generate marriage section"""
        return """
        <div class="page-break">
            <h1 class="section-header">12. Marriage & Relationships / திருமணம்</h1>

            <p class="content">
                Marriage analysis is based on the 7th house, Venus, Jupiter (for females), Mars (for males),
                and the Navamsa chart. The timing of marriage is determined by Dasha periods.
            </p>

            <h2 class="subsection-header">12.1 Marriage Prospects / திருமண வாய்ப்புகள்</h2>

            <div class="highlight-box">
                <p><strong>Favorable Age for Marriage:</strong> 25-30 years</p>
                <p><strong>Spouse Characteristics:</strong> Educated, family-oriented, supportive nature</p>
                <p><strong>Marriage Direction:</strong> East or North direction indicated</p>
            </div>

            <h2 class="subsection-header">12.2 Compatibility Factors / பொருத்த அம்சங்கள்</h2>

            <table>
                <tr>
                    <th>Factor / அம்சம்</th>
                    <th>Importance</th>
                    <th>Recommendation</th>
                </tr>
                <tr>
                    <td>Nakshatra Match</td>
                    <td>High</td>
                    <td>Check 10 poruthams</td>
                </tr>
                <tr>
                    <td>Mangal Dosha</td>
                    <td>Medium</td>
                    <td>Match with similar dosha</td>
                </tr>
                <tr>
                    <td>Dasha Compatibility</td>
                    <td>High</td>
                    <td>Favorable dashas for both</td>
                </tr>
            </table>

            <h2 class="subsection-header">12.3 Married Life / திருமண வாழ்க்கை</h2>

            <p class="content">
                Overall harmonious married life is indicated. There may be initial adjustments,
                but understanding grows with time. Children are indicated, bringing joy to the family.
                Spouse will be supportive of career and personal growth.
            </p>
        </div>
        """

    def _health_section(self) -> str:
        """Generate health section"""
        return """
        <div class="page-break">
            <h1 class="section-header">13. Health Analysis / ஆரோக்கியம்</h1>

            <p class="content">
                Health analysis is derived from the 1st house (body), 6th house (diseases), 8th house (longevity),
                and the positions of Sun (vitality) and Moon (mental health).
            </p>

            <h2 class="subsection-header">13.1 General Health / பொது ஆரோக்கியம்</h2>

            <div class="highlight-box">
                <p><strong>Constitution:</strong> Generally robust constitution with good vitality.</p>
                <p><strong>Strong Areas:</strong> Digestive system, bones, overall immunity.</p>
                <p><strong>Areas of Attention:</strong> Stress management, eye care, respiratory system.</p>
            </div>

            <h2 class="subsection-header">13.2 Health Recommendations / ஆரோக்கிய பரிந்துரைகள்</h2>

            <ul>
                <li>Practice yoga and pranayama regularly for stress management</li>
                <li>Maintain regular sleep patterns for mental well-being</li>
                <li>Include cooling foods in diet during summer months</li>
                <li>Regular eye check-ups recommended after age 35</li>
                <li>Moderate exercise routine suitable for your body type</li>
            </ul>

            <h2 class="subsection-header">13.3 Favorable Health Periods</h2>

            <p class="content">
                Jupiter and Venus periods are generally favorable for health. Saturn periods may require
                extra attention to bone health and chronic conditions. Rahu periods suggest caution
                with mysterious ailments and mental stress.
            </p>
        </div>
        """

    def _wealth_section(self) -> str:
        """Generate wealth section"""
        return """
        <div class="page-break">
            <h1 class="section-header">14. Wealth & Finance / செல்வம்</h1>

            <p class="content">
                Financial prospects are analyzed through the 2nd house (accumulated wealth), 11th house (gains),
                and the positions of Jupiter (fortune) and Venus (luxury).
            </p>

            <h2 class="subsection-header">14.1 Financial Prospects / நிதி வாய்ப்புகள்</h2>

            <div class="highlight-box">
                <p><strong>Wealth Potential:</strong> Above average wealth accumulation indicated.</p>
                <p><strong>Primary Sources:</strong> Salary/profession, investments, family inheritance.</p>
                <p><strong>Peak Earning Period:</strong> Age 35-50 years.</p>
            </div>

            <h2 class="subsection-header">14.2 Investment Guidance / முதலீட்டு வழிகாட்டுதல்</h2>

            <table>
                <tr>
                    <th>Investment Type</th>
                    <th>Suitability</th>
                    <th>Best Period</th>
                </tr>
                <tr>
                    <td>Real Estate</td>
                    <td>Highly Favorable</td>
                    <td>Saturn periods</td>
                </tr>
                <tr>
                    <td>Gold & Jewelry</td>
                    <td>Favorable</td>
                    <td>Jupiter/Venus periods</td>
                </tr>
                <tr>
                    <td>Stock Market</td>
                    <td>Moderate</td>
                    <td>Mercury periods</td>
                </tr>
                <tr>
                    <td>Fixed Deposits</td>
                    <td>Safe Choice</td>
                    <td>All periods</td>
                </tr>
            </table>

            <h2 class="subsection-header">14.3 Financial Cautions</h2>

            <ul>
                <li>Avoid speculative investments during Rahu/Ketu periods</li>
                <li>Maintain emergency funds for Saturn transit periods</li>
                <li>Review financial plans during major planetary transits</li>
            </ul>
        </div>
        """

    def _remedies_section(self) -> str:
        """Generate remedies section"""
        remedies_html = ""

        planet_remedies = [
            ('Sun / சூரியன்', [
                'Offer water to Sun at sunrise (Surya Arghya)',
                'Recite Aditya Hridayam on Sundays',
                'Wear Ruby (Manikya) after consultation',
                'Donate wheat, jaggery, and red clothes on Sundays'
            ]),
            ('Moon / சந்திரன்', [
                'Wear Pearl (Moti) after consultation',
                'Recite Chandra Kavacham on Mondays',
                'Offer milk to Shiva Lingam on Mondays',
                'Serve mother and elderly women'
            ]),
            ('Mars / செவ்வாய்', [
                'Recite Mangal mantra on Tuesdays',
                'Wear Red Coral (Moonga) after consultation',
                'Donate red lentils and red clothes on Tuesdays',
                'Perform Mangal Shanti puja if Mangal Dosha exists'
            ]),
            ('Mercury / புதன்', [
                'Recite Budha mantra on Wednesdays',
                'Wear Emerald (Panna) after consultation',
                'Donate green clothes and moong dal on Wednesdays',
                'Feed green vegetables to cows'
            ]),
            ('Jupiter / குரு', [
                'Recite Guru mantra on Thursdays',
                'Wear Yellow Sapphire (Pukhraj) after consultation',
                'Donate yellow clothes, turmeric, and books on Thursdays',
                'Respect teachers and elders'
            ]),
            ('Venus / சுக்கிரன்', [
                'Recite Shukra mantra on Fridays',
                'Wear Diamond or White Sapphire after consultation',
                'Donate white clothes, rice, and sugar on Fridays',
                'Respect women and artists'
            ]),
            ('Saturn / சனி', [
                'Recite Shani mantra on Saturdays',
                'Wear Blue Sapphire only after careful consultation',
                'Donate black sesame, mustard oil, and iron on Saturdays',
                'Serve the poor and disabled'
            ]),
        ]

        for planet, remedies in planet_remedies:
            items = ''.join([f'<li>{r}</li>' for r in remedies])
            remedies_html += f"""
            <div class="remedy-section">
                <div class="remedy-title">{planet}</div>
                <ul>{items}</ul>
            </div>
            """

        return f"""
        <div class="page-break">
            <h1 class="section-header">15. Remedies / பரிகாரங்கள்</h1>

            <p class="content">
                Vedic astrology prescribes various remedies to strengthen weak planets and reduce malefic effects.
                These remedies include mantras, gemstones, charity, and rituals.
            </p>

            <h2 class="subsection-header">15.1 Planet-wise Remedies / கிரக பரிகாரங்கள்</h2>

            {remedies_html}

            <h2 class="subsection-header">15.2 General Remedies / பொது பரிகாரங்கள்</h2>

            <ul>
                <li>Recite Navagraha Stotram daily for overall planetary blessings</li>
                <li>Light a lamp (deepam) in the evening facing east</li>
                <li>Feed birds and animals regularly as an act of compassion</li>
                <li>Donate according to your capacity on auspicious days</li>
                <li>Visit temples on your nakshatra day every month</li>
                <li>Practice meditation and maintain positive thoughts</li>
            </ul>
        </div>
        """

    def _favorable_section(self) -> str:
        """Generate favorable periods section"""
        return """
        <div class="page-break">
            <h1 class="section-header">16. Favorable Periods / சுப காலங்கள்</h1>

            <p class="content">
                This section identifies favorable periods for various activities based on your planetary periods
                and transits. Planning important activities during favorable times increases success probability.
            </p>

            <h2 class="subsection-header">16.1 Activity-wise Favorable Periods</h2>

            <table>
                <tr>
                    <th>Activity / செயல்</th>
                    <th>Favorable Periods</th>
                    <th>Best Days</th>
                </tr>
                <tr>
                    <td>Career Change</td>
                    <td>Jupiter/Venus periods</td>
                    <td>Thursday, Friday</td>
                </tr>
                <tr>
                    <td>Starting Business</td>
                    <td>Sun/Jupiter periods</td>
                    <td>Sunday, Thursday</td>
                </tr>
                <tr>
                    <td>Marriage</td>
                    <td>Venus/Moon periods</td>
                    <td>Friday, Monday</td>
                </tr>
                <tr>
                    <td>Property Purchase</td>
                    <td>Saturn/Mars periods</td>
                    <td>Saturday, Tuesday</td>
                </tr>
                <tr>
                    <td>Education</td>
                    <td>Jupiter/Mercury periods</td>
                    <td>Thursday, Wednesday</td>
                </tr>
                <tr>
                    <td>Spiritual Activities</td>
                    <td>Jupiter/Ketu periods</td>
                    <td>Thursday, Tuesday</td>
                </tr>
            </table>

            <h2 class="subsection-header">16.2 Lucky Elements / அதிர்ஷ்ட அம்சங்கள்</h2>

            <table>
                <tr>
                    <th>Element</th>
                    <th>Value / மதிப்பு</th>
                </tr>
                <tr>
                    <td>Lucky Numbers / அதிர்ஷ்ட எண்கள்</td>
                    <td>3, 6, 9</td>
                </tr>
                <tr>
                    <td>Lucky Colors / அதிர்ஷ்ட நிறங்கள்</td>
                    <td>Yellow, Orange, White</td>
                </tr>
                <tr>
                    <td>Lucky Days / அதிர்ஷ்ட நாட்கள்</td>
                    <td>Thursday, Friday, Monday</td>
                </tr>
                <tr>
                    <td>Lucky Gems / அதிர்ஷ்ட கற்கள்</td>
                    <td>Yellow Sapphire, Pearl</td>
                </tr>
                <tr>
                    <td>Lucky Direction / அதிர்ஷ்ட திசை</td>
                    <td>North-East</td>
                </tr>
            </table>
        </div>
        """

    def _yearly_predictions_section(self) -> str:
        """Generate yearly predictions section"""
        current_year = datetime.now().year

        months = [
            ('January / ஜனவரி', 'Career opportunities arise. Financial planning needed.'),
            ('February / பிப்ரவரி', 'Relationship matters take focus. Short travels indicated.'),
            ('March / மார்ச்', 'Property matters favorable. Family gatherings likely.'),
            ('April / ஏப்ரல்', 'Professional growth continues. Health needs attention.'),
            ('May / மே', 'Financial gains expected. Social activities increase.'),
            ('June / ஜூன்', 'Balance work and personal life. Spiritual inclinations rise.'),
            ('July / ஜூலை', 'Favorable for investments. Recognition in profession.'),
            ('August / ஆகஸ்ட்', 'Communication brings success. Short journeys beneficial.'),
            ('September / செப்டம்பர்', 'Relationships strengthen. Creative pursuits favored.'),
            ('October / அக்டோபர்', 'Career milestone possible. Financial stability improves.'),
            ('November / நவம்பர்', 'Family focus. Property matters may finalize.'),
            ('December / டிசம்பர்', 'Year ends on positive note. Plan for coming year.'),
        ]

        rows_html = ""
        for month, prediction in months:
            rows_html += f"""
            <tr>
                <td><strong>{month}</strong></td>
                <td>{prediction}</td>
            </tr>
            """

        return f"""
        <div class="page-break">
            <h1 class="section-header">17. Yearly Predictions {current_year} / வருட பலன்கள்</h1>

            <p class="content">
                Month-by-month predictions for the year {current_year} based on planetary transits
                over your natal chart positions.
            </p>

            <table>
                <tr>
                    <th>Month / மாதம்</th>
                    <th>Predictions / பலன்கள்</th>
                </tr>
                {rows_html}
            </table>

            <h2 class="subsection-header">17.1 Year Overview / வருட கண்ணோட்டம்</h2>

            <div class="highlight-box">
                <p><strong>Overall Theme:</strong> Growth and consolidation</p>
                <p><strong>Best Months:</strong> March, July, October</p>
                <p><strong>Challenging Months:</strong> April, August (requires caution)</p>
                <p><strong>Key Focus Areas:</strong> Career advancement, financial planning, relationships</p>
            </div>

            <div style="margin-top: 40px; text-align: center; color: #666; font-style: italic;">
                <p>॥ சர்வே ஜனாஃ சுகினோ பவந்து ॥</p>
                <p>May all beings be happy and prosperous</p>
                <p style="margin-top: 20px;">— End of Report —</p>
            </div>
        </div>
        """


def generate_jathagam_report_html(chart_data: Dict[str, Any], user_data: Dict[str, Any], language: str = 'ta') -> bytes:
    """Main function to generate PDF report using HTML"""
    generator = HTMLReportGenerator(chart_data, user_data, language)
    return generator.generate()
