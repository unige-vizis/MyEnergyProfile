// ISO 3166-1 numeric to alpha-2 country code mapping
// TopoJSON uses numeric codes, our energy data uses alpha-2 codes
export const numericToAlpha2 = {
  // Europe
  '008': 'AL', // Albania
  '020': 'AD', // Andorra
  '040': 'AT', // Austria
  '056': 'BE', // Belgium
  '070': 'BA', // Bosnia and Herzegovina
  '100': 'BG', // Bulgaria
  '112': 'BY', // Belarus
  '191': 'HR', // Croatia
  '196': 'CY', // Cyprus
  '203': 'CZ', // Czechia
  '208': 'DK', // Denmark
  '233': 'EE', // Estonia
  '246': 'FI', // Finland
  '250': 'FR', // France
  '276': 'DE', // Germany
  '300': 'GR', // Greece
  '348': 'HU', // Hungary
  '352': 'IS', // Iceland
  '372': 'IE', // Ireland
  '380': 'IT', // Italy
  '428': 'LV', // Latvia
  '438': 'LI', // Liechtenstein
  '440': 'LT', // Lithuania
  '442': 'LU', // Luxembourg
  '807': 'MK', // North Macedonia
  '470': 'MT', // Malta
  '498': 'MD', // Moldova
  '492': 'MC', // Monaco
  '499': 'ME', // Montenegro
  '528': 'NL', // Netherlands
  '578': 'NO', // Norway
  '616': 'PL', // Poland
  '620': 'PT', // Portugal
  '642': 'RO', // Romania
  '643': 'RU', // Russia
  '674': 'SM', // San Marino
  '688': 'RS', // Serbia
  '703': 'SK', // Slovakia
  '705': 'SI', // Slovenia
  '724': 'ES', // Spain
  '752': 'SE', // Sweden
  '756': 'CH', // Switzerland
  '804': 'UA', // Ukraine
  '826': 'GB', // United Kingdom
  '336': 'VA', // Vatican City

  // Non-European key trading partners
  '012': 'DZ', // Algeria
  '024': 'AO', // Angola
  '031': 'AZ', // Azerbaijan
  '032': 'AR', // Argentina
  '036': 'AU', // Australia
  '048': 'BH', // Bahrain
  '076': 'BR', // Brazil
  '096': 'BN', // Brunei
  '124': 'CA', // Canada
  '156': 'CN', // China
  '170': 'CO', // Colombia
  '178': 'CG', // Congo
  '180': 'CD', // Democratic Republic of Congo
  '218': 'EC', // Ecuador
  '818': 'EG', // Egypt
  '226': 'GQ', // Equatorial Guinea
  '266': 'GA', // Gabon
  '268': 'GE', // Georgia
  '288': 'GH', // Ghana
  '356': 'IN', // India
  '360': 'ID', // Indonesia
  '364': 'IR', // Iran
  '368': 'IQ', // Iraq
  '376': 'IL', // Israel
  '392': 'JP', // Japan
  '398': 'KZ', // Kazakhstan
  '400': 'JO', // Jordan
  '414': 'KW', // Kuwait
  '422': 'LB', // Lebanon
  '434': 'LY', // Libya
  '458': 'MY', // Malaysia
  '484': 'MX', // Mexico
  '504': 'MA', // Morocco
  '508': 'MZ', // Mozambique
  '516': 'NA', // Namibia
  '566': 'NG', // Nigeria
  '512': 'OM', // Oman
  '586': 'PK', // Pakistan
  '608': 'PH', // Philippines
  '634': 'QA', // Qatar
  '682': 'SA', // Saudi Arabia
  '702': 'SG', // Singapore
  '710': 'ZA', // South Africa
  '410': 'KR', // South Korea
  '729': 'SD', // Sudan
  '728': 'SS', // South Sudan
  '760': 'SY', // Syria
  '764': 'TH', // Thailand
  '780': 'TT', // Trinidad and Tobago
  '788': 'TN', // Tunisia
  '792': 'TR', // Turkey
  '795': 'TM', // Turkmenistan
  '784': 'AE', // United Arab Emirates
  '840': 'US', // United States
  '860': 'UZ', // Uzbekistan
  '862': 'VE', // Venezuela
  '704': 'VN', // Vietnam
  '887': 'YE', // Yemen

  // Additional countries that might appear in trade data
  '004': 'AF', // Afghanistan
  '050': 'BD', // Bangladesh
  '064': 'BT', // Bhutan
  '068': 'BO', // Bolivia
  '072': 'BW', // Botswana
  '084': 'BZ', // Belize
  '090': 'SB', // Solomon Islands
  '104': 'MM', // Myanmar
  '108': 'BI', // Burundi
  '116': 'KH', // Cambodia
  '120': 'CM', // Cameroon
  '132': 'CV', // Cape Verde
  '140': 'CF', // Central African Republic
  '144': 'LK', // Sri Lanka
  '148': 'TD', // Chad
  '152': 'CL', // Chile
  '158': 'TW', // Taiwan
  '174': 'KM', // Comoros
  '188': 'CR', // Costa Rica
  '192': 'CU', // Cuba
  '204': 'BJ', // Benin
  '214': 'DO', // Dominican Republic
  '222': 'SV', // El Salvador
  '231': 'ET', // Ethiopia
  '232': 'ER', // Eritrea
  '242': 'FJ', // Fiji
  '262': 'DJ', // Djibouti
  '270': 'GM', // Gambia
  '275': 'PS', // Palestine
  '292': 'GI', // Gibraltar
  '296': 'KI', // Kiribati
  '308': 'GD', // Grenada
  '320': 'GT', // Guatemala
  '324': 'GN', // Guinea
  '328': 'GY', // Guyana
  '332': 'HT', // Haiti
  '340': 'HN', // Honduras
  '344': 'HK', // Hong Kong
  '384': 'CI', // Ivory Coast
  '388': 'JM', // Jamaica
  '404': 'KE', // Kenya
  '408': 'KP', // North Korea
  '417': 'KG', // Kyrgyzstan
  '418': 'LA', // Laos
  '426': 'LS', // Lesotho
  '430': 'LR', // Liberia
  '446': 'MO', // Macao
  '450': 'MG', // Madagascar
  '454': 'MW', // Malawi
  '462': 'MV', // Maldives
  '466': 'ML', // Mali
  '478': 'MR', // Mauritania
  '480': 'MU', // Mauritius
  '496': 'MN', // Mongolia
  '524': 'NP', // Nepal
  '540': 'NC', // New Caledonia
  '548': 'VU', // Vanuatu
  '554': 'NZ', // New Zealand
  '558': 'NI', // Nicaragua
  '562': 'NE', // Niger
  '591': 'PA', // Panama
  '598': 'PG', // Papua New Guinea
  '600': 'PY', // Paraguay
  '604': 'PE', // Peru
  '638': 'RE', // Reunion
  '646': 'RW', // Rwanda
  '662': 'LC', // Saint Lucia
  '678': 'ST', // Sao Tome and Principe
  '686': 'SN', // Senegal
  '694': 'SL', // Sierra Leone
  '706': 'SO', // Somalia
  '716': 'ZW', // Zimbabwe
  '732': 'EH', // Western Sahara
  '740': 'SR', // Suriname
  '748': 'SZ', // Eswatini
  '762': 'TJ', // Tajikistan
  '834': 'TZ', // Tanzania
  '768': 'TG', // Togo
  '776': 'TO', // Tonga
  '800': 'UG', // Uganda
  '854': 'BF', // Burkina Faso
  '858': 'UY', // Uruguay
  '882': 'WS', // Samoa
  '894': 'ZM', // Zambia
  '926': 'XK', // Kosovo (not ISO official, but commonly used)
}

