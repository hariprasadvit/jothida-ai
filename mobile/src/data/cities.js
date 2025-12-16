/**
 * Comprehensive City Database for Jothida AI
 * Contains cities from all Indian states and major world cities
 * Each city has: name (local), nameEn (English), lat, lng, state/country
 */

// =============================================
// INDIA - ALL STATES & UNION TERRITORIES
// =============================================

// Tamil Nadu
export const TAMIL_NADU_CITIES = [
  { name: 'சென்னை', nameEn: 'Chennai', lat: 13.0827, lng: 80.2707, state: 'Tamil Nadu' },
  { name: 'மதுரை', nameEn: 'Madurai', lat: 9.9252, lng: 78.1198, state: 'Tamil Nadu' },
  { name: 'கோயம்புத்தூர்', nameEn: 'Coimbatore', lat: 11.0168, lng: 76.9558, state: 'Tamil Nadu' },
  { name: 'திருச்சி', nameEn: 'Tiruchirappalli', lat: 10.7905, lng: 78.7047, state: 'Tamil Nadu' },
  { name: 'சேலம்', nameEn: 'Salem', lat: 11.6643, lng: 78.1460, state: 'Tamil Nadu' },
  { name: 'திருநெல்வேலி', nameEn: 'Tirunelveli', lat: 8.7139, lng: 77.7567, state: 'Tamil Nadu' },
  { name: 'ஈரோடு', nameEn: 'Erode', lat: 11.3410, lng: 77.7172, state: 'Tamil Nadu' },
  { name: 'வேலூர்', nameEn: 'Vellore', lat: 12.9165, lng: 79.1325, state: 'Tamil Nadu' },
  { name: 'தஞ்சாவூர்', nameEn: 'Thanjavur', lat: 10.7870, lng: 79.1378, state: 'Tamil Nadu' },
  { name: 'திண்டுக்கல்', nameEn: 'Dindigul', lat: 10.3624, lng: 77.9695, state: 'Tamil Nadu' },
  { name: 'நாகர்கோவில்', nameEn: 'Nagercoil', lat: 8.1833, lng: 77.4119, state: 'Tamil Nadu' },
  { name: 'காஞ்சிபுரம்', nameEn: 'Kanchipuram', lat: 12.8342, lng: 79.7036, state: 'Tamil Nadu' },
  { name: 'குடந்தை', nameEn: 'Kumbakonam', lat: 10.9617, lng: 79.3881, state: 'Tamil Nadu' },
  { name: 'கரூர்', nameEn: 'Karur', lat: 10.9601, lng: 78.0766, state: 'Tamil Nadu' },
  { name: 'தூத்துக்குடி', nameEn: 'Thoothukudi', lat: 8.7642, lng: 78.1348, state: 'Tamil Nadu' },
  { name: 'விருதுநகர்', nameEn: 'Virudhunagar', lat: 9.5680, lng: 77.9624, state: 'Tamil Nadu' },
  { name: 'ராமநாதபுரம்', nameEn: 'Ramanathapuram', lat: 9.3639, lng: 78.8395, state: 'Tamil Nadu' },
  { name: 'புதுக்கோட்டை', nameEn: 'Pudukkottai', lat: 10.3833, lng: 78.8001, state: 'Tamil Nadu' },
  { name: 'சிவகங்கை', nameEn: 'Sivaganga', lat: 9.8433, lng: 78.4809, state: 'Tamil Nadu' },
  { name: 'நாமக்கல்', nameEn: 'Namakkal', lat: 11.2189, lng: 78.1674, state: 'Tamil Nadu' },
  { name: 'திருப்பூர்', nameEn: 'Tiruppur', lat: 11.1085, lng: 77.3411, state: 'Tamil Nadu' },
  { name: 'கன்னியாகுமரி', nameEn: 'Kanyakumari', lat: 8.0883, lng: 77.5385, state: 'Tamil Nadu' },
  { name: 'தேனி', nameEn: 'Theni', lat: 10.0104, lng: 77.4768, state: 'Tamil Nadu' },
  { name: 'விழுப்புரம்', nameEn: 'Villupuram', lat: 11.9401, lng: 79.4861, state: 'Tamil Nadu' },
  { name: 'கடலூர்', nameEn: 'Cuddalore', lat: 11.7480, lng: 79.7714, state: 'Tamil Nadu' },
  { name: 'நாகப்பட்டினம்', nameEn: 'Nagapattinam', lat: 10.7672, lng: 79.8449, state: 'Tamil Nadu' },
  { name: 'திருவாரூர்', nameEn: 'Tiruvarur', lat: 10.7668, lng: 79.6345, state: 'Tamil Nadu' },
  { name: 'பெரம்பலூர்', nameEn: 'Perambalur', lat: 11.2340, lng: 78.8807, state: 'Tamil Nadu' },
  { name: 'அரியலூர்', nameEn: 'Ariyalur', lat: 11.1428, lng: 79.0783, state: 'Tamil Nadu' },
  { name: 'கிருஷ்ணகிரி', nameEn: 'Krishnagiri', lat: 12.5266, lng: 78.2141, state: 'Tamil Nadu' },
  { name: 'தர்மபுரி', nameEn: 'Dharmapuri', lat: 12.1211, lng: 78.1582, state: 'Tamil Nadu' },
  { name: 'திருவண்ணாமலை', nameEn: 'Tiruvannamalai', lat: 12.2253, lng: 79.0747, state: 'Tamil Nadu' },
  { name: 'ஓசூர்', nameEn: 'Hosur', lat: 12.7409, lng: 77.8253, state: 'Tamil Nadu' },
  { name: 'ஆம்பூர்', nameEn: 'Ambur', lat: 12.7910, lng: 78.7160, state: 'Tamil Nadu' },
  { name: 'திருப்பத்தூர்', nameEn: 'Tirupattur', lat: 12.4955, lng: 78.5730, state: 'Tamil Nadu' },
  { name: 'ராணிப்பேட்டை', nameEn: 'Ranipet', lat: 12.9224, lng: 79.3326, state: 'Tamil Nadu' },
  { name: 'ஆரணி', nameEn: 'Arani', lat: 12.6691, lng: 79.2843, state: 'Tamil Nadu' },
  { name: 'சிதம்பரம்', nameEn: 'Chidambaram', lat: 11.3992, lng: 79.6912, state: 'Tamil Nadu' },
  { name: 'மயிலாடுதுறை', nameEn: 'Mayiladuthurai', lat: 11.1018, lng: 79.6551, state: 'Tamil Nadu' },
  { name: 'காரைக்கால்', nameEn: 'Karaikal', lat: 10.9254, lng: 79.8380, state: 'Tamil Nadu' },
  { name: 'பொள்ளாச்சி', nameEn: 'Pollachi', lat: 10.6609, lng: 77.0087, state: 'Tamil Nadu' },
  { name: 'உதகமண்டலம்', nameEn: 'Ooty', lat: 11.4102, lng: 76.6950, state: 'Tamil Nadu' },
  { name: 'கொடைக்கானல்', nameEn: 'Kodaikanal', lat: 10.2381, lng: 77.4892, state: 'Tamil Nadu' },
  { name: 'ஸ்ரீவில்லிபுத்தூர்', nameEn: 'Srivilliputhur', lat: 9.5121, lng: 77.6336, state: 'Tamil Nadu' },
  { name: 'திருவாடானை', nameEn: 'Tiruvadanai', lat: 9.7513, lng: 78.9943, state: 'Tamil Nadu' },
  { name: 'பரமக்குடி', nameEn: 'Paramakudi', lat: 9.5459, lng: 78.5909, state: 'Tamil Nadu' },
  { name: 'கோவில்பட்டி', nameEn: 'Kovilpatti', lat: 9.1741, lng: 77.8696, state: 'Tamil Nadu' },
  { name: 'தென்காசி', nameEn: 'Tenkasi', lat: 8.9604, lng: 77.3152, state: 'Tamil Nadu' },
  { name: 'சங்கரன்கோவில்', nameEn: 'Sankarankovil', lat: 9.1667, lng: 77.5333, state: 'Tamil Nadu' },
  { name: 'கடையநல்லூர்', nameEn: 'Kadayanallur', lat: 9.0731, lng: 77.3418, state: 'Tamil Nadu' },
];

