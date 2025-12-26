"""
Comprehensive Traits Data for Jyotish Report Generation
Rich, descriptive content (300-500 words) for storytelling-style reports

Contains:
- RASI_TRAITS: Detailed personality descriptions for all 12 zodiac signs
- NAKSHATRA_TRAITS: Detailed personality descriptions for all 27 nakshatras
- DASHA_LIFE_PREDICTIONS: How life unfolds during each planetary period
- PLANET_IN_HOUSE_EFFECTS: Descriptive effects of planets in houses
- LIFE_AREA_NARRATIVES: Templates for career, marriage, health, wealth sections
"""

# ============== RASI (MOON SIGN) TRAITS ==============
# Each entry contains rich personality description based on Moon placement

RASI_TRAITS = {
    "Aries": {
        "tamil": "மேஷம்",
        "element": "Fire",
        "quality": "Cardinal",
        "lord": "Mars",
        "personality": """You possess the fiery spirit of a natural pioneer, blessed with an innate courage that propels you to take initiative where others hesitate. Your personality radiates with the dynamic energy of Mars, making you a natural leader who thrives on challenges and new beginnings. There is an unmistakable spark in your eyes that reveals your ambitious nature and your refusal to accept defeat.

Your approach to life is marked by directness and honesty. You speak your mind without pretense, and while this candor can sometimes seem blunt to others, it stems from your genuine nature rather than any desire to offend. You value authenticity above social niceties, and you expect the same forthrightness from those around you.

In matters of action, you are swift and decisive. When you see a goal worth pursuing, you charge toward it with remarkable determination. This pioneering spirit means you are often the first to venture into unexplored territories, whether in your career, relationships, or personal development. However, this same impulsiveness can sometimes lead you to act before fully considering the consequences.

Your emotional nature is passionate and intense, though your feelings tend to arise quickly and dissipate just as fast. You rarely hold grudges, preferring to express your anger openly and then move forward. This emotional transparency, while sometimes startling to more reserved individuals, ensures that your relationships remain free of hidden resentments.

Physically, you tend to have abundant energy and a natural athleticism. You may be drawn to competitive sports or physical activities that allow you to channel your Mars-driven vitality. Your constitution is generally robust, though you may be prone to head-related ailments or fevers when stressed.

In relationships, you seek partners who can match your energy and independence. You are fiercely loyal to those you love, though you need space to pursue your individual interests. Your ideal partner understands that your need for independence is not a rejection of intimacy but rather an essential aspect of your nature.""",
        "strengths": ["Leadership", "Courage", "Initiative", "Honesty", "Enthusiasm", "Independence"],
        "weaknesses": ["Impatience", "Impulsiveness", "Short temper", "Selfishness at times", "Restlessness"],
        "career_inclinations": ["Entrepreneurship", "Military", "Sports", "Surgery", "Engineering", "Politics", "Emergency services"],
        "relationship_style": "Passionate, direct, needs independence, fiercely loyal but requires personal space"
    },

    "Taurus": {
        "tamil": "ரிஷபம்",
        "element": "Earth",
        "quality": "Fixed",
        "lord": "Venus",
        "personality": """You embody the steadfast nature of the earth itself, grounded and reliable in ways that others find deeply reassuring. Ruled by Venus, the planet of beauty and pleasure, you possess a refined appreciation for the finer things in life and a natural ability to create comfort and harmony in your surroundings. Your presence brings a sense of stability to any environment you enter.

Your approach to life is methodical and patient. Unlike those who rush toward their goals, you understand that lasting achievements require time and persistent effort. You build your success brick by brick, and what you create tends to endure. This patience extends to your relationships as well, where you prove to be a loyal and dependable partner who values commitment over fleeting passion.

Sensory experiences hold deep meaning for you. You appreciate good food, beautiful music, comfortable textures, and pleasant fragrances. This connection to the physical world keeps you grounded and present, though it can sometimes manifest as attachment to material possessions or resistance to change.

Your emotional nature is calm and stable, like a deep, still lake. You do not easily reveal your feelings, but when you love, you love completely and enduringly. However, when pushed too far or when your security is threatened, you can display the famous Taurus temper - slow to ignite but formidable when aroused.

Financially, you have a natural talent for accumulating and preserving wealth. You understand the value of money and rarely make impulsive purchases. Your practical nature ensures that you build a secure foundation for yourself and your loved ones.

In your physical constitution, you tend toward strength and endurance rather than speed. You may have a strong connection to nature and find peace in gardens, forests, or any place where you can connect with the earth. Your throat and neck areas may require attention, as these are particularly sensitive for your sign.

Your loyalty to friends and family is legendary. Once you commit to someone, you remain devoted through all circumstances. This same quality, however, can sometimes manifest as possessiveness or stubbornness when you feel your relationships or possessions are threatened.""",
        "strengths": ["Reliability", "Patience", "Practicality", "Devotion", "Financial wisdom", "Artistic sense"],
        "weaknesses": ["Stubbornness", "Possessiveness", "Resistance to change", "Materialism", "Slow to act"],
        "career_inclinations": ["Banking", "Real estate", "Agriculture", "Art", "Music", "Culinary arts", "Fashion", "Architecture"],
        "relationship_style": "Devoted, sensual, seeks security, slow to commit but utterly loyal once committed"
    },

    "Gemini": {
        "tamil": "மிதுனம்",
        "element": "Air",
        "quality": "Mutable",
        "lord": "Mercury",
        "personality": """Your mind is your greatest asset, blessed with the quicksilver intelligence of Mercury that allows you to process information with remarkable speed and communicate with exceptional clarity. You are the eternal student of the zodiac, forever curious about the world around you and eager to share your discoveries with others. Your versatility knows few bounds, and you can adapt to almost any situation with ease.

Communication is your native language in more ways than one. You possess a natural gift for expressing ideas, whether through speech, writing, or other forms of expression. Your wit is sharp, your humor engaging, and your ability to connect with people from all walks of life makes you a social butterfly who rarely lacks for company.

Your mind operates on multiple tracks simultaneously. While others focus on one task, you juggle several with apparent ease. This mental agility is one of your greatest strengths, though it can sometimes manifest as restlessness or difficulty seeing projects through to completion. You thrive on variety and may become bored with routine.

Intellectually, you are drawn to ideas themselves rather than their practical applications. You love to learn, discuss, debate, and explore concepts from multiple angles. This makes you an excellent conversationalist and a perpetual source of interesting information. However, you may sometimes prioritize intellectual understanding over emotional depth.

Your dual nature is not duplicity but rather a genuine ability to see multiple perspectives. You can understand opposing viewpoints and often find yourself playing devil's advocate simply to explore all sides of an issue. This same quality can sometimes make decision-making challenging, as you see merit in many options.

In relationships, you need mental stimulation above all else. A partner who can engage your mind, share your love of conversation, and allow you the freedom to explore your varied interests will find in you a charming, entertaining, and endlessly interesting companion.

Your physical energy tends to be nervous and quick rather than sustained. You may find that your hands are always busy, and you express yourself through gestures as much as words. Stress tends to affect your nervous system and respiratory health, making relaxation techniques particularly beneficial for you.""",
        "strengths": ["Intelligence", "Communication", "Adaptability", "Wit", "Versatility", "Social skills"],
        "weaknesses": ["Inconsistency", "Superficiality", "Restlessness", "Indecision", "Nervous energy"],
        "career_inclinations": ["Writing", "Journalism", "Teaching", "Sales", "Marketing", "Translation", "Media", "Technology"],
        "relationship_style": "Intellectually engaging, needs variety and mental connection, can seem emotionally distant"
    },

    "Cancer": {
        "tamil": "கடகம்",
        "element": "Water",
        "quality": "Cardinal",
        "lord": "Moon",
        "personality": """You carry within you the nurturing essence of the Moon, blessed with profound emotional depth and an instinctive ability to care for others. Your sensitivity is both your gift and your challenge, allowing you to perceive the emotional undercurrents that others miss while also making you vulnerable to the moods and energies around you. Home and family form the center of your universe, and you pour your heart into creating a sanctuary for those you love.

Your emotional nature runs deep like the ocean, with currents that shift and change like the lunar cycles that govern your sign. You experience feelings with intensity, from the heights of joy to the depths of melancholy. This emotional range gives you remarkable empathy and the ability to truly understand what others are experiencing.

Memory is powerful for you, and you have a strong connection to the past. You treasure family traditions, ancestral wisdom, and the objects that carry sentimental value. This connection to history provides you with a sense of continuity and belonging, though it can sometimes make letting go of past hurts particularly challenging.

Your protective instincts are legendary. Like the crab that symbolizes your sign, you develop a tough exterior to protect your soft, vulnerable interior. When you sense threat to yourself or your loved ones, you can become surprisingly fierce and determined. Yet beneath this shell, you possess one of the most caring and nurturing hearts in the zodiac.

In matters of the home, you excel at creating comfort and emotional security. You may have natural talents in cooking, decorating, or any activity that transforms a house into a home. Your domestic instincts are strong, and you find genuine fulfillment in caring for family.

Your intuition is highly developed, often manifesting as gut feelings that prove remarkably accurate. You may have psychic sensitivity or at least a powerful ability to read people and situations. Learning to trust this inner knowing while also developing emotional resilience is part of your life's work.

Financially, you tend toward caution and security. You save for the future and are reluctant to take risks with resources that provide for your family's needs. This prudent approach generally serves you well, creating the stability you so deeply need.""",
        "strengths": ["Nurturing", "Intuition", "Loyalty", "Emotional depth", "Protectiveness", "Domestic skills"],
        "weaknesses": ["Moodiness", "Over-sensitivity", "Clinginess", "Living in the past", "Indirect communication"],
        "career_inclinations": ["Nursing", "Childcare", "Real estate", "Hospitality", "Psychology", "History", "Culinary arts", "Social work"],
        "relationship_style": "Deeply nurturing, needs emotional security, forms strong family bonds, can be possessive"
    },

    "Leo": {
        "tamil": "சிம்மம்",
        "element": "Fire",
        "quality": "Fixed",
        "lord": "Sun",
        "personality": """You radiate the magnificent energy of the Sun itself, born to shine and inspire others with your warmth, creativity, and natural authority. There is a regal quality to your presence that commands attention without demanding it, a natural charisma that draws others into your orbit. You possess the heart of a lion - generous, proud, and fiercely protective of those you love.

Your creative spirit burns bright, seeking expression in everything you do. Whether through art, performance, leadership, or simply the way you live your life, you have an innate need to create and to leave your mark on the world. You approach life as if it were a grand stage, and you are determined to play your role with passion and excellence.

Generosity flows naturally from you. You give freely of your time, resources, and affection, finding genuine joy in making others happy. Your warmth can light up a room, and your encouragement has the power to inspire confidence in those who doubt themselves. However, you do expect appreciation in return, and lack of recognition can wound your proud heart.

Your sense of self is strong and central to your identity. You have clear ideas about who you are and what you deserve, and you carry yourself with dignity and self-respect. This self-assurance is generally attractive to others, though it can sometimes be perceived as arrogance, particularly when wounded pride causes you to become domineering.

In leadership, you excel naturally. You have the ability to inspire others with your vision and enthusiasm, and you lead with heart rather than mere authority. Your loyalty to those who serve under you is unwavering, and you take genuine pride in the success of your team.

Romance holds special importance for you. You love with grandeur and passion, showering your beloved with attention, gifts, and affection. You need a partner who appreciates your dramatic expressions of love and who can reciprocate with admiration and devotion.

Your physical vitality is generally strong, connected to the life-giving energy of your ruling Sun. You tend to have a robust constitution, though issues related to the heart or spine may require attention. Regular physical activity that allows you to express your dynamic energy is essential for your wellbeing.""",
        "strengths": ["Creativity", "Leadership", "Generosity", "Confidence", "Warmth", "Loyalty", "Courage"],
        "weaknesses": ["Pride", "Need for attention", "Stubbornness", "Domineering tendencies", "Sensitivity to criticism"],
        "career_inclinations": ["Entertainment", "Politics", "Management", "Teaching", "Arts", "Sports", "Luxury goods", "Gold/jewelry"],
        "relationship_style": "Romantic, generous, needs admiration, loyal and protective, enjoys grand gestures"
    },

    "Virgo": {
        "tamil": "கன்னி",
        "element": "Earth",
        "quality": "Mutable",
        "lord": "Mercury",
        "personality": """You possess the discriminating intelligence of Mercury expressed through the practical lens of earth, giving you an unparalleled ability to analyze, improve, and perfect whatever you touch. Your mind naturally perceives patterns and details that others miss, and you have an innate drive toward excellence that makes you an invaluable contributor in any endeavor. Service to others and the pursuit of purity in all forms are central to your nature.

Your analytical abilities are exceptional. You can break down complex problems into manageable components and find practical solutions that work in the real world. This same faculty extends to your perception of people and situations, where you quickly identify both strengths and areas for improvement. While this discernment is a gift, you must guard against becoming overly critical of yourself and others.

Practicality grounds everything you do. Unlike those who dream without acting, you focus on what can actually be accomplished with the resources at hand. You have little patience for impractical schemes or inefficient methods, and you constantly seek ways to streamline and optimize processes.

Your desire to be of service runs deep. You find genuine fulfillment in helping others and contributing to something larger than yourself. Whether in your career or personal life, you are often the one who quietly ensures that things run smoothly. This service orientation is a beautiful quality, though you must remember to care for yourself as diligently as you care for others.

Health and wellness hold particular interest for you. You are naturally attuned to the body's signals and often drawn to healing arts, nutrition, or fitness. This awareness generally serves you well, though anxiety about health can sometimes become excessive.

In relationships, you express love through practical acts of service and thoughtful attention to your partner's needs. You may not be the most demonstrative romantic, but your care shows in countless small ways - remembering preferences, anticipating needs, and working steadily to improve the life you share.

Your nervous system can be sensitive, and worry is your particular challenge. Learning to accept imperfection - in yourself and in the world - is part of your spiritual journey. When you can combine your gift for analysis with compassion and acceptance, you become a truly helpful presence in the lives of all you touch.""",
        "strengths": ["Analytical mind", "Practicality", "Service orientation", "Attention to detail", "Health consciousness", "Reliability"],
        "weaknesses": ["Over-criticism", "Perfectionism", "Worry", "Excessive modesty", "Difficulty relaxing"],
        "career_inclinations": ["Healthcare", "Accounting", "Research", "Writing", "Nutrition", "Quality control", "Veterinary", "Administration"],
        "relationship_style": "Shows love through service, needs intellectual connection, can be critical, deeply devoted"
    },

    "Libra": {
        "tamil": "துலாம்",
        "element": "Air",
        "quality": "Cardinal",
        "lord": "Venus",
        "personality": """You embody the grace and harmony of Venus expressed through the social realm of air, blessed with natural diplomacy and an aesthetic sense that seeks beauty in all things. Balance is both your gift and your quest - you instinctively work to create equilibrium in relationships, environments, and situations. Your charm and social intelligence make you a natural peacemaker and a valued companion in any setting.

Relationships form the central focus of your life. You understand yourself most clearly through your connections with others, and you invest considerable energy in maintaining harmony in your partnerships. This relational orientation gives you exceptional skills in cooperation and negotiation, though it can sometimes lead to difficulty making decisions independently or standing firm in your own preferences.

Your aesthetic sensibilities are highly refined. You have an innate appreciation for beauty, art, and elegance, and you naturally gravitate toward environments and experiences that please the senses. This appreciation extends to your personal presentation, and you often have excellent taste in fashion, decor, and social graces.

Justice and fairness are deeply important to you. You cannot bear to witness injustice and will often speak up for those who cannot speak for themselves. Your ability to see all sides of an issue makes you an excellent mediator and counselor, though this same quality can sometimes leave you paralyzed with indecision when forced to choose.

Socially, you excel. Your natural charm, diplomatic skills, and genuine interest in others make you popular in almost any setting. You have a gift for making people feel comfortable and valued, and you intuitively understand the unwritten rules of social interaction.

In love, you are romantic and devoted. You seek a true partnership of equals - someone who can be both your best friend and your romantic companion. Harmony in relationships is essential to your wellbeing, and conflict disturbs you deeply.

Your challenge lies in developing your individual identity and learning to assert your own needs. The desire to please others and maintain harmony can sometimes lead you to suppress your true feelings. Finding the balance between accommodation and authenticity is part of your life's journey.""",
        "strengths": ["Diplomacy", "Fairness", "Charm", "Aesthetic sense", "Social intelligence", "Partnership skills"],
        "weaknesses": ["Indecision", "People-pleasing", "Avoiding conflict", "Dependency", "Superficiality at times"],
        "career_inclinations": ["Law", "Diplomacy", "Art", "Fashion", "Interior design", "Counseling", "Public relations", "Beauty industry"],
        "relationship_style": "Seeks true partnership, romantic and devoted, needs harmony, can be indecisive about commitment"
    },

    "Scorpio": {
        "tamil": "விருச்சிகம்",
        "element": "Water",
        "quality": "Fixed",
        "lord": "Mars",
        "personality": """You possess the profound intensity of Mars channeled through the depths of water, giving you penetrating insight and transformative power that sets you apart from all other signs. Nothing about you is superficial - you experience life at its deepest levels and are drawn to explore the mysteries that others fear to approach. Your emotional nature is volcanic, capable of both destruction and the creation of new land.

Your psychological depth is unmatched in the zodiac. You naturally perceive what lies beneath the surface of people and situations, reading hidden motives and unspoken feelings with uncanny accuracy. This penetrating awareness can make you an exceptional therapist, investigator, or strategist, though it can also make it difficult for you to trust others easily.

Transformation is the central theme of your life. You undergo more profound personal metamorphoses than any other sign, repeatedly destroying old versions of yourself to emerge renewed. This process can be painful, but it gives you remarkable resilience and the ability to survive and grow from experiences that would break others.

Your emotional intensity is both your power and your challenge. When you love, you love completely and expect the same total commitment in return. When you are wronged, your capacity for holding grudges can be formidable. Learning to channel your passionate nature constructively is essential to your growth.

Privacy is sacred to you. While you are skilled at uncovering others' secrets, you guard your own carefully. This protective instinct is understandable given your sensitivity, but excessive secretiveness can create barriers to intimacy.

In matters of will and determination, few can match you. Once you set your mind to something, you pursue it with unwavering focus until you achieve your goal or die trying. This intensity can be applied to any field, making you capable of reaching heights of achievement that others cannot imagine.

Sexually and creatively, you possess powerful energy that seeks expression. This force can be channeled into artistic creation, business ventures, or spiritual practice with equal intensity. Learning to manage this potent energy is part of your life's work.""",
        "strengths": ["Intensity", "Insight", "Determination", "Loyalty", "Resourcefulness", "Transformative power"],
        "weaknesses": ["Jealousy", "Secrecy", "Vindictiveness", "Obsession", "Controlling tendencies"],
        "career_inclinations": ["Psychology", "Research", "Investigation", "Medicine", "Surgery", "Finance", "Occult sciences", "Crisis management"],
        "relationship_style": "All-or-nothing commitment, intensely loyal, needs deep emotional bond, can be possessive"
    },

    "Sagittarius": {
        "tamil": "தனுசு",
        "element": "Fire",
        "quality": "Mutable",
        "lord": "Jupiter",
        "personality": """You carry the expansive blessing of Jupiter, filled with optimism, wisdom-seeking, and an adventurous spirit that constantly reaches toward new horizons. Your soul is that of an explorer - whether the territories you seek to discover are geographical, intellectual, or spiritual. Freedom is as essential to you as air, and you cannot thrive when confined by narrow circumstances or limited thinking.

Your philosophical nature sets you apart. You are naturally drawn to the big questions - the meaning of life, the nature of truth, the principles that should guide human conduct. You have an innate teacher's ability to see patterns and share wisdom, and you often find yourself in the role of guide or mentor to others.

Optimism flows through you like a mountain spring. You believe in positive outcomes and approach challenges with confidence that things will work out. This faith in life is genuinely inspiring to those around you, though it can sometimes manifest as overconfidence or failure to prepare for obstacles.

Your love of freedom expresses itself in many ways. You need physical freedom to travel and explore, intellectual freedom to pursue truth wherever it leads, and emotional freedom to express yourself authentically. Attempts to restrict or control you will be met with determined resistance.

Truth matters deeply to you. You value honesty and have difficulty respecting those who deal in deception. Your frankness can sometimes be blunt to the point of tactlessness, but it stems from genuine conviction rather than any desire to wound.

Adventure calls to you constantly. Whether it is a journey to foreign lands, the exploration of a new field of study, or a spiritual quest, you need the stimulation of new experiences to feel fully alive. Routine and predictability drain your spirit.

In relationships, you seek a companion who can share your adventures and respect your need for independence. You are generous and warm-hearted with those you love, though your restless nature can sometimes make commitment challenging. The ideal partner understands that your need for freedom does not diminish your love.""",
        "strengths": ["Optimism", "Wisdom", "Honesty", "Adventurousness", "Generosity", "Philosophical mind"],
        "weaknesses": ["Restlessness", "Tactlessness", "Overconfidence", "Commitment issues", "Preachy tendencies"],
        "career_inclinations": ["Teaching", "Travel industry", "Philosophy", "Religion", "Law", "Publishing", "Sports", "International business"],
        "relationship_style": "Freedom-loving, generous, honest to a fault, needs intellectual and adventurous partner"
    },

    "Capricorn": {
        "tamil": "மகரம்",
        "element": "Earth",
        "quality": "Cardinal",
        "lord": "Saturn",
        "personality": """You embody the disciplined wisdom of Saturn, blessed with ambition, endurance, and the practical intelligence to build lasting achievements. Your approach to life is serious and responsible, and you understand that meaningful success requires sustained effort over time. While others may sprint and tire, you maintain a steady pace that ultimately carries you to heights they cannot reach.

Ambition drives you, but it is not the flashy ambition of ego - rather, it is a deep-seated need to accomplish something of lasting value. You set high standards for yourself and work methodically toward your goals, undeterred by obstacles that would discourage lesser souls. Your patience in pursuing long-term objectives is remarkable.

Responsibility comes naturally to you. Even from a young age, you likely took on duties beyond your years, and others have always sensed that they can depend on you. This reliability is one of your greatest assets, though the weight of responsibility can sometimes feel heavy on your shoulders.

Your practical wisdom is exceptional. You understand how the world actually works, not how it should work in theory. This realism allows you to navigate systems effectively and to build on solid foundations. You rarely waste resources on impractical ventures.

Structure and tradition hold meaning for you. You respect established systems and understand the value of institutions that have stood the test of time. This respect for order can make you somewhat conservative, but it also gives you a solid foundation from which to operate.

Authority is something you understand instinctively, both how to exercise it and how to work within hierarchies. You have natural leadership abilities, though your style is more that of the seasoned executive than the charismatic visionary.

In relationships, you are loyal and committed, though you may struggle to express emotions openly. You show love through practical support and long-term dedication rather than romantic gestures. Finding a partner who appreciates your steady devotion and understands your reserved nature is essential.

Your greatest challenge is learning to balance ambition with enjoyment of life. Saturn's influence can make you too focused on duty and achievement at the expense of pleasure and relaxation. Remember that rest is not laziness - it is necessary for sustained excellence.""",
        "strengths": ["Discipline", "Ambition", "Responsibility", "Practicality", "Endurance", "Leadership"],
        "weaknesses": ["Pessimism", "Rigidity", "Workaholism", "Emotional coldness", "Excessive seriousness"],
        "career_inclinations": ["Business", "Government", "Management", "Finance", "Architecture", "Engineering", "Administration", "Traditional professions"],
        "relationship_style": "Committed and loyal, shows love through actions, reserved emotionally, needs respect and stability"
    },

    "Aquarius": {
        "tamil": "கும்பம்",
        "element": "Air",
        "quality": "Fixed",
        "lord": "Saturn",
        "personality": """You are touched by the progressive vision of Saturn expressed through the realm of ideas, making you a natural humanitarian with a unique perspective on human potential. Your mind operates on a different frequency than most, perceiving possibilities and patterns that remain invisible to conventional thinkers. You are here to contribute to human progress and to champion the causes of freedom and equality.

Your intellectual independence is remarkable. You form your own opinions through careful analysis rather than accepting received wisdom, and you are not swayed by peer pressure or popular opinion. This independent thinking can make you seem eccentric to conventional minds, but it is the source of your original contributions.

Humanitarian ideals guide your life. You genuinely care about the welfare of humanity as a whole and feel called to contribute to social progress. This orientation can sometimes make you more comfortable with abstract humanity than with messy individual relationships, but at its best, it motivates you to work for a better world.

Friendship holds special importance for you. You value your network of connections and often find your deepest bonds in friendships rather than romantic relationships. You are loyal to your friends and treat them as equals regardless of their social status.

Your vision for the future is clear and compelling. You can see how things could be improved and are willing to experiment with new approaches to achieve better results. This forward-thinking quality makes you a natural innovator and reformer.

Detachment is both your strength and your challenge. Your ability to remain objective allows you to see situations clearly and to avoid being overwhelmed by emotions. However, this same detachment can sometimes create distance in intimate relationships, where partners may long for more emotional warmth.

In relationships, you need a partner who can be your intellectual equal and who respects your need for independence. You are more interested in a meeting of minds than in conventional romance, and you thrive with a partner who shares your ideals and supports your humanitarian work.

Your challenge is to balance your natural detachment with genuine emotional connection. Learning to express warmth while maintaining your intellectual integrity is part of your growth.""",
        "strengths": ["Originality", "Humanitarianism", "Independence", "Intellect", "Progressiveness", "Objectivity"],
        "weaknesses": ["Detachment", "Stubbornness", "Unpredictability", "Emotional aloofness", "Rebelliousness"],
        "career_inclinations": ["Technology", "Science", "Social work", "Politics", "Astrology", "Aviation", "Invention", "Non-profits"],
        "relationship_style": "Values friendship in love, needs intellectual connection, emotionally detached, fiercely independent"
    },

    "Pisces": {
        "tamil": "மீனம்",
        "element": "Water",
        "quality": "Mutable",
        "lord": "Jupiter",
        "personality": """You swim in the cosmic ocean of consciousness, blessed with imagination, compassion, and spiritual sensitivity that connects you to dimensions beyond the ordinary. Jupiter's wisdom expresses through you as intuitive understanding and creative vision, while your water nature gives you profound empathy for all beings. You are here to dream, to heal, and to remind others of the sacred dimensions of existence.

Your compassion knows no bounds. You feel the suffering of others as if it were your own and are naturally drawn to help those in need. This sensitivity is a beautiful gift, though you must learn to establish healthy boundaries to avoid being overwhelmed by the world's pain.

Imagination flows through you like water through a river delta, branching into countless creative channels. Whether expressed through art, music, writing, or other creative forms, this imaginative capacity is one of your greatest gifts. You have access to inspiration that comes from beyond the rational mind.

Your intuition is highly developed, often manifesting as psychic sensitivity or at least a powerful ability to sense what cannot be seen. You pick up on subtle energies and emotional undercurrents, and your dreams may carry significant meaning or prophetic content.

Spirituality is natural to you. You may feel drawn to meditation, mysticism, or other practices that connect you with transcendent reality. Even if you do not follow a formal spiritual path, you sense that there is more to life than material existence.

Your boundaries can be fluid, which is both a gift and a challenge. This permeability allows you to merge with others in profound intimacy and to access creative inspiration, but it can also make you vulnerable to absorbing negative energies or losing yourself in relationships.

In love, you are romantic and devoted, capable of profound spiritual union with your partner. You may idealize loved ones or sacrifice too much for their sake. Finding a partner who appreciates your sensitivity without exploiting it is essential.

Your greatest challenge is learning to function in the practical world while maintaining your spiritual vision. You may tend toward escapism when reality becomes too harsh. Developing grounding practices while honoring your transcendent nature is part of your life's work.""",
        "strengths": ["Compassion", "Intuition", "Creativity", "Spirituality", "Adaptability", "Healing abilities"],
        "weaknesses": ["Escapism", "Over-sensitivity", "Victim mentality", "Lack of boundaries", "Impracticality"],
        "career_inclinations": ["Arts", "Music", "Healing", "Spirituality", "Psychology", "Photography", "Film", "Charitable work"],
        "relationship_style": "Deeply romantic, spiritually connected, needs emotional depth, can be self-sacrificing"
    }
}


