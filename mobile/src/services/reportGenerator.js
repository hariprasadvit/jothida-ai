/**
 * Comprehensive Jathagam Report Generator
 * Generates detailed 20-30 page PDF reports with AI analysis
 */

// Tamil month names
const TAMIL_MONTHS = ['சித்திரை', 'வைகாசி', 'ஆனி', 'ஆடி', 'ஆவணி', 'புரட்டாசி', 'ஐப்பசி', 'கார்த்திகை', 'மார்கழி', 'தை', 'மாசி', 'பங்குனி'];

// Tithi names
const TITHIS = ['பிரதமை', 'துவிதியை', 'திருதியை', 'சதுர்த்தி', 'பஞ்சமி', 'சஷ்டி', 'சப்தமி', 'அஷ்டமி', 'நவமி', 'தசமி', 'ஏகாதசி', 'துவாதசி', 'திரயோதசி', 'சதுர்த்தசி', 'பூர்ணிமை', 'அமாவாசை'];

// Nakshatra details with ruling deity, characteristics, and predictions
const NAKSHATRA_DETAILS = {
  'அஸ்வினி': { deity: 'அஸ்வினி குமாரர்கள்', symbol: 'குதிரை தலை', quality: 'சுறுசுறுப்பு, வேகம்', career: 'மருத்துவம், போக்குவரத்து', lucky_gems: 'வைடூர்யம்' },
  'பரணி': { deity: 'யமன்', symbol: 'யோனி', quality: 'சுய கட்டுப்பாடு', career: 'நீதி, சட்டம்', lucky_gems: 'வைரம்' },
  'கார்த்திகை': { deity: 'அக்னி', symbol: 'தீ', quality: 'தீவிரம், உறுதி', career: 'ராணுவம், காவல்துறை', lucky_gems: 'மாணிக்கம்' },
  'ரோகிணி': { deity: 'பிரம்மா', symbol: 'மாட்டு வண்டி', quality: 'அழகு, கலை', career: 'கலை, திரைப்படம்', lucky_gems: 'முத்து' },
  'மிருகசீரிடம்': { deity: 'சந்திரன்', symbol: 'மான் தலை', quality: 'ஆராய்ச்சி', career: 'ஆராய்ச்சி, அறிவியல்', lucky_gems: 'முத்து' },
  'திருவாதிரை': { deity: 'ருத்ரன்', symbol: 'கண்ணீர் துளி', quality: 'ஆன்மீகம்', career: 'ஆன்மீகம், யோகா', lucky_gems: 'கோமேதகம்' },
  'புனர்பூசம்': { deity: 'அதிதி', symbol: 'அம்பு கூடு', quality: 'புத்துணர்வு', career: 'ஆசிரியர், எழுத்தாளர்', lucky_gems: 'புஷ்பராகம்' },
  'பூசம்': { deity: 'பிரஹஸ்பதி', symbol: 'பசு மடி', quality: 'அன்பு, கருணை', career: 'சமூக சேவை', lucky_gems: 'நீலம்' },
  'ஆயில்யம்': { deity: 'சர்ப்பம்', symbol: 'பாம்பு', quality: 'புத்திசாலித்தனம்', career: 'மருந்து, ஆராய்ச்சி', lucky_gems: 'வைடூர்யம்' },
  'மகம்': { deity: 'பிதுர்கள்', symbol: 'அரியணை', quality: 'தலைமை', career: 'அரசியல், நிர்வாகம்', lucky_gems: 'மாணிக்கம்' },
  'பூரம்': { deity: 'பகன்', symbol: 'கட்டில்', quality: 'சுகம்', career: 'கலை, பொழுதுபோக்கு', lucky_gems: 'வைரம்' },
  'உத்திரம்': { deity: 'சூரியன்', symbol: 'படுக்கை', quality: 'நிலைத்தன்மை', career: 'அரசு வேலை', lucky_gems: 'மாணிக்கம்' },
  'அஸ்தம்': { deity: 'சூரியன்', symbol: 'கை', quality: 'திறமை', career: 'கைவினை, தொழில்நுட்பம்', lucky_gems: 'மரகதம்' },
  'சித்திரை': { deity: 'விஸ்வகர்மா', symbol: 'முத்து', quality: 'படைப்பாற்றல்', career: 'கட்டிடக்கலை, வடிவமைப்பு', lucky_gems: 'வைடூர்யம்' },
  'சுவாதி': { deity: 'வாயு', symbol: 'பவளம்', quality: 'சுதந்திரம்', career: 'வணிகம், வர்த்தகம்', lucky_gems: 'கோமேதகம்' },
  'விசாகம்': { deity: 'இந்திராக்னி', symbol: 'தோரணம்', quality: 'லட்சியம்', career: 'ஆராய்ச்சி, அரசியல்', lucky_gems: 'புஷ்பராகம்' },
  'அனுஷம்': { deity: 'மித்ரன்', symbol: 'குடை', quality: 'நட்பு', career: 'வெளியுறவு, பேச்சுவார்த்தை', lucky_gems: 'நீலம்' },
  'கேட்டை': { deity: 'இந்திரன்', symbol: 'குண்டலம்', quality: 'அதிகாரம்', career: 'நிர்வாகம், தலைமை', lucky_gems: 'வைடூர்யம்' },
  'மூலம்': { deity: 'நிர்ருதி', symbol: 'வேர்', quality: 'ஆராய்ச்சி', career: 'மருத்துவம், ஆராய்ச்சி', lucky_gems: 'வைடூர்யம்' },
  'பூராடம்': { deity: 'அபஹ்', symbol: 'யானை தந்தம்', quality: 'வெற்றி', career: 'கலை, ஊடகம்', lucky_gems: 'வைரம்' },
  'உத்திராடம்': { deity: 'விஸ்வதேவர்', symbol: 'யானை தந்தம்', quality: 'நேர்மை', career: 'சட்டம், நீதி', lucky_gems: 'மாணிக்கம்' },
  'திருவோணம்': { deity: 'விஷ்ணு', symbol: 'காதுகள்', quality: 'கேட்டறிதல்', career: 'ஊடகம், தொலைத்தொடர்பு', lucky_gems: 'முத்து' },
  'அவிட்டம்': { deity: 'வசுக்கள்', symbol: 'முரசு', quality: 'செல்வம்', career: 'வணிகம், நிதி', lucky_gems: 'நீலம்' },
  'சதயம்': { deity: 'வருணன்', symbol: 'வட்டம்', quality: 'குணப்படுத்துதல்', career: 'மருத்துவம்', lucky_gems: 'நீலம்' },
  'பூரட்டாதி': { deity: 'அஜைகபாத்', symbol: 'கட்டில் கால்கள்', quality: 'துறவு', career: 'ஆன்மீகம், தத்துவம்', lucky_gems: 'புஷ்பராகம்' },
  'உத்திரட்டாதி': { deity: 'அஹிர்புத்னியா', symbol: 'இரட்டை முகம்', quality: 'ஞானம்', career: 'ஆசிரியர், ஆலோசகர்', lucky_gems: 'நீலம்' },
  'ரேவதி': { deity: 'பூஷன்', symbol: 'மீன்', quality: 'இரக்கம்', career: 'சமூக சேவை, மருத்துவம்', lucky_gems: 'வைடூர்யம்' },
};

