/* LUMEN BOTANICA — catalog & content -------------------------------------- */
window.LB = window.LB || {};

LB.currency = { code: 'EUR', locale: 'en-IE' };

LB.products = [
  { id:'monstera-deliciosa', name:'Monstera Deliciosa', latin:'Monstera deliciosa', price:68, cat:'indoor',
    light:'bright', water:'medium', size:'L', diff:'easy', petSafe:false, rating:4.9, reviews:412, badge:'Bestseller',
    blurb:'The archetype. Fenestrated leaves that widen with every new node.' },
  { id:'monstera-obliqua', name:'Monstera Obliqua', latin:'Monstera obliqua', price:340, was:395, cat:'rare',
    light:'bright', water:'high', size:'M', diff:'expert', petSafe:false, rating:4.8, reviews:38, badge:'1 of 12',
    blurb:'More hole than leaf. Propagated in-house from a single mother plant.' },
  { id:'fiddle-leaf-fig', name:'Fiddle Leaf Fig', latin:'Ficus lyrata', price:96, cat:'indoor',
    light:'bright', water:'medium', size:'XL', diff:'moderate', petSafe:false, rating:4.6, reviews:271,
    blurb:'Architectural, upright, unapologetic. Give it one bright window and never move it.' },
  { id:'rubber-tree', name:"Rubber Tree 'Noir'", latin:'Ficus elastica', price:54, cat:'indoor',
    light:'medium', water:'low', size:'L', diff:'easy', petSafe:false, rating:4.7, reviews:188,
    blurb:'Near-black foliage with a lacquered finish. Thrives on benign neglect.' },
  { id:'calathea-orbifolia', name:'Calathea Orbifolia', latin:'Goeppertia orbifolia', price:62, cat:'indoor',
    light:'medium', water:'high', size:'M', diff:'expert', petSafe:true, rating:4.5, reviews:154,
    blurb:'Silver-banded discs that fold upward at dusk. Loves humidity, hates hard water.' },
  { id:'bird-of-paradise', name:'Bird of Paradise', latin:'Strelitzia nicolai', price:120, cat:'indoor',
    light:'bright', water:'medium', size:'XL', diff:'moderate', petSafe:false, rating:4.8, reviews:96,
    blurb:'Two metres of paddle leaves. The fastest way to make a room feel tropical.' },
  { id:'anthurium-crystal', name:'Anthurium Crystallinum', latin:'Anthurium crystallinum', price:185, cat:'rare',
    light:'medium', water:'high', size:'M', diff:'expert', petSafe:false, rating:4.9, reviews:64, badge:'Collector',
    blurb:'Velvet leaves veined in white. Grown in our high-humidity chamber.' },
  { id:'philodendron-pink', name:'Philodendron Pink Princess', latin:'Philodendron erubescens', price:240, cat:'rare',
    light:'bright', water:'medium', size:'M', diff:'expert', petSafe:false, rating:5.0, reviews:51, badge:'Rare',
    blurb:'Every plant variegates differently. Yours is photographed before it ships.' },
  { id:'alocasia-frydek', name:'Alocasia Frydek', latin:'Alocasia micholitziana', price:88, cat:'rare',
    light:'medium', water:'high', size:'M', diff:'moderate', petSafe:false, rating:4.6, reviews:77,
    blurb:'Arrow-shaped velvet with neon veining. Dramatic, and it knows it.' },
  { id:'echeveria-glow', name:'Echeveria Glow', latin:'Echeveria elegans', price:18, cat:'succulents',
    light:'bright', water:'low', size:'S', diff:'easy', petSafe:true, rating:4.8, reviews:523, badge:'Under €20',
    blurb:'A geometric rosette that blushes coral under strong light.' },
  { id:'haworthia-zebra', name:'Haworthia Zebra', latin:'Haworthiopsis attenuata', price:16, cat:'succulents',
    light:'medium', water:'low', size:'S', diff:'easy', petSafe:true, rating:4.7, reviews:318,
    blurb:'White-banded spears. Survives desks, dorms and forgetful owners.' },
  { id:'jade-prism', name:'Jade Prism', latin:'Crassula ovata', price:24, cat:'succulents',
    light:'bright', water:'low', size:'S', diff:'easy', petSafe:false, rating:4.6, reviews:205,
    blurb:'Thick faceted pads on a woody stem. Will outlive most of your furniture.' },
  { id:'snake-plant', name:"Snake Plant 'Laurentii'", latin:'Dracaena trifasciata', price:42, cat:'indoor',
    light:'low', water:'low', size:'L', diff:'easy', petSafe:false, rating:4.9, reviews:604, badge:'Low light',
    blurb:'Vertical, gold-edged, indestructible. Filters air while you sleep.' },
  { id:'aloe-vera', name:'Aloe Vera', latin:'Aloe barbadensis', price:22, cat:'succulents',
    light:'bright', water:'low', size:'M', diff:'easy', petSafe:false, rating:4.8, reviews:430,
    blurb:'Functional and sculptural. Snap a leaf for burns; the plant shrugs it off.' },
  { id:'dracaena-spike', name:'Dracaena Spike', latin:'Dracaena marginata', price:38, cat:'indoor',
    light:'medium', water:'low', size:'L', diff:'easy', petSafe:false, rating:4.5, reviews:122,
    blurb:'A firework of thin blades on a slender cane. Great for narrow corners.' },
  { id:'boston-fern', name:'Boston Fern', latin:'Nephrolepis exaltata', price:34, cat:'hanging',
    light:'medium', water:'high', size:'M', diff:'moderate', petSafe:true, rating:4.4, reviews:167,
    blurb:'Arching fronds that soften every hard edge in the room.' },
  { id:'maidenhair-fern', name:'Maidenhair Fern', latin:'Adiantum raddianum', price:29, cat:'indoor',
    light:'medium', water:'high', size:'S', diff:'expert', petSafe:true, rating:4.3, reviews:89,
    blurb:'Impossibly fine foliage. Rewards a humidifier; punishes a radiator.' },
  { id:'pothos-neon', name:'Pothos Neon', latin:'Epipremnum aureum', price:26, cat:'hanging',
    light:'low', water:'low', size:'M', diff:'easy', petSafe:false, rating:4.9, reviews:712, badge:'Easiest',
    blurb:'Acid-green hearts that trail a metre a year. The perfect first plant.' },
  { id:'string-of-pearls', name:'String of Pearls', latin:'Curio rowleyanus', price:31, cat:'hanging',
    light:'bright', water:'low', size:'S', diff:'moderate', petSafe:false, rating:4.6, reviews:244,
    blurb:'Beaded strands that fall like a curtain. Water sparingly, hang high.' },
  { id:'bamboo-screen', name:'Bamboo Screen', latin:'Fargesia rufa', price:145, cat:'outdoor',
    light:'bright', water:'medium', size:'XL', diff:'easy', petSafe:true, rating:4.7, reviews:58,
    blurb:'Clumping, non-invasive privacy in a single season. Sold as a five-cane set.' },
  { id:'japanese-maple', name:'Japanese Maple', latin:'Acer palmatum', price:210, was:245, cat:'outdoor',
    light:'medium', water:'medium', size:'XL', diff:'moderate', petSafe:true, rating:4.9, reviews:71, badge:'Sale',
    blurb:'Lace-cut leaves that run crimson in October. Ten-year-old rootstock.' },
  { id:'olive-tree', name:'Olive Tree', latin:'Olea europaea', price:165, cat:'outdoor',
    light:'bright', water:'low', size:'XL', diff:'easy', petSafe:true, rating:4.8, reviews:113,
    blurb:'Silvered leaves and a gnarled trunk. Hardy to −8°C once established.' },
  { id:'columnar-cactus', name:'Columnar Cactus', latin:'Cereus repandus', price:58, cat:'succulents',
    light:'bright', water:'low', size:'L', diff:'easy', petSafe:true, rating:4.7, reviews:95,
    blurb:'A living monolith. Ribbed, spined, and utterly self-sufficient.' },
  { id:'lavender-row', name:'Lavender Row', latin:'Lavandula angustifolia', price:19, cat:'outdoor',
    light:'bright', water:'low', size:'S', diff:'easy', petSafe:true, rating:4.8, reviews:386, badge:'Pollinator',
    blurb:'Six starter plugs. Plant 30cm apart for a hedge by midsummer.' }
];