# ============== NAKSHATRA TRAITS ==============
# Detailed personality descriptions for all 27 nakshatras

NAKSHATRA_TRAITS = {
    "Ashwini": {
        "tamil": "அசுவினி",
        "lord": "Ketu",
        "deity": "Ashwini Kumaras",
        "symbol": "Horse head",
        "guna": "Rajas",
        "personality": """Born under the swift energy of Ashwini, you possess the healing touch and pioneering spirit of the divine physicians. Like the celestial horses that symbolize your birth star, you are quick, energetic, and always ready to race toward new beginnings. Your soul carries an innate desire to heal, help, and bring about miraculous transformations in the lives of others.

Your nature is marked by spontaneous enthusiasm and youthful vitality that rarely dims regardless of your actual age. You approach life with freshness and optimism, seeing possibilities where others see obstacles. This pioneering quality often places you at the forefront of new ventures, first to try what others fear to attempt.

Speed and efficiency characterize your actions. You dislike delays and complicated procedures, preferring direct approaches that yield quick results. This impatience can sometimes lead to hasty decisions, but more often it simply means you accomplish in hours what takes others days.

The healing abilities bestowed by your nakshatra's ruling deities manifest in various ways. You may be drawn to medical or therapeutic professions, or you may simply have a natural ability to make others feel better through your presence and encouragement. Even your words carry healing power.

Your independence is strong, and you resist being controlled or constrained by others. You need freedom to act on your impulses and follow your own path. Attempts to restrict you will be met with determined resistance.

In relationships, you are passionate and direct, pursuing your beloved with the same enthusiasm you bring to all endeavors. However, you may need to cultivate patience and learn to appreciate slower, more gradual developments in love.

Your challenges include managing your impulsive nature and learning to complete what you start before racing to the next adventure. Developing patience while maintaining your beautiful spontaneity is part of your life's growth.""",
        "career_strengths": ["Medicine", "Emergency services", "Sports", "Entrepreneurship", "Veterinary", "Physical therapy"],
        "relationship_nature": "Enthusiastic and direct in love, needs independence, can be impatient with slow-developing relationships"
    },

    "Bharani": {
        "tamil": "பரணி",
        "lord": "Venus",
        "deity": "Yama",
        "symbol": "Yoni/Womb",
        "guna": "Rajas",
        "personality": """The powerful nakshatra of Bharani has gifted you with the ability to hold and transform life itself. Ruled by Venus and presided over by Yama, the god of death and dharma, you carry the profound understanding that creation and destruction are two faces of the same cosmic process. This awareness gives you unique perspective and remarkable resilience.

Your capacity to bear burdens and responsibilities is exceptional. Like the womb that symbolizes your nakshatra, you can carry weight that would crush others, nurturing what grows within you until it is ready to emerge. This makes you invaluable in crisis situations and positions of heavy responsibility.

Your sensual nature is strong, blessed by Venus with appreciation for pleasure, beauty, and the arts. You experience life intensely through your senses and seek experiences that engage you fully. This vitality can sometimes be perceived as excessive by more restrained temperaments.

The influence of Yama gives you natural understanding of dharma - the moral order that governs existence. You have strong convictions about right and wrong and may find yourself in positions where you must make difficult judgments. Your sense of justice is keen, sometimes severe.

Transformation is your special power. You can take raw, chaotic material - whether in projects, relationships, or your own character - and shape it into something meaningful. This creative-destructive capacity extends to helping others through their own transformations.

Your emotional intensity runs deep. You love and hate with equal passion, and you do not easily forget those who have wronged you. Learning to channel this intensity constructively is essential to your growth.

In relationships, you are devoted and passionate, capable of profound intimacy. You need a partner who can match your intensity and who is not frightened by the depth of your emotional nature.""",
        "career_strengths": ["Psychology", "Crisis management", "Midwifery", "Therapy", "Arts", "Entertainment industry"],
        "relationship_nature": "Intensely passionate, deeply devoted, needs emotional depth, can be possessive"
    },

    "Krittika": {
        "tamil": "கார்த்திகை",
        "lord": "Sun",
        "deity": "Agni",
        "symbol": "Razor/Flame",
        "guna": "Rajas",
        "personality": """Born under the blazing light of Krittika, you carry the purifying fire of Agni within your soul. Like the divine flame that burns away impurities, you have a sharp, penetrating nature that cuts through deception and reveals truth. Your presence can be warming and illuminating or burning and harsh, depending on how you choose to express your considerable power.

Your intellect is sharp as the razor that symbolizes your nakshatra. You have the ability to analyze situations with precision and to separate essential truths from superficial appearances. This discriminating capacity makes you excellent in any field requiring critical judgment.

Truth and authenticity are paramount to you. You cannot tolerate deception and will speak honestly even when the truth is uncomfortable. This directness can win you respect from those who value authenticity, though it may create conflicts with those who prefer comfortable illusions.

The nurturing aspect of fire also lives within you. Like the flame that cooks food and makes it nourishing, you have the capacity to take raw potential and refine it into something valuable. You may excel as a teacher, mentor, or guide who helps others develop their abilities.

Your sense of righteousness is strong, and you feel compelled to fight against injustice and protect those who cannot protect themselves. This warrior quality can make you formidable in defense of what you believe is right.

Physical warmth and vital energy are your gifts. You tend to have strong digestion and robust health, and you radiate a warmth that others find compelling. Your passionate nature extends to all areas of life.

In relationships, you need a partner who can appreciate your intensity and who is not diminished by your strong personality. You are loyal and protective but expect the same commitment in return.""",
        "career_strengths": ["Military", "Leadership", "Cooking", "Metallurgy", "Teaching", "Spiritual guidance"],
        "relationship_nature": "Passionate and protective, needs honest communication, can be too critical at times"
    },

    "Rohini": {
        "tamil": "ரோகிணி",
        "lord": "Moon",
        "deity": "Brahma",
        "symbol": "Cart/Chariot",
        "guna": "Rajas",
        "personality": """Rohini, the beloved of the Moon, has blessed you with beauty, charm, and the creative power of Brahma himself. You are naturally attractive, drawing others to you with an almost magnetic quality that goes beyond mere physical appearance. Your presence evokes the lush fertility of the earth and the nurturing coolness of moonlight.

Your creative abilities are exceptional. Like Brahma the creator, you have the power to bring new things into existence - whether children, artistic works, business ventures, or new ways of living. Growth and abundance seem to follow wherever you focus your attention.

Material comfort and security matter greatly to you. You appreciate fine things and work to create a beautiful, comfortable environment for yourself and those you love. This is not mere materialism but a genuine need for stability and physical wellbeing.

Your sensual nature is pronounced. You experience the world through your senses and take genuine pleasure in good food, beautiful surroundings, pleasant fragrances, and the touch of those you love. This embodied appreciation for life's pleasures is a gift, though it requires balance.

The fixed, grounded quality of your nakshatra gives you persistence and determination. Once you set your mind on something, you work steadily toward it without wavering. This stability is reassuring to those around you.

Your emotional nature is deep and responsive, like the fertile earth responding to moon and rain. You feel things strongly and need emotional nourishment just as the body needs food.

In relationships, you are devoted and sensual, creating a luxurious environment of love for your partner. You need stability and commitment, and you offer the same in return. Your ideal partner appreciates your creative nature and shares your love of comfort and beauty.""",
        "career_strengths": ["Agriculture", "Fashion", "Beauty industry", "Arts", "Real estate", "Hospitality"],
        "relationship_nature": "Romantic and sensual, deeply devoted, needs security, can be possessive"
    },

    "Mrigashira": {
        "tamil": "மிருகசீரிடம்",
        "lord": "Mars",
        "deity": "Soma",
        "symbol": "Deer head",
        "guna": "Tamas",
        "personality": """Like the gentle deer that symbolizes your nakshatra, you possess a curious, searching nature combined with sensitivity and grace. Ruled by Mars yet presided over by the cooling Soma, you embody the meeting of opposites - the warrior's energy tamed by lunar gentleness. Your life is a constant quest for that which will truly satisfy your seeking soul.

Curiosity drives you forward through life. You are never content with surface understanding but must explore, investigate, and discover what lies beneath appearances. This searching quality leads you on many journeys, both physical and intellectual, always seeking the next horizon.

Your sensitivity is notable. You perceive subtleties that others miss and respond to your environment with delicate awareness. This sensitivity makes you an excellent judge of situations and people, though it also means you can be easily wounded.

The deer's alertness lives in you - you are quick to sense danger or opportunity and respond swiftly. This vigilance serves you well but can sometimes manifest as anxiety or excessive caution.

Your romantic and idealistic nature seeks the perfect love, the perfect experience, the perfect understanding. This quest for perfection drives much of your achievement but can also lead to dissatisfaction with imperfect reality.

Grace characterizes your movements and manner. There is something refined and elegant about your presence that others find attractive. You move through life with a light touch, preferring persuasion to force.

In relationships, you are romantic and idealistic, seeking the soulmate who will end your searching. You need a partner who can engage both your mind and your heart, and who appreciates your gentle yet questing nature.""",
        "career_strengths": ["Research", "Travel", "Writing", "Music", "Textiles", "Perfumery", "Teaching"],
        "relationship_nature": "Romantic seeker, gentle yet passionate, needs intellectual stimulation, can be restless"
    },

    "Ardra": {
        "tamil": "திருவாதிரை",
        "lord": "Rahu",
        "deity": "Rudra",
        "symbol": "Teardrop/Diamond",
        "guna": "Tamas",
        "personality": """Born under the storm star Ardra, you carry within you the tempestuous power of Rudra, the howling form of Shiva. Your nature includes both the destruction of the storm and the renewal that follows rain. You have the capacity to tear down what is old and create space for what is new, making you a force of transformation.

Your intellect is sharp and penetrating, given unusual power by Rahu's influence. You can see through pretense and analyze situations with almost ruthless clarity. This mental acuity makes you formidable in debate or any arena requiring critical thinking.

Emotional intensity characterizes your inner life. You feel things deeply and may experience storms of emotion that reflect your nakshatra's tempestuous nature. Learning to ride these waves without being overwhelmed is part of your life's work.

The transformative power of your nakshatra means you often experience significant life changes. What seems like destruction is often necessary clearing for new growth. You have the resilience to survive upheavals that would break others.

Your capacity for hard work is remarkable. When you focus your considerable energy on a task, you can accomplish tremendous things. The challenge is directing this power constructively.

Truth matters to you, and you may have little patience for social niceties that mask reality. Your directness can be challenging for some, but those who value authenticity appreciate your honesty.

In relationships, you need a partner who can weather your storms and appreciate the depth of your nature. You offer intense loyalty and passion but require the same in return.""",
        "career_strengths": ["Research", "Technology", "Psychology", "Engineering", "Sciences", "Investigation"],
        "relationship_nature": "Intense and transformative, needs deep emotional connection, can be stormy but loyal"
    },

    "Punarvasu": {
        "tamil": "புனர்பூசம்",
        "lord": "Jupiter",
        "deity": "Aditi",
        "symbol": "Bow and quiver",
        "guna": "Tamas",
        "personality": """Blessed by Jupiter and the cosmic mother Aditi, you possess the gift of renewal and return. Like the arrow that can be shot again and again, you have remarkable ability to recover from setbacks and begin anew. Your nature is essentially optimistic, trusting in the benevolence of the universe to provide what you need.

Your generosity of spirit is notable. You share freely of your resources, wisdom, and support, trusting that what you give will return to you multiplied. This generous nature attracts abundance and goodwill.

Home and family hold deep importance for you. You have strong nurturing instincts and work to create security for those you love. The cosmic mother's influence gives you protective, caring qualities.

Your philosophical nature seeks understanding of life's deeper meanings. You are naturally drawn to spiritual wisdom and may serve as a guide or teacher for others on their journeys.

The returning quality of your nakshatra means you often revisit themes, places, and people throughout your life. What was lost can be found; what was broken can be healed.

Your optimism is genuine and infectious. You believe in positive outcomes and this faith often creates the conditions for good fortune to manifest.

In relationships, you are nurturing and devoted, creating a safe harbor for those you love. You need a partner who appreciates your caring nature and shares your values of home and family.""",
        "career_strengths": ["Teaching", "Counseling", "Spirituality", "Publishing", "Hospitality", "Real estate"],
        "relationship_nature": "Nurturing and optimistic, values home and family, needs stability, generous in love"
    },

    "Pushya": {
        "tamil": "பூசம்",
        "lord": "Saturn",
        "deity": "Brihaspati",
        "symbol": "Flower/Circle",
        "guna": "Tamas",
        "personality": """Pushya, considered the most auspicious of all nakshatras, has blessed you with the capacity to nourish and support growth in all its forms. Under Saturn's discipline and Brihaspati's wisdom, you embody the highest potential for selfless service and the cultivation of excellence. Your nature is essentially nurturing, seeking to help others flourish.

Your capacity for hard work and sustained effort is exceptional. Saturn's influence gives you patience and endurance, while Jupiter's wisdom ensures your efforts are directed toward worthy goals. You understand that meaningful achievement requires time and persistence.

Service to others comes naturally to you. You find genuine fulfillment in contributing to the welfare of your family, community, and the larger world. This service orientation is your path to spiritual growth.

Your practical wisdom allows you to find effective solutions to complex problems. You combine idealism with realism, dreaming of what could be while working skillfully with what is.

The nurturing quality of your nakshatra extends to all life. You may feel drawn to care for plants, animals, children, or any beings who need protection and support.

Your emotional stability provides a calm center for those around you. In times of crisis, others naturally turn to you for guidance and reassurance.

In relationships, you are devoted and reliable, offering the steady support that allows your partner to thrive. You need a partner who appreciates your giving nature and who contributes equally to the relationship.""",
        "career_strengths": ["Education", "Agriculture", "Healthcare", "Social work", "Management", "Counseling"],
        "relationship_nature": "Nurturing and devoted, needs to feel appreciated, steady and reliable in love"
    },

    "Ashlesha": {
        "tamil": "ஆயில்யம்",
        "lord": "Mercury",
        "deity": "Nagas",
        "symbol": "Coiled serpent",
        "guna": "Tamas",
        "personality": """Born under the mysterious influence of Ashlesha, you carry the wisdom and power of the Nagas - the serpent beings of ancient lore. Your nature is penetrating and perceptive, able to perceive hidden truths and navigate the shadowy realms that others fear to enter. Mercury's intelligence combines with serpentine wisdom to give you exceptional insight.

Your psychological acuity is remarkable. You understand the hidden motivations that drive human behavior and can read people with unusual accuracy. This insight can be used for healing or manipulation - the choice is yours.

The transformative power of the serpent lives within you. Like the snake that sheds its skin, you have the capacity for profound personal transformation and renewal.

Your grip on what you value is tenacious. Once you commit to a person, goal, or belief, you hold on with the determination of a coiled serpent. This persistence is valuable but must be balanced with knowing when to let go.

Mystery surrounds you, and you may be drawn to esoteric knowledge, hidden sciences, or the exploration of consciousness. The serpent's wisdom is yours to access.

Your sensuality is deep and powerful, reflecting the kundalini energy that the serpent symbolizes. This vital force can be channeled into creative, spiritual, or physical expression.

In relationships, you form deep attachments and expect the same commitment in return. You need a partner who can handle your intensity and who appreciates your complex nature.""",
        "career_strengths": ["Psychology", "Research", "Healing arts", "Astrology", "Investigation", "Politics"],
        "relationship_nature": "Intense and possessive, deeply loyal, needs complete trust, can be jealous"
    },

    "Magha": {
        "tamil": "மகம்",
        "lord": "Ketu",
        "deity": "Pitris",
        "symbol": "Throne/Royal chamber",
        "guna": "Tamas",
        "personality": """Magha bestows upon you the dignity of royal lineage and connection to ancestral wisdom. Ruled by Ketu and presided over by the Pitris (ancestral spirits), you carry within you the weight and privilege of heritage. Your nature is noble and authoritative, commanding respect through inherent dignity rather than force.

Leadership comes naturally to you. You have the bearing of one born to authority, and others instinctively recognize your capacity to guide and protect. This regal quality sets you apart in any group.

Connection to ancestors and tradition runs deep in your consciousness. You may feel strongly linked to your family lineage and called to honor those who came before you. This ancestral awareness provides both guidance and responsibility.

Your sense of honor and dignity is pronounced. You cannot tolerate insult or disrespect and expect to be treated with the consideration your nature deserves. This pride, when balanced, gives you noble bearing; when excessive, it can create conflicts.

Material success and recognition often come to you, as your nakshatra carries the energy of accomplishment and worldly achievement. You are meant to hold positions of influence.

The spiritual detachment of Ketu combines with worldly power in your nature. You may achieve great success while maintaining awareness that material accomplishment is not the ultimate goal.

In relationships, you need a partner who respects your dignity and shares your values. You are generous and protective with those you love, offering the security of your strength.""",
        "career_strengths": ["Leadership", "Government", "Management", "History", "Genealogy", "Politics"],
        "relationship_nature": "Noble and protective, expects respect, generous with loved ones, needs admiration"
    },

    "Purva Phalguni": {
        "tamil": "பூரம்",
        "lord": "Venus",
        "deity": "Bhaga",
        "symbol": "Hammock/Couch",
        "guna": "Tamas",
        "personality": """Blessed by Venus and the god of good fortune Bhaga, you are born for pleasure, creativity, and the enjoyment of life's gifts. Purva Phalguni bestows charm, artistic talent, and the ability to create beauty and happiness wherever you go. Your nature is essentially joyful, seeking to experience and share the sweetness of existence.

Your creative abilities are exceptional. Whether in art, music, performance, or any form of creative expression, you have natural talent and the charisma to share your gifts with others.

Pleasure and enjoyment are not merely indulgences for you but essential aspects of your nature. You understand that life is meant to be savored, and you have the capacity to find joy in simple experiences.

Your social nature draws others to you. You are charming, attractive, and naturally popular. Parties and social gatherings come alive with your presence.

Romance holds special importance for you. You are deeply romantic, approaching love with creativity and passion. Your ideal relationship includes both sensual pleasure and emotional connection.

The relaxation symbolized by your nakshatra's hammock is necessary for your wellbeing. You need time for leisure and pleasure to function at your best.

Generosity flows naturally from you. You share your resources, talents, and joy freely with those you love.

In relationships, you are romantic, creative, and devoted. You need a partner who appreciates beauty and pleasure as you do and who can match your capacity for love.""",
        "career_strengths": ["Arts", "Entertainment", "Music", "Hospitality", "Beauty industry", "Diplomacy"],
        "relationship_nature": "Romantic and creative, seeks pleasure in love, generous, needs affection and beauty"
    },

    "Uttara Phalguni": {
        "tamil": "உத்திரம்",
        "lord": "Sun",
        "deity": "Aryaman",
        "symbol": "Bed/Hammock",
        "guna": "Sattva",
        "personality": """Born under the auspicious light of Uttara Phalguni, you possess the noble qualities of friendship, generosity, and righteous leadership. The Sun's radiance and Aryaman's patronage give you natural authority combined with genuine concern for others' welfare. You are meant to lead through service and to prosper through generosity.

Your capacity for genuine friendship is exceptional. You form lasting bonds based on mutual respect and support, and you are loyal to your friends through all circumstances. Others know they can depend on you.

Leadership comes naturally, but it is the leadership of service rather than domination. You inspire others through example and create environments where everyone can thrive.

Material prosperity often follows you, as your nakshatra carries the blessing of abundance. You have the ability to earn and to attract resources, which you use generously for the benefit of all.

Your nature is essentially noble and dignified. You maintain high standards for yourself and inspire others to rise to their potential.

Contract and agreement are themes in your life. You understand the importance of keeping your word and honoring commitments, and you expect the same from others.

The combination of personal success and service to others defines your path. You prosper by helping others prosper.

In relationships, you are reliable, generous, and committed. Marriage is often especially important for you, and you take partnership seriously. You need a partner who shares your values and appreciates your loyal nature.""",
        "career_strengths": ["Management", "Government", "Social service", "Law", "Counseling", "Business"],
        "relationship_nature": "Committed and generous, values marriage, reliable partner, needs mutual respect"
    },

    "Hasta": {
        "tamil": "அஸ்தம்",
        "lord": "Moon",
        "deity": "Savitar",
        "symbol": "Hand/Palm",
        "guna": "Sattva",
        "personality": """Hasta has blessed you with the magical hands of Savitar, the solar deity who sets things in motion. Your manual dexterity and ability to craft, heal, and create with your hands is exceptional. The Moon's influence adds intuition and emotional sensitivity to your skillful nature.

Your hands are your instruments of power. Whether you work as a healer, artist, craftsperson, or in any profession requiring manual skill, your hands seem to carry their own intelligence.

Adaptability is one of your greatest strengths. You can adjust to circumstances and turn situations to your advantage with remarkable ease. This resourcefulness serves you well in challenging times.

Your wit and humor brighten any gathering. You have the ability to find levity even in difficult situations and to help others see the lighter side of life.

Attention to detail characterizes your work. You notice the small things that others miss and have the patience to perfect your craft through careful attention.

The Moon's influence gives you sensitivity to others' feelings and needs. You can sense what is needed and respond with appropriate care.

In relationships, you express love through touch and practical care. You are attentive to your partner's needs and skilled at creating comfort and pleasure.""",
        "career_strengths": ["Crafts", "Healing", "Manufacturing", "Counseling", "Comedy", "Magic"],
        "relationship_nature": "Caring and attentive, expresses love through touch and service, adaptable partner"
    },

    "Chitra": {
        "tamil": "சித்திரை",
        "lord": "Mars",
        "deity": "Tvashtar",
        "symbol": "Bright jewel/Pearl",
        "guna": "Sattva",
        "personality": """Born under the brilliant light of Chitra, you carry within you the creative fire of Tvashtar, the divine architect. Your nature combines artistic vision with the energy to manifest your designs in the world. Like the gem that symbolizes your nakshatra, you are meant to shine brightly and attract admiration.

Your creative abilities are exceptional, particularly in visual arts, design, and architecture. You have natural aesthetic sense and the practical ability to create beautiful things.

Physical attractiveness often accompanies this nakshatra. You tend to be beautiful or handsome and know how to present yourself to advantage.

Your ambition drives you toward excellence. You are not content with mediocrity in yourself or your creations. This perfectionism produces remarkable work but may sometimes create frustration.

The warrior energy of Mars gives you the courage to pursue your vision despite obstacles. You fight for your creative dreams with determination.

You see beauty and potential everywhere. Your vision transforms the ordinary into the extraordinary, and you cannot rest until you have brought your vision into reality.

In relationships, you seek a partner who can appreciate and match your aesthetic sensibilities. You create beauty in your relationships as in all areas of life.""",
        "career_strengths": ["Architecture", "Design", "Art", "Jewelry", "Engineering", "Fashion"],
        "relationship_nature": "Passionate and creative, seeks beauty in partnership, can be demanding, deeply romantic"
    },

    "Swati": {
        "tamil": "சுவாதி",
        "lord": "Rahu",
        "deity": "Vayu",
        "symbol": "Coral/Sword",
        "guna": "Sattva",
        "personality": """Swati, ruled by Rahu and blessed by Vayu the wind god, has given you the gift of freedom and the ability to move through life with independence and flexibility. Like the wind, you cannot be contained or controlled; your spirit requires the freedom to explore and expand in all directions.

Independence is central to your nature. You need the freedom to pursue your own path, make your own decisions, and live by your own values. Attempts to control you meet with determined resistance.

Your business acumen is notable. You have natural talent for commerce and the ability to identify profitable opportunities. This commercial sense often leads to financial success.

Flexibility and adaptability help you navigate life's changes. Like the wind, you can shift direction as needed without losing your essential nature.

Balance is important to you, represented by the scales of Libra where Swati resides. You seek equilibrium in all areas of life and can help others find middle ground.

Your diplomatic skills allow you to move easily in different social environments. You can adapt your approach to suit the company without losing authenticity.

In relationships, you need a partner who respects your independence while providing emotional connection. You are devoted when your freedom is honored.""",
        "career_strengths": ["Business", "Trade", "Law", "Diplomacy", "Travel", "Air/wind related fields"],
        "relationship_nature": "Independent yet devoted, needs freedom, seeks balanced partnership, diplomatic in love"
    },

    "Vishakha": {
        "tamil": "விசாகம்",
        "lord": "Jupiter",
        "deity": "Indra-Agni",
        "symbol": "Triumphal arch/Potter's wheel",
        "guna": "Sattva",
        "personality": """Vishakha, ruled by Jupiter and blessed by the combined powers of Indra and Agni, gives you singular determination to achieve your goals. Your nature is focused and purposeful, pursuing objectives with unwavering concentration until success is achieved. You are meant for conquest and triumph.

Your determination is legendary. Once you set a goal, you pursue it with focus that borders on obsession. This single-mindedness produces remarkable achievements but requires balance.

Courage characterizes your approach to challenges. You are willing to fight for what you want and do not back down from opposition.

The combination of Jupiter's wisdom and Indra's power gives you natural leadership abilities. You can inspire others to join your cause and lead them to victory.

Transformation is a theme in your life. Like the potter's wheel that reshapes clay, you have the power to remake yourself and your circumstances.

Your passionate nature extends to all areas of life. You pursue love, work, and spiritual growth with equal intensity.

In relationships, you are devoted and passionate, but your focus on goals may sometimes compete with attention to partnership. You need a partner who understands your driven nature and supports your ambitions.""",
        "career_strengths": ["Leadership", "Politics", "Military", "Sports", "Research", "Sales"],
        "relationship_nature": "Passionate and determined, devoted but goal-focused, needs supportive partner"
    },

    "Anuradha": {
        "tamil": "அனுஷம்",
        "lord": "Saturn",
        "deity": "Mitra",
        "symbol": "Lotus/Staff",
        "guna": "Sattva",
        "personality": """Anuradha has blessed you with the divine gift of friendship and the ability to succeed far from your place of birth. Under Saturn's discipline and Mitra's blessing of alliance, you form bonds that endure through all circumstances. Like the lotus that blooms in murky waters, you find beauty and meaning in difficult conditions.

Your capacity for friendship is exceptional. You form deep, lasting bonds and are loyal to your friends through all circumstances. Others know they can depend on you.

Success often comes to you away from home. You have the ability to thrive in foreign environments and may find your greatest opportunities far from your birthplace.

Organization and discipline characterize your approach. Saturn's influence gives you the patience and structure needed for long-term success.

Despite your reserved exterior, you possess deep emotional capacity. You feel things profoundly but may not always show it.

Spiritual aspiration runs through your nature. You seek meaning beyond material success and may be drawn to devotional or mystical practices.

In relationships, you are devoted and loyal, forming bonds that deepen with time. You need a partner who can appreciate your depth and return your loyalty.""",
        "career_strengths": ["Organization", "Research", "International business", "Astrology", "Mining", "Insurance"],
        "relationship_nature": "Deeply loyal, devoted friend and partner, reserved but emotionally deep, needs trust"
    },

    "Jyeshtha": {
        "tamil": "கேட்டை",
        "lord": "Mercury",
        "deity": "Indra",
        "symbol": "Earring/Umbrella",
        "guna": "Sattva",
        "personality": """Born under Jyeshtha, you carry the mantle of the eldest, the firstborn, the one who leads and protects. Mercury's intelligence combines with Indra's kingship to give you natural authority and the mental acuity to exercise it wisely. Your nature is to be first, to lead, to protect those under your care.

Leadership is your birthright. You naturally assume positions of authority and feel responsible for those around you. This protective instinct makes you a natural guardian.

Your intelligence is sharp and strategic. Mercury's influence gives you the mental agility to navigate complex situations and to see several moves ahead.

Pride in your position and achievements is part of your nature. You expect and deserve recognition for your accomplishments. This pride, when balanced, gives you dignity; when excessive, it can create conflicts.

Protection of family and dependents is central to your purpose. You take seriously your role as guardian and provider.

Secrets and hidden knowledge may attract you. You have the capacity to hold confidential information and to understand what is not spoken.

In relationships, you seek a partner who respects your authority and appreciates your protective nature. You are generous and devoted when your position is honored.""",
        "career_strengths": ["Management", "Government", "Military", "Police", "Protection services", "Elder care"],
        "relationship_nature": "Protective and authoritative, needs respect, devoted to family, can be controlling"
    },

    "Mula": {
        "tamil": "மூலம்",
        "lord": "Ketu",
        "deity": "Nirriti",
        "symbol": "Roots/Tied roots",
        "guna": "Sattva",
        "personality": """Mula, ruled by Ketu and presided over by Nirriti, goddess of dissolution, gives you the power to reach the root of things - to tear down falsehood and discover fundamental truth. Your nature is investigative and transformative, driven to understand the origin and essence of whatever you encounter.

Your investigative abilities are exceptional. You naturally dig beneath the surface to find the root cause, the hidden truth, the fundamental reality beneath appearances.

Transformation through destruction is your power. Sometimes old structures must be dismantled before new growth can occur, and you have the courage to break down what no longer serves.

Spiritual seeking runs deep in your nature. Ketu's influence draws you toward liberation from material bondage and understanding of ultimate reality.

You may experience more dramatic ups and downs than most. The energy of destruction and creation both flow through you.

Your honesty can be searing. You speak truth even when it is uncomfortable, cutting through pretense to expose reality.

In relationships, you need a partner who can handle your intensity and who shares your desire for authentic connection beyond superficiality.""",
        "career_strengths": ["Research", "Investigation", "Medicine", "Psychology", "Spirituality", "Archaeology"],
        "relationship_nature": "Intense and transformative, seeks authentic connection, can be unsettling, deeply passionate"
    },

    "Purva Ashadha": {
        "tamil": "பூராடம்",
        "lord": "Venus",
        "deity": "Apas",
        "symbol": "Fan/Winnowing basket",
        "guna": "Rajas",
        "personality": """Purva Ashadha, blessed by Venus and the water deities, gives you invincible determination combined with grace and charm. Your nature is essentially victorious - you have the power to overcome obstacles and achieve what you set out to accomplish. Like water that eventually wears away stone, your persistence is unstoppable.

Victory comes naturally to you. You have the combination of determination, intelligence, and grace that allows you to succeed where others fail.

Your powers of persuasion are exceptional. Venus gives you charm, and your water deity blessing gives you flexibility in approach. You can win people to your cause through influence rather than force.

Purification and renewal are themes in your life. Like water that cleanses, you have the ability to refresh and renew situations and relationships.

Pride in your accomplishments is justified but requires balance. You have genuine achievements to celebrate, but excessive pride can create opposition.

The creative arts may attract you, as Venus's influence enhances aesthetic appreciation and artistic ability.

In relationships, you are devoted and charming, using your considerable persuasive abilities to create harmony. You need a partner who can appreciate your victories and stand beside you with equal confidence.""",
        "career_strengths": ["Law", "Philosophy", "Water-related fields", "Arts", "Media", "Shipping"],
        "relationship_nature": "Charming and devoted, seeks victory in love too, persuasive, needs admiring partner"
    },

    "Uttara Ashadha": {
        "tamil": "உத்திராடம்",
        "lord": "Sun",
        "deity": "Vishvedevas",
        "symbol": "Elephant tusk/Planks of bed",
        "guna": "Rajas",
        "personality": """Born under Uttara Ashadha, you are blessed with the final, lasting victory that endures beyond initial success. The Sun's radiance and the blessing of the universal gods give you authority, righteousness, and the power to achieve permanent accomplishment. Your success, when it comes, is meant to last.

Your leadership is grounded in righteousness. You seek to lead in ways that are ethical and just, earning respect through moral authority.

Patience characterizes your approach. Unlike quick victories that fade, you build toward lasting achievement through sustained effort.

Universal principles guide you. You are drawn to truth that transcends personal or cultural limitations.

Your achievements have lasting impact. What you build is meant to endure beyond your lifetime.

Service to higher ideals motivates your actions. You work not merely for personal gain but for principles you believe in.

In relationships, you are steady and committed, building partnerships that deepen over time. You need a partner who shares your values and supports your long-term vision.""",
        "career_strengths": ["Government", "Law", "Leadership", "Social reform", "Management", "Pioneer work"],
        "relationship_nature": "Committed and ethical, builds lasting bonds, needs shared values, patient in love"
    },

    "Shravana": {
        "tamil": "திருவோணம்",
        "lord": "Moon",
        "deity": "Vishnu",
        "symbol": "Ear/Three footprints",
        "guna": "Rajas",
        "personality": """Shravana, the star of listening and learning, has given you exceptional receptivity to knowledge and wisdom. Blessed by Lord Vishnu the preserver and ruled by the reflective Moon, you have natural ability to receive, retain, and transmit learning. You are meant to be both student and teacher, listening deeply and sharing what you have heard.

Your listening abilities are exceptional. You hear not only words but the meaning beneath them, understanding what is truly being communicated.

Learning comes naturally and is a lifelong passion. You are drawn to knowledge and continue studying throughout your life.

Your capacity to preserve and transmit tradition is notable. Like Vishnu who preserves the cosmic order, you help maintain and pass on what is valuable.

Connection and communication are central to your purpose. You build bridges between people and help information flow where it is needed.

Travel and movement, particularly for learning, may feature prominently in your life.

In relationships, you are attentive and understanding, truly listening to your partner's needs and concerns. You need a partner who values communication and is willing to learn alongside you.""",
        "career_strengths": ["Teaching", "Media", "Music", "Religious work", "Counseling", "Languages"],
        "relationship_nature": "Attentive listener, values communication, devoted student of partnership, needs mental connection"
    },

    "Dhanishta": {
        "tamil": "அவிட்டம்",
        "lord": "Mars",
        "deity": "Vasus",
        "symbol": "Drum/Flute",
        "guna": "Rajas",
        "personality": """Dhanishta has blessed you with wealth, rhythm, and the ability to create harmony from discord. Ruled by Mars and blessed by the Vasus (elemental gods), you have both the drive to acquire and the wisdom to use resources for collective benefit. Music and rhythm resonate with your soul.

Material prosperity often accompanies this nakshatra. You have the ability to attract and accumulate wealth.

Musical ability or at least deep appreciation for rhythm and sound is part of your nature. You may be drawn to music, dance, or other rhythmic arts.

Your energy and vitality are strong, driven by Mars. You have the capacity for sustained effort and physical achievement.

Group dynamics interest you, and you often work best as part of a team or organization. You understand how to create harmony among different elements.

Adaptability to different environments serves you well. Like the Vasus who govern natural elements, you can work with various forces and conditions.

In relationships, you are energetic and generous, creating rhythm and harmony in partnership. You need a partner who can match your vitality and appreciate your drive for abundance.""",
        "career_strengths": ["Music", "Real estate", "Sports", "Military", "Mining", "Scientific research"],
        "relationship_nature": "Energetic and generous, creates harmony, needs dynamic partnership, can be competitive"
    },

    "Shatabhisha": {
        "tamil": "சதயம்",
        "lord": "Rahu",
        "deity": "Varuna",
        "symbol": "Empty circle/1000 flowers",
        "guna": "Rajas",
        "personality": """Born under the mysterious hundred healers of Shatabhisha, you possess unusual powers of healing and transformation. Rahu's influence combined with Varuna's oceanic wisdom gives you access to knowledge and abilities that others cannot comprehend. You walk between worlds, understanding truths that are hidden from ordinary perception.

Your healing abilities are exceptional, particularly in areas that conventional medicine cannot address. You may be drawn to alternative healing modalities or research into cutting-edge treatments.

Mystery surrounds you and attracts you. You are naturally drawn to the hidden, the secret, the not-yet-understood aspects of life.

Independence is essential to your nature. You must be free to explore your unique path without constraint from convention.

Your thinking is original and may seem eccentric to more conventional minds. You see possibilities that others miss.

Privacy is important to you. You share your deepest thoughts and experiences only with those you truly trust.

In relationships, you need a partner who can accept your mysterious nature and who respects your need for privacy and independence. You offer unusual understanding and healing to those you love.""",
        "career_strengths": ["Healing", "Research", "Technology", "Astronomy", "Psychology", "Electricity"],
        "relationship_nature": "Independent and mysterious, needs privacy, offers unusual understanding, can seem distant"
    },

    "Purva Bhadrapada": {
        "tamil": "பூரட்டாதி",
        "lord": "Jupiter",
        "deity": "Ajaikapada",
        "symbol": "Sword/Two front legs of funeral cot",
        "guna": "Rajas",
        "personality": """Purva Bhadrapada has given you the intense, transformative power of the one-footed goat Ajaikapada. Jupiter's wisdom combines with this fierce deity's energy to create a nature capable of both destruction and spiritual elevation. You walk the edge between worlds, carrying both human wisdom and divine fire.

Intensity characterizes your nature. Whatever you do, you do with full commitment and passion.

Transformation through purifying fire is your power. You can burn away what is false and leave only truth remaining.

Idealism drives you to work for causes greater than personal gain. You are willing to sacrifice for principles you believe in.

Your nature contains contradictions that you must learn to integrate. The fire of passion and the coolness of detachment both live within you.

Spiritual aspiration runs deep, even if you do not recognize it as such. You are drawn toward liberation and transcendence.

In relationships, you are passionate and transformative, challenging your partner to grow. You need someone who can handle your intensity and appreciate your depth.""",
        "career_strengths": ["Spirituality", "Philosophy", "Astrology", "Research", "Metalwork", "Occult sciences"],
        "relationship_nature": "Intense and transformative, deeply passionate, can be challenging, seeks spiritual connection"
    },

    "Uttara Bhadrapada": {
        "tamil": "உத்திரட்டாதி",
        "lord": "Saturn",
        "deity": "Ahirbudhnya",
        "symbol": "Back legs of funeral cot/Twins",
        "guna": "Tamas",
        "personality": """Born under the deep wisdom of Uttara Bhadrapada, you carry the profound insight of the serpent of the deep, Ahirbudhnya. Saturn's discipline combines with this oceanic wisdom to give you patience, endurance, and access to knowledge hidden in the depths. You understand the cycles of life and death and can guide others through transformation.

Your wisdom runs deep, drawing from sources not accessible to ordinary perception. You understand things that cannot be explained logically.

Patience characterizes your approach to life. You understand that some things take time and cannot be rushed.

Your compassion extends to all beings. You have natural empathy for those who suffer and seek to alleviate their pain.

Spiritual practice is likely important to you. You may be drawn to meditation, yoga, or other disciplines that quiet the mind and open deeper awareness.

The ability to counsel others through difficult transitions is your gift. You understand death, loss, and transformation and can guide others through these passages.

In relationships, you are steady and compassionate, offering the comfort of deep understanding. You need a partner who appreciates your depth and supports your spiritual journey.""",
        "career_strengths": ["Counseling", "Yoga", "Meditation", "End of life care", "Psychology", "Charity"],
        "relationship_nature": "Compassionate and steady, offers deep understanding, needs spiritual connection, patient in love"
    },

    "Revati": {
        "tamil": "ரேவதி",
        "lord": "Mercury",
        "deity": "Pushan",
        "symbol": "Fish/Drum",
        "guna": "Tamas",
        "personality": """Revati, the final nakshatra, has blessed you with the nurturing protection of Pushan, the divine shepherd. Mercury's intelligence combines with this guardian energy to give you the ability to guide, protect, and lead others toward their destination. Like the fish that navigates the ocean, you have natural orientation and the ability to find your way.

Your nurturing abilities are exceptional. You naturally care for those who are vulnerable, lost, or in need of guidance.

Travel and journeys feature prominently in your life. You may be drawn to work that involves movement, transportation, or helping others on their journeys.

Creativity and imagination are strong in you. The watery, dreamy quality of your nakshatra enhances artistic and intuitive abilities.

Prosperity often accompanies this nakshatra. Pushan's blessing includes material protection and abundance.

Completion and endings are themes in your life, as Revati is the final nakshatra. You have natural ability to bring things to proper conclusion.

In relationships, you are nurturing and protective, caring deeply for your partner's wellbeing. You need someone who appreciates your gentle nature and can join you in creating a sanctuary of love.""",
        "career_strengths": ["Travel", "Transport", "Animal care", "Arts", "Music", "Counseling", "Marine activities"],
        "relationship_nature": "Nurturing and protective, gentle soul, needs emotional security, deeply romantic"
    }
}