// Kerala
export const KERALA_CITIES = [
  { name: 'Thiruvananthapuram', nameEn: 'Thiruvananthapuram', lat: 8.5241, lng: 76.9366, state: 'Kerala' },
  { name: 'Kochi', nameEn: 'Kochi', lat: 9.9312, lng: 76.2673, state: 'Kerala' },
  { name: 'Kozhikode', nameEn: 'Kozhikode', lat: 11.2588, lng: 75.7804, state: 'Kerala' },
  { name: 'Thrissur', nameEn: 'Thrissur', lat: 10.5276, lng: 76.2144, state: 'Kerala' },
  { name: 'Kannur', nameEn: 'Kannur', lat: 11.8745, lng: 75.3704, state: 'Kerala' },
  { name: 'Kollam', nameEn: 'Kollam', lat: 8.8932, lng: 76.6141, state: 'Kerala' },
  { name: 'Palakkad', nameEn: 'Palakkad', lat: 10.7867, lng: 76.6548, state: 'Kerala' },
  { name: 'Alappuzha', nameEn: 'Alappuzha', lat: 9.4981, lng: 76.3388, state: 'Kerala' },
  { name: 'Malappuram', nameEn: 'Malappuram', lat: 11.0510, lng: 76.0711, state: 'Kerala' },
  { name: 'Kottayam', nameEn: 'Kottayam', lat: 9.5916, lng: 76.5222, state: 'Kerala' },
  { name: 'Kasaragod', nameEn: 'Kasaragod', lat: 12.4996, lng: 74.9869, state: 'Kerala' },
  { name: 'Pathanamthitta', nameEn: 'Pathanamthitta', lat: 9.2648, lng: 76.7870, state: 'Kerala' },
  { name: 'Idukki', nameEn: 'Idukki', lat: 9.8494, lng: 76.9714, state: 'Kerala' },
  { name: 'Wayanad', nameEn: 'Wayanad', lat: 11.6854, lng: 76.1320, state: 'Kerala' },
  { name: 'Munnar', nameEn: 'Munnar', lat: 10.0889, lng: 77.0595, state: 'Kerala' },
  { name: 'Guruvayur', nameEn: 'Guruvayur', lat: 10.5935, lng: 76.0410, state: 'Kerala' },
];

// Karnataka
export const KARNATAKA_CITIES = [
  { name: 'ಬೆಂಗಳೂರು', nameEn: 'Bangalore', lat: 12.9716, lng: 77.5946, state: 'Karnataka' },
  { name: 'ಮೈಸೂರು', nameEn: 'Mysore', lat: 12.2958, lng: 76.6394, state: 'Karnataka' },
  { name: 'ಮಂಗಳೂರು', nameEn: 'Mangalore', lat: 12.9141, lng: 74.8560, state: 'Karnataka' },
  { name: 'ಹುಬ್ಬಳ್ಳಿ', nameEn: 'Hubli', lat: 15.3647, lng: 75.1240, state: 'Karnataka' },
  { name: 'ಬೆಳಗಾವಿ', nameEn: 'Belgaum', lat: 15.8497, lng: 74.4977, state: 'Karnataka' },
  { name: 'ಗುಲ್ಬರ್ಗಾ', nameEn: 'Gulbarga', lat: 17.3297, lng: 76.8343, state: 'Karnataka' },
  { name: 'ದಾವಣಗೆರೆ', nameEn: 'Davangere', lat: 14.4644, lng: 75.9218, state: 'Karnataka' },
  { name: 'ಬಳ್ಳಾರಿ', nameEn: 'Bellary', lat: 15.1394, lng: 76.9214, state: 'Karnataka' },
  { name: 'ಶಿವಮೊಗ್ಗ', nameEn: 'Shimoga', lat: 13.9299, lng: 75.5681, state: 'Karnataka' },
  { name: 'ತುಮಕೂರು', nameEn: 'Tumkur', lat: 13.3379, lng: 77.1173, state: 'Karnataka' },
  { name: 'ರಾಯಚೂರು', nameEn: 'Raichur', lat: 16.2120, lng: 77.3439, state: 'Karnataka' },
  { name: 'ಬೀದರ್', nameEn: 'Bidar', lat: 17.9104, lng: 77.5199, state: 'Karnataka' },
  { name: 'ಉಡುಪಿ', nameEn: 'Udupi', lat: 13.3409, lng: 74.7421, state: 'Karnataka' },
  { name: 'ಹಾಸನ', nameEn: 'Hassan', lat: 13.0068, lng: 76.1004, state: 'Karnataka' },
  { name: 'ಚಿತ್ರದುರ್ಗ', nameEn: 'Chitradurga', lat: 14.2226, lng: 76.3980, state: 'Karnataka' },
  { name: 'ಕೊಪ್ಪಳ', nameEn: 'Koppal', lat: 15.3505, lng: 76.1552, state: 'Karnataka' },
  { name: 'ಮಂಡ್ಯ', nameEn: 'Mandya', lat: 12.5218, lng: 76.8951, state: 'Karnataka' },
  { name: 'ಚಾಮರಾಜನಗರ', nameEn: 'Chamarajanagar', lat: 11.9236, lng: 76.9390, state: 'Karnataka' },
  { name: 'ಕೋಲಾರ', nameEn: 'Kolar', lat: 13.1360, lng: 78.1292, state: 'Karnataka' },
  { name: 'ಚಿಕ್ಕಮಗಳೂರು', nameEn: 'Chikmagalur', lat: 13.3161, lng: 75.7720, state: 'Karnataka' },
];

// Andhra Pradesh
export const ANDHRA_PRADESH_CITIES = [
  { name: 'Visakhapatnam', nameEn: 'Visakhapatnam', lat: 17.6868, lng: 83.2185, state: 'Andhra Pradesh' },
  { name: 'Vijayawada', nameEn: 'Vijayawada', lat: 16.5062, lng: 80.6480, state: 'Andhra Pradesh' },
  { name: 'Guntur', nameEn: 'Guntur', lat: 16.3067, lng: 80.4365, state: 'Andhra Pradesh' },
  { name: 'Nellore', nameEn: 'Nellore', lat: 14.4426, lng: 79.9865, state: 'Andhra Pradesh' },
  { name: 'Tirupati', nameEn: 'Tirupati', lat: 13.6288, lng: 79.4192, state: 'Andhra Pradesh' },
  { name: 'Rajahmundry', nameEn: 'Rajahmundry', lat: 17.0005, lng: 81.8040, state: 'Andhra Pradesh' },
  { name: 'Kakinada', nameEn: 'Kakinada', lat: 16.9891, lng: 82.2475, state: 'Andhra Pradesh' },
  { name: 'Kadapa', nameEn: 'Kadapa', lat: 14.4674, lng: 78.8241, state: 'Andhra Pradesh' },
  { name: 'Anantapur', nameEn: 'Anantapur', lat: 14.6819, lng: 77.6006, state: 'Andhra Pradesh' },
  { name: 'Kurnool', nameEn: 'Kurnool', lat: 15.8281, lng: 78.0373, state: 'Andhra Pradesh' },
  { name: 'Eluru', nameEn: 'Eluru', lat: 16.7107, lng: 81.0952, state: 'Andhra Pradesh' },
  { name: 'Ongole', nameEn: 'Ongole', lat: 15.5057, lng: 80.0499, state: 'Andhra Pradesh' },
  { name: 'Chittoor', nameEn: 'Chittoor', lat: 13.2172, lng: 79.1003, state: 'Andhra Pradesh' },
  { name: 'Srikakulam', nameEn: 'Srikakulam', lat: 18.2949, lng: 83.8938, state: 'Andhra Pradesh' },
  { name: 'Vizianagaram', nameEn: 'Vizianagaram', lat: 18.1066, lng: 83.3956, state: 'Andhra Pradesh' },
  { name: 'Amaravati', nameEn: 'Amaravati', lat: 16.5131, lng: 80.5158, state: 'Andhra Pradesh' },
];

// Telangana
export const TELANGANA_CITIES = [
  { name: 'హైదరాబాద్', nameEn: 'Hyderabad', lat: 17.3850, lng: 78.4867, state: 'Telangana' },
  { name: 'Warangal', nameEn: 'Warangal', lat: 17.9784, lng: 79.5941, state: 'Telangana' },
  { name: 'Nizamabad', nameEn: 'Nizamabad', lat: 18.6725, lng: 78.0941, state: 'Telangana' },
  { name: 'Karimnagar', nameEn: 'Karimnagar', lat: 18.4386, lng: 79.1288, state: 'Telangana' },
  { name: 'Khammam', nameEn: 'Khammam', lat: 17.2473, lng: 80.1514, state: 'Telangana' },
  { name: 'Mahbubnagar', nameEn: 'Mahbubnagar', lat: 16.7488, lng: 77.9855, state: 'Telangana' },
  { name: 'Nalgonda', nameEn: 'Nalgonda', lat: 17.0500, lng: 79.2667, state: 'Telangana' },
  { name: 'Adilabad', nameEn: 'Adilabad', lat: 19.6667, lng: 78.5333, state: 'Telangana' },
  { name: 'Secunderabad', nameEn: 'Secunderabad', lat: 17.4399, lng: 78.4983, state: 'Telangana' },
  { name: 'Sangareddy', nameEn: 'Sangareddy', lat: 17.6186, lng: 78.0866, state: 'Telangana' },
  { name: 'Siddipet', nameEn: 'Siddipet', lat: 18.1018, lng: 78.8520, state: 'Telangana' },
];

