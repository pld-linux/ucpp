#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	C preprocessor compliant to ISO-C99
Summary(pl.UTF-8):	Preprocesor C zgodny z ISO-C99
Name:		ucpp
Version:	1.3.5
Release:	1
License:	BSD
Group:		Development/Tools
#Source0Download: https://gitlab.com/scarabeusiv/ucpp/-/tags
Source0:	https://gitlab.com/scarabeusiv/ucpp/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	2a8529e9a7ecb6e39876e6266edfeb2d
URL:		https://gitlab.com/scarabeusiv/ucpp
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C preprocessor is a part of a C compiler responsible for macro
replacement, conditional compilation and inclusion of header files. It
is often found as a stand-alone program on Unix systems.

ucpp is such a preprocessor; it is designed to be quick and light, but
anyway fully compliant to the ISO standard 9899:1999, also known as
C99. ucpp can be compiled as a stand-alone program, or linked to some
other code; in the latter case, ucpp will output tokens, one at a
time, on demand, as an integrated lexer.

%description -l pl.UTF-8
Preprocesor C to część kompilatora C, odpowiedzialna za podstawianie
makr, kompilację warunkową i dołączanie plików nagłówkowych. W
systemach uniksowych często jest to samodzielny program.

ucpp jest takim preprocesorem. Został zaprojektowany jako szybki i
lekki, ale jest w pełni zgodny ze standardem ISO 9899:1999, znanym
jako C99. ucpp może być zbudowany jako samodzielny program lub
wlinkowany do innego kodu - w tym przypadku ucpp przekazuje na żądanie
tokeny wyjściowe, po jednym naraz, jako zintegrowany analizator
leksykalny.

%package libs
Summary:	UCPP preprocessor library
Summary(pl.UTF-8):	Biblioteka preprocesora UCPP
Group:		Libraries

%description libs
UCPP preprocessor library.

%description libs -l pl.UTF-8
Biblioteka preprocesora UCPP.

%package devel
Summary:	Header files for UCPP preprocessor library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki preprocesora UCPP
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for UCPP preprocessor library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki preprocesora UCPP.

%package static
Summary:	Static UCPP preprocessor library
Summary(pl.UTF-8):	Statyczna biblioteka preprocesora UCPP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static UCPP preprocessor library.

%description static -l pl.UTF-8
Statyczna biblioteka preprocesora UCPP.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libucpp.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog.old README README.md
%attr(755,root,root) %{_bindir}/ucpp
%{_mandir}/man1/ucpp.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libucpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libucpp.so.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libucpp.so
%{_includedir}/libucpp
%{_pkgconfigdir}/libucpp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libucpp.a
%endif
