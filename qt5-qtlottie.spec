%ifarch %{armx}
%define build_docs 0
%else
%define build_docs 1
%endif

%define rel 1
%define beta %{nil}
%define qtmajor %(echo %{version} |cut -d. -f1)

%define libqtbodymovin   %mklibname qt5bodymovin %qtmajor
%define libqtbodymovin_d %mklibname qt5bodymovin -d

Name:           qt5-qtlottie
Version:        5.15.3
%if "%{beta}" != ""
%define qttarballdir qtlottie-everywhere-src-%{version}-%{beta}
Release:	0.%{beta}.1
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
%define qttarballdir qtlottie-everywhere-opensource-src-%{version}
Release:        2
Source0:        http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
# From KDE
# [currently no patches required]
Summary:        Qt%{qtmajor} Lottie
Group:          Development/KDE and Qt
License:        LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:            https://www.qt.io/
BuildRequires:  qt5-qtbase-devel 
BuildRequires:	qt5-qtbase-doc
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)

%description
Qt%{qtmajor} Lottie is a family of player software for a certain
json-based file format for describing 2d vector graphics animations.

%files
%{_qt5_libdir}/qt5/qml/Qt/labs/lottieqt/

#------------------------------------------------------------------------------

%if %{build_docs}
%package        doc
Summary:        QtLottie%{qtmajor} APIs and tools docs
Group:          Documentation
BuildArch:      noarch
BuildRequires:  qt5-assistant
BuildRequires:  qdoc5
# This one is required to build QCH-format documentation
# for APIs and tools in this package set
BuildRequires:  qt5-qttools
Recommends:     qt5-qttools

%description doc
Documentation for APIs and tools in QtLottie%{qtmajor} package for
use with Qt Assistant.

%files doc
%{_qt5_docdir}/qtlottieanimation.qch
%{_qt5_docdir}/qtlottieanimation/
%endif

#------------------------------------------------------------------------------

%package -n     %{libqtbodymovin}
Summary:        Qt%{qtmajor} Bodymovin Component Library
Group:          System/Libraries
Requires:       %{name} >= %{version}-%{release}

%description -n %{libqtbodymovin}
Qt%{qtmajor} Bodymovin Component Library.

%files -n %{libqtbodymovin}
%{_qt5_libdir}/libQt5Bodymovin.so.*

#------------------------------------------------------------------------------

%package -n     %{libqtbodymovin_d}
Summary:        Devel files needed to build apps based on QtBodymovin
Group:          Development/KDE and Qt
Requires:       %{libqtbodymovin} = %{version}
Provides:       libqt5bodymovin-devel = %{version}
Provides:       libqtbodymovin5-devel = %{version}
Provides:       qt5bodymovin-devel = %{version}
Provides:       libqt5lottie-devel = %{version}
Provides:       libqtlottie5-devel = %{version}
Provides:       qt5lottie-devel = %{version}

%description -n %{libqtbodymovin_d}
Devel files needed to build apps based on Qt Bodymovin.

%files -n %{libqtbodymovin_d}
%{_qt5_includedir}/QtBodymovin/
%{_qt5_libdir}/qt5/mkspecs/modules/qt_lib_bodymovin_private.pri
%{_qt5_libdir}/libQt5Bodymovin.prl
%{_qt5_libdir}/libQt5Bodymovin.so
%{_libdir}/cmake/Qt5Bodymovin

#------------------------------------------------------------------------------

%prep
%autosetup -p1 -n %(echo %{qttarballdir}|sed -e 's,-opensource,,')
%{_libdir}/qt5/bin/syncqt.pl -version %{version}

%build
%qmake_qt5
%make_build

%if %{build_docs}
%__make docs
%endif

%install
%make_install INSTALL_ROOT=%{buildroot}

%if %{build_docs}
%make_install install_docs INSTALL_ROOT=%{buildroot}
%endif
