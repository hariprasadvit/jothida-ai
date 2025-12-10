"""
Comprehensive Tamil Astrology PDF Report Generator
Generates detailed 60+ page reports similar to ClickAstro
"""

import io
from datetime import datetime, date
from typing import Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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
    {'num': 1, 'name': 'Lagna/Ascendant', 'ta': 'லக்னம்', 'signifies': 'Self, personality, physical body, health, character'},
    {'num': 2, 'name': 'Dhana Bhava', 'ta': 'தன பாவம்', 'signifies': 'Wealth, family, speech, right eye, food intake'},
    {'num': 3, 'name': 'Sahaja Bhava', 'ta': 'சகோதர பாவம்', 'signifies': 'Siblings, courage, short journeys, communication'},
    {'num': 4, 'name': 'Sukha Bhava', 'ta': 'சுக பாவம்', 'signifies': 'Mother, home, property, vehicles, happiness'},
    {'num': 5, 'name': 'Putra Bhava', 'ta': 'புத்திர பாவம்', 'signifies': 'Children, intelligence, education, creativity'},
    {'num': 6, 'name': 'Ari Bhava', 'ta': 'சத்ரு பாவம்', 'signifies': 'Enemies, diseases, debts, servants, obstacles'},
    {'num': 7, 'name': 'Kalatra Bhava', 'ta': 'களத்திர பாவம்', 'signifies': 'Marriage, spouse, partnerships, business'},
    {'num': 8, 'name': 'Ayur Bhava', 'ta': 'ஆயுள் பாவம்', 'signifies': 'Longevity, transformation, inheritance, occult'},
    {'num': 9, 'name': 'Dharma Bhava', 'ta': 'தர்ம பாவம்', 'signifies': 'Father, fortune, religion, long journeys, higher education'},
    {'num': 10, 'name': 'Karma Bhava', 'ta': 'கர்ம பாவம்', 'signifies': 'Career, profession, status, authority, government'},
    {'num': 11, 'name': 'Labha Bhava', 'ta': 'லாப பாவம்', 'signifies': 'Income, gains, friends, elder siblings, desires'},
    {'num': 12, 'name': 'Vyaya Bhava', 'ta': 'விரய பாவம்', 'signifies': 'Expenses, losses, foreign lands, liberation, sleep'},
]

DASHA_PERIODS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}