// Maharashtra
export const MAHARASHTRA_CITIES = [
  { name: 'मुंबई', nameEn: 'Mumbai', lat: 19.0760, lng: 72.8777, state: 'Maharashtra' },
  { name: 'पुणे', nameEn: 'Pune', lat: 18.5204, lng: 73.8567, state: 'Maharashtra' },
  { name: 'नागपूर', nameEn: 'Nagpur', lat: 21.1458, lng: 79.0882, state: 'Maharashtra' },
  { name: 'ठाणे', nameEn: 'Thane', lat: 19.2183, lng: 72.9781, state: 'Maharashtra' },
  { name: 'नाशिक', nameEn: 'Nashik', lat: 19.9975, lng: 73.7898, state: 'Maharashtra' },
  { name: 'औरंगाबाद', nameEn: 'Aurangabad', lat: 19.8762, lng: 75.3433, state: 'Maharashtra' },
  { name: 'सोलापूर', nameEn: 'Solapur', lat: 17.6599, lng: 75.9064, state: 'Maharashtra' },
  { name: 'अमरावती', nameEn: 'Amravati', lat: 20.9374, lng: 77.7796, state: 'Maharashtra' },
  { name: 'कोल्हापूर', nameEn: 'Kolhapur', lat: 16.7050, lng: 74.2433, state: 'Maharashtra' },
  { name: 'नवी मुंबई', nameEn: 'Navi Mumbai', lat: 19.0330, lng: 73.0297, state: 'Maharashtra' },
  { name: 'सांगली', nameEn: 'Sangli', lat: 16.8524, lng: 74.5815, state: 'Maharashtra' },
  { name: 'जळगाव', nameEn: 'Jalgaon', lat: 21.0077, lng: 75.5626, state: 'Maharashtra' },
  { name: 'अकोला', nameEn: 'Akola', lat: 20.7002, lng: 77.0082, state: 'Maharashtra' },
  { name: 'लातूर', nameEn: 'Latur', lat: 18.4088, lng: 76.5604, state: 'Maharashtra' },
  { name: 'धुळे', nameEn: 'Dhule', lat: 20.9042, lng: 74.7749, state: 'Maharashtra' },
  { name: 'अहमदनगर', nameEn: 'Ahmednagar', lat: 19.0948, lng: 74.7480, state: 'Maharashtra' },
  { name: 'चंद्रपूर', nameEn: 'Chandrapur', lat: 19.9500, lng: 79.3000, state: 'Maharashtra' },
  { name: 'पर्भणी', nameEn: 'Parbhani', lat: 19.2667, lng: 76.7667, state: 'Maharashtra' },
  { name: 'शिर्डी', nameEn: 'Shirdi', lat: 19.7645, lng: 74.4768, state: 'Maharashtra' },
];

// Gujarat
export const GUJARAT_CITIES = [
  { name: 'અમદાવાદ', nameEn: 'Ahmedabad', lat: 23.0225, lng: 72.5714, state: 'Gujarat' },
  { name: 'સુરત', nameEn: 'Surat', lat: 21.1702, lng: 72.8311, state: 'Gujarat' },
  { name: 'વડોદરા', nameEn: 'Vadodara', lat: 22.3072, lng: 73.1812, state: 'Gujarat' },
  { name: 'રાજકોટ', nameEn: 'Rajkot', lat: 22.3039, lng: 70.8022, state: 'Gujarat' },
  { name: 'ભાવનગર', nameEn: 'Bhavnagar', lat: 21.7645, lng: 72.1519, state: 'Gujarat' },
  { name: 'જામનગર', nameEn: 'Jamnagar', lat: 22.4707, lng: 70.0577, state: 'Gujarat' },
  { name: 'જૂનાગઢ', nameEn: 'Junagadh', lat: 21.5222, lng: 70.4579, state: 'Gujarat' },
  { name: 'ગાંધીનગર', nameEn: 'Gandhinagar', lat: 23.2156, lng: 72.6369, state: 'Gujarat' },
  { name: 'અણંદ', nameEn: 'Anand', lat: 22.5645, lng: 72.9289, state: 'Gujarat' },
  { name: 'મોરબી', nameEn: 'Morbi', lat: 22.8173, lng: 70.8370, state: 'Gujarat' },
  { name: 'નડિયાદ', nameEn: 'Nadiad', lat: 22.6916, lng: 72.8634, state: 'Gujarat' },
  { name: 'મહેસાણા', nameEn: 'Mehsana', lat: 23.5880, lng: 72.3693, state: 'Gujarat' },
  { name: 'સુરેન્દ્રનગર', nameEn: 'Surendranagar', lat: 22.7289, lng: 71.6488, state: 'Gujarat' },
  { name: 'પોરબંદર', nameEn: 'Porbandar', lat: 21.6417, lng: 69.6293, state: 'Gujarat' },
  { name: 'ભુજ', nameEn: 'Bhuj', lat: 23.2419, lng: 69.6669, state: 'Gujarat' },
  { name: 'દ્વારકા', nameEn: 'Dwarka', lat: 22.2442, lng: 68.9685, state: 'Gujarat' },
  { name: 'સોમનાથ', nameEn: 'Somnath', lat: 20.8880, lng: 70.4016, state: 'Gujarat' },
];

// Rajasthan
export const RAJASTHAN_CITIES = [
  { name: 'जयपुर', nameEn: 'Jaipur', lat: 26.9124, lng: 75.7873, state: 'Rajasthan' },
  { name: 'जोधपुर', nameEn: 'Jodhpur', lat: 26.2389, lng: 73.0243, state: 'Rajasthan' },
  { name: 'उदयपुर', nameEn: 'Udaipur', lat: 24.5854, lng: 73.7125, state: 'Rajasthan' },
  { name: 'कोटा', nameEn: 'Kota', lat: 25.2138, lng: 75.8648, state: 'Rajasthan' },
  { name: 'बीकानेर', nameEn: 'Bikaner', lat: 28.0229, lng: 73.3119, state: 'Rajasthan' },
  { name: 'अजमेर', nameEn: 'Ajmer', lat: 26.4499, lng: 74.6399, state: 'Rajasthan' },
  { name: 'भरतपुर', nameEn: 'Bharatpur', lat: 27.2152, lng: 77.5030, state: 'Rajasthan' },
  { name: 'अलवर', nameEn: 'Alwar', lat: 27.5530, lng: 76.6346, state: 'Rajasthan' },
  { name: 'सीकर', nameEn: 'Sikar', lat: 27.6094, lng: 75.1399, state: 'Rajasthan' },
  { name: 'श्रीगंगानगर', nameEn: 'Sri Ganganagar', lat: 29.9038, lng: 73.8772, state: 'Rajasthan' },
  { name: 'पाली', nameEn: 'Pali', lat: 25.7711, lng: 73.3234, state: 'Rajasthan' },
  { name: 'जैसलमेर', nameEn: 'Jaisalmer', lat: 26.9157, lng: 70.9083, state: 'Rajasthan' },
  { name: 'झुंझुनू', nameEn: 'Jhunjhunu', lat: 28.1289, lng: 75.3996, state: 'Rajasthan' },
  { name: 'चूरू', nameEn: 'Churu', lat: 28.2900, lng: 74.9680, state: 'Rajasthan' },
  { name: 'माउंट आबू', nameEn: 'Mount Abu', lat: 24.5926, lng: 72.7156, state: 'Rajasthan' },
  { name: 'पुष्कर', nameEn: 'Pushkar', lat: 26.4897, lng: 74.5511, state: 'Rajasthan' },
];

// Delhi NCR
export const DELHI_NCR_CITIES = [
  { name: 'नई दिल्ली', nameEn: 'New Delhi', lat: 28.6139, lng: 77.2090, state: 'Delhi' },
  { name: 'दिल्ली', nameEn: 'Delhi', lat: 28.7041, lng: 77.1025, state: 'Delhi' },
  { name: 'गुड़गांव', nameEn: 'Gurgaon', lat: 28.4595, lng: 77.0266, state: 'Haryana' },
  { name: 'नोएडा', nameEn: 'Noida', lat: 28.5355, lng: 77.3910, state: 'Uttar Pradesh' },
  { name: 'गाजियाबाद', nameEn: 'Ghaziabad', lat: 28.6692, lng: 77.4538, state: 'Uttar Pradesh' },
  { name: 'फरीदाबाद', nameEn: 'Faridabad', lat: 28.4089, lng: 77.3178, state: 'Haryana' },
  { name: 'ग्रेटर नोएडा', nameEn: 'Greater Noida', lat: 28.4744, lng: 77.5040, state: 'Uttar Pradesh' },
];

// Uttar Pradesh
export const UTTAR_PRADESH_CITIES = [
  { name: 'लखनऊ', nameEn: 'Lucknow', lat: 26.8467, lng: 80.9462, state: 'Uttar Pradesh' },
  { name: 'कानपुर', nameEn: 'Kanpur', lat: 26.4499, lng: 80.3319, state: 'Uttar Pradesh' },
  { name: 'वाराणसी', nameEn: 'Varanasi', lat: 25.3176, lng: 82.9739, state: 'Uttar Pradesh' },
  { name: 'आगरा', nameEn: 'Agra', lat: 27.1767, lng: 78.0081, state: 'Uttar Pradesh' },
  { name: 'प्रयागराज', nameEn: 'Prayagraj', lat: 25.4358, lng: 81.8463, state: 'Uttar Pradesh' },
  { name: 'मेरठ', nameEn: 'Meerut', lat: 28.9845, lng: 77.7064, state: 'Uttar Pradesh' },
  { name: 'बरेली', nameEn: 'Bareilly', lat: 28.3670, lng: 79.4304, state: 'Uttar Pradesh' },
  { name: 'अलीगढ़', nameEn: 'Aligarh', lat: 27.8974, lng: 78.0880, state: 'Uttar Pradesh' },
  { name: 'मुरादाबाद', nameEn: 'Moradabad', lat: 28.8386, lng: 78.7733, state: 'Uttar Pradesh' },
  { name: 'सहारनपुर', nameEn: 'Saharanpur', lat: 29.9680, lng: 77.5510, state: 'Uttar Pradesh' },
  { name: 'गोरखपुर', nameEn: 'Gorakhpur', lat: 26.7606, lng: 83.3732, state: 'Uttar Pradesh' },
  { name: 'मथुरा', nameEn: 'Mathura', lat: 27.4924, lng: 77.6737, state: 'Uttar Pradesh' },
  { name: 'झांसी', nameEn: 'Jhansi', lat: 25.4484, lng: 78.5685, state: 'Uttar Pradesh' },
  { name: 'अयोध्या', nameEn: 'Ayodhya', lat: 26.7922, lng: 82.1998, state: 'Uttar Pradesh' },
  { name: 'वृंदावन', nameEn: 'Vrindavan', lat: 27.5809, lng: 77.6960, state: 'Uttar Pradesh' },
];