# ============== DASHA LIFE PREDICTIONS ==============
# How life unfolds during each planetary period

DASHA_PREDICTIONS = {
    "Sun": {
        "general": """During this Sun Dasha period, you will experience themes of authority, self-expression, and recognition. The Sun illuminates your path, bringing clarity about your life direction and purpose. This is a time when your leadership abilities come to the fore, and you may find yourself in positions of authority or dealing more closely with authority figures.

Government matters, relations with your father or father figures, and questions of personal honor will be prominent. Your health and vitality are generally strong during this period, though you should be mindful of issues related to heart, eyes, and overall constitution.

Career advancement is likely, particularly if you work in government, administration, or any field requiring leadership. Your public image may improve, and recognition for your efforts becomes more probable.

Spiritually, this is a time for developing stronger connection with your inner self and clarifying your dharma - your righteous path in life. The ego must be balanced with humility for best results.""",
        "strong": "With a well-placed Sun, this period brings recognition, career advancement, improved health and vitality, better relations with authority figures, and increased confidence and self-expression.",
        "weak": "A challenging Sun placement may bring conflicts with authority, health issues particularly related to heart or eyes, ego conflicts, and struggles with father figures or government matters."
    },

    "Moon": {
        "general": """The Moon Dasha brings your emotional and mental life into focus. This is a period of increased sensitivity, intuition, and connection with your inner world. Mother, home, and emotional security become central themes.

Your relationship with your mother or mother figures deepens during this time, for better or worse depending on the Moon's condition in your chart. Matters of home, property, and domestic life require attention.

Mental peace and emotional stability fluctuate more than usual. You may experience vivid dreams, enhanced intuition, and greater sensitivity to the moods of others. Travel, particularly over water, may feature in this period.

This is an excellent time for connecting with the public, particularly for those in service industries or public-facing roles. Your popularity may increase as others respond to your approachable, nurturing energy.

Women play significant roles during this period, whether as supporters, teachers, or through relationships that shape your emotional growth.""",
        "strong": "A well-placed Moon brings emotional contentment, good relations with mother, domestic happiness, mental peace, public popularity, and intuitive development.",
        "weak": "Challenging Moon placement may bring emotional turbulence, mental anxiety, issues with mother or women, domestic discord, and fluctuating health particularly related to mind and water-related issues."
    },

    "Mars": {
        "general": """Mars Dasha ignites your life with energy, courage, and the drive to accomplish. This is a period of action, initiative, and the assertion of personal will. Physical energy increases, and you feel more motivated to pursue your goals.

Property matters, siblings (especially brothers), and competitions become prominent themes. This is an excellent time for any endeavor requiring courage, physical effort, or competitive drive.

Conflicts may arise more readily during this period. Mars's energy can manifest as courage or aggression depending on how you channel it. Physical activity and competitive outlets help manage this powerful energy.

Technical and mechanical skills are highlighted. This is a good time for surgery, working with metals, real estate transactions, and any Mars-related profession.

The key challenge is managing anger and impulsiveness. Physical discipline, exercise, and constructive channels for your energy produce the best results.""",
        "strong": "Strong Mars placement brings courage, success in competitions, property gains, good relations with siblings, physical strength, and success in technical or military fields.",
        "weak": "Challenging Mars may bring accidents, conflicts, surgery, property disputes, issues with siblings, anger problems, and blood-related health issues."
    },

    "Mercury": {
        "general": """Mercury Dasha brings themes of communication, learning, business, and intellectual growth to the forefront. Your mind becomes sharper, and opportunities arise through speech, writing, and exchange of ideas.

Education and learning are favored during this period. Whether formal study or self-education, your capacity to absorb and process information increases. This is an excellent time for examinations, certifications, and skill development.

Business and trade opportunities multiply. Mercury's commercial nature supports buying, selling, negotiating, and all forms of exchange. Communication-related fields are particularly favored.

Relationships with younger siblings, maternal uncles, and intellectual companions become significant. You may find yourself surrounded by people who stimulate your mind.

The nervous system may be more sensitive during this period. Maintaining mental calm through meditation and avoiding excessive mental stimulation supports your wellbeing.""",
        "strong": "Strong Mercury brings intellectual success, business growth, communication opportunities, educational achievement, and good relations with siblings and friends.",
        "weak": "Challenging Mercury may bring communication problems, business difficulties, nervous disorders, skin issues, and problems with siblings or education."
    },

    "Jupiter": {
        "general": """Jupiter Dasha is traditionally considered one of the most auspicious periods, bringing expansion, wisdom, and grace into your life. This is a time of growth in all areas - material, intellectual, and spiritual.

Financial prosperity tends to increase during this period. Jupiter's benevolent nature attracts wealth and resources, often through fortunate circumstances that seem like luck but reflect your accumulated merit.

Education, spirituality, and higher knowledge become important focus areas. You may be drawn to philosophy, religion, or teaching. Your own wisdom develops, and you naturally attract students or those seeking guidance.

Children and grandchildren bring joy during this period. If you are seeking children, this period often brings fertility. Relations with teachers, mentors, and wise elders improve.

The key challenge is avoiding excessive optimism or expansion beyond sustainable limits. Jupiter's abundance must be managed wisely.""",
        "strong": "Well-placed Jupiter brings wealth, wisdom, children's happiness, spiritual growth, educational success, and fortunate opportunities.",
        "weak": "Challenging Jupiter may bring problems with children or education, liver issues, weight gain, excessive spending, and false optimism that leads to overextension."
    },

    "Venus": {
        "general": """Venus Dasha, the longest Dasha at 20 years, brings themes of love, beauty, pleasure, and material enjoyment. This is a period for experiencing the sweeter aspects of life - romance, art, luxury, and comfort.

Romantic relationships flourish during this period. Whether you are seeking love, deepening an existing relationship, or enjoying the pleasures of partnership, Venus brings opportunity for romantic fulfillment.

Material comforts and luxury tend to increase. You are drawn to beautiful things and may acquire jewelry, vehicles, fine clothing, or other items of beauty. Your aesthetic sensibilities refine.

Creative and artistic abilities are enhanced. Music, art, dance, and all forms of creative expression find support during this period.

The key challenge is avoiding excessive indulgence in pleasure. Balance between enjoyment and responsibility produces the best results.""",
        "strong": "Strong Venus brings love, luxury, artistic success, marital happiness, beauty, and material comfort.",
        "weak": "Challenging Venus may bring relationship difficulties, excessive spending on luxury, health issues related to reproductive system, and problems with vehicles or finances."
    },

    "Saturn": {
        "general": """Saturn Dasha brings themes of discipline, responsibility, structure, and karmic reckoning. This is one of the most important periods for soul growth, as Saturn teaches through challenges that develop strength and wisdom.

Work and career require serious attention. Saturn rewards persistent effort and penalizes shortcuts. This is a time to build lasting foundations through disciplined, sustained work.

Responsibilities increase, often involving care for elders, service to others, or the demands of duty. You may feel burdened at times, but accepting responsibility with grace accelerates your growth.

Health requires attention, particularly bones, joints, and chronic conditions. Discipline in diet, exercise, and lifestyle becomes more important.

The lessons of Saturn, while challenging, produce lasting benefits. Character development, wisdom, and material stability are the rewards of navigating this period well.""",
        "strong": "Well-placed Saturn brings career stability, lasting achievements, wisdom through experience, property gains, and the respect that comes from proven character.",
        "weak": "Challenging Saturn may bring delays, obstacles, health issues particularly related to bones and chronic conditions, separation from loved ones, and heavy responsibilities."
    },

    "Rahu": {
        "general": """Rahu Dasha brings intensity, ambition, and often unexpected changes. This 18-year period challenges you to grow beyond your comfort zone and can bring remarkable worldly success alongside spiritual challenges.

Ambition intensifies during this period. You feel driven to achieve, to acquire, to experience more than before. This drive can lead to significant worldly accomplishment if channeled wisely.

Foreign connections often develop - travel abroad, business with foreigners, or adoption of unconventional paths. Rahu pushes you beyond familiar boundaries.

Technology, research, and unconventional fields may attract you. Rahu favors innovation and breaking with tradition.

The key challenge is maintaining ethical grounding while pursuing worldly success. Rahu's energy can be deceptive, and discernment is essential.

Spiritual practice becomes especially important during Rahu Dasha to maintain balance and clarity amid the intense experiences this period brings.""",
        "strong": "Strong Rahu brings worldly success, foreign opportunities, technical advancement, and breakthrough achievements.",
        "weak": "Challenging Rahu may bring confusion, deception, addiction, foreign troubles, sudden reversals, and spiritual confusion."
    },

    "Ketu": {
        "general": """Ketu Dasha brings themes of spirituality, detachment, and liberation from material attachments. This 7-year period often marks significant spiritual development, though the process may involve letting go of worldly attachments.

Spiritual inclinations strengthen during this period. You may feel drawn to meditation, yoga, or other practices that connect you with transcendent reality. The material world may feel less satisfying.

Endings and completions characterize this period. Relationships, careers, or situations that have run their course naturally conclude, making space for new beginnings.

Intuition and psychic sensitivity may increase. You perceive subtle dimensions more readily and may experience meaningful dreams or spiritual insights.

The key challenge is balancing spiritual aspiration with practical responsibilities. Complete withdrawal from the world is rarely appropriate; learning to be in the world but not of it is the goal.

Health requires attention, particularly regarding mysterious or hard-to-diagnose conditions. Alternative and spiritual healing approaches may be helpful.""",
        "strong": "Well-placed Ketu brings spiritual progress, intuitive development, liberation from limiting attachments, and deep insight into the nature of reality.",
        "weak": "Challenging Ketu may bring confusion, loss, mysterious health issues, isolation, and difficulty maintaining practical affairs."
    }
}


