%bcond_without	tracker

Summary:	Nautilus is a file manager for the GNOME desktop environment
Name:		nautilus
Version:	3.6.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/nautilus/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	a0ef8ce24933aa897568aef98645d4e8
URL:		http://nautilus.eazel.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	exempi-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	libexif-devel
BuildRequires:	librsvg-devel
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.7.8
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
%{?with_tracker:BuildRequires:	tracker-devel}
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	shared-mime-info
Requires:	gdk-pixbuf-rsvg
Requires:	gvfs
Requires:	xdg-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Nautilus integrates access to files, applications, media,
Internet-based resources and the Web. Nautilus delivers a dynamic and
rich user experience. Nautilus is an free software project developed
under the GNU General Public License and is a core component of the
GNOME desktop project.

%package libs
Summary:	Nautilus libraries
Group:		X11/Libraries

%description libs
Nautilus libraries.

%package devel
Summary:	Libraries and include files for developing Nautilus components
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop Nautilus components.

%package apidocs
Summary:	libnautilus-extension API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libnautilus-extension API documentation.

%package shell-search-provider
Summary:	GNOME Shell search provider
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell

%description shell-search-provider
Search result provider for GNOME Shell.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--disable-update-mimedb	\
	%{!?with_tracker:--enable-tracker=no} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,crh,ha,ig,io,ps}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database
%update_desktop_database
%update_gsettings_cache

%postun
%update_desktop_database
%update_mime_database
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README THANKS
%attr(755,root,root) %{_bindir}/nautilus
%attr(755,root,root) %{_bindir}/nautilus-autorun-software
%attr(755,root,root) %{_bindir}/nautilus-connect-server

%dir %{_libexecdir}
%dir %{_libexecdir}/extensions-3.0
%attr(755,root,root) %{_libexecdir}/extensions-3.0/libnautilus-sendto.so
%attr(755,root,root) %{_libexecdir}/nautilus-convert-metadata

%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/mime/packages/*.xml
%{_datadir}/nautilus

%{_desktopdir}/*.desktop

%{_mandir}/man1/nautilus*.1*

%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/nautilus
%attr(755,root,root) %ghost %{_libdir}/libnautilus-extension.so.?
%attr(755,root,root) %{_libdir}/libnautilus-extension.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnautilus-extension.so
%{_libdir}/libnautilus-extension.la
%{_includedir}/%{name}
%{_pkgconfigdir}/libnautilus-extension.pc
%{_datadir}/gir-1.0/Nautilus-3.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libnautilus-extension

%files shell-search-provider
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}//nautilus/nautilus-shell-search-provider
%{_datadir}/dbus-1/services/org.gnome.Nautilus.SearchProvider.service
%{_datadir}/gnome-shell/search-providers/nautilus-search-provider.ini

