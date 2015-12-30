SUBDIRS = data src po

bin_SCRIPTS = usage

EXTRA_DIST = \
	src/main.py \
	VERSION.in \
	$(NULL)

CLEANFILES = \
	$(bin_SCRIPTS) \
	$(NULL)

MAINTAINERCLEANFILES = \
	$(GITIGNORE_MAINTAINERCLEANFILES_TOPLEVEL) \
	$(GITIGNORE_MAINTAINERCLEANFILES_MAKEFILE_IN) \
	$(GITIGNORE_MAINTAINERCLEANFILES_M4_LIBTOOL)

DISTCHECK_CONFIGURE_FLAGS = \
	--enable-appstream-util \
	$(NULL)

GITIGNOREFILES = \
	**/*.swp \
	m4/ \
	autom4te.cache/ \
	aclocal.m4 \
	ChangeLog \
	INSTALL \
	install-sh \
	missing \
	py-compile \
	VERSION \
	$(NULL)

usage: src/main.py Makefile
	$(AM_V_GEN)sed						\
		-e s!\@srcdir\@!$(abs_top_srcdir)!	\
		-e s!\@prefix\@!$(prefix)!		\
		-e s!\@datadir\@!$(datadir)!		\
		-e s!\@pkgdatadir\@!$(pkgdatadir)!	\
		-e s!\@libexecdir\@!$(libexecdir)!	\
		-e s!\@libdir\@!$(libdir)!		\
		-e s!\@pkglibdir\@!$(pkglibdir)!	\
		-e s!\@localedir\@!$(localedir)!	\
		-e s!\@pythondir\@!$(pythondir)!	\
		-e s!\@pyexecdir\@!$(pyexecdir)!	\
		-e s!\@PACKAGE\@!$(PACKAGE)!		\
		-e s!\@VERSION\@!$(VERSION)!		\
		< $< > $@
	chmod a+x $@

all-local: usage

-include $(top_srcdir)/git.mk