LB.products.forEach(function (p, i) {
  p.img = 'assets/img/plant-' + p.id + '.svg';
  p.added = LB.products.length - i;          // newest-first ordering key
  p.pop = p.reviews * p.rating;               // popularity key
});

LB.categories = [
  { id:'all',        label:'Everything' },
  { id:'indoor',     label:'Indoor' },
  { id:'outdoor',    label:'Outdoor' },
  { id:'succulents', label:'Succulents' },
  { id:'hanging',    label:'Trailing' },
  { id:'rare',       label:'Rare' }
];

LB.collections = [
  { id:'indoor',     title:'Indoor Architecture', img:'assets/img/collection-indoor.svg',
    blurb:'Statement foliage sized for real rooms — from desk to double-height ceiling.' },
  { id:'rare',       title:'The Rare Room',        img:'assets/img/collection-rare.svg',
    blurb:'Limited propagations from our mother-plant library. Numbered, photographed, released monthly.' },
  { id:'succulents', title:'Arid Systems',         img:'assets/img/collection-succulents.svg',
    blurb:'Low-water geometry for bright windowsills and anyone who travels.' },
  { id:'hanging',    title:'Trailing & Suspended', img:'assets/img/collection-hanging.svg',
    blurb:'Vines, beads and fronds engineered to fall — shelf, rail or ceiling hook.' },
  { id:'outdoor',    title:'Terrace & Garden',     img:'assets/img/collection-outdoor.svg',
    blurb:'Hardy structure for balconies and beds, acclimatised outdoors before it ships.' },
  { id:'statement',  title:'Statement Pieces',     img:'assets/img/collection-statement.svg',
    blurb:'One plant, whole room. Our largest specimens, delivered by two-person crew.' }
];

