from django.db import models
from django.utils.text import slugify


# ---------------------------------------------------------------- generic ---
class SiteConfig(models.Model):
    """Global site configuration for homepage content management."""
    site_name = models.CharField(max_length=255, default='Pixind', verbose_name='Nombre del sitio')
    meta_title = models.CharField(max_length=255, default='Pixind - Django Responsive Landing Page Template',
                                  verbose_name='Título del navegador (pestaña)')
    meta_description = models.CharField(max_length=255, default='Responsive Tailwind CSS Template',
                                        verbose_name='Meta descripción')
    copyright_text = models.TextField(default='2026 Pixind. All rights reserved.', verbose_name='Copyright')
    credits_text = models.CharField(max_length=255, default='Design & Develop with', blank=True,
                                    verbose_name='Créditos: texto antes del corazón')
    credits_by = models.CharField(max_length=100, default='by', blank=True,
                                  verbose_name='Créditos: texto entre el corazón y el nombre')
    credits_name = models.CharField(max_length=255, default='', blank=True,
                                    verbose_name='Créditos: nombre (enlace) — vacío = nombre del sitio')
    credits_url = models.CharField(max_length=255, default='/', blank=True,
                                   verbose_name='Créditos: enlace')
    show_theme_switcher = models.BooleanField(default=True,
                                              verbose_name='Mostrar botón claro/oscuro en el sitio')
    show_rtl_switcher = models.BooleanField(default=True,
                                            verbose_name='Mostrar botón LTR/RTL en el sitio')
    THEME_CHOICES = [('dark', 'Oscuro (predeterminado)'), ('light', 'Claro'), ('auto', 'Según el sistema')]
    default_theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark',
                                     verbose_name='Tema por defecto del sitio')
    color_primary = models.CharField(max_length=9, default='', blank=True,
                                     verbose_name='Paleta: color primario (#hex, vacio = original)')
    color_text = models.CharField(max_length=9, default='', blank=True,
                                  verbose_name='Paleta: color de texto (#hex, vacio = original)')
    color_hover = models.CharField(max_length=9, default='', blank=True,
                                   verbose_name='Paleta: color al pasar el mouse (#hex, vacio = original)')
    color_bg = models.CharField(max_length=9, default='', blank=True,
                                verbose_name='Paleta: color de fondo (#hex, vacio = original)')
    whatsapp_enabled = models.BooleanField(default=True,
                                           verbose_name='Mostrar boton flotante de WhatsApp')
    whatsapp_phone = models.CharField(max_length=30, default='', blank=True,
                                      verbose_name='WhatsApp: telefono (codigo de pais, sin +)')
    whatsapp_message = models.CharField(max_length=255, default='', blank=True,
                                        verbose_name='WhatsApp: mensaje de inicio')
    logo = models.ImageField(upload_to='site_logos/', blank=True, null=True, verbose_name='Logo')
    favicon = models.ImageField(upload_to='site_favicons/', blank=True, null=True, verbose_name='Favicon')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '01 · Sitio (logo, favicon, copyright)'
        verbose_name_plural = '01 · Sitio (logo, favicon, copyright)'

    def __str__(self):
        return self.site_name


class StickyNav(models.Model):
    """Header sticky (botonera): logo + boton de accion. Singleton."""
    logo = models.ImageField(upload_to='nav_logos/', blank=True, null=True,
                             verbose_name='Logo del header (si esta vacio usa el del Sitio)')
    logo_scroll = models.ImageField(upload_to='nav_logos/', blank=True, null=True,
                                    verbose_name='Logo al hacer scroll (segundo logo, se activa al pegarse el header)')
    cta_label = models.CharField(max_length=100, default='Get in Touch', verbose_name='Texto del boton')
    cta_url = models.CharField(max_length=255, default='', blank=True, verbose_name='Enlace del boton')

    class Meta:
        verbose_name = '02 · Header / botonera sticky'
        verbose_name_plural = '02 · Header / botonera sticky'

    def __str__(self):
        return self.cta_label or 'Header'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class NavItem(models.Model):
    """Enlace del menu del header sticky."""
    label = models.CharField(max_length=100, default='', verbose_name='Texto')
    url = models.CharField(max_length=255, default='#home', verbose_name='Enlace (#ancla o /ruta)')
    order = models.IntegerField(default=0, verbose_name='Orden')
    visible = models.BooleanField(default=True, verbose_name='Visible en el menu')

    class Meta:
        ordering = ['order']
        verbose_name = '03 · Enlace de menu'
        verbose_name_plural = '03 · Enlaces de menu'

    def __str__(self):
        return self.label or 'Menu'


