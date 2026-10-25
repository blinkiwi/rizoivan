"""Contenido actual del home como valores por defecto del CMS.

Estos datos son la "base del template": si una tabla esta vacia el front sigue
mostrando exactamente el contenido original de la plantilla. Con `seed_homepage`
se copian a la base de datos para poder editarlos desde el panel.
"""
from django.templatetags.static import static

COMMON_DESC = ('Unleash the power of our platform with a multitude of powerful '
               'features, empowering you to achieve your goals.')
LOREM_ANSWER = ('There are many variations of passages of Lorem Ipsum available, '
                'but the majority have suffered alteration in some form.')
CARD_TEXT = 'This is required when, for example, the final text is not yet available.'

SITE = {
    'site_name': 'Pixind',
    'meta_title': 'Pixind - Django Responsive Landing Page Template',
    'meta_description': 'Responsive Tailwind CSS Template',
    'copyright_text': '2026 Pixind. All rights reserved.',
    'credits_text': 'Design & Develop with',
    'credits_by': 'by',
    'credits_name': '',
    'credits_url': '/',
    'show_theme_switcher': True,
    'show_rtl_switcher': True,
    'default_theme': 'dark',
}

STICKY_NAV = {
    'cta_label': 'Get in Touch',
    'cta_url': '',
}

NAV_ITEMS = [
    {'label': 'Home', 'url': '#home'},
    {'label': 'Features', 'url': '#features'},
    {'label': 'Portfolio', 'url': '#projects'},
    {'label': 'Pricing', 'url': '#pricing'},
    {'label': 'Review', 'url': '#reviews'},
    {'label': 'Blog', 'url': '#blogs'},
    {'label': 'Contact us', 'url': '#contactus'},
]

HERO = {
    'title': 'Analytics That Drive',
    'title_line2': 'Better Decisions',
    'subtitle': COMMON_DESC,
    'button_text': 'Contact Us',
    'button_link': '',
    'video_id': 'S_CGed6E610',
    'video_label': 'Watch Now',
    'image': static('app/images/bg/2.jpg'),
    'card_title': 'We are offering 14 \ndays free trial',
    'card_name_label': 'Your Name :',
    'card_email_label': 'Your Email :',
    'card_phone_label': 'Phone No. :',
    'card_button_text': 'Free Trial',
}

SECTIONS = {
    'about': {
        'eyebrow': 'Empowering businesses',
        'title': 'We Create & Enhance \nDigital Solutions',
        'description': COMMON_DESC,
        'button_label': 'Learn More',
        'button_url': '',
        'background_image': static('app/images/map.png'),
        'image': static('app/images/about.jpg'),
        'extra_image': static('app/images/client/01.jpg'),
        'badge_text': "let's talk about ideas",
        'person_text': 'Calvin Carlo',
        'checklist': 'Reporting & analysis\nInvestment decision\nCompetitive analysis\nMarket research',
        'stat_label': 'Revenue',
        'stat_number': '39548',
        'stat_target': 45485,
        'stat_percent': '3.85%',
        'show_stat': True,
        'show_learn_more': True,
        'show_play': True,
        'show_eyebrow': True,
        'show_title': True,
        'show_description': True,
        'show_checklist': True,
        'show_avatar': True,
        'show_avatar_dup': True,
        'show_main_image': True,
    },
    'features': {
        'eyebrow': 'Features',
        'title': 'Our Innovative Services',
        'description': COMMON_DESC,
    },
    'choose_us': {
        'eyebrow': 'Why choose us ?',
        'title': 'Your Partner for \nCustomized Solutions',
        'description': COMMON_DESC,
    },
    'portfolio': {
        'eyebrow': 'Portfolio',
        'title': 'Our Digital Portfolio',
        'description': COMMON_DESC,
        'button_label': 'See More Portfolio',
        'button_url': '',
    },
    'partners': {
        'title': 'Our Partners',
        'description': COMMON_DESC,
    },
    'cta': {
        'eyebrow': 'C.T.A',
        'title': 'Understand expectations, \nthen delight customers completely',
        'description': COMMON_DESC,
        'button_label': 'Get Started !',
        'button_url': '',
        'background_image': static('app/images/bg/cta.jpg'),
    },
    'pricing': {
        'eyebrow': 'Flexible Pricing',
        'title': 'Select the Perfect \nPlan for Your Needs',
        'description': COMMON_DESC,
    },
    'faqs': {
        'eyebrow': 'FAQs',
        'title': 'Frequently Asked Questions',
        'description': COMMON_DESC,
    },
    'reviews': {
        'eyebrow': 'Testimonial',
        'title': 'What Our Users Are \nSaying About us',
        'description': COMMON_DESC,
    },
    'blogs': {
        'eyebrow': 'Blog',
        'title': 'Latest News',
        'description': COMMON_DESC,
    },
    'contactus': {
        'eyebrow': 'Contact us',
        'title': 'Get In Touch !',
        'description': COMMON_DESC,
        'form_name_label': 'Name :',
        'form_email_label': 'Email :',
        'form_subject_label': 'Subject :',
        'form_message_label': 'Message :',
        'form_button_label': 'Send Message',
    },
    'map': {
        'embed_url': ('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d39206.002432144705!'
                      '!2d-95.4973981212445!3d29.709510002925988!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!'
                      '4f13.1!3m3!1m2!1s0x8640c16de81f3ca5%3A0xf43e0b60ae539ac9!'
                      '2sGerald+D.+Hines+Waterwall+Park!5e0!3m2!1sen!2sin!4v1566305861440!5m2!1sen!2sin'),
    },
}