# ============== PLANET IN HOUSE NARRATIVE EFFECTS ==============
# Descriptive effects of planets in different houses for life areas

PLANET_HOUSE_EFFECTS = {
    "Sun": {
        1: "Your personality radiates with natural authority and confidence. Leadership comes easily to you.",
        2: "Wealth comes through government, authority figures, or positions of power. Your speech carries weight.",
        3: "Courage and initiative are your strengths. Relations with siblings may be competitive but ultimately growth-producing.",
        4: "Home life is central to your sense of self. Your relationship with your mother shapes your identity.",
        5: "Creative self-expression and children bring great joy. You may have leadership abilities in education or speculation.",
        6: "You overcome enemies and obstacles through personal strength. Service and health matters require your attention.",
        7: "Partnership dynamics involve power balance. You attract strong, authoritative partners.",
        8: "Transformation and hidden matters reveal your inner strength. Inheritances may come through father's side.",
        9: "Fortune, philosophy, and spiritual authority shape your path. Your father is an important influence.",
        10: "Career brings recognition and authority. You are destined for leadership in your profession.",
        11: "Gains come through influential connections. Your aspirations include positions of honor.",
        12: "Spiritual retreat and service are important. Authority may be exercised behind the scenes."
    },
    "Moon": {
        1: "Your emotional nature is visible to all. You are nurturing, sensitive, and responsive to others.",
        2: "Wealth fluctuates but emotional security matters more than material. Family is your treasure.",
        3: "Your mind is active and curious. Siblings, especially sisters, play important roles.",
        4: "Domestic bliss is essential for your wellbeing. Your mother's influence is profound.",
        5: "Creativity flows from emotional depth. Children bring great emotional fulfillment.",
        6: "Emotional patterns affect health. Service to others nurtures your soul.",
        7: "You seek emotional security in partnership. Your spouse reflects your inner needs.",
        8: "Emotional intensity and transformation define your journey. Intuition penetrates secrets.",
        9: "Spiritual and philosophical pursuits satisfy your soul. Travel brings emotional growth.",
        10: "Public visibility and emotional expression combine. You may nurture through your profession.",
        11: "Friends provide emotional support. Your hopes are tied to family and belonging.",
        12: "Spiritual depths attract you. Emotional healing comes through retreat and reflection."
    },
    "Mars": {
        1: "Your energy is dynamic and assertive. Physical vitality and courage define your approach.",
        2: "You fight for financial security. Speech can be sharp but direct.",
        3: "Courage and initiative are exceptional. Competitive relations with siblings are likely.",
        4: "Energy pours into home and property. Relations with mother may be intense.",
        5: "Creative energy is strong and dynamic. Competition and sports attract you.",
        6: "Victory over enemies and obstacles. Excellent for military, medicine, or competition.",
        7: "Partnership brings passion and sometimes conflict. You need a strong partner.",
        8: "Transformation through confrontation with power. Research and investigation call you.",
        9: "You fight for your beliefs. Fortune comes through courage and initiative.",
        10: "Career requires energy and leadership. Military, engineering, or executive roles suit you.",
        11: "Gains come through bold action. You achieve your desires through effort.",
        12: "Hidden strength and spiritual battles. Energy works best behind the scenes."
    },
    "Mercury": {
        1: "Your intelligence and communication skills are immediately apparent. Curiosity defines you.",
        2: "Wealth comes through intellect and communication. Your speech is valuable.",
        3: "Communication and learning are natural strengths. Excellent relations with siblings.",
        4: "Intellectual stimulation at home. Education and learning matter in domestic life.",
        5: "Creative intelligence is exceptional. Education and speculation favor you.",
        6: "Analytical skills overcome obstacles. Detail-oriented service is your strength.",
        7: "You seek intellectual connection in partnership. Business partnerships may flourish.",
        8: "Research and investigation abilities. You understand hidden patterns and systems.",
        9: "Higher learning and philosophy attract. Teaching and publishing may be your path.",
        10: "Career through communication and intellect. Writing, speaking, or technical fields suit you.",
        11: "Gains through networks and communication. Friends share intellectual interests.",
        12: "Hidden intellectual abilities. Writing or research in seclusion benefits you."
    },
    "Jupiter": {
        1: "Wisdom, optimism, and good fortune grace your personality. You inspire others.",
        2: "Wealth accumulates naturally. Your speech carries wisdom and benefit.",
        3: "Wisdom guides your communications. Relations with siblings are beneficial.",
        4: "Happiness at home and emotional wisdom. Your mother may be a teacher figure.",
        5: "Children bring joy and good fortune. Creative and educational success is likely.",
        6: "You overcome obstacles through wisdom. Service professions may suit you.",
        7: "Partnership brings growth and abundance. Your spouse may be wise or fortunate.",
        8: "Transformation brings wisdom. Inheritance and partner's wealth may increase.",
        9: "This is Jupiter's own house. Fortune, spirituality, and higher learning flourish.",
        10: "Career brings recognition and growth. You may rise to positions of guidance.",
        11: "Abundant gains and fortunate aspirations. Friends are generous and supportive.",
        12: "Spiritual wisdom develops. Charitable work and retreat bring growth."
    },
    "Venus": {
        1: "Beauty, charm, and artistic nature are evident. You attract love and pleasure.",
        2: "Wealth flows toward you. Beauty in speech and valuable possessions.",
        3: "Artistic communication skills. Pleasant relations with siblings.",
        4: "Beautiful home and domestic happiness. Comfort and vehicles are likely.",
        5: "Romantic and creative fulfillment. Children bring joy and beauty.",
        6: "Service through art or beauty. Health benefits from pleasant activities.",
        7: "Partnership is central to happiness. Love and marriage are especially blessed.",
        8: "Transformation through relationships. Partner's wealth may increase.",
        9: "Philosophy and beauty combine. Fortune through arts or women.",
        10: "Career in arts, beauty, or luxury. Public appreciation is likely.",
        11: "Gains through beauty and relationships. Friends share artistic interests.",
        12: "Hidden pleasures and spiritual beauty. Retreat brings romantic satisfaction."
    },
    "Saturn": {
        1: "Serious, disciplined nature is evident. Life teaches through responsibility.",
        2: "Wealth comes slowly but lastingly. Conservative with resources.",
        3: "Careful, methodical communication. Relations with siblings involve responsibility.",
        4: "Domestic responsibility and property matters. Mother may be a source of duty.",
        5: "Creative expression is disciplined. Children come with responsibility.",
        6: "Excellent for service and overcoming obstacles. Health requires discipline.",
        7: "Partnership involves commitment and responsibility. Marriage may come later.",
        8: "Longevity and transformation through discipline. Deep research abilities.",
        9: "Disciplined approach to philosophy. Fortune comes through persistent effort.",
        10: "Career through sustained effort. Authority achieved through merit.",
        11: "Gains through patience and organization. Long-term goals are achieved.",
        12: "Spiritual discipline and solitary work. Hospitals or institutions may feature."
    },
    "Rahu": {
        1: "Unusual personality and unconventional path. Ambition drives you forward.",
        2: "Wealth through unconventional means. Foreign connections in finances.",
        3: "Unusual communication abilities. Foreign influences through siblings.",
        4: "Unconventional home life. Foreign residence or unusual property.",
        5: "Unusual creativity or children. Speculation has mixed results.",
        6: "Ability to overcome unusual obstacles. Foreign enemies or competitions.",
        7: "Unconventional partnerships. Foreign spouse or unusual marriage.",
        8: "Transformation through unusual means. Research into hidden matters.",
        9: "Unconventional philosophy or religion. Foreign travel and fortune.",
        10: "Career through unusual means. Foreign recognition or unconventional profession.",
        11: "Gains through unusual sources. Foreign friends and organizations.",
        12: "Unusual spiritual path. Foreign residence or retreat."
    },
    "Ketu": {
        1: "Spiritual nature and detachment are evident. Unusual perspective on life.",
        2: "Detachment from wealth. Spiritual values over material.",
        3: "Intuitive communication. Unusual relations with siblings.",
        4: "Detachment from home or mother. Spiritual focus in domestic life.",
        5: "Unusual creativity or approach to children. Spiritual insights.",
        6: "Victory over enemies through detachment. Alternative health approaches.",
        7: "Detachment in partnership. Spiritual connection in marriage.",
        8: "Deep transformation and spiritual insight. Psychic abilities.",
        9: "Strong spiritual inclinations. Wisdom through renunciation.",
        10: "Unusual or spiritual career. Recognition through service.",
        11: "Detachment from desires. Spiritual friends and organizations.",
        12: "Liberation is favored. Deep spiritual development."
    }
}


