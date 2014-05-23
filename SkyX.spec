Name:           SkyX
Version:        0.4
Release:        5%{?dist}
Summary:        Photo-realistic sky simulator

License:        LGPLv2+
URL:            http://www.paradise-studios.net/?page_id=183
Source0:        http://modclub.rigsofrods.com/xavi/SkyX/SkyX-v0.4.rar
Source1:        http://modclub.rigsofrods.com/xavi/SkyX/SkyX-v0.3_CMake.rar
# This patch contains some modifications made by the Gazebo project.
# It is mostly comment changes, but there are some API extensions needed
# by the gazebo robot simulator.
Patch0:         skyx_gazebo.patch

BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  ogre-devel
BuildRequires:  ois-devel
BuildRequires:  dos2unix
BuildRequires:  unar

%description
SkyX is a photo-realistic, simple and fast sky simulator.  It can be used
with the OGRE engine.

%package devel
Summary: Development files and libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -T -c
unar %{SOURCE0}
mv SkyX-v0.4/* .
unar %{SOURCE1}
cp -r SkyX-v0.3/* .
rm -rf SkyX-v0.*
rm -f SkyXCommon/Bin/Media/packs/OgreCore.zip

%patch0 -p1

# Remove Windows line endings
dos2unix Readme.txt License.txt
# Convert to UTF8
iconv -f ISO-8859-15 -t UTF-8 License.txt > License.conv && mv -f License.{conv,txt}
iconv -f ISO-8859-15 -t UTF-8 Readme.txt > Readme.conv && mv -f Readme.{conv,txt}

%build
mkdir build
cd build
%cmake .. \
  -DSKYX_BUILD_SAMPLES=OFF 
make %{?_smp_mflags}


%install
make -C build install DESTDIR=%{buildroot}
mv %{buildroot}/SKYX/cmake %{buildroot}%{_datadir}/SKYX
%if %{_lib} == "lib64"
mv %{buildroot}/%{_usr}/lib %{buildroot}%{_libdir}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc License.txt Readme.txt
%{_libdir}/*.so.*
%exclude %{_datadir}/SKYX/cmake
%{_datadir}/SKYX

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/SKYX
%{_datadir}/SKYX/cmake

%changelog
* Sat May 24 2014 Petr Machata <pmachata@redhat.com> - 0.4-5
- Rebuild for boost 1.55.0

* Sun Oct 20 2013 Rich Mattes <richmattes@gmail.com> - 0.4-4
- Fix build on i686 systems
- Correct project URL
- Correct license field (License.txt indicates LGPLv2+)

* Sun Oct 06 2013 Rich Mattes <richmattes@gmail.com> - 0.4-3
- Added patch containing Gazebo extensions

* Tue Aug 06 2013 Rich Mattes <richmattes@gmail.com> - 0.4-2
- Use upstream sources and unar

* Sun Jun 09 2013 Rich Mattes <richmattes@gmail.com> - 0.4-1
- Update to release 0.4

* Sun Jun 09 2013 Rich Mattes <richmattes@gmail.com> - 0.3.1-1
- Initial release