class HeaderBlock(models.Model):
    """Hero / seccion superior del home (singleton, order=0)."""
    title = models.CharField(max_length=255, default='', verbose_name='Titulo linea 1')
    title_line2 = models.CharField(max_length=255, default='', blank=True, verbose_name='Titulo linea 2')
    subtitle = models.CharField(max_length=500, default='', blank=True, verbose_name='Descripcion (vacio = oculta)')
    button_text = models.CharField(max_length=100, default='Contact Us', blank=True,
                                   verbose_name='Boton principal texto (vacio = oculto)')
    button_link = models.CharField(max_length=255, default='', blank=True, verbose_name='Boton principal enlace')
    video_id = models.CharField(max_length=50, default='S_CGed6E610', blank=True, verbose_name='Video YouTube ID')
    video_label = models.CharField(max_length=100, default='Watch Now', blank=True, verbose_name='Texto junto al video')
    show_subtitle = models.BooleanField(default=True,
                                        verbose_name='Mostrar la descripcion (Titulos y texto)')
    show_cta = models.BooleanField(default=True,
                                   verbose_name='Mostrar el boton principal + video')
    image = models.ImageField(upload_to='header_blocks/', blank=True, null=True,
                              verbose_name='Imagen de fondo (si esta vacia usa la del template)')
    card_title = models.CharField(max_length=255, default='', blank=True, verbose_name='Titulo de la tarjeta')
    card_name_label = models.CharField(max_length=100, default='Your Name :', blank=True, verbose_name='Label Nombre')
    card_email_label = models.CharField(max_length=100, default='Your Email :', blank=True, verbose_name='Label Email')
    card_phone_label = models.CharField(max_length=100, default='Phone No. :', blank=True, verbose_name='Label Telefono')
    card_button_text = models.CharField(max_length=100, default='Free Trial', blank=True, verbose_name='Texto boton tarjeta')
    order = models.IntegerField(default=0, verbose_name='Display Order')

    class Meta:
        ordering = ['order']
        verbose_name = '04 · Hero (portada)'
        verbose_name_plural = '04 · Hero (portada)'

    def __str__(self):
        return self.title or 'Hero'