// Reverse mapping: alpha-2 to numeric
export const alpha2ToNumeric = Object.fromEntries(
  Object.entries(numericToAlpha2).map(([num, alpha]) => [alpha, num])
)

// Eurostat uses non-standard codes for some countries
export const eurostatToStandard = {
  'EL': 'GR', // Greece
  'UK': 'GB', // United Kingdom
}

// Reverse mapping
export const standardToEurostat = {
  'GR': 'EL',
  'GB': 'UK',
}

// Regional aggregates that cannot be mapped to geographic locations
export const regionalAggregates = new Set([
  'EUR_OTH',
  'AFR_OTH',
  'AME_OTH',
  'ASI_OTH',
  'ASI_NME_OTH',
  'EU27_2020',
  'EA19',
  'EA20',
  'WORLD',
  'TOTAL',
  'OTH',
  'OTHER',
  'UNKNOWN',
])

// Check if a country code is a regional aggregate
export function isRegionalAggregate(code) {
  if (!code) return false
  return regionalAggregates.has(code.toUpperCase())
}

// Normalize a country code from Eurostat format to standard ISO alpha-2
export function normalizeGeo(code) {
  if (!code) return null
  const upper = code.toUpperCase()
  return eurostatToStandard[upper] || upper
}

// Get the numeric code for an alpha-2 code (handles Eurostat special codes)
export function getNumericCode(alpha2Code) {
  if (!alpha2Code) return null
  const normalized = normalizeGeo(alpha2Code)
  return alpha2ToNumeric[normalized] || null
}