# ============== LIFE AREA NARRATIVE TEMPLATES ==============
# Templates for generating descriptive content for life areas

LIFE_AREA_NARRATIVES = {
    "career": {
        "intro_template": """Your career path is illuminated by the {house_sign} energy of your 10th house, ruled by {house_lord}. This celestial configuration shapes your professional destiny in distinctive ways, influencing not only what kind of work you gravitate toward but also how you approach success and recognition in the world.""",

        "lord_strong": """With your 10th lord {house_lord} in a position of strength, your career trajectory is blessed with favorable momentum. You have natural ability to rise in your chosen field, and recognition for your efforts comes more readily than for many others. Authority figures tend to view you favorably, and opportunities for advancement present themselves at appropriate times.""",

        "lord_weak": """Your 10th lord {house_lord} faces some challenges in its placement, suggesting that career success requires more deliberate effort and patience. While obstacles may appear on your professional path, these challenges serve to develop your character and ultimately make your achievements more meaningful. Persistence and strategic planning will be your allies.""",

        "karaka_analysis": """Saturn, the natural significator of career, {karaka_status} in your chart. This influences your relationship with authority, your capacity for sustained professional effort, and the timing of career milestones. {karaka_detail}""",

        "timing_note": """The {current_dasha} Dasha period brings specific influences to your professional life. {dasha_career_effect} Understanding this timing helps you align your efforts with cosmic rhythms for optimal results.""",

        "recommended_fields": """Based on the {house_sign} influence on your career house and the placement of relevant planets, you are naturally suited for fields involving {field_description}. Your {planet_influences} suggest particular aptitude for {specific_careers}."""
    },

    "marriage": {
        "intro_template": """Your partnership destiny is written in the {house_sign} energy of your 7th house, guided by {house_lord}. This celestial pattern reveals the qualities you seek in a partner, the dynamics that will characterize your closest relationships, and the timing of significant partnership developments in your life.""",

        "partner_nature": """Your ideal partner carries the essence of {house_sign} - someone who embodies {sign_qualities}. You are attracted to individuals who {partner_description}. The placement of your 7th lord suggests that you may meet significant partners through {meeting_context}.""",

        "venus_analysis": """Venus, the planet of love and relationship, {venus_status} in your chart. This significantly influences your romantic nature, your capacity to give and receive love, and your overall relationship satisfaction. {venus_detail}""",

        "timing_indication": """Marriage and significant partnerships are indicated during {favorable_periods}. The {current_dasha} period brings {dasha_relationship_effect} to your relationship sphere.""",

        "relationship_dynamics": """In partnership, you tend to {dynamic_description}. Your relationships are characterized by {relationship_qualities}. For lasting harmony, you benefit from {advice_for_harmony}."""
    },

    "wealth": {
        "intro_template": """Your financial destiny is shaped by the {house_sign} energy of your 2nd house of accumulated wealth and the {11_house_sign} energy of your 11th house of gains. Together with the placement of Jupiter, the planet of abundance, these factors reveal your relationship with money, your capacity for wealth accumulation, and the sources from which prosperity flows to you.""",

        "wealth_potential": """Your chart indicates {wealth_level} potential for material accumulation. {wealth_description} The 2nd house lord {second_lord} in {lord_position} suggests that your wealth {lord_effect}.""",

        "income_sources": """Gains flow to you primarily through {income_sources}. The 11th house configuration suggests that {gains_description}. Your professional income {professional_income_note}.""",

        "jupiter_analysis": """Jupiter, the great benefic and significator of wealth, {jupiter_status} in your chart. This planetary blessing {jupiter_effect}. {jupiter_detail}""",

        "financial_timing": """Financial developments are particularly favorable during {favorable_periods}. The current planetary period suggests {current_period_effect} regarding material matters."""
    },

    "health": {
        "intro_template": """Your vitality and physical constitution are governed by the strength of your Lagna (ascendant) lord {lagna_lord} and the condition of the 6th house of health challenges. Understanding these astrological indicators helps you take proactive measures for maintaining wellness throughout life.""",

        "constitution": """Your basic constitution tends toward {constitution_type}. The {lagna_sign} rising gives you {constitutional_qualities}. Your physical energy {energy_description}.""",

        "vulnerable_areas": """Based on planetary positions, the areas requiring particular attention include {body_areas}. These are not predictions of illness but rather indications of where preventive care is most valuable. {prevention_advice}""",

        "vitality_assessment": """Your overall vitality, as indicated by the Sun's strength and Lagna lord condition, is {vitality_level}. {vitality_description}""",

        "health_timing": """Health matters require particular attention during {challenging_periods}. The current planetary period suggests {current_health_indication}. Regular health practices and preventive care during these times are especially valuable."""
    },

    "education": {
        "intro_template": """Your intellectual development and educational journey are illuminated by the {house_sign} energy of your 4th house of foundational learning and the {9_house_sign} energy of your 9th house of higher wisdom. Mercury, the planet of intellect, and Jupiter, the guru of wisdom, together reveal your learning style, academic potential, and areas of natural intellectual strength.""",

        "learning_style": """You learn best through {learning_style}. Your mind naturally gravitates toward {subjects_of_interest}. The placement of Mercury suggests that {mercury_learning_effect}.""",

        "academic_potential": """Your potential for academic achievement is {academic_level}. The 5th house of intelligence, combined with the condition of Mercury and Jupiter, indicates {academic_description}. {academic_advice}""",

        "higher_education": """Higher education and specialized knowledge are indicated through {higher_ed_indication}. The 9th house configuration suggests {wisdom_path}. Teachers and mentors play {mentor_role} in your intellectual development.""",

        "timing_for_learning": """Educational pursuits are particularly favored during {favorable_periods}. The current planetary period {current_education_effect}."""
    },

    "children": {
        "intro_template": """The blessing of children in your life is revealed through the {house_sign} energy of your 5th house and its lord {house_lord}. Jupiter, the natural significator of children and divine grace, together with the 5th house configuration, indicates your relationship with progeny and the joy they bring to your life.""",

        "children_indication": """Your chart indicates {children_potential} regarding progeny. The 5th lord {fifth_lord} in {lord_position} suggests {children_description}. {timing_note}""",

        "relationship_with_children": """Your relationship with children is characterized by {relationship_quality}. You approach parenting with {parenting_style}. Your children are likely to {children_nature}.""",

        "jupiter_blessing": """Jupiter's placement {jupiter_children_effect}. This divine blessing {blessing_description}.""",

        "timing_for_children": """Matters related to children are particularly significant during {favorable_periods}. The current planetary period {current_children_effect}."""
    }
}