class SectionBlock(models.Model):
    """Cabecera editable de cada seccion del home, identificada por `key`."""
    KEY_CHOICES = [
        ('about', 'About (We Create & Enhance)'),
        ('features', 'Features'),
        ('choose_us', 'Why choose us'),
        ('portfolio', 'Portfolio'),
        ('partners', 'Partners'),
        ('cta', 'C.T.A'),
        ('pricing', 'Pricing'),
        ('faqs', 'FAQs'),
        ('reviews', 'Testimonial'),
        ('blogs', 'Blog'),
        ('contactus', 'Contact us'),
        ('map', 'Mapa (iframe)'),
    ]
    key = models.CharField(max_length=30, choices=KEY_CHOICES, verbose_name='Seccion')
    block = models.OneToOneField('HomeBlock', null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='content',
                                 verbose_name='Bloque del home (solo si es copia)')
    eyebrow = models.CharField(max_length=255, default='', blank=True, verbose_name='Texto pequeno superior')
    eyebrow_size = models.CharField(max_length=12, default='', blank=True,
                                    verbose_name='Tamano del texto pequeno (ej. 18px; vacio = original)')
    eyebrow_color = models.CharField(max_length=9, default='', blank=True,
                                     verbose_name='Color del texto pequeno (#hex; vacio = original)')
    title = models.CharField(max_length=255, default='', blank=True, verbose_name='Titulo')
    description = models.TextField(default='', blank=True, verbose_name='Descripcion')
    TITLE_FONTS = [('', 'Por defecto de la plantilla'), ('waterfall', 'Waterfall (Google Fonts)')]
    title_font = models.CharField(max_length=20, choices=TITLE_FONTS, default='', blank=True,
                                  verbose_name='Tipografia del titulo (seccion 5 · Partners)')
    title_size = models.CharField(max_length=12, default='', blank=True,
                                  verbose_name='Tamano del titulo (ej. 48px, 3rem; vacio = original)')
    title_color = models.CharField(max_length=9, default='', blank=True,
                                   verbose_name='Color del titulo (#hex; vacio = original)')
    button_label = models.CharField(max_length=100, default='', blank=True, verbose_name='Texto del boton')
    button_url = models.CharField(max_length=255, default='', blank=True, verbose_name='Enlace del boton')
    image = models.ImageField(upload_to='sections/', blank=True, null=True, verbose_name='Imagen de la seccion')
    background_image = models.ImageField(upload_to='sections_bg/', blank=True, null=True,
                                         verbose_name='Imagen de fondo')
    embed_url = models.URLField(default='', blank=True, verbose_name='URL de mapa embebido (solo seccion map)')
    extra_image = models.ImageField(upload_to='sections/', blank=True, null=True,
                                    verbose_name='Imagen secundaria (avatar del About)')
    extra_image_dup = models.ImageField(upload_to='sections/', blank=True, null=True,
                                        verbose_name='Imagen secundaria de la fila duplicada (About) — vacio = igual que la original')
    badge_text = models.CharField(max_length=255, default='', blank=True, verbose_name='Insignia / badge (About)')
    badge_text_dup = models.CharField(max_length=255, default='', blank=True,
                                      verbose_name='Insignia / badge de la fila duplicada (About) — vacio = igual que la original')
    person_text = models.CharField(max_length=255, default='', blank=True, verbose_name='Texto "Hi, This is..." (About)')
    checklist = models.TextField(default='', blank=True,
                                 verbose_name='Checklist (una linea por item, solo About)')
    stat_label = models.CharField(max_length=100, default='Revenue', blank=True,
                                  verbose_name='Label de la stat flotante (About)')
    stat_number = models.CharField(max_length=50, default='39548', blank=True,
                                   verbose_name='Numero de la stat (About)')
    stat_target = models.PositiveIntegerField(default=45485, blank=True,
                                              verbose_name='Objetivo de animacion de la stat')
    stat_percent = models.CharField(max_length=20, default='3.85%', blank=True,
                                    verbose_name='Porcentaje de la stat (About)')
    show_stat = models.BooleanField(default=True,
                                    verbose_name='Mostrar stat flotante (About)')
    show_learn_more = models.BooleanField(default=True,
                                          verbose_name='Mostrar boton Learn More (About)')
    show_play = models.BooleanField(default=True,
                                     verbose_name='Mostrar boton play del video (About)')
    show_eyebrow = models.BooleanField(default=True,
                                        verbose_name='Mostrar texto pequeno superior (About)')
    show_title = models.BooleanField(default=True,
                                      verbose_name='Mostrar titulo (About)')
    show_description = models.BooleanField(default=True,
                                            verbose_name='Mostrar descripcion (About)')
    show_checklist = models.BooleanField(default=True,
                                          verbose_name='Mostrar lista / checklist (About)')
    show_avatar = models.BooleanField(default=True,
                                       verbose_name='Mostrar fila 1: avatar + insignia (About)')
    show_avatar_dup = models.BooleanField(default=True,
                                           verbose_name='Mostrar fila 2: avatar + insignia (duplicada)')
    show_main_image = models.BooleanField(default=True,
                                           verbose_name='Mostrar imagen principal (About)')
    form_name_label = models.CharField(max_length=100, default='Name :', blank=True,
                                       verbose_name='Form placeholder Nombre (Contacto)')
    form_email_label = models.CharField(max_length=100, default='Email :', blank=True,
                                        verbose_name='Form placeholder Email (Contacto)')
    form_subject_label = models.CharField(max_length=100, default='Subject :', blank=True,
                                          verbose_name='Form placeholder Asunto (Contacto)')
    form_message_label = models.CharField(max_length=100, default='Message :', blank=True,
                                          verbose_name='Form placeholder Mensaje (Contacto)')
    form_button_label = models.CharField(max_length=100, default='Send Message', blank=True,
                                         verbose_name='Form boton enviar (Contacto)')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '05 · Seccion (titulos y textos)'
        verbose_name_plural = '05 · Secciones (titulos y textos)'

    def __str__(self):
        return self.get_key_display()


class FeatureBlock(models.Model):
    """Card de la rejilla Features."""
    title = models.CharField(max_length=255, default='', verbose_name='Titulo')
    description = models.TextField(default='', verbose_name='Descripcion')
    icon = models.CharField(max_length=100, default='ri-star-line', verbose_name='Icono (classe remix)')
    url = models.CharField(max_length=255, default='', blank=True, verbose_name='Enlace "Read More"')
    order = models.IntegerField(default=0, verbose_name='Display Order')

    class Meta:
        ordering = ['order']
        verbose_name = '06 · Feature (card)'
        verbose_name_plural = '06 · Features (cards)'

    def __str__(self):
        return self.title or 'Feature'


