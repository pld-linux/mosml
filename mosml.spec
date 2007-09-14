Summary:	Moscow ML - Standard ML implementation
Summary(pl.UTF-8):	Moscow ML - implementacja języka Standard ML
Name:		mosml
Version:	2.01
Release:	8
License:	GPL
Group:		Development/Languages
Source0:	http://www.dina.kvl.dk/~sestoft/mosml/mos201src.tar.gz
# Source0-md5:	74aaaf988201fe92a9dbfbcb1e646f70
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-no-static-pq.patch
Patch2:		%{name}-dynamic-gd.patch
Patch3:		%{name}-dynamic-gdbm.patch
Patch4:		%{name}-mmysql.patch
Patch5:		%{name}-msocket.patch
URL:		http://www.dina.kvl.dk/~sestoft/mosml.html
BuildRequires:	gd-devel
BuildRequires:	gdbm-devel
BuildRequires:	mysql-devel
BuildRequires:	perl-base
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Moscow ML provides a light-weight implementation of full Standard ML,
including Modules and some extensions. Standard ML is a strict
functional language widely used in teaching and research.

Moscow ML is based on the Caml Light system, which gives fast
compilation and modest storage consumption.

%description -l pl.UTF-8
Moscow ML udostępnia zgrabną implementację pełnego Standard MLa,
włączając w to moduły i niektóre rozszerzenia. Standard ML jest ściśle
funkcyjnym językiem, szeroko używanym w nauczaniu i badaniach
naukowych.

Moscow ML jest oparty na Caml Light, co daje w efekcie szybką
kompilację i przyzwoitą objętość kodu.

%package gd
Summary:	MoscowML bindings for gd library
Summary(pl.UTF-8):	Wiązania MoscowML-a dla biblioteki gd
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description gd
MoscowML bindings for gd library.

%description gd -l pl.UTF-8
Wiązania MoscowML-a do biblioteki gd.

%package gdbm
Summary:	MoscowML bindings for gdbm library
Summary(pl.UTF-8):	Wiązania MoscowML-a dla biblioteki gdbm
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description gdbm
MoscowML bindings for gdbm library.

%description gdbm -l pl.UTF-8
Wiązania MoscowML-a do biblioteki gdbm.

%package pq
Summary:	MoscowML libraries for Posgresql
Summary(pl.UTF-8):	Biblioteki MoscowML-a do Postgresql
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description pq
MoscowML libraries for Posgresql.

%description pq -l pl.UTF-8
Biblioteki MoscowML-a do Postgresql.

%package mysql
Summary:	MoscowML libraries for Mysql
Summary(pl.UTF-8):	Biblioteki MoscowML-a do Mysql
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description mysql
MoscowML libraries for Mysql.

%description mysql -l pl.UTF-8
Biblioteki MoscowML-a do Mysql.

%package doc
Summary:	MoscowML pdf documentation
Summary(pl.UTF-8):	Dokumentacja dla MoscowML w formacie pdf
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description doc
MoscowML pdf documentation.

%description doc -l pl.UTF-8
Dokumentacja dla MoscowML w formacie pdf.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} -C src world \
	BINDIR=%{_bindir} \
	LIBDIR=%{_libdir}/mosml \
	INCDIR=%{_includedir}/mosml \
	TOOLDIR=%{_libdir}/mosml/tools \
	OPTCFLAGS="%{rpmcflags}"

%{__make} -C src/dynlibs \
	LIBDIR=%{_libdir}/mosml \
	INCDIR=`pwd`/src/runtime \
	MYSQLLIBDIR=%{_libdir}/mysql \
	MYSQLINCDIR=%{_includedir}/mysql \
	PGSQLLIBDIR=%{_libdir} \
	PGSQLINCDIR=%{_includedir}/postgresql \
	OPTCFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/mosml

%{__make} -C src install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mosml \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/mosml \
	TOOLDIR=$RPM_BUILD_ROOT%{_libdir}/mosml/tools \
	MOSMLHOME=$RPM_BUILD_ROOT%{_prefix}/mosml

%{__make} -C src/dynlibs install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/mosml \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/mosml \
	TOOLDIR=$RPM_BUILD_ROOT%{_libdir}/mosml/tools \
	MOSMLHOME=$RPM_BUILD_ROOT%{_prefix}/mosml

echo '#!/usr/bin/camlrunm' > $RPM_BUILD_ROOT%{_libdir}/mosml/header

cp -a tools/Makefile.stub $RPM_BUILD_ROOT%{_libdir}/mosml/tools
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/mosml/
ln -sf ../../bin/camlrunm $RPM_BUILD_ROOT%{_libdir}/mosml/camlrunm

mv -f src/doc/helpsigs/htmlsigs src/doc/helpsigs/mosmllib
mv -f src/doc/helpsigs/index.html src/doc/helpsigs/mosmllib

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README copyrght/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/mosml
%attr(755,root,root) %{_libdir}/mosml/libmregex.so
%attr(755,root,root) %{_libdir}/mosml/libmunix.so
%attr(755,root,root) %{_libdir}/mosml/libmsocket.so
%{_libdir}/mosml/*.sig
%{_libdir}/mosml/*.ui
%{_libdir}/mosml/*.uo
%{_libdir}/mosml/camlrunm
%{_libdir}/mosml/header
%{_libdir}/mosml/helpsigs.val
%{_libdir}/mosml/mosml*
%{_libdir}/mosml/tools
%{_includedir}/mosml
%{_examplesdir}/mosml

%files pq
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mosml/libmpq.so

%files gd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mosml/libmgd.so

%files gdbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mosml/libmgdbm.so

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mosml/libmmysql.so

%files doc
%defattr(644,root,root,755)
%doc src/doc/*.pdf src/doc/helpsigs/mosmllib