# ============== COMBINATION INTERPRETATIONS ==============
# How Rasi + Nakshatra combine for personality

def get_combined_personality(rasi: str, nakshatra: str) -> str:
    """Generate combined personality description based on Rasi and Nakshatra"""
    rasi_data = RASI_TRAITS.get(rasi, {})
    nakshatra_data = NAKSHATRA_TRAITS.get(nakshatra, {})

    if not rasi_data or not nakshatra_data:
        return ""

    rasi_lord = rasi_data.get('lord', '')
    nakshatra_lord = nakshatra_data.get('lord', '')

    combination_text = f"""Your Moon in {rasi} ({rasi_data.get('tamil', '')}) combined with the {nakshatra} ({nakshatra_data.get('tamil', '')}) nakshatra creates a unique personality blend that draws from both influences.

The {rasi_data.get('element', '')} element of {rasi} provides the foundation of your emotional nature - {rasi_data.get('quality', '').lower()} and shaped by {rasi_lord}'s influence. This is refined and colored by the {nakshatra_lord}-ruled {nakshatra} nakshatra, which adds specific qualities to your basic emotional constitution.

From your Moon sign {rasi}, you carry the fundamental traits of {', '.join(rasi_data.get('strengths', [])[:3])}. These core qualities form the base of your personality. The {nakshatra} nakshatra then adds its distinctive flavor - the energy of {nakshatra_data.get('deity', '')} and the guidance of {nakshatra_lord}.

In daily life, this combination manifests as {_get_combination_manifestation(rasi, nakshatra)}. Your emotional responses, instinctive reactions, and deep-seated habits all reflect this unique blending of lunar influences.

This Rasi-Nakshatra combination particularly influences your approach to relationships, your comfort zones, and what you need to feel emotionally secure. Understanding this helps you work with your natural tendencies rather than against them."""

    return combination_text