// Rasi characteristics and predictions
const RASI_DETAILS = {
  'மேஷம்': { element: 'நெருப்பு', ruler: 'செவ்வாய்', quality: 'தலைமை, துணிச்சல்', lucky_color: 'சிவப்பு', lucky_number: '9', career: 'ராணுவம், விளையாட்டு, தொழில்முனைவு' },
  'ரிஷபம்': { element: 'பூமி', ruler: 'சுக்கிரன்', quality: 'நிலைத்தன்மை, அழகு', lucky_color: 'வெள்ளை', lucky_number: '6', career: 'கலை, நிதி, வேளாண்மை' },
  'மிதுனம்': { element: 'காற்று', ruler: 'புதன்', quality: 'புத்திசாலித்தனம், தொடர்பு', lucky_color: 'பச்சை', lucky_number: '5', career: 'எழுத்து, ஊடகம், வணிகம்' },
  'கடகம்': { element: 'நீர்', ruler: 'சந்திரன்', quality: 'அன்பு, பாதுகாப்பு', lucky_color: 'வெள்ளை', lucky_number: '2', career: 'வீடு, உணவு, மருத்துவம்' },
  'சிம்மம்': { element: 'நெருப்பு', ruler: 'சூரியன்', quality: 'தலைமை, கம்பீரம்', lucky_color: 'தங்கம்', lucky_number: '1', career: 'அரசியல், நிர்வாகம், கலை' },
  'கன்னி': { element: 'பூமி', ruler: 'புதன்', quality: 'பகுப்பாய்வு, சேவை', lucky_color: 'பச்சை', lucky_number: '5', career: 'மருத்துவம், கணக்கியல், ஆராய்ச்சி' },
  'துலாம்': { element: 'காற்று', ruler: 'சுக்கிரன்', quality: 'சமநிலை, அழகு', lucky_color: 'நீலம்', lucky_number: '6', career: 'சட்டம், கலை, வெளியுறவு' },
  'விருச்சிகம்': { element: 'நீர்', ruler: 'செவ்வாய்', quality: 'ஆழ்ந்த சிந்தனை, மாற்றம்', lucky_color: 'சிவப்பு', lucky_number: '9', career: 'ஆராய்ச்சி, மருத்துவம், உளவியல்' },
  'தனுசு': { element: 'நெருப்பு', ruler: 'குரு', quality: 'ஞானம், பயணம்', lucky_color: 'மஞ்சள்', lucky_number: '3', career: 'கல்வி, சட்டம், பயணம்' },
  'மகரம்': { element: 'பூமி', ruler: 'சனி', quality: 'உழைப்பு, பொறுப்பு', lucky_color: 'கருப்பு', lucky_number: '8', career: 'அரசு, நிர்வாகம், கட்டுமானம்' },
  'கும்பம்': { element: 'காற்று', ruler: 'சனி', quality: 'புதுமை, சமூக சேவை', lucky_color: 'நீலம்', lucky_number: '8', career: 'தொழில்நுட்பம், சமூக சேவை, அறிவியல்' },
  'மீனம்': { element: 'நீர்', ruler: 'குரு', quality: 'இரக்கம், கற்பனை', lucky_color: 'மஞ்சள்', lucky_number: '3', career: 'கலை, ஆன்மீகம், மருத்துவம்' },
};

