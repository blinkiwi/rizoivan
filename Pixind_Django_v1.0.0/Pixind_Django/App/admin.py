from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    HomeBlock,
    SiteConfig, StickyNav, NavItem, HeaderBlock, SectionBlock, FeatureBlock,
    ServiceTab, PricingBlock, FAQItem, ReviewItem, CounterItem, PartnerLogo,
    FooterColumn, FooterLink, SocialLink, FooterBlock, ContactInfo, TeamBlock,
    Blog, Portfolio,
)

admin.site.site_header = "Rizoivan · Panel de contenido"
admin.site.site_title = "Rizoivan CMS"
admin.site.index_title = "Dashboard"


# --------------------------------------------------------------- panel CMS ---
def _cms_home(request):
    from django.template.response import TemplateResponse
    from .cms import cms_context

    context = dict(admin.site.each_context(request))
    context.update(cms_context())
    context["title"] = "Panel de contenido"
    return TemplateResponse(request, "admin/cms_home.html", context)


_orig_get_urls = admin.AdminSite.get_urls


def _reorder_homeblocks(request):
    """POST {"ids":[...]} -> guarda el nuevo orden de los bloques del home."""
    import json as _json
    from django.http import JsonResponse
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Se espera POST"}, status=405)
    try:
        ids = [int(i) for i in _json.loads(request.body.decode("utf-8")).get("ids", [])]
    except Exception:
        return JsonResponse({"ok": False, "error": "Payload invalido"}, status=400)
    from .models import HomeBlock as _HB
    validos = list(_HB.objects.values_list("id", flat=True))
    ids = [i for i in ids if i in validos]
    for pos, pk in enumerate(ids):
        _HB.objects.filter(pk=pk).update(order=pos)
    for pos, pk in enumerate(sorted(set(validos) - set(ids)), start=len(ids)):
        _HB.objects.filter(pk=pk).update(order=pos)
    return JsonResponse({"ok": True, "count": len(ids)})