FEATURES = [
    {'title': 'Web Development', 'description': CARD_TEXT, 'icon': 'ri-code-line', 'url': ''},
    {'title': 'Digital Marketing', 'description': CARD_TEXT, 'icon': 'ri-megaphone-line', 'url': ''},
    {'title': 'Motion Graphics', 'description': CARD_TEXT, 'icon': 'ri-movie-line', 'url': ''},
    {'title': 'UI/UX Design', 'description': CARD_TEXT, 'icon': 'ri-pencil-ruler-line', 'url': ''},
]

SERVICE_TABS = [
    {'label': '01. Web Development', 'title': 'Web Development', 'image': static('app/images/services/1.jpg')},
    {'label': '02. Digital Marketing', 'title': 'Digital Marketing', 'image': static('app/images/services/2.jpg')},
    {'label': '03. Motion Graphics', 'title': 'Motion Graphics', 'image': static('app/images/services/3.jpg')},
    {'label': '04. UI/UX Design', 'title': 'UI/UX Design', 'image': static('app/images/services/4.jpg')},
]
for _tab in SERVICE_TABS:
    _tab.setdefault('text', CARD_TEXT)
    _tab.setdefault('url', '')

PRICING_FEATURES = 'Full Access\nSource Files\nFree Appointments\nEnhanced Security\nFree Installment'
PRICING = [
    {'billing': 1, 'title': 'Basic', 'price': '29', 'period': '/per month', 'highlight': False},
    {'billing': 1, 'title': 'Professional', 'price': '99', 'period': '/per month', 'highlight': True},
    {'billing': 2, 'title': 'Basic', 'price': '19', 'period': '/per month', 'highlight': False},
    {'billing': 2, 'title': 'Professional', 'price': '59', 'period': '/per month', 'highlight': True},
]
for _plan in PRICING:
    _plan.setdefault('features', PRICING_FEATURES)
    _plan.setdefault('button_text', 'Choose Your Plan')
    _plan.setdefault('button_link', '')

FAQS = [
    {'question': 'How does it work ?', 'answer': LOREM_ANSWER},
    {'question': 'Do I need a designer to use Pixind ?', 'answer': LOREM_ANSWER},
    {'question': 'What do I need to do to start selling ?', 'answer': LOREM_ANSWER},
    {'question': 'What happens when I receive an order ?', 'answer': LOREM_ANSWER},
    {'question': 'How does it work ?', 'answer': LOREM_ANSWER},
    {'question': 'Do I need a designer to use Pixind ?', 'answer': LOREM_ANSWER},
    {'question': 'What do I need to do to start selling ?', 'answer': LOREM_ANSWER},
    {'question': 'What happens when I receive an order ?', 'answer': LOREM_ANSWER},
]

REVIEWS = [
    {'name': 'Calvin Carlo', 'role': 'CEO / Anywhere', 'text': LOREM_ANSWER,
     'avatar': static('app/images/client/01.jpg')},
    {'name': 'Sunny Sthal', 'role': 'Manager / Company', 'text': LOREM_ANSWER,
     'avatar': static('app/images/client/02.jpg')},
    {'name': 'Cristina Roma', 'role': 'Freelancer', 'text': LOREM_ANSWER,
     'avatar': static('app/images/client/03.jpg')},
]

COUNTERS = [
    {'icon': 'ri-user-line', 'number': '4548', 'target': 4548, 'symbol': '+', 'title': 'Happy Clients'},
    {'icon': 'ri-survey-line', 'number': '2000', 'target': 2000, 'symbol': '+', 'title': 'Project Done'},
    {'icon': 'ri-global-line', 'number': '15', 'target': 15, 'symbol': '+', 'title': 'Countries'},
    {'icon': 'ri-trophy-line', 'number': '45', 'target': 45, 'symbol': '', 'title': 'Awards'},
]