// Yoga definitions with effects and timing
const YOGA_DEFINITIONS = {
  'Gajakesari Yoga': {
    tamil: 'கஜகேசரி யோகம்',
    formation: 'குரு சந்திரனிலிருந்து கேந்திரத்தில் இருக்கும்போது',
    effects: ['புகழ் மற்றும் அங்கீகாரம்', 'நல்ல சொத்துக்கள்', 'அறிவு மற்றும் ஞானம்', 'சமூகத்தில் மரியாதை'],
    activation: 'குரு அல்லது சந்திர தசையில் செயல்படும்',
    strength_factors: ['குரு பலம்', 'சந்திர பலம்', 'கேந்திர அதிபதித்துவம்'],
  },
  'Lakshmi Yoga': {
    tamil: 'லக்ஷ்மி யோகம்',
    formation: 'சுக்கிரன் சுபஸ்தானத்தில் பலமாக இருக்கும்போது',
    effects: ['செல்வம் மற்றும் வளம்', 'அழகு மற்றும் கவர்ச்சி', 'இல்ல சுகம்', 'கலை திறமை'],
    activation: 'சுக்கிர தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சுக்கிர பலம்', '2ம், 7ம் வீட்டு தொடர்பு'],
  },
  'Raja Yoga': {
    tamil: 'ராஜ யோகம்',
    formation: 'கேந்திர-திரிகோண அதிபதிகள் இணையும்போது',
    effects: ['அதிகாரம் மற்றும் பதவி', 'சமூக அந்தஸ்து', 'தலைமைத் திறன்', 'வெற்றி'],
    activation: 'சம்பந்தப்பட்ட கிரக தசையில் செயல்படும்',
    strength_factors: ['கேந்திர அதிபதித்துவம்', 'திரிகோண அதிபதித்துவம்'],
  },
  'Dhana Yoga': {
    tamil: 'தன யோகம்',
    formation: '2ம், 11ம் வீட்டு அதிபதிகள் இணையும்போது',
    effects: ['நிதி வளர்ச்சி', 'சொத்து சேர்க்கை', 'வருமான அதிகரிப்பு', 'வணிக வெற்றி'],
    activation: '2ம் அல்லது 11ம் அதிபதி தசையில் செயல்படும்',
    strength_factors: ['2ம் வீட்டு பலம்', '11ம் வீட்டு பலம்'],
  },
  'Budhaditya Yoga': {
    tamil: 'புதாதித்ய யோகம்',
    formation: 'சூரியன் மற்றும் புதன் ஒரே வீட்டில்',
    effects: ['அறிவு மற்றும் புத்திசாலித்தனம்', 'பேச்சு திறமை', 'கணித திறன்', 'வணிக புத்தி'],
    activation: 'சூரிய அல்லது புத மதசையில் செயல்படும்',
    strength_factors: ['சூரிய பலம்', 'புத பலம்', 'வீட்டு நிலை'],
  },
  'Hamsa Yoga': {
    tamil: 'ஹம்ச யோகம்',
    formation: 'குரு லக்னம், 4ம், 7ம், 10ம் வீட்டில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['ஆன்மீக வளர்ச்சி', 'கல்வியில் சிறப்பு', 'நற்பண்புகள்', 'மரியாதை'],
    activation: 'குரு தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['குரு பலம்', 'கேந்திர நிலை'],
  },
  'Malavya Yoga': {
    tamil: 'மாளவ்ய யோகம்',
    formation: 'சுக்கிரன் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['அழகு மற்றும் கவர்ச்சி', 'சுக வாழ்க்கை', 'கலை திறமை', 'வாகன யோகம்'],
    activation: 'சுக்கிர தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சுக்கிர பலம்', 'கேந்திர நிலை'],
  },
  'Ruchaka Yoga': {
    tamil: 'ருசக யோகம்',
    formation: 'செவ்வாய் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['துணிச்சல் மற்றும் வீரம்', 'தலைமைத் திறன்', 'நிலம் சேர்க்கை', 'அதிகாரம்'],
    activation: 'செவ்வாய் தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['செவ்வாய் பலம்', 'கேந்திர நிலை'],
  },
  'Shasha Yoga': {
    tamil: 'சச யோகம்',
    formation: 'சனி கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['அதிகாரம் மற்றும் பதவி', 'பொறுமை', 'நீண்ட ஆயுள்', 'செல்வம்'],
    activation: 'சனி தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சனி பலம்', 'கேந்திர நிலை'],
  },
  'Bhadra Yoga': {
    tamil: 'பத்ர யோகம்',
    formation: 'புதன் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['புத்திசாலித்தனம்', 'பேச்சு திறமை', 'வணிக வெற்றி', 'நல்ல ஆரோக்கியம்'],
    activation: 'புத தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['புத பலம்', 'கேந்திர நிலை'],
  },
};

