Summary:	Moscow ML
Name:		mosml
Version:	2.00
Release:	3
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
URL:		http://www.dina.kvl.dk/~sestoft/mosml.html
Source0:	ftp://ftp.dina.kvl.dk/pub/mosml/mos20src.tar.gz
Patch0:		%{name}_dynlibs_setup.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Moscow ML provides a light-weight implementation of full Standard ML,
including Modules and some extensions. Standard ML is a strict
functional language widely used in teaching and research.

Moscow ML is based on the Caml Light system, which gives fast
compilation and modest storage consumption.

   - The full SML Modules language (structures, signatures, and functors)
     is now supported, thanks to Claudio Russo.
   - Also, several extensions to the SML Modules language are provided:
      - higher-order functors: functors may be defined within structures and
        functors
      - first-class modules: structures and functors may be packed and then
        handled as Core language values, which may then be unpacked as
        structures or functors again
      - recursive modules: signatures and structures may be recursively
        defined
   - Despite that improvements, Moscow ML remains backwards compatible.
   - Value polymorphism has become friendlier: non-generalizable free
     type variables are left free, and become instantiated (once only) when
     the bound variable is used
   - Added facilities for creating and communicating with subprocesses
     (structure Unix and Signal from SML Basis Library).
   - Added facilities for efficient functional generation of HTML code
     (structure Msp); also supports the writing of ML Server Page scripts.
   - Added facilities setting and accessing `cookies' in CGI scripts
     (structure Mosmlcookie), thanks to Hans Molin, Uppsala, Sweden.
   - The Gdimage structure now produces PNG images (using Thomas
     Boutell's gd library).

%prep
%setup -q -n mosml
%patch0 -p1

%build
cd src
%{__make} \
	BINDIR=%{_bindir} \
	LIBDIR=%{_libdir}/mosml \
	INCDIR=%{_includedir}/mosml \
	TOOLDIR=%{_libdir}/mosml/tools \
	MOSMLHOME=%{_prefix}/mosml \
	world

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/mosml

cd src
%{__make} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mosml \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/mosml \
	TOOLDIR=$RPM_BUILD_ROOT%{_libdir}/mosml/tools \
	MOSMLHOME=$RPM_BUILD_ROOT%{_prefix}/mosml \
	install

perl -pi -e "s/\.\.\/config\///" $RPM_BUILD_ROOT%{_includedir}/mosml/config.h

cd dynlibs
%{__make} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mosml \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/mosml \
	TOOLDIR=$RPM_BUILD_ROOT%{_libdir}/mosml/tools \
	MOSMLHOME=$RPM_BUILD_ROOT%{_prefix}/mosml

%{__make} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mosml \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/mosml \
	TOOLDIR=$RPM_BUILD_ROOT%{_libdir}/mosml/tools \
	MOSMLHOME=$RPM_BUILD_ROOT%{_prefix}/mosml \
	install
cd ../..

cp -a tools/Makefile.stub $RPM_BUILD_ROOT%{_libdir}/mosml/tools
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/mosml/

mv -f $RPM_BUILD_ROOT%{_libdir}/mosml/*.so $RPM_BUILD_ROOT%{_libdir}
ln -sf ../../bin/camlrunm $RPM_BUILD_ROOT%{_libdir}/mosml/camlrunm

gzip -9nf README copyrght/* doc/* src/doc/*.pdf
mv -f src/doc/helpsigs/htmlsigs src/doc/helpsigs/mosmllib

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.gz copyrght/*.gz doc/*.gz
%doc src/doc/*.gz src/doc/helpsigs/mosmllib
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libm*.so
%{_libdir}/mosml
%{_includedir}/mosml
%{_examplesdir}/mosml