def _get_combination_manifestation(rasi: str, nakshatra: str) -> str:
    """Get specific manifestation description for Rasi-Nakshatra combination"""
    # Fire signs
    fire_signs = ['Aries', 'Leo', 'Sagittarius']
    earth_signs = ['Taurus', 'Virgo', 'Capricorn']
    air_signs = ['Gemini', 'Libra', 'Aquarius']
    water_signs = ['Cancer', 'Scorpio', 'Pisces']

    if rasi in fire_signs:
        return "dynamic energy combined with emotional intensity, quick reactions, and a passionate approach to life's experiences"
    elif rasi in earth_signs:
        return "steady, grounded emotional responses, practical approach to feelings, and need for material and emotional security"
    elif rasi in air_signs:
        return "intellectual processing of emotions, need for mental understanding of feelings, and communication-oriented emotional expression"
    else:
        return "deep emotional sensitivity, intuitive responses, and strong connection to the feeling dimensions of experience"


# Helper function for report generation
def get_personality_narrative(rasi: str, nakshatra: str, lagna: str) -> str:
    """Generate comprehensive personality narrative for PDF report"""
    rasi_data = RASI_TRAITS.get(rasi, {})
    nakshatra_data = NAKSHATRA_TRAITS.get(nakshatra, {})
    lagna_data = RASI_TRAITS.get(lagna, {})

    narrative = f"""## உங்கள் ஆளுமை குணாதிசயங்கள் / Your Personality Profile

### Moon Sign Influence: {rasi} ({rasi_data.get('tamil', '')})

{rasi_data.get('personality', '')}

### Birth Star Influence: {nakshatra} ({nakshatra_data.get('tamil', '')})

{nakshatra_data.get('personality', '')}

### Rising Sign: {lagna} ({lagna_data.get('tamil', '')})

Your {lagna} Lagna shapes how the world perceives you and how you present yourself. While your Moon sign reveals your inner emotional nature, your rising sign is the mask you wear and the approach you take to new situations.

{lagna_data.get('personality', '')[:500]}

### Combined Influence

{get_combined_personality(rasi, nakshatra)}

### Your Core Strengths
Based on your unique combination of {rasi} Moon, {nakshatra} Nakshatra, and {lagna} Lagna:
- {rasi_data.get('strengths', ['Leadership'])[0]}
- {nakshatra_data.get('career_strengths', ['Service'])[0] if 'career_strengths' in nakshatra_data else 'Intuition'}
- {lagna_data.get('strengths', ['Adaptability'])[0]}

### Areas for Growth
Your chart suggests focusing on:
- Balancing {rasi_data.get('weaknesses', ['impulsiveness'])[0] if rasi_data.get('weaknesses') else 'intensity'}
- Developing patience with {nakshatra_data.get('relationship_nature', 'relationship challenges').split(',')[0].lower()}
- Integrating the lessons of your rising sign
"""

    return narrative


def get_dasha_narrative(dasha_lord: str, is_current: bool = False) -> str:
    """Generate narrative description for a Dasha period"""
    dasha_data = DASHA_PREDICTIONS.get(dasha_lord, {})

    if not dasha_data:
        return f"The {dasha_lord} period brings its unique influences to your life journey."

    current_note = "\n\n**As your current operating period**, this Dasha's themes are actively shaping your life now. Pay particular attention to the opportunities and challenges described above." if is_current else ""

    return f"""{dasha_data.get('general', '')}

### When {dasha_lord} is Strong
{dasha_data.get('strong', '')}

### Challenges to Watch For
{dasha_data.get('weak', '')}
{current_note}"""


# ============== YOGA DESCRIPTIONS ==============
# Rich descriptions for major yogas found in charts