// Madhya Pradesh
export const MADHYA_PRADESH_CITIES = [
  { name: 'भोपाल', nameEn: 'Bhopal', lat: 23.2599, lng: 77.4126, state: 'Madhya Pradesh' },
  { name: 'इंदौर', nameEn: 'Indore', lat: 22.7196, lng: 75.8577, state: 'Madhya Pradesh' },
  { name: 'जबलपुर', nameEn: 'Jabalpur', lat: 23.1815, lng: 79.9864, state: 'Madhya Pradesh' },
  { name: 'ग्वालियर', nameEn: 'Gwalior', lat: 26.2183, lng: 78.1828, state: 'Madhya Pradesh' },
  { name: 'उज्जैन', nameEn: 'Ujjain', lat: 23.1765, lng: 75.7885, state: 'Madhya Pradesh' },
  { name: 'सागर', nameEn: 'Sagar', lat: 23.8388, lng: 78.7378, state: 'Madhya Pradesh' },
  { name: 'देवास', nameEn: 'Dewas', lat: 22.9623, lng: 76.0508, state: 'Madhya Pradesh' },
  { name: 'सतना', nameEn: 'Satna', lat: 24.6005, lng: 80.8322, state: 'Madhya Pradesh' },
  { name: 'रतलाम', nameEn: 'Ratlam', lat: 23.3341, lng: 75.0387, state: 'Madhya Pradesh' },
  { name: 'रीवा', nameEn: 'Rewa', lat: 24.5373, lng: 81.2996, state: 'Madhya Pradesh' },
  { name: 'खजुराहो', nameEn: 'Khajuraho', lat: 24.8318, lng: 79.9199, state: 'Madhya Pradesh' },
  { name: 'ओंकारेश्वर', nameEn: 'Omkareshwar', lat: 22.2447, lng: 76.1519, state: 'Madhya Pradesh' },
];

// Bihar
export const BIHAR_CITIES = [
  { name: 'पटना', nameEn: 'Patna', lat: 25.5941, lng: 85.1376, state: 'Bihar' },
  { name: 'गया', nameEn: 'Gaya', lat: 24.7914, lng: 85.0002, state: 'Bihar' },
  { name: 'भागलपुर', nameEn: 'Bhagalpur', lat: 25.2425, lng: 87.0079, state: 'Bihar' },
  { name: 'मुज़फ़्फ़रपुर', nameEn: 'Muzaffarpur', lat: 26.1225, lng: 85.3906, state: 'Bihar' },
  { name: 'दरभंगा', nameEn: 'Darbhanga', lat: 26.1542, lng: 85.8918, state: 'Bihar' },
  { name: 'पूर्णिया', nameEn: 'Purnia', lat: 25.7771, lng: 87.4753, state: 'Bihar' },
  { name: 'बिहारशरीफ', nameEn: 'Bihar Sharif', lat: 25.1982, lng: 85.5150, state: 'Bihar' },
  { name: 'आरा', nameEn: 'Arrah', lat: 25.5565, lng: 84.6678, state: 'Bihar' },
  { name: 'बेगूसराय', nameEn: 'Begusarai', lat: 25.4182, lng: 86.1272, state: 'Bihar' },
  { name: 'कटिहार', nameEn: 'Katihar', lat: 25.5421, lng: 87.5714, state: 'Bihar' },
  { name: 'बोधगया', nameEn: 'Bodh Gaya', lat: 24.6961, lng: 84.9869, state: 'Bihar' },
  { name: 'राजगीर', nameEn: 'Rajgir', lat: 25.0268, lng: 85.4187, state: 'Bihar' },
  { name: 'नालंदा', nameEn: 'Nalanda', lat: 25.1351, lng: 85.4427, state: 'Bihar' },
];

// West Bengal
export const WEST_BENGAL_CITIES = [
  { name: 'কলকাতা', nameEn: 'Kolkata', lat: 22.5726, lng: 88.3639, state: 'West Bengal' },
  { name: 'হাওড়া', nameEn: 'Howrah', lat: 22.5958, lng: 88.2636, state: 'West Bengal' },
  { name: 'দুর্গাপুর', nameEn: 'Durgapur', lat: 23.5204, lng: 87.3119, state: 'West Bengal' },
  { name: 'আসানসোল', nameEn: 'Asansol', lat: 23.6739, lng: 86.9524, state: 'West Bengal' },
  { name: 'সিলিগুড়ি', nameEn: 'Siliguri', lat: 26.7271, lng: 88.3953, state: 'West Bengal' },
  { name: 'বর্ধমান', nameEn: 'Bardhaman', lat: 23.2324, lng: 87.8615, state: 'West Bengal' },
  { name: 'খড়গপুর', nameEn: 'Kharagpur', lat: 22.3460, lng: 87.3234, state: 'West Bengal' },
  { name: 'দার্জিলিং', nameEn: 'Darjeeling', lat: 27.0410, lng: 88.2663, state: 'West Bengal' },
  { name: 'মালদা', nameEn: 'Malda', lat: 25.0108, lng: 88.1411, state: 'West Bengal' },
  { name: 'কোচবিহার', nameEn: 'Cooch Behar', lat: 26.3452, lng: 89.4482, state: 'West Bengal' },
  { name: 'শান্তিনিকেতন', nameEn: 'Santiniketan', lat: 23.6784, lng: 87.6855, state: 'West Bengal' },
];

// Odisha
export const ODISHA_CITIES = [
  { name: 'ଭୁବନେଶ୍ୱର', nameEn: 'Bhubaneswar', lat: 20.2961, lng: 85.8245, state: 'Odisha' },
  { name: 'କଟକ', nameEn: 'Cuttack', lat: 20.4625, lng: 85.8830, state: 'Odisha' },
  { name: 'ରାଉରକେଲା', nameEn: 'Rourkela', lat: 22.2604, lng: 84.8536, state: 'Odisha' },
  { name: 'ବ୍ରହ୍ମପୁର', nameEn: 'Brahmapur', lat: 19.3150, lng: 84.7941, state: 'Odisha' },
  { name: 'ସମ୍ବଲପୁର', nameEn: 'Sambalpur', lat: 21.4669, lng: 83.9756, state: 'Odisha' },
  { name: 'ପୁରୀ', nameEn: 'Puri', lat: 19.8135, lng: 85.8312, state: 'Odisha' },
  { name: 'ବାଲେଶ୍ୱର', nameEn: 'Balasore', lat: 21.4934, lng: 86.9135, state: 'Odisha' },
  { name: 'ଭଦ୍ରକ', nameEn: 'Bhadrak', lat: 21.0548, lng: 86.4979, state: 'Odisha' },
  { name: 'କୋଣାର୍କ', nameEn: 'Konark', lat: 19.8876, lng: 86.0945, state: 'Odisha' },
];

// Punjab
export const PUNJAB_CITIES = [
  { name: 'ਲੁਧਿਆਣਾ', nameEn: 'Ludhiana', lat: 30.9010, lng: 75.8573, state: 'Punjab' },
  { name: 'ਅੰਮ੍ਰਿਤਸਰ', nameEn: 'Amritsar', lat: 31.6340, lng: 74.8723, state: 'Punjab' },
  { name: 'ਜਲੰਧਰ', nameEn: 'Jalandhar', lat: 31.3260, lng: 75.5762, state: 'Punjab' },
  { name: 'ਪਟਿਆਲਾ', nameEn: 'Patiala', lat: 30.3398, lng: 76.3869, state: 'Punjab' },
  { name: 'ਬਠਿੰਡਾ', nameEn: 'Bathinda', lat: 30.2110, lng: 74.9455, state: 'Punjab' },
  { name: 'ਮੋਹਾਲੀ', nameEn: 'Mohali', lat: 30.7046, lng: 76.7179, state: 'Punjab' },
  { name: 'ਹੁਸ਼ਿਆਰਪੁਰ', nameEn: 'Hoshiarpur', lat: 31.5143, lng: 75.9115, state: 'Punjab' },
  { name: 'ਪਠਾਨਕੋਟ', nameEn: 'Pathankot', lat: 32.2643, lng: 75.6421, state: 'Punjab' },
  { name: 'ਮੋਗਾ', nameEn: 'Moga', lat: 30.8231, lng: 75.1719, state: 'Punjab' },
  { name: 'ਫਿਰੋਜ਼ਪੁਰ', nameEn: 'Firozpur', lat: 30.9331, lng: 74.6225, state: 'Punjab' },
];