def _toggle_generic(request, modelo, campo="visible"):
    """POST {"id": n} -> conmuta un campo booleano (visible) de una fila."""
    import json as _json
    from django.http import JsonResponse
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Se espera POST"}, status=405)
    try:
        pk = int(_json.loads(request.body.decode("utf-8")).get("id"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Payload invalido"}, status=400)
    fila = modelo.objects.filter(pk=pk).first()
    if fila is None:
        return JsonResponse({"ok": False, "error": "Fila no encontrada"}, status=404)
    setattr(fila, campo, not getattr(fila, campo))
    fila.save(update_fields=[campo])
    return JsonResponse({"ok": True, campo: getattr(fila, campo)})


def _toggle_homeblock(request):
    from .models import HomeBlock
    return _toggle_generic(request, HomeBlock)


def _toggle_sociallink(request):
    from .models import SocialLink
    return _toggle_generic(request, SocialLink)


def _toggle_navitem(request):
    from .models import NavItem
    return _toggle_generic(request, NavItem)


def _toggle_footercolumn(request):
    from .models import FooterColumn
    return _toggle_generic(request, FooterColumn)


def _get_urls_with_cms(self):
    from django.contrib.admin.views.decorators import staff_member_required
    from django.urls import path as _path

    return [
        _path("cms/", staff_member_required(_cms_home), name="cms-home"),
        _path("homeblock/reorder/", staff_member_required(_reorder_homeblocks),
              name="homeblock-reorder"),
        _path("homeblock/toggle/", staff_member_required(_toggle_homeblock),
              name="homeblock-toggle"),
        _path("sociallink/toggle/", staff_member_required(_toggle_sociallink),
              name="sociallink-toggle"),
        _path("navitem/toggle/", staff_member_required(_toggle_navitem),
              name="navitem-toggle"),
        _path("footercolumn/toggle/", staff_member_required(_toggle_footercolumn),
              name="footercolumn-toggle"),
    ] + _orig_get_urls(self)


admin.AdminSite.get_urls = _get_urls_with_cms


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'meta_title', 'updated_at')

    fieldsets = (
        ('Identidad', {'fields': ('site_name', 'meta_title', 'meta_description', 'logo', 'favicon')}),
        ('Footer', {'fields': ('copyright_text',)}),
        ('Créditos del footer (al lado del copyright)', {
            'fields': ('credits_text', 'credits_by', 'credits_name', 'credits_url'),
            'description': 'Se renderizan como: © año COPYRIGHT · TEXTO ♥ NOMBRE_NOMBRE. Déjalos vacíos para ocultar los créditos.',
        }),
        ('Apariencia del sitio (botones flotantes)', {
            'fields': ('default_theme', 'show_theme_switcher', 'show_rtl_switcher'),
            'description': 'Tema por defecto (oscuro) y activar/desactivar los botones flotantes de tema y LTR/RTL de la web.',
        }),
        ('Paleta de colores', {
            'fields': ('color_primary', 'color_text', 'color_hover', 'color_bg'),
            'description': 'Formato #rrggbb. Vacio = color original de la plantilla. '
                           'Primario: botones/enlaces/iconos · Texto: cuerpo y titulos · '
                           'Hover: al pasar el mouse · Fondo: fondo general del sitio.',
        }),
        ('Boton flotante de WhatsApp', {
            'fields': ('whatsapp_enabled', 'whatsapp_phone', 'whatsapp_message'),
            'description': 'Telefono con codigo de pais y sin + ni espacios (ej. 584121234567). '
                           'El mensaje se abre como inicio de la conversacion en wa.me. '
                           'Sin telefono el boton no se muestra.',
        }),
        ('Tecnicos', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StickyNav)
class StickyNavAdmin(admin.ModelAdmin):
    list_display = ('cta_label', 'cta_url')
    fieldsets = (
        ('Logos del header', {
            'fields': ('logo', 'logo_scroll'),
            'description': 'El segundo logo aparece cuando el header se pega al hacer scroll (nav-sticky).',
        }),
        ('Boton de accion', {'fields': ('cta_label', 'cta_url')}),
    )

    def has_add_permission(self, request):
        return not StickyNav.objects.exists()  # singleton


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    ordering = ('order',)


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ('visible_col', 'label', 'url', 'order')
    list_editable = ('label', 'url', 'order')   # texto y enlace editables en la tabla
    ordering = ('order',)
    change_list_template = 'admin/navitem_changelist.html'

    @admin.display(description='Visible')
    def visible_col(self, obj):
        marcado = ' checked' if obj.visible else ''
        return mark_safe(
            f'<input type="checkbox" class="rz-visible" data-id="{obj.pk}"{marcado} '
            f'title="Mostrar/ocultar este enlace del menu">')


@admin.register(HeaderBlock)
class HeaderBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_line2', 'button_text', 'order')

    fieldsets = (
        ('Titulos y texto', {
            'fields': ('title', 'title_line2', 'subtitle', 'show_subtitle', 'order'),
            'description': 'La descripcion es opcional: desmarca "Mostrar" o deja el texto vacio '
                           'y el hero la oculta.',
        }),
        ('Boton principal + video', {
            'fields': ('show_cta', 'button_text', 'button_link', 'video_id', 'video_label'),
            'description': 'Desmarca "Mostrar el boton principal + video" para ocultar la fila '
                           'completa; tambien se ocultan los campos que dejes vacios.',
        }),
        ('Fondo', {'fields': ('image',)}),
        ('Tarjeta del formulario', {
            'fields': ('card_title', 'card_name_label', 'card_email_label',
                       'card_phone_label', 'card_button_text'),
        }),
    )


@admin.register(SectionBlock)
class SectionBlockAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', 'eyebrow', 'order')
    list_editable = ('title', 'eyebrow', 'order')
    list_display_links = ('key',)
    search_fields = ('title', 'eyebrow')

    fieldsets = (
        ('Seccion', {'fields': ('key', 'order')}),
        ('Cabecera (texto)', {'fields': ('eyebrow', 'title', 'description')}),
        ('Boton', {'fields': ('button_label', 'button_url')}),
        ('Imagenes / fondo', {'fields': ('image', 'background_image', 'extra_image', 'extra_image_dup')}),
        ('Solo About', {'fields': ('badge_text', 'badge_text_dup', 'person_text', 'checklist')}),
        ('Solo About (stat flotante)', {
            'fields': ('stat_label', 'stat_number', 'stat_target', 'stat_percent'),
            'classes': ('collapse',),
        }),
        ('Solo About (mostrar / ocultar)', {
            'fields': ('show_eyebrow', 'show_title', 'show_description', 'show_checklist',
                       'show_avatar', 'show_avatar_dup', 'show_main_image',
                       'show_stat', 'show_learn_more', 'show_play'),
            'description': 'Marcado = visible en la web. Activa o apaga por separado el texto '
                           'pequeno, el titulo, la descripcion, la lista, cada fila de '
                           'avatar + insignia, la imagen principal, la stat flotante, el boton '
                           'Learn More y el play (solo aplica a la fila About y a sus copias).',
        }),
        ('Solo Mapa', {'fields': ('embed_url',)}),
        ('Solo Contacto (placeholders del formulario)', {
            'fields': ('form_name_label', 'form_email_label', 'form_subject_label',
                       'form_message_label', 'form_button_label'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        """La personalizacion del titulo (tipografia/tamano/color) solo se muestra
        en las secciones donde aplica: 5 (Partners) y About.
        El banner CTA ademas muestra su interruptor de visibilidad."""
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            return fieldsets
        out = []
        for name, opts in fieldsets:
            if name == 'Cabecera (texto)' and obj.key in ('partners', 'about'):
                opts = dict(opts)
                campos = tuple(opts['fields']) + ('title_font', 'title_size', 'title_color')
                if obj.key == 'about':
                    # el texto pequeno superior solo se personaliza en About
                    campos = ('eyebrow', 'eyebrow_size', 'eyebrow_color',
                              'title', 'description', 'title_font', 'title_size', 'title_color')
                    opts['description'] = ('Personaliza el titulo (tipografia Waterfall, tamano, color) '
                                           'y el texto pequeno superior (tamano y color) de About. '
                                           'Vacio = estilo original.')
                else:
                    opts['description'] = ('Personaliza el titulo de esta seccion (seccion 5 Partners): '
                                           'tipografia Waterfall, tamano y color. Vacio = estilo original.')
                opts['fields'] = campos
            out.append((name, opts))
        if obj.key == 'cta':
            out.append(('Mostrar el banner CTA', {
                'fields': ('cta_visible',),
                'description': 'Al desmarcarlo el banner desaparece del home (misma casilla Visible '
                               'del bloque CTA en "Orden de bloques").',
            }))
        return tuple(out)

    def get_form(self, request, obj=None, **kwargs):
        # cta_visible no es un campo del modelo: quítalo de la lista que valida
        # el ModelForm (el admin la pasa en fields=) antes de llamar a super().
        if obj is not None and obj.key == 'cta' and isinstance(kwargs.get('fields'), (list, tuple)):
            kwargs['fields'] = [f for f in kwargs['fields'] if f != 'cta_visible']
        form = super().get_form(request, obj, **kwargs)
        if obj is None or obj.key != 'cta':
            return form
        from django import forms as _forms
        hb = HomeBlock.objects.filter(key='cta').first()
        inicial = hb.visible if hb else True

        class CtaForm(form):
            cta_visible = _forms.BooleanField(
                required=False, initial=inicial, label='Mostrar el banner CTA en la web')

        return CtaForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.key == 'cta':
            hb = HomeBlock.objects.filter(key='cta').first()
            if hb:
                hb.visible = bool(form.cleaned_data.get('cta_visible', hb.visible))
                hb.save(update_fields=['visible'])


class ContenidoSeccionInline(admin.StackedInline):
    """Contenido propio del bloque: solo se llena en los duplicados."""
    model = SectionBlock
    fk_name = 'block'
    extra = 0
    max_num = 1
    verbose_name = 'Contenido (títulos y textos)'
    verbose_name_plural = 'Contenido propio de este bloque (se crea al duplicar)'

    def has_add_permission(self, request, obj=None):
        # solo editable si el bloque YA tiene contenido (es una copia)
        return obj is not None and getattr(obj, 'content', None) is not None


@admin.register(HomeBlock)
class HomeBlockAdmin(admin.ModelAdmin):
    """Filas arrastrables: reordenan los bloques del home (drag & drop)."""
    list_display = ('position', 'label', 'visible_col', 'key')
    ordering = ('order', 'id')
    change_list_template = 'admin/homeblock_changelist.html'
    actions = ('duplicar', 'delete_selected')
    inlines = [ContenidoSeccionInline]

    @admin.action(description='Duplicar seleccionados (2 veces en la web, editable por separado)')
    def duplicar(self, request, queryset):
        from . import homepage_defaults as D
        from .models import SectionBlock
        clonadas = set(SectionBlock.objects.exclude(block=None).values_list('pk', flat=True))
        canonicas = SectionBlock.objects.exclude(pk__in=clonadas)
        n = 0
        for b in queryset:
            nueva = HomeBlock.objects.create(
                key=b.key,
                label=(b.label[:90] + ' (copia)')[:100],
                order=b.order,      # mismo orden: la copia cae justo debajo (mayor id)
                visible=b.visible,
            )
            skey = D.BLOCK_SECTION.get(b.key)
            origen = getattr(b, 'content', None) or (canonicas.filter(key=skey).first() if skey else None)
            if origen:
                vals = {f.attname: getattr(origen, f.attname)
                        for f in SectionBlock._meta.concrete_fields
                        if f.attname not in ('id', 'block_id')}
                clon = SectionBlock(**vals)
                clon.pk = None
                clon.block = nueva    # CASCADE: borrar la copia borra su contenido
                clon.save()
            n += 1
        self.message_user(
            request,
            f'{n} bloque(s) duplicado(s): aparecen 2 veces y cada uno tiene su contenido propio '
            f'(edítalo entrando a la fila "… (copia)").')

    @admin.display(description='#', ordering='order')
    def position(self, obj):
        return obj.order + 1

    @admin.display(description='Visible')
    def visible_col(self, obj):
        marcado = ' checked' if obj.visible else ''
        return mark_safe(
            f'<input type="checkbox" class="rz-visible" data-id="{obj.pk}"{marcado} '
            f'title="Mostrar/ocultar este bloque en la web">')


@admin.register(FeatureBlock)
class FeatureBlockAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'order')
    list_editable = ('title', 'order')
    search_fields = ('title',)


@admin.register(ServiceTab)
class ServiceTabAdmin(admin.ModelAdmin):
    list_display = ('label', 'title', 'order')
    list_editable = ('order',)


@admin.register(PricingBlock)
class PricingBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'period', 'billing', 'highlight', 'order')
    list_editable = ('price', 'order', 'highlight')
    list_filter = ('billing',)


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question',)


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)


@admin.register(CounterItem)
class CounterItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'symbol', 'order')
    list_editable = ('number', 'symbol', 'order')


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ('alt', 'order')
    list_editable = ('order',)


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ('visible_col', 'key', 'heading', 'order')
    list_editable = ('heading', 'order')
    ordering = ('order',)
    inlines = [FooterLinkInline]
    change_list_template = 'admin/footercolumn_changelist.html'

    @admin.display(description='Visible')
    def visible_col(self, obj):
        marcado = ' checked' if obj.visible else ''
        return mark_safe(
            f'<input type="checkbox" class="rz-visible" data-id="{obj.pk}"{marcado} '
            f'title="Mostrar/ocultar esta columna en el footer">')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('visible_col', 'icon', 'url', 'order')
    list_editable = ('icon', 'url', 'order')   # editar enlaces directo en la tabla
    ordering = ('order',)
    change_list_template = 'admin/sociallink_changelist.html'

    @admin.display(description='Visible')
    def visible_col(self, obj):
        marcado = ' checked' if obj.visible else ''
        return mark_safe(
            f'<input type="checkbox" class="rz-visible" data-id="{obj.pk}"{marcado} '
            f'title="Mostrar/ocultar esta red en el footer">')


@admin.register(FooterBlock)
class FooterBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'icon')
    list_editable = ('value', 'icon')


@admin.register(TeamBlock)
class TeamBlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('role', 'order')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