YOGA_DESCRIPTIONS = {
    "Gajakesari": {
        "name_tamil": "கஜகேசரி யோகம்",
        "category": "Wealth & Wisdom",
        "formation": "Jupiter in Kendra (1,4,7,10) from Moon",
        "description": """Gajakesari Yoga is one of the most celebrated yogas in Vedic astrology, formed when Jupiter occupies a Kendra (angular house) from the Moon. The name combines 'Gaja' (elephant) and 'Kesari' (lion), symbolizing the majestic combination of wisdom and power.

This yoga bestows upon you the rare combination of intelligence and authority. Like the elephant known for its memory and wisdom, and the lion known for its courage and leadership, you possess both the mental acuity to understand complex situations and the strength to act decisively upon that understanding.

Those blessed with Gajakesari Yoga often rise to positions of prominence and influence. You have natural ability to inspire others and to be recognized for your contributions. Financial prosperity tends to follow, not through mere luck, but through the wise application of your talents and the respect you command from others.

The effects of this yoga manifest most strongly during Jupiter's Dasha periods and when Jupiter transits favorable positions. Education, philosophy, and spiritual pursuits bring particular fulfillment. You may find yourself drawn to teaching, counseling, or any field where wisdom can be shared for the benefit of others.

In relationships, this yoga grants you the ability to be both nurturing and authoritative - a partner and parent who commands respect while providing emotional security. Your reputation tends to grow throughout life as your wisdom becomes more widely recognized.""",
        "effects": ["Fame and recognition", "Wealth accumulation", "Wisdom and learning", "Leadership positions", "Respect in society"],
        "activation": "Most powerful during Jupiter and Moon Dasha periods"
    },

    "Budhaditya": {
        "name_tamil": "புதாதித்ய யோகம்",
        "category": "Intelligence",
        "formation": "Sun and Mercury conjunction in same sign",
        "description": """Budhaditya Yoga forms when the Sun and Mercury occupy the same sign in the birth chart. Since Mercury is never more than 28 degrees from the Sun, this is a relatively common yoga, but its effects vary greatly based on the strength and house placement of the conjunction.

This yoga blesses you with sharp intellect and excellent communication abilities. The combination of the Sun's confidence and Mercury's mental agility creates a mind that is both brilliant and expressive. You have natural talent for articulating complex ideas in ways others can understand.

Your intellectual pursuits are backed by strong willpower. Unlike those who have ideas but lack the determination to implement them, you possess both the creative intelligence to conceive plans and the solar energy to see them through. This makes you effective in any field requiring both thinking and doing.

Education and learning come easily to you. You may have excelled academically and continue to be a lifelong learner. Writing, speaking, teaching, and any form of communication are natural outlets for your talents.

The yoga is strongest when the conjunction occurs in Mercury's signs (Gemini, Virgo) or the Sun's sign (Leo), and when Mercury is not combust (too close to the Sun). In such cases, the intellectual brilliance is exceptional. Even with combustion, the yoga grants above-average intelligence, though the person may sometimes struggle to receive full credit for their ideas.""",
        "effects": ["Sharp intellect", "Communication skills", "Success in education", "Writing and speaking ability", "Logical thinking"],
        "activation": "Enhanced during Sun and Mercury Dasha periods"
    },

    "Chandra-Mangal": {
        "name_tamil": "சந்திர மங்கள யோகம்",
        "category": "Wealth",
        "formation": "Moon and Mars conjunction or mutual aspect",
        "description": """Chandra-Mangal Yoga forms when the Moon and Mars are in conjunction or mutual aspect. This combination brings together the nurturing, emotional Moon with the aggressive, action-oriented Mars, creating a personality that is both sensitive and strong.

This yoga is particularly noted for its wealth-giving properties. The combination of Mars's drive and Moon's intuition creates excellent business acumen. You have the ability to sense opportunities (Moon) and the courage to act on them decisively (Mars). This makes you effective in commerce, real estate, and any field requiring both emotional intelligence and assertive action.

Emotionally, this yoga creates intensity. Your feelings are strong and you act on them. While this can sometimes lead to impulsive emotional reactions, it also means you are genuine and passionate in your connections with others. You protect those you love fiercely.

The yoga grants physical courage and the ability to take initiative. You are not one to wait passively for opportunities - you create them. This proactive nature, combined with emotional intelligence, makes you effective in leadership roles where both strength and sensitivity are required.

For women, this yoga is particularly significant for marriage, often indicating a spouse with Mars-like qualities - assertive, protective, and passionate. The yoga also indicates strong connection with mother and ability to nurture others while maintaining personal strength.""",
        "effects": ["Wealth through effort", "Business success", "Emotional strength", "Property gains", "Courage and initiative"],
        "activation": "Active during Moon and Mars Dasha periods"
    },

    "Hamsa": {
        "name_tamil": "ஹம்ச யோகம்",
        "category": "Pancha Mahapurusha",
        "formation": "Jupiter in own sign or exaltation in Kendra",
        "description": """Hamsa Yoga is one of the five Mahapurusha (great person) Yogas, formed when Jupiter occupies its own sign (Sagittarius, Pisces) or exaltation sign (Cancer) in a Kendra house (1, 4, 7, or 10). The Hamsa (swan) symbolizes discrimination between good and evil, like the mythical swan that can separate milk from water.

This is one of the most auspicious yogas possible, indicating a person of exceptional wisdom, righteousness, and spiritual inclination. You possess the rare ability to discern truth from falsehood, the essential from the superficial. This discriminating wisdom guides all your decisions and actions.

Those with Hamsa Yoga are naturally drawn to knowledge, philosophy, and spiritual pursuits. You may become a teacher, guide, or counselor - someone others look to for wisdom and direction. Your advice is valued because it comes from genuine understanding rather than mere opinion.

Material prosperity accompanies this yoga, but it is prosperity earned through righteous means. You are unlikely to compromise your principles for financial gain, yet abundance tends to flow to you naturally as a result of your integrity and wisdom.

Physical characteristics often include a fair complexion, well-proportioned body, and a dignified bearing that commands respect. Your presence has a calming, elevating effect on others. Even in conflict, you maintain your composure and seek resolution through understanding.

The spiritual dimension of this yoga is significant. Whether or not you follow a formal spiritual path, you have natural inclination toward higher truths and the development of consciousness.""",
        "effects": ["Great wisdom", "Spiritual inclination", "Respected position", "Righteous wealth", "Teaching ability"],
        "activation": "Especially powerful during Jupiter Dasha"
    },

    "Malavya": {
        "name_tamil": "மாளவ்ய யோகம்",
        "category": "Pancha Mahapurusha",
        "formation": "Venus in own sign or exaltation in Kendra",
        "description": """Malavya Yoga is one of the five Mahapurusha Yogas, formed when Venus occupies its own sign (Taurus, Libra) or exaltation sign (Pisces) in a Kendra house. This yoga bestows beauty, luxury, artistic talent, and the ability to enjoy life's pleasures with refinement and grace.

Those blessed with Malavya Yoga possess natural charm and attractiveness that goes beyond mere physical beauty. There is an aesthetic quality to your entire being - the way you move, speak, dress, and create your environment. You have innate understanding of beauty and harmony that influences everything you touch.

Artistic and creative talents are strongly indicated. Whether in visual arts, music, fashion, design, or any creative field, you have the ability to create beauty that moves others. Even if art is not your profession, your life itself becomes a form of artistic expression.

Material comforts and luxury tend to come to you naturally. You appreciate quality and have the ability to attract the finer things in life. Your home is likely beautiful and comfortable, reflecting your refined taste. Vehicles, jewelry, and beautiful possessions are often associated with this yoga.

In relationships, you are romantic, devoted, and capable of deep love. You seek beauty and harmony in partnership and have the ability to create it. Marriage is often blessed with this yoga, bringing a partner who shares your appreciation for life's pleasures.

The spiritual dimension of Venus is also enhanced - you may find transcendence through beauty, art, or devotional practices. The path of bhakti (devotion) may particularly appeal to you.""",
        "effects": ["Physical beauty", "Artistic talent", "Material luxury", "Happy marriage", "Refined taste"],
        "activation": "Most powerful during Venus Dasha"
    },

    "Ruchaka": {
        "name_tamil": "ருசக யோகம்",
        "category": "Pancha Mahapurusha",
        "formation": "Mars in own sign or exaltation in Kendra",
        "description": """Ruchaka Yoga is one of the five Mahapurusha Yogas, formed when Mars occupies its own sign (Aries, Scorpio) or exaltation sign (Capricorn) in a Kendra house. This yoga creates a warrior personality - courageous, strong, commanding, and capable of great achievement through determined action.

Those with Ruchaka Yoga possess exceptional physical vitality and courage. You have the constitution of a warrior and the temperament to match. Challenges that intimidate others are opportunities for you to demonstrate your strength and capability.

Leadership in competitive or challenging environments comes naturally. You may be drawn to military, sports, law enforcement, surgery, or any field requiring courage and decisive action. You have the ability to command others and to perform under pressure.

Physical characteristics often include a strong, well-built body, reddish complexion, and an imposing presence. Your bearing communicates strength and confidence. Others instinctively recognize your capability and either follow your lead or step aside.

Property and land ownership are often associated with this yoga. You have the ability to acquire and hold assets, particularly real estate. Your determination ensures that what you gain, you keep.

The challenge with this yoga is managing the intense Mars energy constructively. When well-directed, this energy accomplishes remarkable things. When misdirected, it can manifest as aggression, conflict, or recklessness. Discipline and worthy goals are essential for the highest expression of this yoga.""",
        "effects": ["Physical strength", "Courage and valor", "Leadership ability", "Property gains", "Competitive success"],
        "activation": "Most powerful during Mars Dasha"
    },

    "Bhadra": {
        "name_tamil": "பத்ர யோகம்",
        "category": "Pancha Mahapurusha",
        "formation": "Mercury in own sign or exaltation in Kendra",
        "description": """Bhadra Yoga is one of the five Mahapurusha Yogas, formed when Mercury occupies its own sign (Gemini, Virgo) or exaltation sign (Virgo) in a Kendra house. This yoga creates exceptional intellectual ability, communication skills, and business acumen.

Those blessed with Bhadra Yoga possess minds of remarkable clarity and agility. You process information quickly, see connections others miss, and express your thoughts with precision and eloquence. Learning comes easily, and you likely excel in academic pursuits.

Communication in all forms is your natural domain. Writing, speaking, teaching, negotiating - any field requiring the skilled use of language benefits from your talents. You have the ability to persuade, explain, and influence through the power of your words.

Business and commerce are strongly favored. Your analytical mind, combined with your communication skills, makes you effective in trade, finance, and any commercial enterprise. You understand markets, can negotiate skillfully, and have the mental stamina for complex business operations.

Physical characteristics often include a youthful appearance, well-proportioned body, and expressive features. Your face reflects the quick intelligence of your mind. You may appear younger than your years throughout life.

The spiritual expression of this yoga manifests as discrimination and discernment. You have the ability to analyze spiritual teachings, to separate genuine wisdom from pretense, and to articulate your understanding clearly. The path of Jnana (knowledge) may particularly appeal to you.""",
        "effects": ["Exceptional intellect", "Communication mastery", "Business success", "Academic achievement", "Youthful appearance"],
        "activation": "Most powerful during Mercury Dasha"
    },

    "Shasha": {
        "name_tamil": "சச யோகம்",
        "category": "Pancha Mahapurusha",
        "formation": "Saturn in own sign or exaltation in Kendra",
        "description": """Shasha Yoga is one of the five Mahapurusha Yogas, formed when Saturn occupies its own sign (Capricorn, Aquarius) or exaltation sign (Libra) in a Kendra house. This yoga creates a person of great endurance, authority, and the ability to build lasting structures.

Those with Shasha Yoga possess exceptional patience and persistence. You understand that meaningful achievement takes time, and you have the stamina to work steadily toward long-term goals. While others sprint and tire, you maintain a pace that ultimately carries you further.

Authority and positions of power come through merit with this yoga. You earn respect through demonstrated competence and reliability. Over time, you rise to positions of significant responsibility, often in government, large organizations, or any structured hierarchy.

Material success tends to come later in life rather than early, but what you build is lasting. Your achievements have staying power because they are built on solid foundations. Property, land, and tangible assets accumulate through patient effort.

Physical characteristics may include a lean, angular body and serious demeanor. You may appear older than your years when young, but often age more gracefully than others. There is a quality of gravitas to your presence.

The spiritual dimension of this yoga relates to karma yoga - the path of selfless action and duty. You understand the value of discipline, service, and accepting responsibility. Meditation practices requiring patience and persistence suit your nature.""",
        "effects": ["Lasting authority", "Patient success", "Material stability", "Government favor", "Endurance"],
        "activation": "Results fully manifest after age 36, Saturn's maturity"
    },

    "Dhana": {
        "name_tamil": "தன யோகம்",
        "category": "Wealth",
        "formation": "Lords of 1st, 2nd, 5th, 9th, 11th houses connected",
        "description": """Dhana Yoga refers to various combinations that indicate wealth and prosperity. These yogas form when the lords of wealth-related houses (2nd for accumulated wealth, 11th for gains) connect with fortune houses (1st, 5th, 9th) through conjunction, aspect, or exchange.

When present in your chart, Dhana Yoga indicates natural ability to attract and accumulate wealth. The specific nature of your prosperity depends on which planets and houses are involved in the yoga's formation.

First and second house connection indicates wealth through personal effort and initiative. Fifth house involvement suggests gains through intelligence, speculation, or children. Ninth house participation indicates fortune through father, luck, or righteous means. Eleventh house connection shows income through networks, friends, and fulfillment of desires.

The strength of Dhana Yoga depends on the strength of the planets involved. Strong, well-placed planets give abundant results; weak or afflicted planets indicate wealth that comes with struggle or that may not last.

Multiple Dhana Yogas in a chart amplify the wealth-giving potential. However, other factors in the chart must also support material accumulation. The Dasha periods of planets forming Dhana Yoga are particularly significant for financial developments.

True prosperity encompasses more than money. The highest expression of Dhana Yoga includes not only material wealth but also the wisdom to use resources well and the generosity to share with others.""",
        "effects": ["Wealth accumulation", "Financial success", "Material prosperity", "Resource attraction", "Comfortable life"],
        "activation": "During Dashas of planets forming the yoga"
    },

    "Raja": {
        "name_tamil": "ராஜ யோகம்",
        "category": "Power & Status",
        "formation": "Lords of Kendra and Trikona houses connected",
        "description": """Raja Yoga is formed when the lords of Kendra houses (1, 4, 7, 10) and Trikona houses (1, 5, 9) form a connection through conjunction, aspect, or exchange. This is one of the most important yogas for worldly success and recognition.

The combination of Kendra (action) and Trikona (fortune) energies creates the conditions for rising to positions of power and prominence. You have both the capability to achieve (Kendra) and the fortune to be recognized (Trikona).

Those with strong Raja Yoga often rise above their birth circumstances to positions of authority and influence. This may manifest in politics, business, administration, or any field where power and recognition are possible. Leadership opportunities seek you out.

The strength and quality of Raja Yoga depends on which specific houses and planets are involved. Some combinations are more powerful than others. The first house lord involved makes the yoga more personal and powerful. Jupiter or Venus as participating planets tends to give more benefic results.

Raja Yoga indicates not just power but legitimate authority - the kind that comes with recognition and respect from others. You are seen as worthy of your position rather than having merely grabbed power.

The timing of Raja Yoga's manifestation depends on the Dasha periods. When the planets forming Raja Yoga operate, opportunities for advancement and recognition increase significantly. The yoga may remain dormant until activated by appropriate planetary periods.""",
        "effects": ["Rise to power", "Authority and status", "Leadership opportunities", "Recognition and fame", "Influential position"],
        "activation": "During Dashas of planets forming the yoga"
    },

    "Viparita Raja": {
        "name_tamil": "விபரீத ராஜ யோகம்",
        "category": "Unexpected Rise",
        "formation": "Lords of 6th, 8th, or 12th houses in each other's signs",
        "description": """Viparita Raja Yoga is a unique yoga formed when the lords of dusthana houses (6th, 8th, 12th) are placed in each other's houses or are in conjunction. Paradoxically, this combination of difficult house lords produces positive results.

The principle is that when difficulties cancel each other out, fortune results. The challenging significations of these houses neutralize each other, and from adversity emerges success. This is often called the yoga of the "phoenix rising from ashes."

Those with Viparita Raja Yoga often achieve success through or after significant challenges. You may face obstacles that would defeat others, only to emerge stronger and more successful. Your victories come not despite difficulties but because of them.

This yoga often manifests as unexpected rise to power or sudden reversal of fortune from negative to positive. You may succeed in situations where failure seemed inevitable. Others may underestimate you based on your challenges, only to be surprised by your achievements.

The strength of this yoga depends on the planets involved and their overall condition. Benefic planets as house lords give better results than malefic planets. The Dasha periods of the involved planets are critical for manifestation.

Spiritually, this yoga teaches that adversity can be transformed into advantage, that difficulties are opportunities for growth, and that the soul's strength is revealed through challenge rather than ease.""",
        "effects": ["Success through adversity", "Unexpected rise", "Victory over enemies", "Reversal of fortune", "Hidden strength revealed"],
        "activation": "Often manifests suddenly during related Dasha periods"
    },

    "Neecha Bhanga Raja": {
        "name_tamil": "நீச பங்க ராஜ யோகம்",
        "category": "Cancellation & Rise",
        "formation": "Debilitated planet with cancellation factors",
        "description": """Neecha Bhanga Raja Yoga occurs when a debilitated planet has its weakness cancelled by specific factors, transforming the debilitation into a source of strength. This yoga converts apparent weakness into extraordinary capability.

Cancellation can occur through several mechanisms: the lord of the debilitation sign being strong, the lord of the exaltation sign aspecting the debilitated planet, the debilitated planet being in a Kendra from Moon or Lagna, or other specific combinations.

When present, this yoga indicates that your perceived weaknesses become your greatest strengths. What appears to be a disadvantage transforms into unique capability. The area of life represented by the debilitated planet, rather than being problematic, becomes a source of exceptional achievement.

This yoga often manifests as success that comes through unconventional means or in unexpected areas. You may achieve greatness precisely where others predicted failure. Your path to success may be unusual but ultimately more meaningful.

The deeper teaching of this yoga is that apparent limitations can be doorways to unique gifts. The very challenge you face becomes the source of your distinctive contribution. What looks like weakness is actually strength waiting to be recognized.

The manifestation of this yoga requires the Dasha periods of the involved planets. During these times, the transformation from weakness to strength becomes visible in concrete achievements.""",
        "effects": ["Weakness becomes strength", "Unusual success", "Overcoming limitations", "Unique achievements", "Rising above expectations"],
        "activation": "During Dasha of the debilitated planet or its dispositor"
    },

    "Saraswati": {
        "name_tamil": "சரஸ்வதி யோகம்",
        "category": "Learning & Arts",
        "formation": "Jupiter, Venus, Mercury in Kendras or Trikonas, strong",
        "description": """Saraswati Yoga, named after the goddess of learning and arts, forms when Jupiter, Venus, and Mercury - the three planets of wisdom and culture - occupy Kendra or Trikona houses in strength. This yoga bestows exceptional talent in learning, arts, and eloquent expression.

Those blessed with this yoga possess genuine scholarship and artistic refinement. You have both the intellectual capacity for deep learning (Jupiter), the aesthetic sensitivity for artistic expression (Venus), and the communicative ability to share your knowledge (Mercury).

Education and learning are not merely pursuits but passions. You may excel in multiple fields of knowledge, achieving depth that goes beyond surface understanding. Your love of learning continues throughout life, making you a perpetual student of wisdom.

Artistic expression in various forms comes naturally. Whether through music, writing, visual arts, or other creative media, you have the ability to create works of lasting value. Your creations reflect both technical skill and inspired vision.

Speaking and writing abilities are exceptional. You can articulate complex ideas with clarity and beauty. Teaching, lecturing, writing, and any form of knowledge transmission are natural outlets for your talents.

The spiritual dimension of this yoga connects to Saraswati as the goddess who reveals the power of knowledge to transform consciousness. Learning is not merely intellectual acquisition but a spiritual practice that elevates awareness.""",
        "effects": ["Exceptional learning", "Artistic talent", "Eloquent speech", "Writing ability", "Teaching gifts"],
        "activation": "Throughout life, enhanced during Jupiter, Venus, Mercury Dashas"
    },

    "Lakshmi": {
        "name_tamil": "லக்ஷ்மி யோகம்",
        "category": "Wealth & Fortune",
        "formation": "9th lord strong in Kendra/Trikona with Lagna lord",
        "description": """Lakshmi Yoga, named after the goddess of wealth and prosperity, forms when the 9th house lord (bhagya/fortune) is strongly placed in a Kendra or Trikona while connected with the Lagna lord. This yoga brings the blessings of fortune and material prosperity.

Those with Lakshmi Yoga are blessed with good fortune that manifests as material prosperity. Wealth comes through legitimate means, often connected to the significations of the 9th house - father, dharma, higher learning, or good karma from past lives.

The nature of this yoga is such that prosperity comes not just through personal effort but through fortunate circumstances that support your endeavors. Opportunities appear at the right time, helpful people enter your life, and resources become available when needed.

Unlike wealth that comes through struggle alone, Lakshmi Yoga brings prosperity with grace. There is ease in your relationship with money and material resources. You attract abundance rather than constantly chasing it.

The spiritual dimension of this yoga suggests that your material prosperity is connected to dharmic living. Wealth comes as a result of righteous action, and it carries the responsibility to use resources wisely and generously.

This yoga also indicates physical beauty and comfortable living circumstances. The goddess Lakshmi represents not just wealth but all forms of auspiciousness - beauty, fertility, and good fortune in multiple dimensions of life.""",
        "effects": ["Material prosperity", "Good fortune", "Beautiful appearance", "Comfortable life", "Blessed circumstances"],
        "activation": "Throughout life, especially during 9th lord and Lagna lord Dashas"
    },

    "Kemadruma": {
        "name_tamil": "கேமத்ரும யோகம்",
        "category": "Challenging",
        "formation": "No planets in 2nd or 12th from Moon (with cancellation factors)",
        "description": """Kemadruma Yoga forms when there are no planets in the 2nd or 12th houses from the Moon. However, this yoga has numerous cancellation factors, and its negative effects are often overstated in traditional texts.

When present without cancellation, this yoga can indicate periods of loneliness, financial struggle, or lack of support. The Moon, representing the mind and emotional nature, lacks the support of neighboring planets, creating a sense of isolation.

However, cancellation occurs if planets aspect the Moon, if the Moon is in a Kendra, if the Moon is with or aspected by benefics, or through several other combinations. In most charts, cancellation factors are present, significantly reducing or eliminating the yoga's challenging effects.

Even when present, this yoga can be interpreted positively in certain contexts. The independence it indicates can become self-reliance. The solitude can become spiritual introspection. The challenge can become the seed of compassion for others who struggle.

If you have indications of this yoga, the key is to actively cultivate support systems, maintain connections with others, and develop inner resources that provide stability independent of external circumstances.

The Dasha of the Moon and planets that could provide cancellation are important periods for understanding how this yoga manifests in your specific chart. Remedial measures for the Moon can help strengthen emotional resilience.""",
        "effects": ["Need for self-reliance", "Periods of solitude", "Inner strength development", "Spiritual depth", "Compassion through struggle"],
        "activation": "Particularly during Moon Dasha if uncancelled"
    }
}


def get_yoga_description(yoga_name: str) -> dict:
    """Get detailed description for a yoga"""
    return YOGA_DESCRIPTIONS.get(yoga_name, {
        "description": f"The {yoga_name} yoga brings specific blessings according to its planetary formation.",
        "effects": ["Varies based on planetary strength"],
        "activation": "During related planetary Dasha periods"
    })