// Haryana
export const HARYANA_CITIES = [
  { name: 'चंडीगढ़', nameEn: 'Chandigarh', lat: 30.7333, lng: 76.7794, state: 'Chandigarh' },
  { name: 'अंबाला', nameEn: 'Ambala', lat: 30.3782, lng: 76.7767, state: 'Haryana' },
  { name: 'पानीपत', nameEn: 'Panipat', lat: 29.3909, lng: 76.9635, state: 'Haryana' },
  { name: 'यमुनानगर', nameEn: 'Yamunanagar', lat: 30.1290, lng: 77.2674, state: 'Haryana' },
  { name: 'रोहतक', nameEn: 'Rohtak', lat: 28.8955, lng: 76.6066, state: 'Haryana' },
  { name: 'हिसार', nameEn: 'Hisar', lat: 29.1492, lng: 75.7217, state: 'Haryana' },
  { name: 'करनाल', nameEn: 'Karnal', lat: 29.6857, lng: 76.9905, state: 'Haryana' },
  { name: 'सोनीपत', nameEn: 'Sonipat', lat: 28.9288, lng: 77.0913, state: 'Haryana' },
  { name: 'पंचकूला', nameEn: 'Panchkula', lat: 30.6942, lng: 76.8606, state: 'Haryana' },
  { name: 'कुरुक्षेत्र', nameEn: 'Kurukshetra', lat: 29.9695, lng: 76.8783, state: 'Haryana' },
  { name: 'भिवानी', nameEn: 'Bhiwani', lat: 28.7751, lng: 76.1323, state: 'Haryana' },
  { name: 'सिरसा', nameEn: 'Sirsa', lat: 29.5335, lng: 75.0153, state: 'Haryana' },
];

// Jharkhand
export const JHARKHAND_CITIES = [
  { name: 'रांची', nameEn: 'Ranchi', lat: 23.3441, lng: 85.3096, state: 'Jharkhand' },
  { name: 'जमशेदपुर', nameEn: 'Jamshedpur', lat: 22.8046, lng: 86.2029, state: 'Jharkhand' },
  { name: 'धनबाद', nameEn: 'Dhanbad', lat: 23.7957, lng: 86.4304, state: 'Jharkhand' },
  { name: 'बोकारो', nameEn: 'Bokaro', lat: 23.6693, lng: 86.1511, state: 'Jharkhand' },
  { name: 'हजारीबाग', nameEn: 'Hazaribagh', lat: 23.9925, lng: 85.3637, state: 'Jharkhand' },
  { name: 'देवघर', nameEn: 'Deoghar', lat: 24.4764, lng: 86.6946, state: 'Jharkhand' },
  { name: 'गिरिडीह', nameEn: 'Giridih', lat: 24.1903, lng: 86.3003, state: 'Jharkhand' },
  { name: 'दुमका', nameEn: 'Dumka', lat: 24.2640, lng: 87.2497, state: 'Jharkhand' },
];

// Chhattisgarh
export const CHHATTISGARH_CITIES = [
  { name: 'रायपुर', nameEn: 'Raipur', lat: 21.2514, lng: 81.6296, state: 'Chhattisgarh' },
  { name: 'भिलाई', nameEn: 'Bhilai', lat: 21.2094, lng: 81.4285, state: 'Chhattisgarh' },
  { name: 'बिलासपुर', nameEn: 'Bilaspur', lat: 22.0797, lng: 82.1391, state: 'Chhattisgarh' },
  { name: 'कोरबा', nameEn: 'Korba', lat: 22.3595, lng: 82.7501, state: 'Chhattisgarh' },
  { name: 'दुर्ग', nameEn: 'Durg', lat: 21.1904, lng: 81.2849, state: 'Chhattisgarh' },
  { name: 'रायगढ़', nameEn: 'Raigarh', lat: 21.8974, lng: 83.3950, state: 'Chhattisgarh' },
  { name: 'जगदलपुर', nameEn: 'Jagdalpur', lat: 19.0785, lng: 82.0217, state: 'Chhattisgarh' },
  { name: 'अंबिकापुर', nameEn: 'Ambikapur', lat: 23.1188, lng: 83.1987, state: 'Chhattisgarh' },
];

// Assam
export const ASSAM_CITIES = [
  { name: 'গুৱাহাটী', nameEn: 'Guwahati', lat: 26.1445, lng: 91.7362, state: 'Assam' },
  { name: 'শিলচৰ', nameEn: 'Silchar', lat: 24.8333, lng: 92.7789, state: 'Assam' },
  { name: 'ডিব্ৰুগড়', nameEn: 'Dibrugarh', lat: 27.4728, lng: 94.9120, state: 'Assam' },
  { name: 'জোৰহাট', nameEn: 'Jorhat', lat: 26.7509, lng: 94.2037, state: 'Assam' },
  { name: 'নগাঁও', nameEn: 'Nagaon', lat: 26.3464, lng: 92.6840, state: 'Assam' },
  { name: 'তিনচুকীয়া', nameEn: 'Tinsukia', lat: 27.4922, lng: 95.3474, state: 'Assam' },
  { name: 'তেজপুৰ', nameEn: 'Tezpur', lat: 26.6528, lng: 92.8008, state: 'Assam' },
  { name: 'বঙাইগাঁও', nameEn: 'Bongaigaon', lat: 26.4789, lng: 90.5583, state: 'Assam' },
];

// Himachal Pradesh
export const HIMACHAL_PRADESH_CITIES = [
  { name: 'शिमला', nameEn: 'Shimla', lat: 31.1048, lng: 77.1734, state: 'Himachal Pradesh' },
  { name: 'धर्मशाला', nameEn: 'Dharamshala', lat: 32.2190, lng: 76.3234, state: 'Himachal Pradesh' },
  { name: 'मनाली', nameEn: 'Manali', lat: 32.2432, lng: 77.1892, state: 'Himachal Pradesh' },
  { name: 'कुल्लू', nameEn: 'Kullu', lat: 31.9592, lng: 77.1089, state: 'Himachal Pradesh' },
  { name: 'सोलन', nameEn: 'Solan', lat: 30.9045, lng: 77.0967, state: 'Himachal Pradesh' },
  { name: 'मंडी', nameEn: 'Mandi', lat: 31.7085, lng: 76.9318, state: 'Himachal Pradesh' },
  { name: 'ऊना', nameEn: 'Una', lat: 31.4684, lng: 76.2708, state: 'Himachal Pradesh' },
  { name: 'कसौली', nameEn: 'Kasauli', lat: 30.8992, lng: 76.9656, state: 'Himachal Pradesh' },
  { name: 'डलहौजी', nameEn: 'Dalhousie', lat: 32.5387, lng: 75.9706, state: 'Himachal Pradesh' },
  { name: 'बद्दी', nameEn: 'Baddi', lat: 30.9578, lng: 76.7914, state: 'Himachal Pradesh' },
];

// Uttarakhand
export const UTTARAKHAND_CITIES = [
  { name: 'देहरादून', nameEn: 'Dehradun', lat: 30.3165, lng: 78.0322, state: 'Uttarakhand' },
  { name: 'हरिद्वार', nameEn: 'Haridwar', lat: 29.9457, lng: 78.1642, state: 'Uttarakhand' },
  { name: 'ऋषिकेश', nameEn: 'Rishikesh', lat: 30.0869, lng: 78.2676, state: 'Uttarakhand' },
  { name: 'नैनीताल', nameEn: 'Nainital', lat: 29.3919, lng: 79.4542, state: 'Uttarakhand' },
  { name: 'मसूरी', nameEn: 'Mussoorie', lat: 30.4598, lng: 78.0644, state: 'Uttarakhand' },
  { name: 'रुड़की', nameEn: 'Roorkee', lat: 29.8543, lng: 77.8880, state: 'Uttarakhand' },
  { name: 'हल्द्वानी', nameEn: 'Haldwani', lat: 29.2183, lng: 79.5130, state: 'Uttarakhand' },
  { name: 'अल्मोड़ा', nameEn: 'Almora', lat: 29.5892, lng: 79.6591, state: 'Uttarakhand' },
  { name: 'रामनगर', nameEn: 'Ramnagar', lat: 29.3940, lng: 79.1260, state: 'Uttarakhand' },
  { name: 'पिथौरागढ़', nameEn: 'Pithoragarh', lat: 29.5829, lng: 80.2181, state: 'Uttarakhand' },
  { name: 'बद्रीनाथ', nameEn: 'Badrinath', lat: 30.7433, lng: 79.4938, state: 'Uttarakhand' },
  { name: 'केदारनाथ', nameEn: 'Kedarnath', lat: 30.7346, lng: 79.0669, state: 'Uttarakhand' },
];

// Jammu & Kashmir
export const JAMMU_KASHMIR_CITIES = [
  { name: 'श्रीनगर', nameEn: 'Srinagar', lat: 34.0837, lng: 74.7973, state: 'Jammu & Kashmir' },
  { name: 'जम्मू', nameEn: 'Jammu', lat: 32.7266, lng: 74.8570, state: 'Jammu & Kashmir' },
  { name: 'गुलमर्ग', nameEn: 'Gulmarg', lat: 34.0484, lng: 74.3805, state: 'Jammu & Kashmir' },
  { name: 'पहलगाम', nameEn: 'Pahalgam', lat: 34.0161, lng: 75.3150, state: 'Jammu & Kashmir' },
  { name: 'सोनमर्ग', nameEn: 'Sonamarg', lat: 34.3048, lng: 75.2940, state: 'Jammu & Kashmir' },
  { name: 'अनंतनाग', nameEn: 'Anantnag', lat: 33.7311, lng: 75.1547, state: 'Jammu & Kashmir' },
  { name: 'बारामुला', nameEn: 'Baramulla', lat: 34.1980, lng: 74.3636, state: 'Jammu & Kashmir' },
  { name: 'लेह', nameEn: 'Leh', lat: 34.1526, lng: 77.5771, state: 'Ladakh' },
  { name: 'कारगिल', nameEn: 'Kargil', lat: 34.5539, lng: 76.1349, state: 'Ladakh' },
];