// Get the alpha-2 code for a numeric code
export function getAlpha2Code(numericCode) {
  if (!numericCode) return null
  const str = String(numericCode).padStart(3, '0')
  return numericToAlpha2[str] || null
}

// Country name lookup for display
export const countryNames = {
  'AL': 'Albania',
  'AD': 'Andorra',
  'AT': 'Austria',
  'BE': 'Belgium',
  'BA': 'Bosnia and Herzegovina',
  'BG': 'Bulgaria',
  'BY': 'Belarus',
  'HR': 'Croatia',
  'CY': 'Cyprus',
  'CZ': 'Czechia',
  'DK': 'Denmark',
  'EE': 'Estonia',
  'FI': 'Finland',
  'FR': 'France',
  'DE': 'Germany',
  'GR': 'Greece',
  'HU': 'Hungary',
  'IS': 'Iceland',
  'IE': 'Ireland',
  'IT': 'Italy',
  'LV': 'Latvia',
  'LI': 'Liechtenstein',
  'LT': 'Lithuania',
  'LU': 'Luxembourg',
  'MK': 'North Macedonia',
  'MT': 'Malta',
  'MD': 'Moldova',
  'MC': 'Monaco',
  'ME': 'Montenegro',
  'NL': 'Netherlands',
  'NO': 'Norway',
  'PL': 'Poland',
  'PT': 'Portugal',
  'RO': 'Romania',
  'RU': 'Russia',
  'SM': 'San Marino',
  'RS': 'Serbia',
  'SK': 'Slovakia',
  'SI': 'Slovenia',
  'ES': 'Spain',
  'SE': 'Sweden',
  'CH': 'Switzerland',
  'UA': 'Ukraine',
  'GB': 'United Kingdom',
  'VA': 'Vatican City',
  'XK': 'Kosovo',
  // Key trading partners
  'DZ': 'Algeria',
  'AO': 'Angola',
  'AZ': 'Azerbaijan',
  'AR': 'Argentina',
  'AU': 'Australia',
  'BH': 'Bahrain',
  'BR': 'Brazil',
  'BN': 'Brunei',
  'CA': 'Canada',
  'CN': 'China',
  'CO': 'Colombia',
  'CG': 'Congo',
  'CD': 'DR Congo',
  'EC': 'Ecuador',
  'EG': 'Egypt',
  'GQ': 'Equatorial Guinea',
  'GA': 'Gabon',
  'GE': 'Georgia',
  'GH': 'Ghana',
  'IN': 'India',
  'ID': 'Indonesia',
  'IR': 'Iran',
  'IQ': 'Iraq',
  'IL': 'Israel',
  'JP': 'Japan',
  'KZ': 'Kazakhstan',
  'JO': 'Jordan',
  'KW': 'Kuwait',
  'LB': 'Lebanon',
  'LY': 'Libya',
  'MY': 'Malaysia',
  'MX': 'Mexico',
  'MA': 'Morocco',
  'MZ': 'Mozambique',
  'NA': 'Namibia',
  'NG': 'Nigeria',
  'OM': 'Oman',
  'PK': 'Pakistan',
  'PH': 'Philippines',
  'QA': 'Qatar',
  'SA': 'Saudi Arabia',
  'SG': 'Singapore',
  'ZA': 'South Africa',
  'KR': 'South Korea',
  'SD': 'Sudan',
  'SS': 'South Sudan',
  'SY': 'Syria',
  'TH': 'Thailand',
  'TT': 'Trinidad and Tobago',
  'TN': 'Tunisia',
  'TR': 'Turkey',
  'TM': 'Turkmenistan',
  'AE': 'UAE',
  'US': 'United States',
  'UZ': 'Uzbekistan',
  'VE': 'Venezuela',
  'VN': 'Vietnam',
  'YE': 'Yemen',
  // Additional countries
  'AF': 'Afghanistan',
  'BD': 'Bangladesh',
  'BT': 'Bhutan',
  'BO': 'Bolivia',
  'BW': 'Botswana',
  'BZ': 'Belize',
  'SB': 'Solomon Islands',
  'MM': 'Myanmar',
  'BI': 'Burundi',
  'KH': 'Cambodia',
  'CM': 'Cameroon',
  'CV': 'Cape Verde',
  'CF': 'Central African Republic',
  'LK': 'Sri Lanka',
  'TD': 'Chad',
  'CL': 'Chile',
  'TW': 'Taiwan',
  'KM': 'Comoros',
  'CR': 'Costa Rica',
  'CU': 'Cuba',
  'BJ': 'Benin',
  'DO': 'Dominican Republic',
  'SV': 'El Salvador',
  'ET': 'Ethiopia',
  'ER': 'Eritrea',
  'FJ': 'Fiji',
  'DJ': 'Djibouti',
  'GM': 'Gambia',
  'PS': 'Palestine',
  'GI': 'Gibraltar',
  'KI': 'Kiribati',
  'GD': 'Grenada',
  'GT': 'Guatemala',
  'GN': 'Guinea',
  'GY': 'Guyana',
  'HT': 'Haiti',
  'HN': 'Honduras',
  'HK': 'Hong Kong',
  'CI': 'Ivory Coast',
  'JM': 'Jamaica',
  'KE': 'Kenya',
  'KP': 'North Korea',
  'KG': 'Kyrgyzstan',
  'LA': 'Laos',
  'LS': 'Lesotho',
  'LR': 'Liberia',
  'MO': 'Macao',
  'MG': 'Madagascar',
  'MW': 'Malawi',
  'MV': 'Maldives',
  'ML': 'Mali',
  'MR': 'Mauritania',
  'MU': 'Mauritius',
  'MN': 'Mongolia',
  'NP': 'Nepal',
  'NC': 'New Caledonia',
  'VU': 'Vanuatu',
  'NZ': 'New Zealand',
  'NI': 'Nicaragua',
  'NE': 'Niger',
  'PA': 'Panama',
  'PG': 'Papua New Guinea',
  'PY': 'Paraguay',
  'PE': 'Peru',
  'RE': 'Reunion',
  'RW': 'Rwanda',
  'LC': 'Saint Lucia',
  'ST': 'Sao Tome and Principe',
  'SN': 'Senegal',
  'SL': 'Sierra Leone',
  'SO': 'Somalia',
  'ZW': 'Zimbabwe',
  'EH': 'Western Sahara',
  'SR': 'Suriname',
  'SZ': 'Eswatini',
  'TJ': 'Tajikistan',
  'TZ': 'Tanzania',
  'TG': 'Togo',
  'TO': 'Tonga',
  'UG': 'Uganda',
  'BF': 'Burkina Faso',
  'UY': 'Uruguay',
  'WS': 'Samoa',
  'ZM': 'Zambia',
}