// House significations for predictions
const HOUSE_MEANINGS = {
  1: { name: 'லக்னம்', areas: ['உடல் ஆரோக்கியம்', 'தன்னம்பிக்கை', 'தோற்றம்', 'ஆளுமை'] },
  2: { name: 'தன ஸ்தானம்', areas: ['குடும்பம்', 'செல்வம்', 'பேச்சு', 'உணவு'] },
  3: { name: 'சகோதர ஸ்தானம்', areas: ['சகோதரர்கள்', 'துணிச்சல்', 'குறுகிய பயணம்', 'தொடர்பு'] },
  4: { name: 'சுக ஸ்தானம்', areas: ['தாய்', 'வீடு', 'வாகனம்', 'நிம்மதி'] },
  5: { name: 'புத்திர ஸ்தானம்', areas: ['குழந்தைகள்', 'கல்வி', 'படைப்பாற்றல்', 'காதல்'] },
  6: { name: 'சத்ரு ஸ்தானம்', areas: ['எதிரிகள்', 'நோய்', 'கடன்', 'வேலை'] },
  7: { name: 'களத்திர ஸ்தானம்', areas: ['திருமணம்', 'வாழ்க்கைத் துணை', 'வணிக பங்காளி', 'பொது உறவுகள்'] },
  8: { name: 'ஆயுள் ஸ்தானம்', areas: ['ஆயுள்', 'மறைவான விஷயங்கள்', 'மரபு சொத்து', 'மாற்றம்'] },
  9: { name: 'பாக்கிய ஸ்தானம்', areas: ['அதிர்ஷ்டம்', 'தந்தை', 'ஆன்மீகம்', 'நீண்ட பயணம்'] },
  10: { name: 'கர்ம ஸ்தானம்', areas: ['தொழில்', 'அந்தஸ்து', 'அரசு', 'புகழ்'] },
  11: { name: 'லாப ஸ்தானம்', areas: ['வருமானம்', 'நண்பர்கள்', 'ஆசைகள்', 'மூத்த சகோதரர்'] },
  12: { name: 'விரய ஸ்தானம்', areas: ['செலவு', 'வெளிநாடு', 'ஆன்மீகம்', 'படுக்கை சுகம்'] },
};

// Dasha predictions by planet
const DASHA_PREDICTIONS = {
  'சூரியன்': {
    positive: ['அரசு வேலை', 'தந்தையின் ஆசி', 'புகழ்', 'தலைமை பதவி', 'ஆரோக்கியம்'],
    challenges: ['அகந்தை', 'அதிகாரிகளுடன் மோதல்', 'கண் பிரச்சனை'],
    remedies: ['சூரிய வழிபாடு', 'ஆதித்ய ஹ்ருதயம்', 'சிவப்பு உடை ஞாயிறு'],
  },
  'சந்திரன்': {
    positive: ['மன நிம்மதி', 'தாயின் ஆசி', 'புதிய வீடு', 'நல்ல உறவுகள்', 'கற்பனை திறன்'],
    challenges: ['மன அழுத்தம்', 'நிலையின்மை', 'குளிர் சம்பந்த நோய்'],
    remedies: ['சந்திர வழிபாடு', 'சிவ வழிபாடு திங்கள்', 'வெள்ளை உடை'],
  },
  'செவ்வாய்': {
    positive: ['துணிச்சல்', 'நிலம் சேர்க்கை', 'சகோதர உதவி', 'விளையாட்டு வெற்றி', 'தொழில்நுட்பம்'],
    challenges: ['எடுத்தெறிந்த குணம்', 'விபத்து', 'ரத்த சம்பந்த நோய்'],
    remedies: ['முருகன் வழிபாடு', 'அங்காரக ஸ்தோத்திரம்', 'சிவப்பு உடை செவ்வாய்'],
  },
  'புதன்': {
    positive: ['கல்வி வெற்றி', 'வணிக லாபம்', 'பேச்சு திறமை', 'புதிய தொடர்புகள்', 'எழுத்து'],
    challenges: ['நரம்பு பிரச்சனை', 'தோல் நோய்', 'மன குழப்பம்'],
    remedies: ['விஷ்ணு வழிபாடு', 'புத ஸ்தோத்திரம்', 'பச்சை உடை புதன்'],
  },
  'குரு': {
    positive: ['ஆன்மீக வளர்ச்சி', 'குழந்தை பாக்கியம்', 'கல்வி', 'குரு ஆசி', 'வெளிநாடு'],
    challenges: ['உடல் பருமன்', 'கல்லீரல் பிரச்சனை', 'அதிக நம்பிக்கை'],
    remedies: ['குரு வழிபாடு', 'விஷ்ணு சஹஸ்ரநாமம்', 'மஞ்சள் உடை வியாழன்'],
  },
  'சுக்கிரன்': {
    positive: ['திருமணம்', 'சொகுசு', 'கலை வெற்றி', 'வாகனம்', 'அழகு'],
    challenges: ['சர்க்கரை நோய்', 'சிறுநீரக பிரச்சனை', 'உறவு சிக்கல்'],
    remedies: ['லக்ஷ்மி வழிபாடு', 'சுக்கிர ஸ்தோத்திரம்', 'வெள்ளை உடை வெள்ளி'],
  },
  'சனி': {
    positive: ['அரசு உதவி', 'நீண்டகால லாபம்', 'நிலம்', 'கட்டிடம்', 'பொறுமை'],
    challenges: ['தாமதம்', 'உடல் வலி', 'மன சோர்வு', 'தடைகள்'],
    remedies: ['ஹனுமான் வழிபாடு', 'சனி ஸ்தோத்திரம்', 'கருப்பு/நீலம் உடை சனி'],
  },
  'ராகு': {
    positive: ['திடீர் வெற்றி', 'வெளிநாடு', 'தொழில்நுட்பம்', 'புதுமை', 'ஆராய்ச்சி'],
    challenges: ['குழப்பம்', 'மோசடி', 'தோல் நோய்', 'நஞ்சு பயம்'],
    remedies: ['துர்கா வழிபாடு', 'ராகு ஸ்தோத்திரம்', 'நீலம் உடை சனி'],
  },
  'கேது': {
    positive: ['ஆன்மீகம்', 'மோட்சம்', 'ஆராய்ச்சி', 'மறைவான ஞானம்', 'வைராக்கியம்'],
    challenges: ['திடீர் நஷ்டம்', 'விபத்து', 'மர்மமான நோய்'],
    remedies: ['கணபதி வழிபாடு', 'கேது ஸ்தோத்திரம்', 'சாம்பல் நிற உடை'],
  },
};