// Goa
export const GOA_CITIES = [
  { name: 'पणजी', nameEn: 'Panaji', lat: 15.4909, lng: 73.8278, state: 'Goa' },
  { name: 'मडगाव', nameEn: 'Margao', lat: 15.2832, lng: 73.9862, state: 'Goa' },
  { name: 'वास्को दा गामा', nameEn: 'Vasco da Gama', lat: 15.3982, lng: 73.8113, state: 'Goa' },
  { name: 'मापुसा', nameEn: 'Mapusa', lat: 15.5916, lng: 73.8087, state: 'Goa' },
  { name: 'पोंडा', nameEn: 'Ponda', lat: 15.4035, lng: 74.0152, state: 'Goa' },
  { name: 'कालंगुट', nameEn: 'Calangute', lat: 15.5449, lng: 73.7553, state: 'Goa' },
  { name: 'बागा', nameEn: 'Baga', lat: 15.5549, lng: 73.7515, state: 'Goa' },
];

// North Eastern States
export const NORTHEAST_CITIES = [
  { name: 'इम्फाल', nameEn: 'Imphal', lat: 24.8170, lng: 93.9368, state: 'Manipur' },
  { name: 'ईटानगर', nameEn: 'Itanagar', lat: 27.0844, lng: 93.6053, state: 'Arunachal Pradesh' },
  { name: 'शिलांग', nameEn: 'Shillong', lat: 25.5788, lng: 91.8933, state: 'Meghalaya' },
  { name: 'आइजोल', nameEn: 'Aizawl', lat: 23.7271, lng: 92.7176, state: 'Mizoram' },
  { name: 'कोहिमा', nameEn: 'Kohima', lat: 25.6751, lng: 94.1086, state: 'Nagaland' },
  { name: 'गंगटोक', nameEn: 'Gangtok', lat: 27.3389, lng: 88.6065, state: 'Sikkim' },
  { name: 'अगरतला', nameEn: 'Agartala', lat: 23.8315, lng: 91.2868, state: 'Tripura' },
  { name: 'दीमापुर', nameEn: 'Dimapur', lat: 25.9084, lng: 93.7265, state: 'Nagaland' },
];

// Union Territories
export const UNION_TERRITORY_CITIES = [
  { name: 'पोर्ट ब्लेयर', nameEn: 'Port Blair', lat: 11.6234, lng: 92.7265, state: 'Andaman & Nicobar' },
  { name: 'पुदुच्चेरी', nameEn: 'Puducherry', lat: 11.9416, lng: 79.8083, state: 'Puducherry' },
  { name: 'दमन', nameEn: 'Daman', lat: 20.3974, lng: 72.8328, state: 'Daman & Diu' },
  { name: 'दीव', nameEn: 'Diu', lat: 20.7197, lng: 70.9904, state: 'Daman & Diu' },
  { name: 'सिल्वासा', nameEn: 'Silvassa', lat: 20.2766, lng: 73.0169, state: 'Dadra & Nagar Haveli' },
  { name: 'कवरत्ती', nameEn: 'Kavaratti', lat: 10.5593, lng: 72.6358, state: 'Lakshadweep' },
];

// =============================================
// WORLD CITIES
// =============================================

// Middle East
export const MIDDLE_EAST_CITIES = [
  { name: 'Dubai', nameEn: 'Dubai', lat: 25.2048, lng: 55.2708, country: 'UAE' },
  { name: 'Abu Dhabi', nameEn: 'Abu Dhabi', lat: 24.4539, lng: 54.3773, country: 'UAE' },
  { name: 'Sharjah', nameEn: 'Sharjah', lat: 25.3463, lng: 55.4209, country: 'UAE' },
  { name: 'Riyadh', nameEn: 'Riyadh', lat: 24.7136, lng: 46.6753, country: 'Saudi Arabia' },
  { name: 'Jeddah', nameEn: 'Jeddah', lat: 21.4858, lng: 39.1925, country: 'Saudi Arabia' },
  { name: 'Mecca', nameEn: 'Mecca', lat: 21.4225, lng: 39.8262, country: 'Saudi Arabia' },
  { name: 'Medina', nameEn: 'Medina', lat: 24.5247, lng: 39.5692, country: 'Saudi Arabia' },
  { name: 'Dammam', nameEn: 'Dammam', lat: 26.4207, lng: 50.0888, country: 'Saudi Arabia' },
  { name: 'Kuwait City', nameEn: 'Kuwait City', lat: 29.3759, lng: 47.9774, country: 'Kuwait' },
  { name: 'Doha', nameEn: 'Doha', lat: 25.2854, lng: 51.5310, country: 'Qatar' },
  { name: 'Manama', nameEn: 'Manama', lat: 26.2285, lng: 50.5860, country: 'Bahrain' },
  { name: 'Muscat', nameEn: 'Muscat', lat: 23.5880, lng: 58.3829, country: 'Oman' },
  { name: 'Tehran', nameEn: 'Tehran', lat: 35.6892, lng: 51.3890, country: 'Iran' },
  { name: 'Baghdad', nameEn: 'Baghdad', lat: 33.3152, lng: 44.3661, country: 'Iraq' },
  { name: 'Amman', nameEn: 'Amman', lat: 31.9454, lng: 35.9284, country: 'Jordan' },
  { name: 'Beirut', nameEn: 'Beirut', lat: 33.8938, lng: 35.5018, country: 'Lebanon' },
  { name: 'Damascus', nameEn: 'Damascus', lat: 33.5138, lng: 36.2765, country: 'Syria' },
  { name: 'Jerusalem', nameEn: 'Jerusalem', lat: 31.7683, lng: 35.2137, country: 'Israel' },
  { name: 'Tel Aviv', nameEn: 'Tel Aviv', lat: 32.0853, lng: 34.7818, country: 'Israel' },
];

// South Asia
export const SOUTH_ASIA_CITIES = [
  { name: 'Colombo', nameEn: 'Colombo', lat: 6.9271, lng: 79.8612, country: 'Sri Lanka' },
  { name: 'Kandy', nameEn: 'Kandy', lat: 7.2906, lng: 80.6337, country: 'Sri Lanka' },
  { name: 'Jaffna', nameEn: 'Jaffna', lat: 9.6615, lng: 80.0255, country: 'Sri Lanka' },
  { name: 'Galle', nameEn: 'Galle', lat: 6.0535, lng: 80.2210, country: 'Sri Lanka' },
  { name: 'Kathmandu', nameEn: 'Kathmandu', lat: 27.7172, lng: 85.3240, country: 'Nepal' },
  { name: 'Pokhara', nameEn: 'Pokhara', lat: 28.2096, lng: 83.9856, country: 'Nepal' },
  { name: 'Dhaka', nameEn: 'Dhaka', lat: 23.8103, lng: 90.4125, country: 'Bangladesh' },
  { name: 'Chittagong', nameEn: 'Chittagong', lat: 22.3569, lng: 91.7832, country: 'Bangladesh' },
  { name: 'Karachi', nameEn: 'Karachi', lat: 24.8607, lng: 67.0011, country: 'Pakistan' },
  { name: 'Lahore', nameEn: 'Lahore', lat: 31.5497, lng: 74.3436, country: 'Pakistan' },
  { name: 'Islamabad', nameEn: 'Islamabad', lat: 33.6844, lng: 73.0479, country: 'Pakistan' },
  { name: 'Thimphu', nameEn: 'Thimphu', lat: 27.4728, lng: 89.6390, country: 'Bhutan' },
  { name: 'Male', nameEn: 'Male', lat: 4.1755, lng: 73.5093, country: 'Maldives' },
];

// Southeast Asia
export const SOUTHEAST_ASIA_CITIES = [
  { name: 'Singapore', nameEn: 'Singapore', lat: 1.3521, lng: 103.8198, country: 'Singapore' },
  { name: 'Kuala Lumpur', nameEn: 'Kuala Lumpur', lat: 3.1390, lng: 101.6869, country: 'Malaysia' },
  { name: 'Penang', nameEn: 'Penang', lat: 5.4141, lng: 100.3288, country: 'Malaysia' },
  { name: 'Bangkok', nameEn: 'Bangkok', lat: 13.7563, lng: 100.5018, country: 'Thailand' },
  { name: 'Phuket', nameEn: 'Phuket', lat: 7.8804, lng: 98.3923, country: 'Thailand' },
  { name: 'Chiang Mai', nameEn: 'Chiang Mai', lat: 18.7883, lng: 98.9853, country: 'Thailand' },
  { name: 'Jakarta', nameEn: 'Jakarta', lat: -6.2088, lng: 106.8456, country: 'Indonesia' },
  { name: 'Bali', nameEn: 'Bali', lat: -8.3405, lng: 115.0920, country: 'Indonesia' },
  { name: 'Manila', nameEn: 'Manila', lat: 14.5995, lng: 120.9842, country: 'Philippines' },
  { name: 'Cebu', nameEn: 'Cebu', lat: 10.3157, lng: 123.8854, country: 'Philippines' },
  { name: 'Ho Chi Minh City', nameEn: 'Ho Chi Minh City', lat: 10.8231, lng: 106.6297, country: 'Vietnam' },
  { name: 'Hanoi', nameEn: 'Hanoi', lat: 21.0285, lng: 105.8542, country: 'Vietnam' },
  { name: 'Yangon', nameEn: 'Yangon', lat: 16.8661, lng: 96.1951, country: 'Myanmar' },
  { name: 'Phnom Penh', nameEn: 'Phnom Penh', lat: 11.5564, lng: 104.9282, country: 'Cambodia' },
];

