SUBDIRS = icons

# Desktop file
@INTLTOOL_DESKTOP_RULE@
desktopdir = $(datadir)/applications
desktop_in_files = org.gnome.Usage.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)

# GSettings
@GSETTINGS_RULES@
gsettings_SCHEMAS = org.gnome.Usage.gschema.xml
# For uninstalled use
gschemas.compiled: $(gsettings_SCHEMAS) Makefile
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) $(builddir)

# AppData
@INTLTOOL_XML_RULE@
@APPSTREAM_XML_RULES@
appstream_in_files = org.gnome.Usage.appdata.xml.in
appstream_XML = $(appstream_in_files:.appdata.xml.in=.appdata.xml)

resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(builddir)/usage.gresource.xml)
usage.gresource: usage.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) --sourcedir=$(builddir) $<

resourcedir = $(pkgdatadir)
resource_DATA = usage.gresource

EXTRA_DIST = \
	$(desktop_in_files) \
	$(appstream_in_files) \
	$(gsettings_SCHEMAS) \
	$(resource_files) \
	usage.gresource.xml \
	$(NULL)

CLEANFILES = \
	$(desktop_DATA) \
	usage.gresource \
	$(appstream_XML) \
	*.valid \
	gschemas.compiled \
	$(NULL)

all-local: gschemas.compiled

-include $(top_srcdir)/git.mk