class ServiceTab(models.Model):
    """Tabs "Why choose us": pestaas + panel con imagen."""
    label = models.CharField(max_length=255, default='', verbose_name='Texto de la pestana (ej. 01. Web Development)')
    title = models.CharField(max_length=255, default='', verbose_name='Titulo del panel')
    text = models.TextField(default='', verbose_name='Texto del panel')
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='Imagen del panel')
    url = models.CharField(max_length=255, default='', blank=True, verbose_name='Enlace "Read More"')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '07 · Servicio / tab (Why choose us)'
        verbose_name_plural = '07 · Servicios / tabs (Why choose us)'

    def __str__(self):
        return self.label or self.title or 'Servicio'


class PricingBlock(models.Model):
    """Plan de precios (monthly / yearly)."""
    BILLING = [(1, 'Mensual'), (2, 'Anual')]
    title = models.CharField(max_length=255, default='', verbose_name='Nombre del plan')
    price = models.CharField(max_length=100, default='', verbose_name='Precio (sin simbolo)')
    period = models.CharField(max_length=50, default='/per month', verbose_name='Periodo')
    features = models.TextField(default='', verbose_name='Features (una linea por feature)')
    button_text = models.CharField(max_length=100, default='Choose Your Plan', verbose_name='Texto del boton')
    button_link = models.CharField(max_length=255, default='', blank=True, verbose_name='Enlace del boton')
    billing = models.PositiveSmallIntegerField(choices=BILLING, default=1, verbose_name='Facturacion')
    highlight = models.BooleanField(default=False, verbose_name='Plan destacado (fondo primary)')
    order = models.IntegerField(default=0, verbose_name='Display Order')

    class Meta:
        ordering = ['billing', 'order']
        verbose_name = '08 · Plan de precios'
        verbose_name_plural = '08 · Planes de precios'

    def __str__(self):
        return self.title or 'Pricing'


class FAQItem(models.Model):
    """Pregunta/respuesta del acordeon FAQs."""
    question = models.CharField(max_length=255, default='', verbose_name='Pregunta')
    answer = models.TextField(default='', verbose_name='Respuesta')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '09 · FAQ'
        verbose_name_plural = '09 · FAQs'

    def __str__(self):
        return self.question or 'FAQ'


class ReviewItem(models.Model):
    """Testimonio del slider."""
    name = models.CharField(max_length=100, default='', verbose_name='Nombre')
    role = models.CharField(max_length=100, default='', blank=True, verbose_name='Cargo / empresa')
    text = models.TextField(default='', verbose_name='Testimonio')
    avatar = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name='Foto')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '10 · Testimonio'
        verbose_name_plural = '10 · Testimonios'

    def __str__(self):
        return self.name or 'Testimonio'


class CounterItem(models.Model):
    """Contador de la seccion de testimonios."""
    icon = models.CharField(max_length=100, default='ri-star-line', verbose_name='Icono')
    number = models.CharField(max_length=50, default='0', verbose_name='Numero visible')
    target = models.PositiveIntegerField(default=0, verbose_name='Objetivo de la animacion')
    symbol = models.CharField(max_length=10, default='', blank=True, verbose_name='Simbolo (+, %, ...) ')
    title = models.CharField(max_length=100, default='', verbose_name='Etiqueta')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '11 · Contador'
        verbose_name_plural = '11 · Contadores'

    def __str__(self):
        return f'{self.number}{self.symbol} {self.title}'.strip()


class PartnerLogo(models.Model):
    """Logo de la rejilla de partners."""
    image = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name='Logo')
    alt = models.CharField(max_length=100, default='', blank=True, verbose_name='Texto alternativo')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '12 · Partner'
        verbose_name_plural = '12 · Partners'

    def __str__(self):
        return self.alt or f'Partner {self.pk}'


class FooterColumn(models.Model):
    """Columna de enlaces del footer."""
    KEY_CHOICES = [('company', 'Company'), ('usefull', 'Usefull Links'), ('bottom', 'Enlaces inferiores')]
    key = models.CharField(max_length=20, choices=KEY_CHOICES, unique=True, verbose_name='Columna')
    heading = models.CharField(max_length=100, default='', verbose_name='Titulo de la columna')
    order = models.IntegerField(default=0, verbose_name='Orden')
    visible = models.BooleanField(default=True, verbose_name='Visible en el footer')

    class Meta:
        ordering = ['order']
        verbose_name = '13 · Columna del footer'
        verbose_name_plural = '13 · Columnas del footer'

    def __str__(self):
        return self.heading or self.get_key_display()