// East Asia
export const EAST_ASIA_CITIES = [
  { name: 'Tokyo', nameEn: 'Tokyo', lat: 35.6762, lng: 139.6503, country: 'Japan' },
  { name: 'Osaka', nameEn: 'Osaka', lat: 34.6937, lng: 135.5023, country: 'Japan' },
  { name: 'Kyoto', nameEn: 'Kyoto', lat: 35.0116, lng: 135.7681, country: 'Japan' },
  { name: 'Seoul', nameEn: 'Seoul', lat: 37.5665, lng: 126.9780, country: 'South Korea' },
  { name: 'Busan', nameEn: 'Busan', lat: 35.1796, lng: 129.0756, country: 'South Korea' },
  { name: 'Beijing', nameEn: 'Beijing', lat: 39.9042, lng: 116.4074, country: 'China' },
  { name: 'Shanghai', nameEn: 'Shanghai', lat: 31.2304, lng: 121.4737, country: 'China' },
  { name: 'Guangzhou', nameEn: 'Guangzhou', lat: 23.1291, lng: 113.2644, country: 'China' },
  { name: 'Shenzhen', nameEn: 'Shenzhen', lat: 22.5431, lng: 114.0579, country: 'China' },
  { name: 'Hong Kong', nameEn: 'Hong Kong', lat: 22.3193, lng: 114.1694, country: 'Hong Kong' },
  { name: 'Macau', nameEn: 'Macau', lat: 22.1987, lng: 113.5439, country: 'Macau' },
  { name: 'Taipei', nameEn: 'Taipei', lat: 25.0330, lng: 121.5654, country: 'Taiwan' },
];

// Europe
export const EUROPE_CITIES = [
  { name: 'London', nameEn: 'London', lat: 51.5074, lng: -0.1278, country: 'UK' },
  { name: 'Manchester', nameEn: 'Manchester', lat: 53.4808, lng: -2.2426, country: 'UK' },
  { name: 'Birmingham', nameEn: 'Birmingham', lat: 52.4862, lng: -1.8904, country: 'UK' },
  { name: 'Edinburgh', nameEn: 'Edinburgh', lat: 55.9533, lng: -3.1883, country: 'UK' },
  { name: 'Paris', nameEn: 'Paris', lat: 48.8566, lng: 2.3522, country: 'France' },
  { name: 'Berlin', nameEn: 'Berlin', lat: 52.5200, lng: 13.4050, country: 'Germany' },
  { name: 'Munich', nameEn: 'Munich', lat: 48.1351, lng: 11.5820, country: 'Germany' },
  { name: 'Frankfurt', nameEn: 'Frankfurt', lat: 50.1109, lng: 8.6821, country: 'Germany' },
  { name: 'Amsterdam', nameEn: 'Amsterdam', lat: 52.3676, lng: 4.9041, country: 'Netherlands' },
  { name: 'Brussels', nameEn: 'Brussels', lat: 50.8503, lng: 4.3517, country: 'Belgium' },
  { name: 'Rome', nameEn: 'Rome', lat: 41.9028, lng: 12.4964, country: 'Italy' },
  { name: 'Milan', nameEn: 'Milan', lat: 45.4642, lng: 9.1900, country: 'Italy' },
  { name: 'Madrid', nameEn: 'Madrid', lat: 40.4168, lng: -3.7038, country: 'Spain' },
  { name: 'Barcelona', nameEn: 'Barcelona', lat: 41.3851, lng: 2.1734, country: 'Spain' },
  { name: 'Vienna', nameEn: 'Vienna', lat: 48.2082, lng: 16.3738, country: 'Austria' },
  { name: 'Zurich', nameEn: 'Zurich', lat: 47.3769, lng: 8.5417, country: 'Switzerland' },
  { name: 'Geneva', nameEn: 'Geneva', lat: 46.2044, lng: 6.1432, country: 'Switzerland' },
  { name: 'Stockholm', nameEn: 'Stockholm', lat: 59.3293, lng: 18.0686, country: 'Sweden' },
  { name: 'Copenhagen', nameEn: 'Copenhagen', lat: 55.6761, lng: 12.5683, country: 'Denmark' },
  { name: 'Oslo', nameEn: 'Oslo', lat: 59.9139, lng: 10.7522, country: 'Norway' },
  { name: 'Helsinki', nameEn: 'Helsinki', lat: 60.1699, lng: 24.9384, country: 'Finland' },
  { name: 'Dublin', nameEn: 'Dublin', lat: 53.3498, lng: -6.2603, country: 'Ireland' },
  { name: 'Lisbon', nameEn: 'Lisbon', lat: 38.7223, lng: -9.1393, country: 'Portugal' },
  { name: 'Athens', nameEn: 'Athens', lat: 37.9838, lng: 23.7275, country: 'Greece' },
  { name: 'Prague', nameEn: 'Prague', lat: 50.0755, lng: 14.4378, country: 'Czech Republic' },
  { name: 'Warsaw', nameEn: 'Warsaw', lat: 52.2297, lng: 21.0122, country: 'Poland' },
  { name: 'Budapest', nameEn: 'Budapest', lat: 47.4979, lng: 19.0402, country: 'Hungary' },
  { name: 'Moscow', nameEn: 'Moscow', lat: 55.7558, lng: 37.6173, country: 'Russia' },
  { name: 'Istanbul', nameEn: 'Istanbul', lat: 41.0082, lng: 28.9784, country: 'Turkey' },
  { name: 'Ankara', nameEn: 'Ankara', lat: 39.9334, lng: 32.8597, country: 'Turkey' },
];

// Americas
export const AMERICAS_CITIES = [
  { name: 'New York', nameEn: 'New York', lat: 40.7128, lng: -74.0060, country: 'USA' },
  { name: 'Los Angeles', nameEn: 'Los Angeles', lat: 34.0522, lng: -118.2437, country: 'USA' },
  { name: 'Chicago', nameEn: 'Chicago', lat: 41.8781, lng: -87.6298, country: 'USA' },
  { name: 'Houston', nameEn: 'Houston', lat: 29.7604, lng: -95.3698, country: 'USA' },
  { name: 'San Francisco', nameEn: 'San Francisco', lat: 37.7749, lng: -122.4194, country: 'USA' },
  { name: 'Seattle', nameEn: 'Seattle', lat: 47.6062, lng: -122.3321, country: 'USA' },
  { name: 'Boston', nameEn: 'Boston', lat: 42.3601, lng: -71.0589, country: 'USA' },
  { name: 'Dallas', nameEn: 'Dallas', lat: 32.7767, lng: -96.7970, country: 'USA' },
  { name: 'Atlanta', nameEn: 'Atlanta', lat: 33.7490, lng: -84.3880, country: 'USA' },
  { name: 'Miami', nameEn: 'Miami', lat: 25.7617, lng: -80.1918, country: 'USA' },
  { name: 'Washington DC', nameEn: 'Washington DC', lat: 38.9072, lng: -77.0369, country: 'USA' },
  { name: 'Denver', nameEn: 'Denver', lat: 39.7392, lng: -104.9903, country: 'USA' },
  { name: 'Phoenix', nameEn: 'Phoenix', lat: 33.4484, lng: -112.0740, country: 'USA' },
  { name: 'San Diego', nameEn: 'San Diego', lat: 32.7157, lng: -117.1611, country: 'USA' },
  { name: 'Toronto', nameEn: 'Toronto', lat: 43.6532, lng: -79.3832, country: 'Canada' },
  { name: 'Vancouver', nameEn: 'Vancouver', lat: 49.2827, lng: -123.1207, country: 'Canada' },
  { name: 'Montreal', nameEn: 'Montreal', lat: 45.5017, lng: -73.5673, country: 'Canada' },
  { name: 'Calgary', nameEn: 'Calgary', lat: 51.0447, lng: -114.0719, country: 'Canada' },
  { name: 'Mexico City', nameEn: 'Mexico City', lat: 19.4326, lng: -99.1332, country: 'Mexico' },
  { name: 'Sao Paulo', nameEn: 'Sao Paulo', lat: -23.5505, lng: -46.6333, country: 'Brazil' },
  { name: 'Rio de Janeiro', nameEn: 'Rio de Janeiro', lat: -22.9068, lng: -43.1729, country: 'Brazil' },
  { name: 'Buenos Aires', nameEn: 'Buenos Aires', lat: -34.6037, lng: -58.3816, country: 'Argentina' },
  { name: 'Lima', nameEn: 'Lima', lat: -12.0464, lng: -77.0428, country: 'Peru' },
  { name: 'Santiago', nameEn: 'Santiago', lat: -33.4489, lng: -70.6693, country: 'Chile' },
  { name: 'Bogota', nameEn: 'Bogota', lat: 4.7110, lng: -74.0721, country: 'Colombia' },
];