LB.guides = [
  { id:'light', title:'Reading light like a plant does',
    excerpt:'Lux, direction and duration — a practical method for auditing any room in ten minutes, no meter required.',
    img:'assets/img/guide-light.svg', cat:'Light', read:'6 min', date:'12 Aug 2026' },
  { id:'water', title:'The only watering schedule that works',
    excerpt:'Throw out the calendar. Weight, finger-depth and drainage tell you far more than any weekly reminder.',
    img:'assets/img/guide-water.svg', cat:'Water', read:'5 min', date:'04 Aug 2026' },
  { id:'soil',  title:'Mixing substrate for aroids',
    excerpt:'Bark, pumice, coco coir and worm castings — the ratios we use across 40,000 plants a year.',
    img:'assets/img/guide-soil.svg', cat:'Substrate', read:'8 min', date:'27 Jul 2026' },
  { id:'pests', title:'Spotting thrips before they spread',
    excerpt:'What the first damage actually looks like, and the three-week protocol that clears an infestation.',
    img:'assets/img/guide-pests.svg', cat:'Health', read:'7 min', date:'19 Jul 2026' },
  { id:'light2', title:'Overwintering under grow lights',
    excerpt:'Spectrum, distance and photoperiod for keeping tropicals in active growth through a northern winter.',
    img:'assets/img/guide-light2.svg', cat:'Light', read:'9 min', date:'02 Jul 2026' }
];

LB.quotes = [
  { text:'The Monstera arrived in a crate with a humidity pack and a QR code that opened its actual grow log. Nine months of data. I have never seen a plant shop do that.',
    name:'Nadia Farouk', role:'Interior designer · Amsterdam', initials:'NF' },
  { text:'I have killed every fern I have ever owned. This one came with a light audit I filled in beforehand, and they sent me a different species than the one I picked. It is still alive.',
    name:'Tomás Ribeiro', role:'Repeat customer · Porto', initials:'TR' },
  { text:'We furnished an entire studio floor — 60 plants, two deliveries, zero losses. The replacement guarantee never even came up.',
    name:'Ingrid Halvorsen', role:'Facilities lead, Nordlys Studio', initials:'IH' },
  { text:'The Pink Princess was photographed the morning it shipped so I knew exactly which variegation I was getting. That is the whole game with rare aroids.',
    name:'Yuki Tanaka', role:'Collector · Berlin', initials:'YT' },
  { text:'Ordered on a Tuesday, potted by Thursday, and the packaging went straight into the compost. No polystyrene anywhere.',
    name:'Marcus Adeyemi', role:'Customer · Dublin', initials:'MA' }
];

LB.steps = [
  { n:'01', title:'Propagated, not imported',
    body:'Every plant starts in our own mother-plant library. No pallets of stressed stock flown in from three continents.',
    img:'assets/img/collection-rare.svg' },
  { n:'02', title:'Grown under full spectrum',
    body:'LED arrays tuned per species, 18 hours a day. Sensors log light, humidity and substrate moisture every 90 seconds.',
    img:'assets/img/guide-light.svg' },
  { n:'03', title:'Acclimatised before it ships',
    body:'Six weeks stepped down to household light levels, so the shock of your living room is a step — not a cliff.',
    img:'assets/img/collection-indoor.svg' },
  { n:'04', title:'Delivered rooted and guaranteed',
    body:'Plastic-free crates, a live grow log per plant, and a 90-day replacement promise we have paid out on 1.4% of orders.',
    img:'assets/img/collection-hanging.svg' }
];
