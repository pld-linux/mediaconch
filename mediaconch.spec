#
# Conditional build:
%bcond_with	webengine	# use Qt5WebEngine instead of Qt5WebKit

Summary:        Implementation checker and policy checker for video and audio files (CLI)
Summary(pl.UTF-8):	Narzędzie do sprawdzania implementacji i polityki dla plików audio i wideo (CLI)
Name:		mediaconch
Version:	18.03.2
Release:	2
License:	BSD or Apache v2.0 or LGPL v2.1+ or GPL v2+ or MPL v2.0+
Group:		Applications/Multimedia
Source0:	https://mediaarea.net/download/source/mediaconch/%{version}/%{name}_%{version}.tar.xz
# Source0-md5:	265c683d0bd68458f537cb1f811ca10f
URL:		https://mediaarea.net/MediaConch
BuildRequires:	OpenGL-devel
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
%{?with_webengine:BuildRequires:	Qt5WebEngine-devel >= 5.6}
%{!?with_webengine:BuildRequires:	Qt5WebKit-devel >= 5}
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	jansson-devel
BuildRequires:	libevent-devel >= 2
BuildRequires:	libmediainfo-devel >= %{version}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	libzen-devel >= 0.4.37
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	libmediainfo >= %{version}
Requires:	libzen >= 0.4.37
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MediaConch is an implementation checker, policy checker, reporter, and
fixer that targets preservation-level audiovisual files (specifically
Matroska, Linear Pulse Code Modulation (LPCM) and FF Video Codec 1
(FFV1)).

%description -l pl.UTF-8
MediaConch to narzędzie do sprawdzania implementacji, sprawdzania
polityki, raportowania i poprawiania, nastawione na poziom zachowania
plików audiowizualnych (w szczególności Matroska, LPCM i FFV1).

%package server
Summary:	Implementation checker and policy checker for video and audio files (Server)
Summary(pl.UTF-8):	Narzędzie do sprawdzania implementacji i polityki dla plików audio i wideo (serwer)
Group:		Networking/Daemons

%description server
MediaConch is an implementation checker, policy checker, reporter, and
fixer that targets preservation-level audiovisual files (specifically
Matroska, Linear Pulse Code Modulation (LPCM) and FF Video Codec 1
(FFV1)).

%description server -l pl.UTF-8
MediaConch to narzędzie do sprawdzania implementacji, sprawdzania
polityki, raportowania i poprawiania, nastawione na poziom zachowania
plików audiowizualnych (w szczególności Matroska, LPCM i FFV1).

%package gui
Summary:	Implementation checker and policy checker for video and audio files (GUI)
Summary(pl.UTF-8):	Narzędzie do sprawdzania implementacji i polityki dla plików audio i wideo (GUI)
Group:		X11/Applications/Multimedia
Requires:	libmediainfo >= %{version}
Requires:	libzen >= 0.4.37

%description gui
MediaConch is an implementation checker, policy checker, reporter, and
fixer that targets preservation-level audiovisual files (specifically
Matroska, Linear Pulse Code Modulation (LPCM) and FF Video Codec 1
(FFV1)).

%description gui -l pl.UTF-8
MediaConch to narzędzie do sprawdzania implementacji, sprawdzania
polityki, raportowania i poprawiania, nastawione na poziom zachowania
plików audiowizualnych (w szczególności Matroska, LPCM i FFV1).

%prep
%setup -q -n MediaConch
%undos *.html *.txt Release/*.txt
chmod 644 *.html *.txt Release/*.txt

%build
# build CLI
cd Project/GNU/CLI
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
# Server
cd ../../../Project/GNU/Server
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
# now build GUI
cd ../../../Project/Qt
qmake-qt5 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	%{?with_webengine:USE_WEBENGINE=1} \
	%{!?with_webengine:USE_WEBKIT=1}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/CLI install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C Project/GNU/Server install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{systemdunitdir},%{_sysconfdir}/mediaconch}
cp -p Project/GNU/Server/mediaconchd.service $RPM_BUILD_ROOT%{systemdunitdir}
cp -p Project/GNU/Server/MediaConch.rc $RPM_BUILD_ROOT%{_sysconfdir}/mediaconch

install -d $RPM_BUILD_ROOT{%{_datadir}/metainfo,%{_desktopdir},%{_iconsdir}/hicolor/{256x256,scalable}/apps}
cp -p Project/GNU/GUI/mediaconch-gui.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p Project/GNU/GUI/mediaconch-gui.metainfo.xml $RPM_BUILD_ROOT%{_datadir}/metainfo
cp -p Source/Resource/Image/MediaConch.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps/mediaconch.png
cp -p Source/Resource/Image/MediaConch.svg $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/mediaconch.svg
install Project/Qt/mediaconch-gui $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc History_CLI.txt LICENSE License.html README.md Release/ReadMe_CLI_Linux.txt
%attr(755,root,root) %{_bindir}/mediaconch

%files server
%defattr(644,root,root,755)
%doc LICENSE License.html
%attr(755,root,root) %{_bindir}/mediaconchd
%{systemdunitdir}/mediaconchd.service
%dir %{_sysconfdir}/mediaconch
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mediaconch/MediaConch.rc

%files gui
%defattr(644,root,root,755)
%doc History_GUI.txt LICENSE License.html Release/ReadMe_GUI_Linux.txt
%attr(755,root,root) %{_bindir}/mediaconch-gui
%{_datadir}/metainfo/mediaconch-gui.metainfo.xml
%{_desktopdir}/mediaconch-gui.desktop
%{_iconsdir}/hicolor/256x256/apps/mediaconch.png
%{_iconsdir}/hicolor/scalable/apps/mediaconch.svg