// Africa
export const AFRICA_CITIES = [
  { name: 'Cairo', nameEn: 'Cairo', lat: 30.0444, lng: 31.2357, country: 'Egypt' },
  { name: 'Alexandria', nameEn: 'Alexandria', lat: 31.2001, lng: 29.9187, country: 'Egypt' },
  { name: 'Johannesburg', nameEn: 'Johannesburg', lat: -26.2041, lng: 28.0473, country: 'South Africa' },
  { name: 'Cape Town', nameEn: 'Cape Town', lat: -33.9249, lng: 18.4241, country: 'South Africa' },
  { name: 'Durban', nameEn: 'Durban', lat: -29.8587, lng: 31.0218, country: 'South Africa' },
  { name: 'Lagos', nameEn: 'Lagos', lat: 6.5244, lng: 3.3792, country: 'Nigeria' },
  { name: 'Nairobi', nameEn: 'Nairobi', lat: -1.2921, lng: 36.8219, country: 'Kenya' },
  { name: 'Dar es Salaam', nameEn: 'Dar es Salaam', lat: -6.7924, lng: 39.2083, country: 'Tanzania' },
  { name: 'Accra', nameEn: 'Accra', lat: 5.6037, lng: -0.1870, country: 'Ghana' },
  { name: 'Addis Ababa', nameEn: 'Addis Ababa', lat: 9.0320, lng: 38.7469, country: 'Ethiopia' },
  { name: 'Casablanca', nameEn: 'Casablanca', lat: 33.5731, lng: -7.5898, country: 'Morocco' },
  { name: 'Tunis', nameEn: 'Tunis', lat: 36.8065, lng: 10.1815, country: 'Tunisia' },
  { name: 'Mauritius', nameEn: 'Port Louis', lat: -20.1609, lng: 57.5012, country: 'Mauritius' },
];

// Oceania
export const OCEANIA_CITIES = [
  { name: 'Sydney', nameEn: 'Sydney', lat: -33.8688, lng: 151.2093, country: 'Australia' },
  { name: 'Melbourne', nameEn: 'Melbourne', lat: -37.8136, lng: 144.9631, country: 'Australia' },
  { name: 'Brisbane', nameEn: 'Brisbane', lat: -27.4698, lng: 153.0251, country: 'Australia' },
  { name: 'Perth', nameEn: 'Perth', lat: -31.9505, lng: 115.8605, country: 'Australia' },
  { name: 'Adelaide', nameEn: 'Adelaide', lat: -34.9285, lng: 138.6007, country: 'Australia' },
  { name: 'Auckland', nameEn: 'Auckland', lat: -36.8485, lng: 174.7633, country: 'New Zealand' },
  { name: 'Wellington', nameEn: 'Wellington', lat: -41.2866, lng: 174.7756, country: 'New Zealand' },
  { name: 'Christchurch', nameEn: 'Christchurch', lat: -43.5321, lng: 172.6362, country: 'New Zealand' },
  { name: 'Fiji', nameEn: 'Suva', lat: -18.1416, lng: 178.4419, country: 'Fiji' },
];

// =============================================
// COMBINED EXPORTS
// =============================================

// All Indian cities combined
export const ALL_INDIA_CITIES = [
  ...TAMIL_NADU_CITIES,
  ...KERALA_CITIES,
  ...KARNATAKA_CITIES,
  ...ANDHRA_PRADESH_CITIES,
  ...TELANGANA_CITIES,
  ...MAHARASHTRA_CITIES,
  ...GUJARAT_CITIES,
  ...RAJASTHAN_CITIES,
  ...DELHI_NCR_CITIES,
  ...UTTAR_PRADESH_CITIES,
  ...MADHYA_PRADESH_CITIES,
  ...BIHAR_CITIES,
  ...WEST_BENGAL_CITIES,
  ...ODISHA_CITIES,
  ...PUNJAB_CITIES,
  ...HARYANA_CITIES,
  ...JHARKHAND_CITIES,
  ...CHHATTISGARH_CITIES,
  ...ASSAM_CITIES,
  ...HIMACHAL_PRADESH_CITIES,
  ...UTTARAKHAND_CITIES,
  ...JAMMU_KASHMIR_CITIES,
  ...GOA_CITIES,
  ...NORTHEAST_CITIES,
  ...UNION_TERRITORY_CITIES,
];

// All world cities combined
export const ALL_WORLD_CITIES = [
  ...MIDDLE_EAST_CITIES,
  ...SOUTH_ASIA_CITIES,
  ...SOUTHEAST_ASIA_CITIES,
  ...EAST_ASIA_CITIES,
  ...EUROPE_CITIES,
  ...AMERICAS_CITIES,
  ...AFRICA_CITIES,
  ...OCEANIA_CITIES,
];

// All cities combined (India + World)
export const ALL_CITIES = [
  ...ALL_INDIA_CITIES,
  ...ALL_WORLD_CITIES,
];

// Popular cities (subset for quick selection)
export const POPULAR_CITIES = [
  // Tamil Nadu Top
  { name: 'சென்னை', nameEn: 'Chennai', lat: 13.0827, lng: 80.2707, state: 'Tamil Nadu' },
  { name: 'மதுரை', nameEn: 'Madurai', lat: 9.9252, lng: 78.1198, state: 'Tamil Nadu' },
  { name: 'கோயம்புத்தூர்', nameEn: 'Coimbatore', lat: 11.0168, lng: 76.9558, state: 'Tamil Nadu' },
  { name: 'திருச்சி', nameEn: 'Tiruchirappalli', lat: 10.7905, lng: 78.7047, state: 'Tamil Nadu' },
  // Major Indian Cities
  { name: 'ಬೆಂಗಳೂರು', nameEn: 'Bangalore', lat: 12.9716, lng: 77.5946, state: 'Karnataka' },
  { name: 'హైదరాబాద్', nameEn: 'Hyderabad', lat: 17.3850, lng: 78.4867, state: 'Telangana' },
  { name: 'मुंबई', nameEn: 'Mumbai', lat: 19.0760, lng: 72.8777, state: 'Maharashtra' },
  { name: 'नई दिल्ली', nameEn: 'New Delhi', lat: 28.6139, lng: 77.2090, state: 'Delhi' },
  { name: 'কলকাতা', nameEn: 'Kolkata', lat: 22.5726, lng: 88.3639, state: 'West Bengal' },
  { name: 'પુણે', nameEn: 'Pune', lat: 18.5204, lng: 73.8567, state: 'Maharashtra' },
  // International
  { name: 'Dubai', nameEn: 'Dubai', lat: 25.2048, lng: 55.2708, country: 'UAE' },
  { name: 'Singapore', nameEn: 'Singapore', lat: 1.3521, lng: 103.8198, country: 'Singapore' },
  { name: 'London', nameEn: 'London', lat: 51.5074, lng: -0.1278, country: 'UK' },
  { name: 'New York', nameEn: 'New York', lat: 40.7128, lng: -74.0060, country: 'USA' },
  { name: 'Sydney', nameEn: 'Sydney', lat: -33.8688, lng: 151.2093, country: 'Australia' },
];

// Search function to find cities
export const searchCities = (query, limit = 50) => {
  if (!query || query.trim().length === 0) {
    return POPULAR_CITIES;
  }

  const searchTerm = query.toLowerCase().trim();

  const results = ALL_CITIES.filter(city => {
    const matchesEnglish = city.nameEn.toLowerCase().includes(searchTerm);
    const matchesLocal = city.name.toLowerCase().includes(searchTerm);
    const matchesState = city.state?.toLowerCase().includes(searchTerm) || false;
    const matchesCountry = city.country?.toLowerCase().includes(searchTerm) || false;
    return matchesEnglish || matchesLocal || matchesState || matchesCountry;
  });

  // Sort by relevance (exact match first, then starts with, then contains)
  results.sort((a, b) => {
    const aExact = a.nameEn.toLowerCase() === searchTerm || a.name.toLowerCase() === searchTerm;
    const bExact = b.nameEn.toLowerCase() === searchTerm || b.name.toLowerCase() === searchTerm;
    if (aExact && !bExact) return -1;
    if (!aExact && bExact) return 1;

    const aStarts = a.nameEn.toLowerCase().startsWith(searchTerm);
    const bStarts = b.nameEn.toLowerCase().startsWith(searchTerm);
    if (aStarts && !bStarts) return -1;
    if (!aStarts && bStarts) return 1;

    return a.nameEn.localeCompare(b.nameEn);
  });

  return results.slice(0, limit);
};

// Get location label (city, state/country)
export const getLocationLabel = (city) => {
  if (city.state) {
    return `${city.nameEn}, ${city.state}`;
  } else if (city.country) {
    return `${city.nameEn}, ${city.country}`;
  }
  return city.nameEn;
};

export default {
  ALL_CITIES,
  ALL_INDIA_CITIES,
  ALL_WORLD_CITIES,
  POPULAR_CITIES,
  TAMIL_NADU_CITIES,
  searchCities,
  getLocationLabel,
};