PARTNERS = [
    {'alt': 'Amazon', 'image': static('app/images/client/Amazon.svg')},
    {'alt': 'Asana', 'image': static('app/images/client/Asana.svg')},
    {'alt': 'BeReal', 'image': static('app/images/client/BeReal.svg')},
    {'alt': 'Behance', 'image': static('app/images/client/Behance.svg')},
    {'alt': 'ClickUp', 'image': static('app/images/client/ClickUp.svg')},
    {'alt': 'Copper', 'image': static('app/images/client/Copper.svg')},
    {'alt': 'Deezer', 'image': static('app/images/client/Deezer.svg')},
    {'alt': 'Evernote', 'image': static('app/images/client/Evernote.svg')},
    {'alt': 'Grammarly', 'image': static('app/images/client/Grammarly.svg')},
    {'alt': 'Google Ads', 'image': static('app/images/client/google-ad.svg')},
]

CONTACTS = [
    {'label': 'Phone', 'value': '+152 534-468-854', 'icon': 'ri-phone-line'},
    {'label': 'Email', 'value': 'contact@example.com', 'icon': 'ri-mail-line'},
    {'label': 'Location', 'value': 'C/54 Northwest Freeway, Suite 558, Houston, USA 485', 'icon': 'ri-map-pin-line'},
]

FOOTER = {
    'description': COMMON_DESC,
}

SOCIALS = [
    {'icon': 'ri-shopping-cart-line', 'url': 'https://1.envato.market/pixind-django'},
    {'icon': 'ri-dribbble-line', 'url': 'https://dribbble.com/shreethemes'},
    {'icon': 'ri-behance-line', 'url': 'https://www.behance.net/shreethemes'},
    {'icon': 'ri-linkedin-line', 'url': 'http://linkedin.com/company/shreethemes'},
    {'icon': 'ri-facebook-circle-line', 'url': 'https://www.facebook.com/shreethemes'},
    {'icon': 'ri-instagram-line', 'url': 'https://www.instagram.com/shreethemes/'},
    {'icon': 'ri-twitter-x-line', 'url': 'https://twitter.com/shreethemes'},
    {'icon': 'ri-mail-line', 'url': 'mailto:support@shreethemes.in'},
]

FOOTER_COLUMNS = [
    {'key': 'company', 'heading': 'Company', 'links': [
        {'label': 'About us', 'url': '/aboutus/'},
        {'label': 'Services', 'url': '/features/'},
        {'label': 'Team', 'url': '/team/'},
        {'label': 'Pricing', 'url': '/pricing/'},
        {'label': 'Portfolio', 'url': '/portfolio/'},
    ]},
    {'key': 'usefull', 'heading': 'Usefull Links', 'links': [
        {'label': 'Terms of Services', 'url': '#'},
        {'label': 'Privacy Policy', 'url': '#'},
        {'label': 'Documentation', 'url': '#'},
    ]},
    {'key': 'bottom', 'heading': '', 'links': [
        {'label': 'Signup', 'url': '#'},
        {'label': 'FAQs', 'url': '#'},
        {'label': 'Contact us', 'url': '#'},
    ]},
]

# Bloques del home en su orden POR DEFECTO (el panel los reordena con drag & drop)
HOME_BLOCKS = [
    ('hero', 'Hero (portada)'),
    ('about', 'About'),
    ('features', 'Features'),
    ('why', '¿Por qué elegirnos? (Why choose us)'),
    ('portfolio', 'Portfolio'),
    ('partners', 'Partners'),
    ('cta', 'C.T.A (banner)'),
    ('pricing', 'Planes de precios'),
    ('faqs', 'Preguntas frecuentes (FAQs)'),
    ('reviews', 'Testimonios + contadores'),
    ('blog', 'Blog'),
    ('contact', 'Contacto'),
    ('map', 'Mapa'),
]
BLOCK_TPL = {key: f'pages/blocks/{key}.html' for key, _ in HOME_BLOCKS}

# Cada bloque del home pinta UNA sección (claves internas distintas en 4 casos)
BLOCK_SECTION = {
    'hero': None,            # el hero usa HeaderBlock, no SectionBlock
    'about': 'about',
    'features': 'features',
    'why': 'choose_us',
    'portfolio': 'portfolio',
    'partners': 'partners',
    'cta': 'cta',
    'pricing': 'pricing',
    'faqs': 'faqs',
    'reviews': 'reviews',
    'blog': 'blogs',
    'contact': 'contactus',
    'map': 'map',
}