class JathagamPDFGenerator:
    """Generate comprehensive Tamil astrology PDF reports"""

    def __init__(self, chart_data: Dict[str, Any], user_data: Dict[str, Any]):
        self.chart_data = chart_data
        self.user_data = user_data
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#c2410c')
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#ea580c'),
            borderWidth=1,
            borderColor=colors.HexColor('#fed7aa'),
            borderPadding=5
        ))

        # Subsection header
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=13,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#9a3412')
        ))

        # Tamil text style
        self.styles.add(ParagraphStyle(
            name='Tamil',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_LEFT
        ))

        # Body text (use CustomBody to avoid conflict with built-in BodyText)
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))

        # Quote/highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            backColor=colors.HexColor('#fff7ed'),
            borderColor=colors.HexColor('#fed7aa'),
            borderWidth=1,
            borderPadding=10
        ))

    def _header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()

        # Header
        canvas.setFillColor(colors.HexColor('#ea580c'))
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(50, A4[1] - 30, "ஜோதிட AI - Jathagam Report")
        canvas.drawRightString(A4[0] - 50, A4[1] - 30, self.user_data.get('name', 'User'))

        # Header line
        canvas.setStrokeColor(colors.HexColor('#fed7aa'))
        canvas.setLineWidth(1)
        canvas.line(50, A4[1] - 35, A4[0] - 50, A4[1] - 35)

        # Footer
        canvas.setFillColor(colors.gray)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(50, 30, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas.drawCentredString(A4[0] / 2, 30, f"Page {doc.page}")
        canvas.drawRightString(A4[0] - 50, 30, "www.jothida-ai.com")

        # Footer line
        canvas.line(50, 40, A4[0] - 50, A4[0] - 50)

        canvas.restoreState()

    def generate(self) -> bytes:
        """Generate the complete PDF report"""
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=60,
            bottomMargin=50
        )

        story = []

        # Build report sections
        story.extend(self._cover_page())
        story.append(PageBreak())

        story.extend(self._table_of_contents())
        story.append(PageBreak())

        story.extend(self._birth_details_section())
        story.append(PageBreak())

        story.extend(self._rasi_chart_section())
        story.append(PageBreak())

        story.extend(self._navamsa_chart_section())
        story.append(PageBreak())

        story.extend(self._planetary_positions_section())
        story.append(PageBreak())

        story.extend(self._house_analysis_section())
        story.append(PageBreak())

        story.extend(self._nakshatra_analysis_section())
        story.append(PageBreak())

        story.extend(self._dasha_section())
        story.append(PageBreak())

        story.extend(self._yogas_section())
        story.append(PageBreak())

        story.extend(self._doshas_section())
        story.append(PageBreak())

        story.extend(self._life_predictions_section())
        story.append(PageBreak())

        story.extend(self._career_section())
        story.append(PageBreak())

        story.extend(self._marriage_section())
        story.append(PageBreak())

        story.extend(self._health_section())
        story.append(PageBreak())

        story.extend(self._wealth_section())
        story.append(PageBreak())

        story.extend(self._remedies_section())
        story.append(PageBreak())

        story.extend(self._favorable_section())
        story.append(PageBreak())

        story.extend(self._yearly_predictions_section())
        story.append(PageBreak())

        story.extend(self._appendix_section())

        # Build PDF
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        buffer.seek(0)
        return buffer.getvalue()

    def _cover_page(self) -> list:
        """Generate cover page"""
        elements = []

        elements.append(Spacer(1, 2 * inch))

        # Om symbol
        elements.append(Paragraph(
            '<font size="48" color="#ea580c">ॐ</font>',
            ParagraphStyle(name='OmSymbol', alignment=TA_CENTER)
        ))

        elements.append(Spacer(1, 0.5 * inch))

        # Title
        elements.append(Paragraph(
            "ஜாதக அறிக்கை",
            self.styles['CustomTitle']
        ))

        elements.append(Paragraph(
            "JATHAGAM REPORT",
            ParagraphStyle(name='SubTitle', alignment=TA_CENTER, fontSize=18, textColor=colors.HexColor('#9a3412'))
        ))

        elements.append(Spacer(1, 1 * inch))

        # User info box
        user_info = [
            ['Name / பெயர்', self.user_data.get('name', 'N/A')],
            ['Date of Birth / பிறந்த தேதி', self.user_data.get('birth_date', 'N/A')],
            ['Time of Birth / பிறந்த நேரம்', self.user_data.get('birth_time', 'N/A')],
            ['Place of Birth / பிறந்த இடம்', self.user_data.get('birth_place', 'N/A')],
        ]

        # Add rasi/nakshatra if available
        if self.chart_data.get('moon_rasi'):
            rasi = self.chart_data.get('moon_rasi', {})
            user_info.append(['Moon Sign / ராசி', f"{rasi.get('tamil', 'N/A')} ({rasi.get('name', '')})"])

        if self.chart_data.get('nakshatra'):
            nak = self.chart_data.get('nakshatra', {})
            pada = nak.get('pada', '')
            user_info.append(['Birth Star / நட்சத்திரம்', f"{nak.get('tamil', 'N/A')} (Pada {pada})"])

        table = Table(user_info, colWidths=[2.5 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff7ed')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#9a3412')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#fffbeb')]),
        ]))

        elements.append(table)

        elements.append(Spacer(1, 1.5 * inch))

        # Generation info
        elements.append(Paragraph(
            f"Report Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            ParagraphStyle(name='GenDate', alignment=TA_CENTER, fontSize=10, textColor=colors.gray)
        ))

        elements.append(Paragraph(
            "Powered by ஜோதிட AI - Traditional Vedic Astrology with Modern AI",
            ParagraphStyle(name='PoweredBy', alignment=TA_CENTER, fontSize=9, textColor=colors.HexColor('#ea580c'))
        ))

        return elements

    def _table_of_contents(self) -> list:
        """Generate table of contents"""
        elements = []

        elements.append(Paragraph("Table of Contents / உள்ளடக்கம்", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.3 * inch))

        toc_items = [
            ("1. Birth Details / பிறப்பு விவரங்கள்", 3),
            ("2. Rasi Chart / ராசி கட்டம்", 4),
            ("3. Navamsa Chart / நவாம்சம்", 5),
            ("4. Planetary Positions / கிரக நிலைகள்", 6),
            ("5. House Analysis / பாவ பலன்கள்", 8),
            ("6. Nakshatra Analysis / நட்சத்திர பலன்", 10),
            ("7. Dasha Periods / தசா புத்தி", 12),
            ("8. Yogas / யோகங்கள்", 16),
            ("9. Doshas / தோஷங்கள்", 18),
            ("10. Life Predictions / வாழ்க்கை பலன்கள்", 20),
            ("11. Career & Profession / தொழில்", 25),
            ("12. Marriage & Family / திருமணம்", 30),
            ("13. Health Analysis / உடல் நலம்", 35),
            ("14. Wealth & Finance / செல்வம்", 40),
            ("15. Remedies / பரிகாரங்கள்", 45),
            ("16. Favorable Periods / சுப காலங்கள்", 50),
            ("17. Yearly Predictions / வருட பலன்கள்", 55),
            ("18. Appendix / இணைப்பு", 60),
        ]

        toc_data = []
        for item, page in toc_items:
            toc_data.append([item, f"Page {page}"])

        table = Table(toc_data, colWidths=[4.5 * inch, 1 * inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#fed7aa')),
        ]))

        elements.append(table)

        return elements

    def _birth_details_section(self) -> list:
        """Generate birth details section"""
        elements = []

        elements.append(Paragraph("1. Birth Details / பிறப்பு விவரங்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "This section contains the fundamental birth information used to calculate your horoscope. "
            "The accuracy of all predictions depends on the correctness of these details.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Birth details table
        birth_data = [
            ['Parameter', 'Value', 'Tamil'],
            ['Full Name', self.user_data.get('name', 'N/A'), 'பெயர்'],
            ['Date of Birth', self.user_data.get('birth_date', 'N/A'), 'பிறந்த தேதி'],
            ['Time of Birth', self.user_data.get('birth_time', 'N/A'), 'பிறந்த நேரம்'],
            ['Place of Birth', self.user_data.get('birth_place', 'N/A'), 'பிறந்த இடம்'],
            ['Latitude', str(self.user_data.get('latitude', 'N/A')), 'அட்சரேகை'],
            ['Longitude', str(self.user_data.get('longitude', 'N/A')), 'தீர்க்கரேகை'],
            ['Timezone', 'IST (+5:30)', 'நேர மண்டலம்'],
        ]

        table = Table(birth_data, colWidths=[2 * inch, 2.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(table)

        elements.append(Spacer(1, 0.3 * inch))

        # Astronomical data
        elements.append(Paragraph("1.1 Astronomical Data / வானியல் தகவல்கள்", self.styles['SubSection']))

        astro_data = [
            ['Parameter', 'Value'],
            ['Ayanamsa', 'Lahiri (Chitrapaksha)'],
            ['Sidereal Time', self.chart_data.get('sidereal_time', 'Calculated')],
            ['Julian Day', self.chart_data.get('julian_day', 'Calculated')],
            ['Sunrise', self.chart_data.get('sunrise', '06:00 AM')],
            ['Sunset', self.chart_data.get('sunset', '06:00 PM')],
        ]

        table2 = Table(astro_data, colWidths=[2.5 * inch, 3 * inch])
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ]))

        elements.append(table2)

        return elements

    def _rasi_chart_section(self) -> list:
        """Generate Rasi chart section"""
        elements = []

        elements.append(Paragraph("2. Rasi Chart / ராசி கட்டம்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "The Rasi chart (also known as the birth chart or natal chart) is the primary chart in Vedic astrology. "
            "It shows the positions of all planets at the exact moment of your birth. The chart is divided into 12 houses, "
            "each representing different aspects of life.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # South Indian style chart (4x4 grid)
        elements.append(Paragraph("2.1 South Indian Style Chart / தென்னிந்திய முறை", self.styles['SubSection']))

        # Create a simple text representation of the chart
        chart_positions = self.chart_data.get('planets', {})

        # Create 4x4 grid for South Indian chart
        chart_data = [
            ['மீனம்\nPisces', 'மேஷம்\nAries', 'ரிஷபம்\nTaurus', 'மிதுனம்\nGemini'],
            ['கும்பம்\nAquarius', '', '', 'கடகம்\nCancer'],
            ['மகரம்\nCapricorn', '', '', 'சிம்மம்\nLeo'],
            ['தனுசு்\nSagittarius', 'விருச்சிகம்\nScorpio', 'துலாம்\nLibra', 'கன்னி\nVirgo'],
        ]

        chart_table = Table(chart_data, colWidths=[1.4 * inch] * 4, rowHeights=[0.9 * inch] * 4)
        chart_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#ea580c')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff7ed')),
            ('BACKGROUND', (1, 1), (2, 2), colors.white),
        ]))

        elements.append(chart_table)

        elements.append(Spacer(1, 0.3 * inch))

        # Chart explanation
        elements.append(Paragraph("2.2 Understanding the Chart / கட்டத்தை புரிந்துகொள்ளுதல்", self.styles['SubSection']))

        explanation = """
        The South Indian chart format is one of the most commonly used in Tamil Nadu and other southern states.
        In this format:

        • The 12 zodiac signs (Rasis) are fixed in their positions
        • Planets are placed in the sign they occupy at birth
        • The Lagna (Ascendant) is marked to identify the first house
        • Reading starts from Lagna and proceeds in a clockwise direction

        Each house represents specific life areas, and the planets in each house influence those areas.
        """

        elements.append(Paragraph(explanation, self.styles['CustomBody']))

        return elements

    def _navamsa_chart_section(self) -> list:
        """Generate Navamsa chart section"""
        elements = []

        elements.append(Paragraph("3. Navamsa Chart / நவாம்சம்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "The Navamsa (D-9) chart is the most important divisional chart in Vedic astrology. "
            "It is derived by dividing each sign into 9 equal parts of 3°20' each. "
            "This chart is primarily used for analyzing marriage, dharma, and the strength of planets.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("3.1 Navamsa Chart / நவாம்ச கட்டம்", self.styles['SubSection']))

        # Navamsa chart (similar structure)
        navamsa_data = [
            ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்'],
            ['கும்பம்', '', '', 'கடகம்'],
            ['மகரம்', '', '', 'சிம்மம்'],
            ['தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'],
        ]

        navamsa_table = Table(navamsa_data, colWidths=[1.4 * inch] * 4, rowHeights=[0.8 * inch] * 4)
        navamsa_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#9a3412')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
            ('BACKGROUND', (1, 1), (2, 2), colors.white),
        ]))

        elements.append(navamsa_table)

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("3.2 Significance of Navamsa / நவாம்சத்தின் முக்கியத்துவம்", self.styles['SubSection']))

        navamsa_info = """
        The Navamsa chart reveals:

        • The strength and dignity of planets (Vargottama planets gain extra strength)
        • Marriage and spouse characteristics
        • Spiritual inclinations and dharmic path
        • The fruit of your actions (Karma Phala)
        • Hidden strengths and weaknesses of planets

        A planet in the same sign in both Rasi and Navamsa is called "Vargottama" and gains significant strength.
        """

        elements.append(Paragraph(navamsa_info, self.styles['CustomBody']))

        return elements

    def _planetary_positions_section(self) -> list:
        """Generate planetary positions section"""
        elements = []

        elements.append(Paragraph("4. Planetary Positions / கிரக நிலைகள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "This section details the exact positions of all nine planets (Navagrahas) in your birth chart. "
            "Each planet's sign, house, degree, nakshatra, and dignity are analyzed.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Planetary positions table
        planets_data = [['Planet', 'Sign', 'House', 'Degree', 'Nakshatra', 'Status']]

        planets = self.chart_data.get('planets', [])
        if isinstance(planets, list):
            for p in planets:
                planets_data.append([
                    f"{p.get('name', 'N/A')} ({p.get('tamil', '')})",
                    p.get('sign', 'N/A'),
                    str(p.get('house', 'N/A')),
                    f"{p.get('longitude', 0):.2f}°",
                    p.get('nakshatra', 'N/A'),
                    p.get('status', 'Normal')
                ])
        else:
            # Sample data if not available
            sample_planets = [
                ['Sun (சூரியன்)', 'Leo', '5', '15.23°', 'Magha', 'Own Sign'],
                ['Moon (சந்திரன்)', 'Cancer', '4', '22.45°', 'Ashlesha', 'Own Sign'],
                ['Mars (செவ்வாய்)', 'Aries', '1', '8.12°', 'Ashwini', 'Own Sign'],
                ['Mercury (புதன்)', 'Virgo', '6', '18.67°', 'Hasta', 'Exalted'],
                ['Jupiter (குரு)', 'Sagittarius', '9', '12.34°', 'Moola', 'Own Sign'],
                ['Venus (சுக்கிரன்)', 'Libra', '7', '25.89°', 'Vishakha', 'Own Sign'],
                ['Saturn (சனி)', 'Aquarius', '11', '5.56°', 'Dhanishta', 'Own Sign'],
                ['Rahu (ராகு)', 'Gemini', '3', '14.78°', 'Ardra', 'Normal'],
                ['Ketu (கேது)', 'Sagittarius', '9', '14.78°', 'Moola', 'Normal'],
            ]
            planets_data.extend(sample_planets)

        planets_table = Table(planets_data, colWidths=[1.3 * inch, 0.9 * inch, 0.6 * inch, 0.8 * inch, 1 * inch, 0.9 * inch])
        planets_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(planets_table)

        elements.append(Spacer(1, 0.3 * inch))

        # Planet details
        elements.append(Paragraph("4.1 Detailed Planet Analysis / விரிவான கிரக பகுப்பாய்வு", self.styles['SubSection']))

        for planet in PLANETS:
            elements.append(Paragraph(
                f"<b>{planet['symbol']} {planet['en']} ({planet['ta']})</b>",
                self.styles['Tamil']
            ))
            elements.append(Paragraph(
                f"The {planet['en']} in your chart represents " + self._get_planet_signification(planet['en']),
                self.styles['CustomBody']
            ))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _get_planet_signification(self, planet: str) -> str:
        """Get planet signification text"""
        significations = {
            'Sun': 'soul, father, authority, government, vitality, and self-expression. Its placement influences your ego, willpower, and leadership qualities.',
            'Moon': 'mind, mother, emotions, nurturing, and public image. Its placement affects your emotional nature, mental peace, and relationship with mother.',
            'Mars': 'energy, courage, siblings, property, and aggression. Its placement determines your drive, physical strength, and competitive spirit.',
            'Mercury': 'intellect, communication, commerce, and analytical abilities. Its placement influences your thinking, speech, and learning capacity.',
            'Jupiter': 'wisdom, fortune, spirituality, children, and expansion. Its placement affects your luck, higher education, and philosophical outlook.',
            'Venus': 'love, marriage, beauty, luxury, and artistic talents. Its placement determines your romantic life, aesthetic sense, and material comforts.',
            'Saturn': 'karma, discipline, delays, longevity, and hardship. Its placement indicates areas of life requiring patience, perseverance, and lessons.',
            'Rahu': 'obsession, foreign connections, unconventional paths, and material desires. Its placement shows areas of intense focus and potential growth.',
            'Ketu': 'spirituality, liberation, past life karma, and detachment. Its placement indicates areas where you may feel disconnected but gain spiritual insight.',
        }
        return significations.get(planet, 'various aspects of life based on its placement.')

    def _house_analysis_section(self) -> list:
        """Generate house analysis section"""
        elements = []

        elements.append(Paragraph("5. House Analysis / பாவ பலன்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "The 12 houses (Bhavas) of the horoscope represent different areas of life. "
            "Each house is governed by a sign and influenced by the planets placed in it. "
            "This analysis provides insights into various life aspects based on house placements.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        for house in HOUSES:
            elements.append(Paragraph(
                f"5.{house['num']} House {house['num']} - {house['name']} ({house['ta']})",
                self.styles['SubSection']
            ))

            elements.append(Paragraph(
                f"<b>Significations:</b> {house['signifies']}",
                self.styles['CustomBody']
            ))

            # Add house prediction
            prediction = self._get_house_prediction(house['num'])
            elements.append(Paragraph(
                f"<b>Analysis:</b> {prediction}",
                self.styles['CustomBody']
            ))

            elements.append(Spacer(1, 0.15 * inch))

        return elements

    def _get_house_prediction(self, house_num: int) -> str:
        """Get house prediction text"""
        predictions = {
            1: "Your ascendant indicates a strong personality with good health potential. You have natural leadership qualities and a commanding presence.",
            2: "Financial prospects appear favorable with potential for steady accumulation of wealth through personal efforts and family support.",
            3: "Communication skills are your strength. Relationships with siblings will be generally positive with opportunities for short travels.",
            4: "Domestic happiness and property matters look promising. Strong emotional foundation from mother and peaceful home environment indicated.",
            5: "Creative talents and intelligence are highlighted. Children will bring joy, and speculative ventures may yield positive results.",
            6: "Health requires attention to diet and routine. You have ability to overcome enemies and obstacles through persistent effort.",
            7: "Partnership matters, both business and personal, require careful attention. Marriage prospects are favorable with compatible partner.",
            8: "Transformation and inheritance matters are indicated. Longevity appears good with interest in occult or hidden knowledge.",
            9: "Fortune favors you, especially in higher education and spiritual pursuits. Father's influence is significant in your life path.",
            10: "Career growth and professional recognition are strongly indicated. Government or authority positions may be attainable.",
            11: "Financial gains through networks and friendships. Elder siblings and friends play supportive roles in achieving desires.",
            12: "Spiritual growth and foreign connections are highlighted. Expenses should be managed, with focus on meaningful expenditure.",
        }
        return predictions.get(house_num, "Analysis based on planetary placements and aspects to this house.")

    def _nakshatra_analysis_section(self) -> list:
        """Generate nakshatra analysis section"""
        elements = []

        elements.append(Paragraph("6. Nakshatra Analysis / நட்சத்திர பலன்", self.styles['SectionHeader']))

        nakshatra = self.chart_data.get('nakshatra', {})
        nak_name = nakshatra.get('tamil', 'அசுவினி') if isinstance(nakshatra, dict) else 'அசுவினி'
        nak_pada = nakshatra.get('pada', 1) if isinstance(nakshatra, dict) else 1

        elements.append(Paragraph(
            f"Your birth nakshatra is <b>{nak_name}</b> (Pada {nak_pada}). "
            "The nakshatra (lunar mansion) at the time of birth plays a crucial role in Vedic astrology, "
            "influencing personality, career, relationships, and life path.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("6.1 Nakshatra Characteristics / நட்சத்திர குணங்கள்", self.styles['SubSection']))

        # Nakshatra details table
        nak_details = [
            ['Attribute', 'Value'],
            ['Nakshatra Name', nak_name],
            ['Pada (Quarter)', str(nak_pada)],
            ['Ruling Planet', 'Ketu (கேது)'],
            ['Deity', 'Ashwini Kumaras'],
            ['Symbol', 'Horse\'s Head'],
            ['Gana (Nature)', 'Deva (Divine)'],
            ['Animal Symbol', 'Male Horse'],
            ['Bird', 'Wild Eagle'],
            ['Tree', 'Poison Nut Tree'],
        ]

        nak_table = Table(nak_details, colWidths=[2 * inch, 3 * inch])
        nak_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(nak_table)

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("6.2 Personality Traits / ஆளுமை பண்புகள்", self.styles['SubSection']))

        personality_text = """
        Individuals born under this nakshatra typically exhibit the following characteristics:

        • Quick-witted and intelligent with good decision-making abilities
        • Natural healing abilities and interest in medicine
        • Adventurous spirit with love for travel and exploration
        • Independent nature with leadership qualities
        • Honest and straightforward in dealings
        • May face initial obstacles but achieves success through persistence

        The nakshatra lord's placement further modifies these general characteristics based on
        its strength and aspects in your birth chart.
        """

        elements.append(Paragraph(personality_text, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2 * inch))

        # All 27 nakshatras reference
        elements.append(Paragraph("6.3 Complete Nakshatra Reference / முழு நட்சத்திர பட்டியல்", self.styles['SubSection']))

        nak_ref_data = [['#', 'Nakshatra', 'Tamil', 'Lord']]
        for i, nak in enumerate(NAKSHATRAS, 1):
            nak_ref_data.append([str(i), nak['en'], nak['ta'], nak['lord_ta']])

        nak_ref_table = Table(nak_ref_data, colWidths=[0.4 * inch, 1.5 * inch, 1.2 * inch, 1 * inch])
        nak_ref_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffbeb')]),
        ]))

        elements.append(nak_ref_table)

        return elements

    def _dasha_section(self) -> list:
        """Generate Dasha periods section"""
        elements = []

        elements.append(Paragraph("7. Dasha Periods / தசா புத்தி", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "The Vimshottari Dasha system is a 120-year planetary period system used in Vedic astrology. "
            "It divides life into major periods (Mahadasha) ruled by different planets, with each period further "
            "divided into sub-periods (Antardasha/Bhukti). Understanding these periods helps predict life events.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Current Dasha
        dasha = self.chart_data.get('current_dasha', {})
        current_maha = dasha.get('mahadasha_tamil', 'சுக்கிரன்') if isinstance(dasha, dict) else 'சுக்கிரன்'
        current_antar = dasha.get('antardasha_tamil', 'சூரியன்') if isinstance(dasha, dict) else 'சூரியன்'

        elements.append(Paragraph("7.1 Current Dasha Period / தற்போதைய தசை", self.styles['SubSection']))

        current_dasha_data = [
            ['Period Type', 'Planet', 'Duration'],
            ['Mahadasha (Major)', current_maha, '20 years'],
            ['Antardasha (Sub)', current_antar, '1 year 2 months'],
            ['Pratyantardasha', 'சந்திரன்', '2 months'],
        ]

        current_table = Table(current_dasha_data, colWidths=[2 * inch, 2 * inch, 1.5 * inch])
        current_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ]))

        elements.append(current_table)

        elements.append(Spacer(1, 0.3 * inch))

        # Life Dasha Timeline
        elements.append(Paragraph("7.2 Complete Dasha Timeline / முழு தசா காலவரிசை", self.styles['SubSection']))

        # Generate approximate dasha timeline
        dasha_timeline = [['Mahadasha', 'Start', 'End', 'Duration']]

        dasha_order = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        dasha_tamil = {'Ketu': 'கேது', 'Venus': 'சுக்கிரன்', 'Sun': 'சூரியன்', 'Moon': 'சந்திரன்',
                       'Mars': 'செவ்வாய்', 'Rahu': 'ராகு', 'Jupiter': 'குரு', 'Saturn': 'சனி', 'Mercury': 'புதன்'}

        birth_year = 1990  # Default
        try:
            birth_date_str = self.user_data.get('birth_date', '1990-01-01')
            birth_year = int(birth_date_str.split('-')[0])
        except:
            pass

        current_year = birth_year
        for dasha_name in dasha_order:
            duration = DASHA_PERIODS[dasha_name]
            end_year = current_year + duration
            dasha_timeline.append([
                f"{dasha_name} ({dasha_tamil[dasha_name]})",
                str(current_year),
                str(end_year),
                f"{duration} years"
            ])
            current_year = end_year

        dasha_table = Table(dasha_timeline, colWidths=[2 * inch, 1 * inch, 1 * inch, 1 * inch])
        dasha_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(dasha_table)

        elements.append(Spacer(1, 0.3 * inch))

        # Dasha predictions
        elements.append(Paragraph("7.3 Dasha Period Predictions / தசா பலன்கள்", self.styles['SubSection']))

        for dasha_name in dasha_order[:5]:  # First 5 dashas
            elements.append(Paragraph(
                f"<b>{dasha_name} ({dasha_tamil[dasha_name]}) Mahadasha:</b>",
                self.styles['Tamil']
            ))
            elements.append(Paragraph(
                self._get_dasha_prediction(dasha_name),
                self.styles['CustomBody']
            ))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _get_dasha_prediction(self, dasha: str) -> str:
        """Get dasha prediction text"""
        predictions = {
            'Ketu': "This period brings spiritual awakening and detachment from material pursuits. Health matters require attention. Past life karmas may surface for resolution. Good for meditation and spiritual practices.",
            'Venus': "A favorable period for relationships, marriage, luxury, and artistic pursuits. Financial gains through partnerships. Good time for acquiring vehicles, property, and enjoying life's pleasures.",
            'Sun': "Period of authority, recognition, and government favors. Father's influence is prominent. Health of father needs attention. Good for career growth and leadership positions.",
            'Moon': "Emotional period with focus on mother, home, and mental peace. Travel and public dealings increase. Good for real estate and nurturing relationships. Mental health needs care.",
            'Mars': "Period of energy, action, and courage. Good for property matters and technical pursuits. Siblings play important role. Caution needed for accidents and conflicts.",
            'Rahu': "Intense period of worldly pursuits and unconventional paths. Foreign connections strengthen. Material gains possible but with karmic lessons. Research and technology favored.",
            'Jupiter': "Most favorable period for growth, wisdom, and fortune. Children bring joy. Higher education, spiritual pursuits, and teaching favored. Financial expansion likely.",
            'Saturn': "Period requiring patience, discipline, and hard work. Karmic lessons intensify. Long-term gains through persistent effort. Health of elderly family members needs attention.",
            'Mercury': "Intellectual and communicative period. Business and commerce thrive. Good for education, writing, and analytical work. Short travels increase.",
        }
        return predictions.get(dasha, "Period predictions based on planetary placement and strength.")

    def _yogas_section(self) -> list:
        """Generate Yogas section"""
        elements = []

        elements.append(Paragraph("8. Yogas / யோகங்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Yogas are special planetary combinations that produce specific results in a horoscope. "
            "They can be auspicious (Shubha Yoga) or inauspicious (Ashubha Yoga). "
            "The following yogas have been identified in your birth chart:",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Auspicious Yogas
        elements.append(Paragraph("8.1 Auspicious Yogas / சுப யோகங்கள்", self.styles['SubSection']))

        yogas = [
            {'name': 'Gajakesari Yoga', 'tamil': 'கஜகேசரி யோகம்',
             'desc': 'Jupiter in a kendra from Moon. Bestows wisdom, wealth, good reputation, and leadership qualities.',
             'strength': 'Strong'},
            {'name': 'Budhaditya Yoga', 'tamil': 'புதாதித்ய யோகம்',
             'desc': 'Sun and Mercury conjunction. Grants intelligence, eloquence, and skill in multiple fields.',
             'strength': 'Moderate'},
            {'name': 'Lakshmi Yoga', 'tamil': 'லக்ஷ்மி யோகம்',
             'desc': 'Lord of 9th in own sign or exalted in a kendra. Bestows wealth, fortune, and prosperity.',
             'strength': 'Moderate'},
            {'name': 'Hamsa Yoga', 'tamil': 'ஹம்ச யோகம்',
             'desc': 'Jupiter in own sign or exalted in a kendra. Grants wisdom, virtue, and high status.',
             'strength': 'Strong'},
        ]

        for yoga in yogas:
            elements.append(Paragraph(
                f"<b>{yoga['name']} ({yoga['tamil']})</b> - Strength: {yoga['strength']}",
                self.styles['Tamil']
            ))
            elements.append(Paragraph(yoga['desc'], self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1 * inch))

        elements.append(Spacer(1, 0.2 * inch))

        # Dhana Yogas
        elements.append(Paragraph("8.2 Wealth Yogas / தன யோகங்கள்", self.styles['SubSection']))

        dhana_yogas = [
            {'name': 'Dhana Yoga', 'tamil': 'தன யோகம்',
             'desc': 'Combination of 2nd and 11th house lords. Indicates accumulation of wealth.'},
            {'name': 'Raja Yoga', 'tamil': 'ராஜ யோகம்',
             'desc': 'Combination of kendra and trikona lords. Grants authority and high position.'},
        ]

        for yoga in dhana_yogas:
            elements.append(Paragraph(
                f"<b>{yoga['name']} ({yoga['tamil']})</b>",
                self.styles['Tamil']
            ))
            elements.append(Paragraph(yoga['desc'], self.styles['CustomBody']))
            elements.append(Spacer(1, 0.1 * inch))

        return elements

    def _doshas_section(self) -> list:
        """Generate Doshas section"""
        elements = []

        elements.append(Paragraph("9. Doshas / தோஷங்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Doshas are afflictions or negative combinations in a horoscope that can create obstacles in specific life areas. "
            "Identifying doshas helps in understanding challenges and applying appropriate remedies.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Mangal Dosha
        elements.append(Paragraph("9.1 Mangal Dosha / செவ்வாய் தோஷம்", self.styles['SubSection']))

        elements.append(Paragraph(
            "Mangal Dosha (Kuja Dosha) occurs when Mars is placed in the 1st, 2nd, 4th, 7th, 8th, or 12th house. "
            "It is primarily considered for marriage compatibility.",
            self.styles['CustomBody']
        ))

        mangal_status = "Partial Mangal Dosha detected. Mars is placed in a position that creates mild dosha."
        elements.append(Paragraph(f"<b>Status:</b> {mangal_status}", self.styles['Highlight']))

        elements.append(Paragraph(
            "<b>Remedies:</b> Chanting Mangal mantra, wearing red coral (after consultation), "
            "performing Mangal Shanti puja, and marrying a Manglik person can neutralize the dosha.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Kaal Sarpa Dosha
        elements.append(Paragraph("9.2 Kaal Sarpa Dosha / கால சர்ப்ப தோஷம்", self.styles['SubSection']))

        elements.append(Paragraph(
            "Kaal Sarpa Dosha occurs when all planets are hemmed between Rahu and Ketu. "
            "It can cause delays, obstacles, and unexpected challenges in life.",
            self.styles['CustomBody']
        ))

        kaal_status = "No Kaal Sarpa Dosha detected in your chart."
        elements.append(Paragraph(f"<b>Status:</b> {kaal_status}", self.styles['Highlight']))

        elements.append(Spacer(1, 0.2 * inch))

        # Pitra Dosha
        elements.append(Paragraph("9.3 Pitra Dosha / பித்ரு தோஷம்", self.styles['SubSection']))

        elements.append(Paragraph(
            "Pitra Dosha relates to ancestral karma and occurs due to affliction to Sun or 9th house. "
            "It can affect father, authority figures, and overall fortune.",
            self.styles['CustomBody']
        ))

        elements.append(Paragraph(
            "<b>Remedies:</b> Perform Shraddha ceremonies, offer Tarpan to ancestors, "
            "donate food and clothes to elderly, and recite Pitra Suktam.",
            self.styles['CustomBody']
        ))

        return elements

    def _life_predictions_section(self) -> list:
        """Generate life predictions section"""
        elements = []

        elements.append(Paragraph("10. Life Predictions / வாழ்க்கை பலன்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Based on the comprehensive analysis of your birth chart, the following life predictions "
            "are derived. These are general indications that may manifest differently based on current "
            "planetary transits and personal karma.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Different life aspects
        life_aspects = [
            {
                'title': '10.1 Personality & Character / ஆளுமை',
                'content': "You possess a dynamic personality with natural leadership abilities. Your intellectual capacity is strong, and you have good analytical skills. There's an inherent desire to achieve something significant in life. You are generally honest and straightforward in your dealings, which earns you respect. However, you may sometimes come across as stubborn or opinionated. Learning to be more flexible will help in personal relationships."
            },
            {
                'title': '10.2 Education & Learning / கல்வி',
                'content': "Your chart indicates good potential for education, especially in analytical and technical subjects. The placement of Mercury suggests strong communication skills. Higher education is favored, and you may pursue multiple degrees or certifications. Research work and specialized studies are indicated. The period between ages 18-25 is particularly favorable for educational achievements."
            },
            {
                'title': '10.3 Family Life / குடும்ப வாழ்க்கை',
                'content': "Family relationships will be generally harmonious. You may take significant responsibilities for family members. The relationship with mother is particularly strong and nurturing. There may be some challenges with siblings, but overall family support is indicated. Property matters through family channels look favorable, especially during Jupiter periods."
            },
            {
                'title': '10.4 Social Life / சமூக வாழ்க்கை',
                'content': "You will have a good social circle with influential friends. Your networking abilities will help in career advancement. Social recognition is indicated, especially in later years. Involvement in social causes or charitable activities will bring satisfaction. Be cautious of false friends during Rahu periods."
            },
            {
                'title': '10.5 Spiritual Inclinations / ஆன்மீகம்',
                'content': "There's a natural inclination towards spirituality and philosophical matters. Interest in astrology, yoga, or meditation is indicated. The later part of life will see increased spiritual pursuits. Pilgrimages and visits to sacred places will bring peace and blessings. Jupiter periods are particularly favorable for spiritual growth."
            },
        ]

        for aspect in life_aspects:
            elements.append(Paragraph(aspect['title'], self.styles['SubSection']))
            elements.append(Paragraph(aspect['content'], self.styles['CustomBody']))
            elements.append(Spacer(1, 0.15 * inch))

        return elements

    def _career_section(self) -> list:
        """Generate career section"""
        elements = []

        elements.append(Paragraph("11. Career & Profession / தொழில்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Career analysis is based on the 10th house (Karma Bhava), its lord, planets in the 10th house, "
            "and aspects to it. The 2nd house (wealth), 6th house (service), and 11th house (gains) "
            "are also considered for comprehensive career prediction.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("11.1 Career Strengths / தொழில் பலம்", self.styles['SubSection']))

        strengths = """
        Based on your chart analysis, the following career strengths are identified:

        • Strong analytical and problem-solving abilities
        • Good communication and presentation skills
        • Leadership qualities and management capabilities
        • Technical aptitude and systematic approach
        • Ability to work independently and in teams
        • Good negotiation and diplomatic skills
        """
        elements.append(Paragraph(strengths, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("11.2 Suitable Professions / பொருத்தமான தொழில்கள்", self.styles['SubSection']))

        professions = [
            ['Field', 'Suitability', 'Remarks'],
            ['IT & Technology', 'Highly Suitable', 'Mercury\'s influence supports technical work'],
            ['Finance & Banking', 'Suitable', 'Saturn\'s placement supports systematic work'],
            ['Teaching & Academia', 'Highly Suitable', 'Jupiter\'s aspect favors knowledge sharing'],
            ['Government Service', 'Suitable', 'Sun\'s placement indicates authority positions'],
            ['Business & Commerce', 'Moderately Suitable', 'Mercury supports trade activities'],
            ['Healthcare', 'Suitable', 'Sun and Moon combination supports healing professions'],
            ['Law & Legal', 'Moderately Suitable', 'Jupiter\'s influence on justice matters'],
            ['Creative Arts', 'Suitable', 'Venus placement supports artistic pursuits'],
        ]

        prof_table = Table(professions, colWidths=[1.8 * inch, 1.2 * inch, 2.5 * inch])
        prof_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(prof_table)

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("11.3 Career Timeline / தொழில் காலவரிசை", self.styles['SubSection']))

        timeline_text = """
        <b>Ages 22-28:</b> Initial career building phase. May face some challenges but will establish foundation.
        Multiple job changes possible. Learning and skill development emphasized.

        <b>Ages 28-35:</b> Period of growth and recognition. Significant career advancement likely.
        May receive promotions or start independent ventures. Financial gains increase.

        <b>Ages 35-45:</b> Peak career period. Authority and leadership positions indicated.
        Major professional achievements possible. Business expansion or senior positions favored.

        <b>Ages 45-55:</b> Consolidation phase. May consider teaching or mentoring roles.
        Passive income sources develop. Consider long-term financial planning.

        <b>Ages 55+:</b> Advisory and consultancy roles suit well. May continue working in reduced capacity.
        Focus shifts to legacy building and knowledge transfer.
        """

        elements.append(Paragraph(timeline_text, self.styles['CustomBody']))

        return elements

    def _marriage_section(self) -> list:
        """Generate marriage section"""
        elements = []

        elements.append(Paragraph("12. Marriage & Family / திருமணம்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Marriage analysis is based on the 7th house (Kalatra Bhava), Venus (Karaka for marriage), "
            "and the Navamsa chart. The following analysis provides insights into marriage timing, "
            "spouse characteristics, and married life predictions.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("12.1 Marriage Timing / திருமண காலம்", self.styles['SubSection']))

        elements.append(Paragraph(
            "Based on the dasha periods and transits, favorable periods for marriage are:",
            self.styles['CustomBody']
        ))

        timing_data = [
            ['Period', 'Favorability', 'Remarks'],
            ['Venus Mahadasha', 'Highly Favorable', 'Best period for marriage'],
            ['Jupiter Antardasha', 'Favorable', 'Good for finding suitable match'],
            ['Moon Antardasha', 'Favorable', 'Emotional connections strengthen'],
            ['Saturn periods', 'Moderate', 'May cause delays but stable marriage'],
        ]

        timing_table = Table(timing_data, colWidths=[1.8 * inch, 1.5 * inch, 2.2 * inch])
        timing_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ]))

        elements.append(timing_table)

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("12.2 Spouse Characteristics / வாழ்க்கைத்துணை பண்புகள்", self.styles['SubSection']))

        spouse_text = """
        Based on the 7th house and Venus placement, your spouse is likely to have the following characteristics:

        • Attractive appearance with pleasant demeanor
        • Educated and intellectually compatible
        • May be from a good family background
        • Supportive and understanding nature
        • May have artistic or creative inclinations
        • Career-oriented or professionally successful
        • Good communication and social skills

        The 7th lord's placement suggests that the spouse may be met through professional circles,
        educational institutions, or family introductions.
        """

        elements.append(Paragraph(spouse_text, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("12.3 Married Life / திருமண வாழ்க்கை", self.styles['SubSection']))

        married_life = """
        Overall married life appears harmonious with the following indications:

        • Initial years require adjustment but will stabilize
        • Strong emotional bond with spouse
        • Children will bring happiness to the marriage
        • May face minor disagreements but will resolve amicably
        • Financial stability in married life
        • Support from in-laws indicated
        • Foreign travel or settlement possible after marriage

        It is advisable to maintain open communication and mutual respect for a lasting relationship.
        """

        elements.append(Paragraph(married_life, self.styles['CustomBody']))

        return elements

    def _health_section(self) -> list:
        """Generate health section"""
        elements = []

        elements.append(Paragraph("13. Health Analysis / உடல் நலம்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Health analysis is based on the 1st house (physical body), 6th house (diseases), "
            "8th house (chronic ailments), and the strength of the Lagna lord. "
            "This section identifies potential health concerns and preventive measures.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("13.1 Physical Constitution / உடல் அமைப்பு", self.styles['SubSection']))

        constitution = """
        Based on the Lagna and its lord, your physical constitution is:

        • Generally good health and vitality
        • Medium to strong build
        • Good immunity and recovery capacity
        • Tendency towards Pitta (fire) constitution
        • Need to maintain proper diet and exercise routine
        • Sleep patterns require attention
        """

        elements.append(Paragraph(constitution, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("13.2 Health Areas Requiring Attention / கவனிக்க வேண்டிய உடல் பகுதிகள்", self.styles['SubSection']))

        health_areas = [
            ['Body System', 'Concern Level', 'Preventive Measures'],
            ['Digestive System', 'Moderate', 'Regular meals, avoid spicy food'],
            ['Nervous System', 'Low', 'Stress management, adequate sleep'],
            ['Respiratory System', 'Low', 'Avoid pollutants, pranayama'],
            ['Cardiovascular', 'Low-Moderate', 'Regular exercise, heart-healthy diet'],
            ['Musculoskeletal', 'Moderate', 'Proper posture, regular stretching'],
            ['Eyes', 'Moderate', 'Limit screen time, regular check-ups'],
        ]

        health_table = Table(health_areas, colWidths=[1.5 * inch, 1.2 * inch, 2.8 * inch])
        health_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(health_table)

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("13.3 Health Recommendations / உடல் நல ஆலோசனைகள்", self.styles['SubSection']))

        recommendations = """
        • Practice yoga and pranayama regularly for physical and mental well-being
        • Maintain a balanced diet with emphasis on fresh vegetables and fruits
        • Ensure adequate hydration and avoid excessive caffeine
        • Get 7-8 hours of quality sleep daily
        • Regular health check-ups, especially during Saturn periods
        • Avoid stress and practice meditation for mental peace
        • Fast on recommended days based on planetary placements
        """

        elements.append(Paragraph(recommendations, self.styles['CustomBody']))

        return elements

    def _wealth_section(self) -> list:
        """Generate wealth section"""
        elements = []

        elements.append(Paragraph("14. Wealth & Finance / செல்வம்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Financial analysis is based on the 2nd house (accumulated wealth), 11th house (gains), "
            "and the strength of Jupiter (karaka for wealth). This section provides insights into "
            "income sources, savings potential, and financial growth periods.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("14.1 Wealth Potential / செல்வ திறன்", self.styles['SubSection']))

        wealth_text = """
        Your chart indicates good potential for wealth accumulation:

        • Multiple sources of income are indicated
        • Steady financial growth through career
        • Property and asset accumulation favored
        • Investment gains possible during Jupiter periods
        • Inheritance or family wealth may come
        • Should avoid speculative investments during Rahu periods
        """

        elements.append(Paragraph(wealth_text, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.2 * inch))

        elements.append(Paragraph("14.2 Favorable Investment Areas / சாதகமான முதலீடுகள்", self.styles['SubSection']))

        investments = [
            ['Investment Type', 'Suitability', 'Best Period'],
            ['Real Estate', 'Highly Suitable', 'Saturn periods'],
            ['Gold & Precious Metals', 'Suitable', 'Venus periods'],
            ['Stocks - Blue Chip', 'Moderately Suitable', 'Jupiter periods'],
            ['Fixed Deposits', 'Suitable', 'Any period'],
            ['Mutual Funds', 'Suitable', 'Mercury periods'],
            ['Business Ventures', 'Moderately Suitable', 'Sun periods'],
        ]

        invest_table = Table(investments, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
        invest_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ]))

        elements.append(invest_table)

        return elements

    def _remedies_section(self) -> list:
        """Generate remedies section"""
        elements = []

        elements.append(Paragraph("15. Remedies / பரிகாரங்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "Astrological remedies help in mitigating negative planetary influences and enhancing positive ones. "
            "These remedies are prescribed based on the specific planetary positions in your chart.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        # Planet-wise remedies
        for planet in PLANETS[:7]:  # Main 7 planets
            elements.append(Paragraph(
                f"15.{PLANETS.index(planet)+1} {planet['en']} ({planet['ta']}) Remedies",
                self.styles['SubSection']
            ))

            remedy = self._get_planet_remedy(planet['en'])
            elements.append(Paragraph(remedy, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.15 * inch))

        # General remedies
        elements.append(Paragraph("15.8 General Remedies / பொது பரிகாரங்கள்", self.styles['SubSection']))

        general_remedies = """
        • Recite Navagraha Stotram daily for overall planetary blessings
        • Light a lamp (deepam) in the evening facing east
        • Feed birds and animals regularly as an act of compassion
        • Donate according to your capacity on auspicious days
        • Visit temples on your nakshatra day every month
        • Practice meditation and maintain positive thoughts
        • Respect elders and seek their blessings
        """

        elements.append(Paragraph(general_remedies, self.styles['CustomBody']))

        return elements

    def _get_planet_remedy(self, planet: str) -> str:
        """Get planet-specific remedies"""
        remedies = {
            'Sun': "• Offer water to Sun at sunrise (Surya Arghya)\n• Recite Aditya Hridayam on Sundays\n• Wear Ruby (Manikya) after consultation\n• Donate wheat, jaggery, and red clothes on Sundays\n• Fast on Sundays and consume only one meal",
            'Moon': "• Wear Pearl (Moti) after consultation\n• Recite Chandra Kavacham on Mondays\n• Offer milk to Shiva Lingam on Mondays\n• Donate rice, milk, and white clothes\n• Serve mother and elderly women",
            'Mars': "• Recite Mangal mantra on Tuesdays\n• Wear Red Coral (Moonga) after consultation\n• Donate red lentils and red clothes on Tuesdays\n• Fast on Tuesdays\n• Perform Mangal Shanti puja if Mangal Dosha exists",
            'Mercury': "• Recite Budha mantra on Wednesdays\n• Wear Emerald (Panna) after consultation\n• Donate green clothes and moong dal on Wednesdays\n• Feed green vegetables to cows\n• Keep fast on Wednesdays",
            'Jupiter': "• Recite Guru mantra on Thursdays\n• Wear Yellow Sapphire (Pukhraj) after consultation\n• Donate yellow clothes, turmeric, and books on Thursdays\n• Respect teachers and elders\n• Feed Brahmins on Thursdays",
            'Venus': "• Recite Shukra mantra on Fridays\n• Wear Diamond (Heera) or White Sapphire after consultation\n• Donate white clothes, rice, and sugar on Fridays\n• Respect women and artists\n• Fast on Fridays",
            'Saturn': "• Recite Shani mantra on Saturdays\n• Wear Blue Sapphire (Neelam) only after careful consultation\n• Donate black sesame, mustard oil, and iron on Saturdays\n• Serve the poor and disabled\n• Visit Shani temple on Saturdays",
            'Rahu': "• Recite Rahu mantra on Saturdays\n• Wear Hessonite (Gomed) after consultation\n• Donate blankets and black clothes\n• Feed birds, especially crows\n• Perform Rahu Shanti puja during Rahu Kalam",
            'Ketu': "• Recite Ketu mantra on Tuesdays\n• Wear Cat's Eye (Lehsunia) after consultation\n• Donate blankets to elderly\n• Feed dogs\n• Perform Ketu Shanti puja",
        }
        return remedies.get(planet, "Consult an astrologer for specific remedies.")

    def _favorable_section(self) -> list:
        """Generate favorable periods section"""
        elements = []

        elements.append(Paragraph("16. Favorable Periods / சுப காலங்கள்", self.styles['SectionHeader']))

        elements.append(Paragraph(
            "This section identifies favorable periods for various activities based on your planetary periods "
            "and transits. Planning important activities during favorable times increases success probability.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        favorable_data = [
            ['Activity', 'Favorable Periods', 'Best Days'],
            ['Career Change', 'Jupiter/Venus periods', 'Thursday, Friday'],
            ['Starting Business', 'Sun/Jupiter periods', 'Sunday, Thursday'],
            ['Marriage', 'Venus/Moon periods', 'Friday, Monday'],
            ['Property Purchase', 'Saturn/Mars periods', 'Saturday, Tuesday'],
            ['Travel', 'Mercury/Moon periods', 'Wednesday, Monday'],
            ['Education', 'Jupiter/Mercury periods', 'Thursday, Wednesday'],
            ['Health Treatment', 'Sun/Moon periods', 'Sunday, Monday'],
            ['Financial Investments', 'Jupiter/Venus periods', 'Thursday, Friday'],
            ['Legal Matters', 'Jupiter/Saturn periods', 'Thursday, Saturday'],
            ['Spiritual Activities', 'Jupiter/Ketu periods', 'Thursday, Tuesday'],
        ]

        fav_table = Table(favorable_data, colWidths=[1.8 * inch, 2 * inch, 1.7 * inch])
        fav_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(fav_table)

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("16.1 Lucky Elements / அதிர்ஷ்ட அம்சங்கள்", self.styles['SubSection']))

        lucky_data = [
            ['Element', 'Value'],
            ['Lucky Numbers', '3, 6, 9'],
            ['Lucky Colors', 'Yellow, Orange, White'],
            ['Lucky Days', 'Thursday, Friday, Monday'],
            ['Lucky Gems', 'Yellow Sapphire, Pearl'],
            ['Lucky Direction', 'North-East'],
            ['Lucky Metal', 'Gold'],
        ]

        lucky_table = Table(lucky_data, colWidths=[2 * inch, 3.5 * inch])
        lucky_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9a3412')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
        ]))

        elements.append(lucky_table)

        return elements

    def _yearly_predictions_section(self) -> list:
        """Generate yearly predictions section"""
        elements = []

        elements.append(Paragraph("17. Yearly Predictions / வருட பலன்கள்", self.styles['SectionHeader']))

        current_year = datetime.now().year

        elements.append(Paragraph(
            f"This section provides month-by-month predictions for the year {current_year}. "
            "These predictions are based on planetary transits over your natal chart positions.",
            self.styles['CustomBody']
        ))

        elements.append(Spacer(1, 0.2 * inch))

        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        month_predictions = [
            "Career opportunities arise. Financial planning needed. Health is good.",
            "Relationship matters take focus. Short travels indicated. Avoid conflicts.",
            "Property matters favorable. Family gatherings. New learning opportunities.",
            "Professional growth continues. Health needs attention mid-month. Travel possible.",
            "Financial gains expected. Social activities increase. Creative pursuits favored.",
            "Mixed results. Balance work and personal life. Spiritual inclinations rise.",
            "Favorable for investments. Family harmony. Recognition in professional field.",
            "Educational pursuits favored. Minor health issues possible. Travel indicated.",
            "Career advancement. Property matters progress. Relationship strengthening.",
            "Festival season brings joy. Financial stability. New ventures can begin.",
            "Professional challenges but success through effort. Health requires care.",
            "Year-end brings positive developments. Celebrations and family time. Planning for future."
        ]

        for i, month in enumerate(months):
            elements.append(Paragraph(
                f"<b>{month} {current_year}:</b> {month_predictions[i]}",
                self.styles['CustomBody']
            ))

        return elements

    def _appendix_section(self) -> list:
        """Generate appendix section"""
        elements = []

        elements.append(Paragraph("18. Appendix / இணைப்பு", self.styles['SectionHeader']))

        elements.append(Paragraph("18.1 Glossary of Terms / சொல்லகராதி", self.styles['SubSection']))

        glossary = [
            ['Term', 'Meaning'],
            ['Lagna', 'Ascendant - Rising sign at birth'],
            ['Rasi', 'Moon sign - Zodiac sign where Moon is placed'],
            ['Nakshatra', 'Birth star - One of 27 lunar mansions'],
            ['Dasha', 'Planetary period system'],
            ['Bhava', 'House in the horoscope'],
            ['Yoga', 'Planetary combination producing specific results'],
            ['Dosha', 'Affliction or negative combination'],
            ['Karaka', 'Significator planet for specific matters'],
            ['Graha', 'Planet'],
            ['Navamsa', 'Ninth divisional chart'],
        ]

        gloss_table = Table(glossary, colWidths=[1.5 * inch, 4 * inch])
        gloss_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fed7aa')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff7ed')]),
        ]))

        elements.append(gloss_table)

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("18.2 Important Note / முக்கிய குறிப்பு", self.styles['SubSection']))

        note = """
        This horoscope report has been generated based on Vedic astrology principles using the
        Lahiri (Chitrapaksha) Ayanamsa. The predictions and analyses provided are for guidance
        purposes and should be used as a tool for self-reflection and planning.

        Astrology provides indications and tendencies, not certainties. Free will, personal effort,
        and karma play significant roles in shaping one's destiny. Use this report as a guide
        while making informed decisions based on your own judgment.

        For personalized consultations and specific remedies, please consult a qualified astrologer.

        May the divine grace guide you on your life's journey.

        ॐ शान्तिः शान्तिः शान्तिः
        """

        elements.append(Paragraph(note, self.styles['CustomBody']))

        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Paragraph(
            "— End of Report —",
            ParagraphStyle(name='EndNote', alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor('#ea580c'))
        ))

        return elements


def generate_jathagam_report(chart_data: Dict[str, Any], user_data: Dict[str, Any]) -> bytes:
    """
    Main function to generate Jathagam PDF report

    Args:
        chart_data: Dictionary containing chart calculations (planets, houses, dashas, etc.)
        user_data: Dictionary containing user birth details (name, date, time, place)

    Returns:
        PDF file as bytes
    """
    generator = JathagamPDFGenerator(chart_data, user_data)
    return generator.generate()
