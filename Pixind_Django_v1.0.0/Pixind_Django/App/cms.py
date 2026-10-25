"""Registro de bloques del CMS: lo que ve el 'Panel de contenido'."""
from django.urls import reverse

from .models import (
    HomeBlock,
    SiteConfig, StickyNav, NavItem, HeaderBlock, SectionBlock, FeatureBlock,
    ServiceTab, PricingBlock, FAQItem, ReviewItem, CounterItem, PartnerLogo,
    FooterColumn, FooterLink, SocialLink, FooterBlock, ContactInfo, Blog, Portfolio,
)

CMS_URL = "/admin/cms/"


def _change_url(model, pk):
    try:
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_change", args=[pk])
    except Exception:
        return CMS_URL


def _list_url(model):
    try:
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")
    except Exception:
        return CMS_URL


def _add_url(model):
    try:
        return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_add")
    except Exception:
        return CMS_URL


def _single(model, **lookup):
    """Primera fila del singleton (o None)."""
    qs = model.objects.all()
    if lookup:
        qs = qs.filter(**lookup)
    return qs.first()


def build_blocks():
    """Lista de tarjetas del panel CMS: icono, titulo, resumen y enlace directo."""
    site = _single(SiteConfig)
    nav = _single(StickyNav)
    hero = _single(HeaderBlock, order=0)
    footer = _single(FooterBlock, order=0)

    def add_card(icon, title, desc, model, summary, singleton=False, lookup=None):
        obj = None
        if singleton:
            obj = _single(model, **(lookup or {}))
        url = _change_url(model, obj.pk) if obj else _add_url(model)
        count = model.objects.count()
        return {
            "icon": icon, "title": title, "desc": desc, "summary": summary,
            "url": url, "count": count, "is_list": not singleton,
        }

    return [
        add_card("⚙", "Sitio, logo y favicon",
                 "Nombre, título de pestaña, logo, favicon, copyright y paleta de colores",
                 SiteConfig,
                 (site.site_name if site else "Sin configurar") +
                 (" · " + (site.copyright_text or "")[:38] if site else ""),
                 singleton=True),
        (lambda cta: {"icon": "🖼", "title": "Banner CTA (textos, imagen, activar)",
                      "desc": "Eyebrow, título, descripción, botón, imagen de fondo y mostrar/ocultar",
                      "summary": ((cta.title[:46] + "…") if cta and len(cta.title) > 46
                                  else (cta.title if cta else "Sin configurar")),
                      "url": _change_url(SectionBlock, cta.pk) if cta else _list_url(SectionBlock),
                      "count": 1, "is_list": False})(SectionBlock.objects.filter(key='cta').first()),
        add_card("☗", "Header / botonera sticky",
                 "Logo del menú, logo al hacer scroll y botón de acción principal",
                 StickyNav,
                 (f"Botón: {nav.cta_label}" if nav else "Sin configurar"),
                 singleton=True),
        add_card("☰", "Menú de navegación",
                 "Enlaces del header (texto y destino)",
                 NavItem, f"{NavItem.objects.count()} enlaces"),
        add_card("◆", "Hero (portada)",
                 "Títulos, descripción, botón, imagen de fondo, vídeo y tarjeta",
                 HeaderBlock,
                 ((hero.title + (" / " + hero.title_line2 if hero.title_line2 else ""))
                  if hero else "Sin configurar"),
                 singleton=True, lookup={"order": 0}),
        {"icon": "▦", "title": "Secciones del home",
         "desc": "Título, texto pequeño, descripción e imagen de cada sección",
         "summary": f"{SectionBlock.objects.count()} secciones",
         "url": _list_url(SectionBlock), "count": SectionBlock.objects.count(),
         "is_list": True, "is_sections": True},
        add_card("↕", "Orden de bloques (drag & drop)",
                 "Arrastra para mover; marca/desmarca la casilla Visible para ocultar bloques",
                 HomeBlock, f"{HomeBlock.objects.filter(visible=True).count()}"
                            f"/{HomeBlock.objects.count()} visibles"),
        add_card("✦", "Features (cards)",
                 "Icono, título y texto de las tarjetas de features",
                 FeatureBlock, f"{FeatureBlock.objects.count()} tarjetas"),
        add_card("⇥", "Servicios / tabs",
                 "Pestañas de '¿Por qué elegirnos?' con su imagen",
                 ServiceTab, f"{ServiceTab.objects.count()} pestañas"),
        add_card("$", "Planes de precios",
                 "Mensual y anual, precio, features y botón",
                 PricingBlock, f"{PricingBlock.objects.count()} planes"),
        add_card("?", "Preguntas frecuentes",
                 "Preguntas y respuestas del acordeón",
                 FAQItem, f"{FAQItem.objects.count()} preguntas"),
        add_card("❝", "Testimonios",
                 "Nombre, cargo, texto y foto",
                 ReviewItem, f"{ReviewItem.objects.count()} testimonios"),
        add_card("#", "Contadores",
                 "Números animados de la sección de testimonios",
                 CounterItem, f"{CounterItem.objects.count()} contadores"),
        add_card("⬡", "Partners",
                 "Logos de la rejilla de partners",
                 PartnerLogo, f"{PartnerLogo.objects.count()} logos"),
        add_card("✎", "Blog",
                 "Posts que aparecen en el home",
                 Blog, f"{Blog.objects.count()} posts"),
        add_card("▣", "Portfolio",
                 "Items de la galería del home",
                 Portfolio, f"{Portfolio.objects.count()} items"),
        add_card("✉", "Datos de contacto",
                 "Teléfono, email y ubicación de la sección de contacto",
                 ContactInfo, f"{ContactInfo.objects.count()} datos"),
        add_card("▬", "Texto del footer",
                 "Descripción de la columna izquierda del pie",
                 FooterBlock,
                 (footer.description[:60] + "…" if footer and len(footer.description or "") > 60
                  else (footer.description if footer else "Sin configurar")),
                 singleton=True, lookup={"order": 0}),
        add_card("⌗", "Columnas del footer",
                 "Títulos y enlaces (Company, Usefull Links, inferiores) — se editan dentro",
                 FooterColumn, f"{FooterColumn.objects.count()} columnas · {FooterLink.objects.count()} enlaces"),
        add_card("@", "Redes sociales",
                 "Iconos y enlaces del pie",
                 SocialLink, f"{SocialLink.objects.count()} redes"),
    ]


def build_sections():
    """Las secciones canonicas del home (sin los clones de bloques duplicados)."""
    out = []
    clonadas = set(SectionBlock.objects.exclude(block=None).values_list("pk", flat=True))
    for s in SectionBlock.objects.exclude(pk__in=clonadas):
        out.append({
            "key": s.get_key_display(),
            "eyebrow": s.eyebrow,
            "title": s.title.replace("\n", " / "),
            "url": _change_url(SectionBlock, s.pk),
        })
    return out


def cms_context():
    return {
        "cms_url": CMS_URL,
        "cms_blocks": build_blocks(),
        "cms_sections": build_sections(),
    }