/**
 * Generate comprehensive PDF HTML
 */
export function generateComprehensivePDFHTML(userProfile, chartData) {
  const planets = chartData?.planets || [];
  const dasha = chartData?.dasha;
  const yogas = chartData?.yogas || [];
  const lagna = chartData?.lagna;
  const moonSign = chartData?.moon_sign;

  const currentDate = new Date().toLocaleDateString('ta-IN');
  const rasiDetails = RASI_DETAILS[moonSign?.rasi_tamil] || {};
  const nakshatraDetails = NAKSHATRA_DETAILS[moonSign?.nakshatra] || {};

  // Generate chart HTML
  const generateChartHTML = (title, isAmsam = false) => {
    const rasiOrder = ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Aquarius', 'Cancer', 'Capricorn', 'Leo', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'];
    const rasiTamil = ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கும்பம்', 'கடகம்', 'மகரம்', 'சிம்மம்', 'தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'];
    const PLANET_ABBR = { 'Sun': 'சூ', 'Moon': 'சந்', 'Mars': 'செ', 'Mercury': 'பு', 'Jupiter': 'கு', 'Venus': 'சு', 'Saturn': 'ச', 'Rahu': 'ரா', 'Ketu': 'கே' };

    const houses = Array(12).fill('');
    planets.forEach(p => {
      const idx = rasiOrder.indexOf(p.rasi);
      if (idx !== -1) {
        const abbr = PLANET_ABBR[p.planet] || p.planet.substring(0, 2);
        houses[idx] = houses[idx] ? houses[idx] + ',' + abbr : abbr;
      }
    });

    if (lagna) {
      const lagnaIdx = rasiOrder.indexOf(lagna.rasi);
      if (lagnaIdx !== -1) {
        houses[lagnaIdx] = 'லக்' + (houses[lagnaIdx] ? ',' + houses[lagnaIdx] : '');
      }
    }

    return `
      <div style="text-align:center;margin:15px 0;">
        <div style="font-weight:bold;font-size:14px;margin-bottom:8px;color:#92400e;">${title}</div>
        <table style="border-collapse:collapse;margin:auto;background:#fffbeb;border:2px solid #92400e;">
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[0]}</div><b>${houses[0]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[1]}</div><b>${houses[1]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[2]}</div><b>${houses[2]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[3]}</div><b>${houses[3]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[4]}</div><b>${houses[4]}</b>
            </td>
            <td colspan="2" rowspan="2" style="border:1px solid #d97706;text-align:center;background:#fef3c7;font-weight:bold;font-size:16px;color:#92400e;">
              ${isAmsam ? 'அம்சம்' : 'ராசி'}
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[5]}</div><b>${houses[5]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[6]}</div><b>${houses[6]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[7]}</div><b>${houses[7]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[8]}</div><b>${houses[8]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[9]}</div><b>${houses[9]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[10]}</div><b>${houses[10]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiTamil[11]}</div><b>${houses[11]}</b>
            </td>
          </tr>
        </table>
      </div>
    `;
  };

  // Generate life area predictions
  const generateLifeAreaPredictions = () => {
    let html = '';
    Object.entries(HOUSE_MEANINGS).forEach(([house, info]) => {
      const housePlanets = planets.filter(p => {
        const rasiOrder = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        const lagnaIndex = lagna ? rasiOrder.indexOf(lagna.rasi) : 0;
        const planetIndex = rasiOrder.indexOf(p.rasi);
        const houseNum = ((planetIndex - lagnaIndex + 12) % 12) + 1;
        return houseNum === parseInt(house);
      });

      html += `
        <div style="margin:10px 0;padding:12px;background:#fff;border:1px solid #fed7aa;border-radius:8px;">
          <div style="font-weight:bold;color:#9a3412;margin-bottom:5px;">${house}ம் வீடு - ${info.name}</div>
          <div style="font-size:11px;color:#6b7280;margin-bottom:5px;">துறைகள்: ${info.areas.join(', ')}</div>
          ${housePlanets.length > 0 ? `
            <div style="font-size:11px;color:#374151;">
              <b>கிரகங்கள்:</b> ${housePlanets.map(p => p.tamil_name + (p.is_retrograde ? ' (வ)' : '')).join(', ')}
            </div>
            <div style="font-size:11px;color:#16a34a;margin-top:5px;">
              <b>பலன்:</b> ${housePlanets.map(p => {
                const pred = DASHA_PREDICTIONS[p.tamil_name];
                return pred ? pred.positive[0] : '';
              }).filter(Boolean).join(', ')}
            </div>
          ` : '<div style="font-size:11px;color:#9ca3af;">இந்த வீட்டில் கிரகங்கள் இல்லை</div>'}
        </div>
      `;
    });
    return html;
  };

  // Generate detailed yoga analysis
  const generateYogaAnalysis = () => {
    let html = '';
    yogas.forEach((yoga, index) => {
      const yogaInfo = YOGA_DEFINITIONS[yoga.name] || {};
      html += `
        <div style="page-break-inside:avoid;margin:15px 0;padding:15px;background:linear-gradient(135deg, #ecfdf5, #d1fae5);border:2px solid #10b981;border-radius:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-size:16px;font-weight:bold;color:#166534;">${index + 1}. ${yogaInfo.tamil || yoga.tamil_name || yoga.name}</span>
            <span style="background:#16a34a;color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;">${yoga.strength}% பலம்</span>
          </div>

          <div style="margin:10px 0;padding:10px;background:#fff;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#374151;margin-bottom:5px;">யோக உருவாக்கம்:</div>
            <div style="font-size:11px;color:#6b7280;">${yogaInfo.formation || yoga.description || '-'}</div>
          </div>

          ${yogaInfo.effects ? `
          <div style="margin:10px 0;">
            <div style="font-size:12px;font-weight:bold;color:#374151;margin-bottom:5px;">எதிர்பார்க்கும் பலன்கள்:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${yogaInfo.effects.map(e => `<li>${e}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          <div style="margin-top:10px;padding:10px;background:#fef3c7;border-radius:8px;">
            <div style="font-size:11px;color:#92400e;">
              <b>செயல்படும் காலம்:</b> ${yogaInfo.activation || 'சம்பந்தப்பட்ட கிரக தசையில்'}
            </div>
          </div>
        </div>
      `;
    });
    return html;
  };

  // Generate dasha timeline analysis
  const generateDashaAnalysis = () => {
    if (!dasha?.all_periods) return '';

    let html = '<div style="page-break-before:always;"></div><h2 style="color:#6b21a8;border-bottom:2px solid #c4b5fd;padding-bottom:5px;">விரிவான தசா புக்தி பலன்கள்</h2>';

    dasha.all_periods.forEach((period, index) => {
      const pred = DASHA_PREDICTIONS[period.tamil_lord] || {};
      const isCurrent = period.is_current;

      html += `
        <div style="page-break-inside:avoid;margin:15px 0;padding:15px;background:${isCurrent ? 'linear-gradient(135deg, #fef3c7, #fde68a)' : '#fff'};border:2px solid ${isCurrent ? '#f59e0b' : '#e5e7eb'};border-radius:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-size:16px;font-weight:bold;color:${isCurrent ? '#92400e' : '#374151'};">
              ${period.tamil_lord} மகா தசை ${isCurrent ? '(தற்போது நடப்பில்)' : ''}
            </span>
            <span style="font-size:12px;color:#6b7280;">${period.start} - ${period.end} (${period.years} வருடம்)</span>
          </div>

          ${pred.positive ? `
          <div style="margin:10px 0;padding:10px;background:#ecfdf5;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#166534;margin-bottom:5px;">சாதகமான பலன்கள்:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.positive.map(p => `<li>${p}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          ${pred.challenges ? `
          <div style="margin:10px 0;padding:10px;background:#fef2f2;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#dc2626;margin-bottom:5px;">கவனிக்க வேண்டியவை:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.challenges.map(c => `<li>${c}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          ${pred.remedies ? `
          <div style="margin:10px 0;padding:10px;background:#eff6ff;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#1d4ed8;margin-bottom:5px;">பரிகாரங்கள்:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.remedies.map(r => `<li>${r}</li>`).join('')}
            </ul>
          </div>
          ` : ''}
        </div>
      `;
    });

    return html;
  };

  // Generate AI summary
  const generateAISummary = () => {
    const strongPlanets = planets.filter(p => (p.strength || 50) >= 60);
    const weakPlanets = planets.filter(p => (p.strength || 50) < 40);
    const currentDasha = dasha?.current_mahadasha?.tamil_lord || dasha?.all_periods?.find(p => p.is_current)?.tamil_lord || '-';

    return `
      <div style="page-break-before:always;"></div>
      <h2 style="color:#7c3aed;border-bottom:2px solid #c4b5fd;padding-bottom:5px;">AI ஜோதிட பகுப்பாய்வு சுருக்கம்</h2>

      <div style="background:linear-gradient(135deg, #faf5ff, #f3e8ff);padding:20px;border-radius:12px;border:2px solid #a855f7;">
        <h3 style="color:#6b21a8;margin-top:0;">ஜாதக அறிமுகம்</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${userProfile?.name || 'நபர்'} அவர்களின் ஜாதகத்தை ஆராய்ந்ததில், <b>${moonSign?.rasi_tamil || ''}</b> ராசியில்
          சந்திரன் <b>${moonSign?.nakshatra || ''}</b> நட்சத்திரத்தில் ${moonSign?.nakshatra_pada || ''}ம் பாதத்தில் அமைந்துள்ளது.
          லக்னம் <b>${lagna?.rasi_tamil || ''}</b> ராசியில் உள்ளது.
        </p>

        <h3 style="color:#6b21a8;">ராசி பண்புகள்</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${moonSign?.rasi_tamil || ''} ராசி <b>${rasiDetails.element || ''}</b> தத்துவத்தைக் கொண்டது.
          இந்த ராசிக்கு அதிபதி <b>${rasiDetails.ruler || ''}</b>.
          ${rasiDetails.quality ? `முக்கிய பண்புகள்: ${rasiDetails.quality}.` : ''}
          ${rasiDetails.career ? `பொருத்தமான தொழில்கள்: ${rasiDetails.career}.` : ''}
        </p>

        <h3 style="color:#6b21a8;">நட்சத்திர பண்புகள்</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${moonSign?.nakshatra || ''} நட்சத்திரத்தின் அதிதேவதை <b>${nakshatraDetails.deity || ''}</b>.
          ${nakshatraDetails.quality ? `இந்த நட்சத்திரத்தின் சிறப்பு பண்பு: ${nakshatraDetails.quality}.` : ''}
          ${nakshatraDetails.career ? `பொருத்தமான தொழில்: ${nakshatraDetails.career}.` : ''}
          ${nakshatraDetails.lucky_gems ? `அதிர்ஷ்ட கல்: ${nakshatraDetails.lucky_gems}.` : ''}
        </p>

        <h3 style="color:#6b21a8;">கிரக பலம் பகுப்பாய்வு</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${strongPlanets.length > 0 ? `<b>பலமான கிரகங்கள்:</b> ${strongPlanets.map(p => p.tamil_name).join(', ')} - இவை நல்ல பலன்களை தரும்.` : ''}
          ${weakPlanets.length > 0 ? `<br/><b>பலவீனமான கிரகங்கள்:</b> ${weakPlanets.map(p => p.tamil_name).join(', ')} - இவற்றிற்கு பரிகாரம் தேவை.` : ''}
        </p>

        <h3 style="color:#6b21a8;">தற்போதைய தசா நிலை</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          தற்போது <b>${currentDasha}</b> மகா தசை நடைபெறுகிறது.
          ${DASHA_PREDICTIONS[currentDasha]?.positive ?
            `இந்த காலகட்டத்தில் ${DASHA_PREDICTIONS[currentDasha].positive.slice(0, 3).join(', ')} போன்ற நல்ல பலன்கள் எதிர்பார்க்கலாம்.` : ''
          }
        </p>

        <h3 style="color:#6b21a8;">யோக பலன்கள்</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${yogas.length > 0 ?
            `இந்த ஜாதகத்தில் ${yogas.length} சிறப்பு யோகங்கள் உள்ளன: ${yogas.map(y => y.tamil_name || y.name).join(', ')}.
            இவை வாழ்வில் சிறப்பான பலன்களை தரும்.` :
            'குறிப்பிட்ட யோகங்கள் எதுவும் கணக்கிடப்படவில்லை.'
          }
        </p>

        <h3 style="color:#6b21a8;">அதிர்ஷ்ட அம்சங்கள்</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          <b>அதிர்ஷ்ட நிறம்:</b> ${rasiDetails.lucky_color || '-'}<br/>
          <b>அதிர்ஷ்ட எண்:</b> ${rasiDetails.lucky_number || '-'}<br/>
          <b>அதிர்ஷ்ட கல்:</b> ${nakshatraDetails.lucky_gems || '-'}
        </p>
      </div>
    `;
  };

  // Main HTML
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        @page { margin: 15mm; size: A4; }
        body {
          font-family: Arial, sans-serif;
          font-size: 12px;
          line-height: 1.6;
          color: #374151;
          background: #fffbeb;
        }
        .header {
          text-align: center;
          border: 3px solid #f97316;
          border-radius: 15px;
          padding: 20px;
          background: linear-gradient(135deg, #fff, #fff7ed);
          margin-bottom: 20px;
        }
        .header h1 {
          color: #9a3412;
          margin: 0;
          font-size: 28px;
        }
        .header .subtitle {
          color: #6b7280;
          margin-top: 5px;
          font-size: 14px;
        }
        .section {
          background: #fff;
          border: 1px solid #fed7aa;
          border-radius: 12px;
          padding: 15px;
          margin-bottom: 15px;
          page-break-inside: avoid;
        }
        .section-title {
          color: #9a3412;
          font-size: 16px;
          font-weight: bold;
          border-bottom: 2px solid #fed7aa;
          padding-bottom: 8px;
          margin-bottom: 12px;
        }
        .info-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }
        .info-item {
          flex: 1;
          min-width: 30%;
          background: #fff7ed;
          padding: 12px;
          border-radius: 8px;
          border: 1px solid #fed7aa;
        }
        .info-label {
          font-size: 10px;
          color: #6b7280;
          text-transform: uppercase;
        }
        .info-value {
          font-size: 14px;
          font-weight: bold;
          color: #1f2937;
          margin-top: 3px;
        }
        .charts-container {
          display: flex;
          justify-content: space-around;
          flex-wrap: wrap;
          margin: 15px 0;
        }
        table.planets {
          width: 100%;
          border-collapse: collapse;
          font-size: 11px;
          margin-top: 10px;
        }
        table.planets th {
          background: #fff7ed;
          color: #9a3412;
          padding: 10px;
          text-align: left;
          border: 1px solid #fed7aa;
        }
        table.planets td {
          padding: 10px;
          border: 1px solid #fed7aa;
        }
        table.planets tr:nth-child(even) {
          background: #fffbeb;
        }
        .footer {
          text-align: center;
          margin-top: 30px;
          padding: 15px;
          background: linear-gradient(135deg, #f97316, #ea580c);
          color: #fff;
          border-radius: 10px;
          font-size: 11px;
        }
        h2 {
          color: #9a3412;
          font-size: 18px;
          margin-top: 25px;
        }
        .page-break { page-break-before: always; }
      </style>
    </head>
    <body>
      <!-- Cover Page -->
      <div class="header">
        <div style="font-size:40px;color:#f97316;">ஓம்</div>
        <h1>ஜாதக அறிக்கை</h1>
        <div class="subtitle">விரிவான ஜோதிட பகுப்பாய்வு</div>
        <div style="margin-top:15px;font-size:16px;color:#374151;font-weight:bold;">${userProfile?.name || ''}</div>
        <div style="color:#6b7280;font-size:12px;">அறிக்கை தேதி: ${currentDate}</div>
      </div>

      <!-- Birth Details -->
      <div class="section">
        <div class="section-title">பிறப்பு விவரங்கள்</div>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">பெயர்</div>
            <div class="info-value">${userProfile?.name || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">பிறந்த தேதி</div>
            <div class="info-value">${userProfile?.birthDate || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">பிறந்த நேரம்</div>
            <div class="info-value">${userProfile?.birthTime || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">பிறந்த இடம்</div>
            <div class="info-value">${userProfile?.birthPlace || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">ராசி</div>
            <div class="info-value">${moonSign?.rasi_tamil || userProfile?.rasi || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">நட்சத்திரம்</div>
            <div class="info-value">${moonSign?.nakshatra || userProfile?.nakshatra || '-'} - ${moonSign?.nakshatra_pada || ''}ம் பாதம்</div>
          </div>
          <div class="info-item">
            <div class="info-label">லக்னம்</div>
            <div class="info-value">${lagna?.rasi_tamil || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">லக்ன நட்சத்திரம்</div>
            <div class="info-value">${lagna?.nakshatra || '-'}</div>
          </div>
        </div>
      </div>

      <!-- Panchagam -->
      <div class="section">
        <div class="section-title">பஞ்சாங்கம் விவரங்கள்</div>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">திதி</div>
            <div class="info-value">${chartData?.panchagam?.tithi || 'சுக்ல பஞ்சமி'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">வாரம்</div>
            <div class="info-value">${chartData?.panchagam?.vaaram || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">யோகம்</div>
            <div class="info-value">${chartData?.panchagam?.yogam || 'சித்த யோகம்'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">கரணம்</div>
            <div class="info-value">${chartData?.panchagam?.karanam || 'பவ கரணம்'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">சூரிய உதயம்</div>
            <div class="info-value">${chartData?.panchagam?.sunrise || '06:00'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">சூரிய அஸ்தமனம்</div>
            <div class="info-value">${chartData?.panchagam?.sunset || '18:00'}</div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="section">
        <div class="section-title">ஜாதக கட்டங்கள்</div>
        <div class="charts-container">
          ${generateChartHTML('ராசி கட்டம்', false)}
          ${generateChartHTML('நவாம்ச கட்டம்', true)}
        </div>
      </div>

      <!-- Planet Positions -->
      <div class="section">
        <div class="section-title">கிரக நிலை விவரங்கள்</div>
        <table class="planets">
          <tr>
            <th>கிரகம்</th>
            <th>ராசி</th>
            <th>டிகிரி</th>
            <th>நட்சத்திரம்</th>
            <th>பாதம்</th>
            <th>பலம்</th>
            <th>நிலை</th>
          </tr>
          ${planets.map(p => `
            <tr>
              <td><b>${p.symbol} ${p.tamil_name}</b>${p.is_retrograde ? ' <span style="color:red;">(வக்கிரம்)</span>' : ''}</td>
              <td>${p.rasi_tamil}</td>
              <td>${p.degree?.toFixed(2) || '-'}°</td>
              <td>${p.nakshatra}</td>
              <td>${p.nakshatra_pada}</td>
              <td>
                <span style="background:${(p.strength || 50) >= 60 ? '#dcfce7' : (p.strength || 50) >= 40 ? '#fef3c7' : '#fef2f2'};padding:2px 8px;border-radius:10px;">
                  ${p.strength || 50}%
                </span>
              </td>
              <td>${p.trend === 'up' ? '↑ நல்லது' : p.trend === 'down' ? '↓ கவனம்' : '→ சாதாரணம்'}</td>
            </tr>
          `).join('')}
        </table>
      </div>

      <!-- AI Summary -->
      ${generateAISummary()}

      <!-- Yoga Analysis -->
      <div class="page-break"></div>
      <h2 style="color:#166534;border-bottom:2px solid #86efac;padding-bottom:5px;">விரிவான யோக பகுப்பாய்வு</h2>
      ${yogas.length > 0 ? generateYogaAnalysis() : '<p>குறிப்பிட்ட யோகங்கள் கணக்கிடப்படவில்லை.</p>'}

      <!-- Dasha Analysis -->
      ${generateDashaAnalysis()}

      <!-- Life Area Predictions -->
      <div class="page-break"></div>
      <h2 style="color:#9a3412;border-bottom:2px solid #fed7aa;padding-bottom:5px;">வாழ்க்கை துறை பலன்கள் (12 வீடுகள்)</h2>
      ${generateLifeAreaPredictions()}

      <!-- Footer -->
      <div class="footer">
        <div style="font-size:14px;font-weight:bold;">ஜோதிட AI</div>
        <div>உங்கள் நம்பகமான ஜோதிட துணைவர்</div>
        <div style="margin-top:5px;">இந்த அறிக்கை AI உதவியுடன் உருவாக்கப்பட்டது</div>
        <div style="margin-top:10px;font-size:10px;">© ${new Date().getFullYear()} Jothida AI. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.</div>
      </div>
    </body>
    </html>
  `;
}

export default { generateComprehensivePDFHTML };