class FooterLink(models.Model):
    """Enlace dentro de una columna del footer."""
    column = models.ForeignKey(FooterColumn, related_name='links', on_delete=models.CASCADE, verbose_name='Columna')
    label = models.CharField(max_length=100, default='', verbose_name='Texto')
    url = models.CharField(max_length=255, default='', verbose_name='Enlace')
    order = models.IntegerField(default=0, verbose_name='Orden')

    class Meta:
        ordering = ['order']
        verbose_name = '14 · Enlace del footer'
        verbose_name_plural = '14 · Enlaces del footer'

    def __str__(self):
        return self.label or 'Link'


class SocialLink(models.Model):
    """Icono social del footer."""
    icon = models.CharField(max_length=100, default='ri-facebook-circle-line', verbose_name='Icono (classe remix)')
    url = models.CharField(max_length=255, default='#', verbose_name='Enlace')
    order = models.IntegerField(default=0, verbose_name='Orden')
    visible = models.BooleanField(default=True, verbose_name='Visible en el footer')

    class Meta:
        ordering = ['order']
        verbose_name = '15 · Red social del footer'
        verbose_name_plural = '15 · Redes sociales del footer'

    def __str__(self):
        return self.icon


class FooterBlock(models.Model):
    """Texto introductorio del footer."""
    title = models.CharField(max_length=255, default='', verbose_name='Titulo')
    description = models.TextField(default='', verbose_name='Descripcion')
    address = models.CharField(max_length=500, default='', blank=True, verbose_name='Direccion')
    phone = models.CharField(max_length=100, default='', blank=True, verbose_name='Telefono')
    email = models.EmailField(default='', blank=True, verbose_name='Email')
    order = models.IntegerField(default=0, verbose_name='Display Order')

    class Meta:
        ordering = ['order']
        verbose_name = '16 · Texto del footer'
        verbose_name_plural = '16 · Textos del footer'

    def __str__(self):
        return self.title or 'Footer'


class ContactInfo(models.Model):
    """Bloques de contacto de la seccion Contact us (Phone / Email / Location)."""
    label = models.CharField(max_length=100, default='', verbose_name='Titulo (Phone, Email, ...)')
    value = models.CharField(max_length=255, default='', verbose_name='Valor')
    icon = models.CharField(max_length=100, default='ri-map-pin-line', verbose_name='Icono')

    class Meta:
        ordering = ['id']
        verbose_name = '17 · Dato de contacto'
        verbose_name_plural = '17 · Datos de contacto'

    def __str__(self):
        return self.label or 'Contact'


class TeamBlock(models.Model):
    """Team horizontal block."""
    name = models.CharField(max_length=255, default='', verbose_name='Name')
    role = models.CharField(max_length=255, default='', verbose_name='Role')
    image = models.ImageField(upload_to='team_blocks/', blank=True, null=True, verbose_name='Photo')
    order = models.IntegerField(default=0, verbose_name='Display Order')

    class Meta:
        ordering = ['order']
        verbose_name = '18 · Team member'
        verbose_name_plural = '18 · Team members'

    def __str__(self):
        return self.name or 'Team Member'


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='blog_images/', verbose_name='Imagen')
    title = models.CharField(max_length=255, verbose_name='Titulo')
    slug = models.SlugField(unique=True)
    desc = models.TextField(default='', blank=True, verbose_name='Extracto')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '19 · Post del blog'
        verbose_name_plural = '19 · Posts del blog'

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='portfolio_images/', verbose_name='Imagen')
    title = models.CharField(max_length=255, verbose_name='Titulo')
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, default='', blank=True, verbose_name='Subtitulo')
    groups = models.CharField(max_length=255, default='["all"]', verbose_name='Grupos de filtro')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '20 · Item de portfolio'
        verbose_name_plural = '20 · Items de portfolio'

    def __str__(self):
        return self.title


class HomeBlock(models.Model):
    """Orden de los bloques del home (arrastrar y soltar en el panel)."""
    key = models.CharField(max_length=30, verbose_name='Clave interna')
    label = models.CharField(max_length=100, verbose_name='Nombre del bloque')
    order = models.PositiveIntegerField(default=0, verbose_name='Posicion')
    visible = models.BooleanField(default=True, verbose_name='Visible en la web')

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Bloque del home (drag & drop)'
        verbose_name_plural = 'Orden de los bloques del home (arrastra para mover)'

    def __str__(self):
        return f"{self.order + 1}. {self.label}"
