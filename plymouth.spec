%define plymouthdaemon_execdir /sbin
%define plymouthclient_execdir /bin
%define plymouth_libdir /%{_lib}
%define _default_patch_fuzz 999

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.8.3
Release: 17%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2
Source1: boot-duration
Source2: plymouth-update-initrd
Source3: rings.plymouth

URL: http://freedesktop.org/software/plymouth/releases
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: system-logos
Requires(post): plymouth-scripts
Requires: initscripts >= 8.83-1

BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libdrm_intel)
BuildRequires: pkgconfig(libdrm_radeon)
BuildRequires: pkgconfig(libdrm_nouveau)
BuildRequires: kernel-headers

Obsoletes: plymouth-text-and-details-only < %{version}-%{release}
Obsoletes: plymouth-plugin-pulser < 0.7.0-0.2009.05.08.2
Obsoletes: plymouth-theme-pulser < 0.7.0-0.2009.05.08.2

Patch0: return-text.patch
Patch1: tty-fix.patch
Patch2: fix-assertion-on-shutdown.patch
Patch3: fix-throbber-glitch.patch
Patch4: use-monospace-font.patch
Patch5: add-window-icon.patch
Patch6: fix-watch-keystroke.patch

# The next three make plymouthd work better on s390
# https://bugzilla.redhat.com/show_bug.cgi?id=606376
Patch7: force-enter-to-output-newline.patch
Patch8: fix-stair-stepping.patch
Patch9: better-tty-fallback.patch
Patch10: fix-exit-crash-with-details.patch
Patch11: build-details-in.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=615912
Patch12: filter-out-duplicate-consoles.patch
Patch99: plymouth-0.8.0-everything-is-better-in-red.patch

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package system-theme
Summary: Plymouth default theme
BuildArch: noarch
Group: System Environment/Base
Obsoletes: rhgb < 1:10.0.0
Provides: rhgb = 1:10.0.0
Obsoletes: %{name}-system-plugin <  %{version}-%{release}
Provides: %{name}-system-plugin = %{version}-%{release}
Provides: rhgb = 1:10.0.0
Requires: plymouth(system-theme) = %{version}-%{release}

%description system-theme
This metapackage tracks the current distribution default theme.

%package core-libs
Summary: Plymouth core libraries
Summary: Plymouth libraries
Group: Development/Libraries

%description core-libs
This package contains the libply and libply-splash-core libraries
used by Plymouth.

%package graphics-libs
Summary: Plymouth graphics libraries
Group: Development/Libraries
Requires: %{name}-core-libs = %{version}-%{release}
Obsoletes: %{name}-libs < %{version}-%{release}
Provides: %{name}-libs = %{version}-%{release}
BuildRequires: libpng-devel

%description graphics-libs
This package contains the libply-splash-graphics library
used by graphical Plymouth splashes.

%package devel
Summary: Libraries and headers for writing Plymouth splash plugins
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%package utils
Summary: Plymouth related utilities
Group: Applications/System
Requires: %{name} = %{version}-%{release}
BuildRequires: gtk2-devel

%description utils
This package contains utilities that integrate with Plymouth
including a boot log viewing application.

%package scripts
Summary: Plymouth related scripts
Group: Applications/System
Requires: sed, gawk, grep, coreutils

%description scripts
This package contains scripts that help integrate Plymouth with
the system.

%package gdm-hooks
Summary: Plymouth GDM integration
Group: Applications/System
Requires: gdm >= 1:2.22.0
Requires: plymouth-utils
Requires: %{name} = %{version}-%{release}

%description gdm-hooks
This package contains support files for integrating Plymouth with GDM
Namely, it adds hooks to show boot messages at the login screen in the
event start-up services fail.

%package plugin-label
Summary: Plymouth label plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: pango-devel >= 1.21.0
BuildRequires: cairo-devel

%description plugin-label
This package contains the label control plugin for
Plymouth. It provides the ability to render text on
graphical boot splashes using pango and cairo.

%package plugin-fade-throbber
Summary: Plymouth "Fade-Throbber" plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}

%description plugin-fade-throbber
This package contains the "Fade-In" boot splash plugin for
Plymouth. It features a centered image that fades in and out
while other images pulsate around during system boot up.

%package theme-fade-in
Summary: Plymouth "Fade-In" theme
Group: System Environment/Base
BuildArch: noarch
Requires: %{name}-plugin-fade-throbber = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme
Obsoletes: plymouth-plugin-fade-in < 0.7.0-0.2009.05.08.2
Provides: plymouth-plugin-fade-in = 0.7.0-0.2009.05.08.2

%description theme-fade-in
This package contains the "Fade-In" boot splash theme for
Plymouth. It features a centered logo that fades in and out
while stars twinkle around the logo during system boot up.

%package plugin-throbgress
Summary: Plymouth "Throbgress" plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-throbgress
This package contains the "throbgress" boot splash plugin for
Plymouth. It features a centered logo and animated spinner that
spins repeatedly while a progress bar advances at the bottom of
the screen.

%package theme-spinfinity
Summary: Plymouth "Spinfinity" theme
Group: System Environment/Base
BuildArch: noarch
Requires: %{name}-plugin-throbgress = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme
Obsoletes: plymouth-plugin-spinfinity < 0.7.0-0.2009.05.08.2
Provides: plymouth-plugin-spinfinity = 0.7.0-0.2009.05.08.2

%description theme-spinfinity
This package contains the "Spinfinity" boot splash theme for
Plymouth. It features a centered logo and animated spinner that
spins in the shape of an infinity sign.

%package plugin-space-flares
Summary: Plymouth "space-flares" plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-space-flares
This package contains the "space-flares" boot splash plugin for
Plymouth. It features a corner image with animated flares.

%package theme-solar
Summary: Plymouth "Solar" theme
Group: System Environment/Base
BuildArch: noarch
Requires: %{name}-plugin-space-flares = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme
Obsoletes: plymouth-plugin-solar < 0.7.0-0.2009.05.08.2
Provides: plymouth-plugin-solar = 0.7.0-0.2009.05.08.2

%description theme-solar
This package contains the "Solar" boot splash theme for
Plymouth. It features a blue flamed sun with animated solar flares.

%package plugin-two-step
Summary: Plymouth "two-step" plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
Requires: plymouth-plugin-label

%description plugin-two-step
This package contains the "two-step" boot splash plugin for
Plymouth. It features a two phased boot process that starts with
a progressing animation synced to boot time and finishes with a
short, fast one-shot animation.

%package theme-rings
Summary: Plymouth "Rings" plugin
Group: System Environment/Base
BuildArch: noarch
Requires: %{name}-plugin-two-step = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme
Provides: plymouth(system-theme) = %{version}-%{release}
Obsoletes: %{name}-theme-charge < %{version}-%{release}
Obsoletes: %{name}-theme-glow < %{version}-%{release}

%description theme-rings
This package contains the "rings" boot splash theme for
Plymouth. It features a large header, and slick spinner
concentric with a circular progress indicator.

%package plugin-script
Summary: Plymouth "script" plugin
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}

%description plugin-script
This package contains the "script" boot splash plugin for
Plymouth. It features an extensible, scriptable boot splash
language that simplifies the process of designing custom
boot splash themes.

%package theme-script
Summary: Plymouth "Script" plugin
Group: System Environment/Base
BuildArch: noarch
Requires: %{name}-plugin-script = %{version}-%{release}
Requires(post): %{_sbindir}/plymouth-set-default-theme

%description theme-script
This package contains the "script" boot splash theme for
Plymouth. It it is a simple example theme the uses the "script"
plugin.

%prep
%setup -q

%patch0 -p1 -b .return-text
%patch1 -p1 -b .tty-fix
%patch2 -p1 -b .tty-assertion-on-shutdown
%patch3 -p1 -b .fix-throbber-glitch
%patch4 -p1 -b .use-monospace-font
%patch5 -p1 -b .add-window-icon
%patch6 -p1 -b .fix-watch-keystroke
%patch7 -p1 -b .force-enter-to-output-newline.patch
%patch8 -p1 -b .fix-stair-stepping.patch
%patch9 -p1 -b .better-tty-fallback.patch
%patch10 -p1 -b .fix-exit-crash-with-details
%patch11 -p1 -b .build-details-in
%patch12 -p1 -b .filter-out-duplicate-consoles
%patch99 -p1 -b .red

# Change the default theme
sed -i -e 's/fade-in/rings/g' src/plymouthd.defaults

# fix up the man page (bug #592305)
iconv -f latin1 -t utf8 docs/plymouth.8 -o docs/plymouth.8.new && mv docs/plymouth.8{.new,}

%build
%configure --enable-tracing --disable-tests                      \
           --with-logo=%{_datadir}/pixmaps/system-logo-white.png \
           --with-background-start-color-stop=0xCC0000           \
           --with-background-end-color-stop=0x700000             \
           --with-background-color=0x500000                      \
           --enable-gdm-transition                               \
           --with-system-root-install                            \
           --with-rhgb-compat-link

make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

# Temporary symlink until rc.sysinit is fixed
(cd $RPM_BUILD_ROOT%{_bindir}; ln -s ../../bin/plymouth)

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth
cp $RPM_SOURCE_DIR/boot-duration $RPM_BUILD_ROOT%{_datadir}/plymouth/default-boot-duration
cp $RPM_SOURCE_DIR/boot-duration $RPM_BUILD_ROOT%{_localstatedir}/lib/plymouth

# Add rings, our distro default
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/rings
cp $RPM_SOURCE_DIR/rings.plymouth $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/rings
cp $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow/{box,bullet,entry,lock}.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/rings

# Remove glow theme
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow

# Override plymouth-update-initrd to work dracut or mkinitrd
cp -f $RPM_SOURCE_DIR/plymouth-update-initrd $RPM_BUILD_ROOT%{_libexecdir}/plymouth/plymouth-update-initrd

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -f %{_localstatedir}/lib/plymouth/boot-duration ] || cp -f %{_datadir}/plymouth/default-boot-duration %{_localstatedir}/lib/plymouth/boot-duration

%postun
if [ $1 -eq 0 ]; then
    rm -f /boot/initrd-plymouth.img
fi

%post core-libs -p /sbin/ldconfig
%postun core-libs -p /sbin/ldconfig

%post graphics-libs -p /sbin/ldconfig
%postun graphics-libs -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth/renderers
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_bindir}/rhgb-client
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*
%{_datadir}/plymouth/default-boot-duration
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%{_mandir}/man?/*
%ghost %{_localstatedir}/lib/plymouth/boot-duration

%files devel
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{plymouth_libdir}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/pkgconfig/ply-splash-core.pc
%{_libdir}/pkgconfig/ply-splash-graphics.pc
%{_libdir}/pkgconfig/ply-boot-client.pc
%{_libdir}/plymouth/renderers/x11*
%{_includedir}/plymouth-1

%files core-libs
%defattr(-, root, root)
%{plymouth_libdir}/libply.so.*
%{plymouth_libdir}/libply-splash-core.so.*
%{_libdir}/libply-boot-client.so.*
%dir %{_libdir}/plymouth

%files graphics-libs
%defattr(-, root, root)
%{_libdir}/libply-splash-graphics.so.*

%files scripts
%defattr(-, root, root)
%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-generate-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd

%files utils
%defattr(-, root, root)
%{_bindir}/plymouth-log-viewer

%files gdm-hooks
%defattr(-, root, root)
%{_datadir}/gdm/autostart/LoginWindow/plymouth-log-viewer.desktop

%files plugin-label
%defattr(-, root, root)
%{_libdir}/plymouth/label.so

%files plugin-fade-throbber
%defattr(-, root, root)
%{_libdir}/plymouth/fade-throbber.so

%files theme-fade-in
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/fade-in
%{_datadir}/plymouth/themes/fade-in/bullet.png
%{_datadir}/plymouth/themes/fade-in/entry.png
%{_datadir}/plymouth/themes/fade-in/lock.png
%{_datadir}/plymouth/themes/fade-in/star.png
%{_datadir}/plymouth/themes/fade-in/fade-in.plymouth

%files plugin-throbgress
%defattr(-, root, root)
%{_libdir}/plymouth/throbgress.so

%files theme-spinfinity
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/spinfinity
%{_datadir}/plymouth/themes/spinfinity/box.png
%{_datadir}/plymouth/themes/spinfinity/bullet.png
%{_datadir}/plymouth/themes/spinfinity/entry.png
%{_datadir}/plymouth/themes/spinfinity/lock.png
%{_datadir}/plymouth/themes/spinfinity/throbber-[0-3][0-9].png
%{_datadir}/plymouth/themes/spinfinity/spinfinity.plymouth

%files plugin-space-flares
%defattr(-, root, root)
%{_libdir}/plymouth/space-flares.so

%files theme-solar
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/solar
%{_datadir}/plymouth/themes/solar/*.png
%{_datadir}/plymouth/themes/solar/solar.plymouth

%files plugin-two-step
%defattr(-, root, root)
%{_libdir}/plymouth/two-step.so

%files theme-rings
%defattr(-, root, root)
%dir %{_datadir}/plymouth/themes/rings
%{_datadir}/plymouth/themes/rings/*.png
%{_datadir}/plymouth/themes/rings/rings.plymouth

%files plugin-script
%defattr(-, root, root)
%{_libdir}/plymouth/script.so

%files theme-script
%defattr(-, root, root)
%{_datadir}/plymouth/themes/script/*.png
%{_datadir}/plymouth/themes/script/script.script
%{_datadir}/plymouth/themes/script/script.plymouth

%files system-theme
%defattr(-, root, root)

%changelog
* Mon Aug 09 2010 Ray Strode <rstrode@redhat.com> 0.8.3-17
- Rebuild plymouthd with -rdynamic so the changes introduced
  in 0.8.3-13 work
  Resolves: #612569

* Wed Aug 04 2010 Ray Strode <rstrode@redhat.com> 0.8.3-16
- Fix up problem introduced in previous patch when kernel
  command line has no consoles
  Related: #615912

* Tue Aug 03 2010 Ray Strode <rstrode@redhat.com> 0.8.3-15
- Filter out duplicate consoles from kernel command line
  Resolves: #615912

* Mon Aug 02 2010 Ray Strode <rstrode@redhat.com> 0.8.3-14
- Use dark gray instead of black background in rings theme
  to prevent monitor sync issues on some hardware.
  Resolves: #620414

* Tue Jul 27 2010 Ray Strode <rstrode@redhat.com> 0.8.3-13
- Built details plugin into binary, so there's always
  some splash available (fixes crash for users with
  separate /usr hitting escape early in boot up)
  Resolves: #612569

* Fri Jul 16 2010 Ray Strode <rstrode@redhat.com> 0.8.3-12
- Drop glow theme
  Resolves: #615251

* Thu Jul 01 2010 Ray Strode <rstrode@redhat.com> 0.8.3-11
- Fix occassional crash on exit when using details plugin
  Resolves: #596791

* Wed Jun 30 2010 Ray Strode <rstrode@redhat.com> 0.8.3-10
- Make work better with big iron
  Resolves: #606376

* Wed Jun 30 2010 Ray Strode <rstrode@redhat.com> 0.8.3-9
- Make watch-keystroke work better
  Related: #605016

* Wed Jun 30 2010 Ray Strode <rstrode@redhat.com> 0.8.3-8
- Use monospace font in plymouth log viewer
  Resolves: #596332
- Add window icon in plymouth log viewer
  Resolves: #605626

* Fri Jun 18 2010 Ray Strode <rstrode@redhat.com> 0.8.3-7
- Make themes noarch
  Resolves: #605509

* Thu Jun 17 2010 Ray Strode <rstrode@redhat.com> 0.8.3-6
- Fix throbber glitch after hitting escape twice
  Resolves: #598448

* Fri Jun 11 2010 Ray Strode <rstrode@redhat.com> 0.8.3-5
- Add some extra requires
  Resolves: #593061

* Wed Jun 09 2010 Ray Strode <rstrode@redhat.com> 0.8.3-4
- Don't blow up on shutdown
  Resolves: #601745

* Fri May 14 2010 Ray Strode <rstrode@redhat.com> 0.8.3-3
- Don't fail if distro default theme isn't installed
  Resolves: #582989

* Fri May 14 2010 Ray Strode <rstrode@redhat.com> 0.8.3-2
- Fix lock tty patch from 0.8.2-2 to properly unlock tty
  Resolves: #590774
- Fix up pkgwrangler niggles
  Resolves: 592305

* Thu May 06 2010 Ray Strode <rstrode@redhat.com> 0.8.3-1
- Add new "rings" theme
- Drop "charge" theme
  Resolves: #558608

* Fri Apr 16 2010 Ray Strode <rstrode@redhat.com> 0.8.2-3
- Don't fail if distro default theme isn't installed
  Resolves: #582989

* Wed Apr 14 2010 Ray Strode <rstrode@redhat.com> 0.8.2-2
- Lock tty into raw mode, so other apps can't muck with it
  Resolves: #582265

* Tue Apr 13 2010 Ray Strode <rstrode@redhat.com> 0.8.2-1
- Update to 0.8.2
  Resolves: #558610

* Thu Apr 01 2010 Ray Strode <rstrode@redhat.com> 0.8.1-2
Resolves: #578157
- Fix assertion failure

* Tue Mar 23 2010 Ray Strode <rstrode@redhat.com> 0.8.1-1
Resolves: #558610
- Update to 0.8.1

* Tue Mar 23 2010 Ray Strode <rstrode@redhat.com> 0.8.0-1
Resolves: #558610
- Update to 0.8.0

* Fri Mar 05 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.03.05.1
Resolves: #568146
- Handle tty disconnects better part two.

* Thu Feb 25 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.02.25.1
Resolves: #568146
- Handle tty disconnects better

* Wed Jan 27 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.01.27.1
Resolves: #558940
- Move libply-splash-core to /lib

* Tue Jan 26 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.01.14.4
Resolves: #546307
- Work better with encrypted setups if plymouthd is unavailable

* Wed Jan 20 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.01.14.3
Resolves: #556906
- Add glow theme

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.2
Resolves: #555605
- Drop plymouth-set-default-plugin

* Thu Jan 14 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.20100114.1
Resolves: #554776
- Make it possible to do a basic plymouth installations without
  libpng

* Fri Jan 08 2010 Ray Strode <rstrode@redhat.com> 0.8.0-0.2010.01.08.1
Resolves: #553659
- Rebase to latest snapshot
- Drop upstream patches

* Wed Jan 06 2010 Dave Airlie <airlied@redhat.com> 0.8.0-0.2009.29.09.19.3
- rebuild for new libdrm radeon API

* Mon Dec 21 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.19.2
Resolves: #549097
- Drop mkinitrd dependency

* Thu Nov 19 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.0-0.2009.29.09.19.1
- Tweak theming (#510311)

* Tue Nov 10 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.19
- Force raw mode on every text draw.  This works around a bug where
  some program at startup is kicking the terminal out of raw mode.

* Wed Nov 04 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.18
- Make plymouth-update-initrd work with dracut

* Tue Nov 03 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.17
- Add nash dep for plymouth-set-default-theme

* Fri Oct 30 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.16
- Drop debug spew that snuck in

* Thu Oct 29 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.15
- Fix plymouth over ppc hyperviser console (bug 531581)

* Thu Oct 29 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.14
- Don't unlink /dev/null (bug 531740)

* Mon Oct 19 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.13
- Drop nash dep (bug 528706)

* Wed Oct 14 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.12
- Don't clear screen in text plugin immediately after displaying
  password prompt (bug 527426)

* Tue Oct 13 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.11
- Clean up terminal on exit (bug 528683 again)

* Tue Oct 13 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.10
- Fix more emergency shell horkage (for users without modesetting)
  (bug 528683)

* Fri Oct 09 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.9
- Fix frame-buffer fallback plugin
  (broken by details fix in 0.8.0-0.2009.29.09.7)

* Fri Oct 09 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.8
- Fix crash in text plugin on shutdown

* Thu Oct 08 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.7
- Fix emergency shell horkage (bug 526597)
- Fix problem with details splash not showing up (bug 527426, bug 527254)

* Wed Oct 07 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.6
- Fix the reason radeon single head users were affected.

* Wed Oct 07 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.5
- Prevent firstboot's X from crashing on radeon hardware. This should
  only affect multihead users, but for some reason it's getting some
  single head users as well.

* Tue Oct 06 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.4
- Prevent firstboot's X from crashing on intel hardware

* Mon Oct 05 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.3
- Fix crasher in text plugin after password prompt (bug 526652)
- Actually apply the patch mentioned in 2009.29.09.2

* Mon Oct  5 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.2
- Fix --show-splash after --hide-splash (bug 527299)

* Tue Sep 29 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.29.09.1
- Fix escape and ask-for-password

* Mon Sep 28 2009 Ray Strode <rstrode@redhat.com> 0.8.0-0.2009.28.09
- Add prerelease of 0.8.0 for multihead support

* Fri Sep 11 2009 Ray Strode <rstrode@redhat.com> 0.7.1-7
- Go back to blue charge background (bug 522460)

* Fri Sep 11 2009 Ray Strode <rstrode@redhat.com> 0.7.1-6
- Remove duplicate Provides: plymouth(system-theme)

* Thu Sep 10 2009 Ray Strode <rstrode@redhat.com> 0.7.1-5
- Fix set_verbose error reported by yaneti.

* Wed Sep  9 2009 Ray Strode <rstrode@redhat.com> 0.7.1-4
- Look for inst() in dracut as well as mkinitrd bash source file
- Drop plymouth initrd for now.

* Fri Aug 28 2009 Ray Strode <rstrode@redhat.com> 0.7.1-3
- Create plymouth supplementary initrd in post (bug 515589)

* Tue Aug 25 2009 Ray Strode <rstrode@redhat.com> 0.7.1-2
- Get plugin path from plymouth instead of trying
  to guess.  Should fix bug 502667

* Tue Aug 25 2009 Ray Strode <rstrode@redhat.com> 0.7.1-1
- Update to 0.7.1

* Mon Aug 24 2009 Adam Jackson <ajax@redhat.com> 0.7.0-2
- Set charge bgcolor to black. (#519052)

* Tue Aug 11 2009 Ray Strode <rstrode@redhat.com> 0.7.0-1
- Update to 0.7.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-0.2010.05.15.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.15.1
- Fix spinfinity theme to point to the right image directory
  (bug 500994)

* Thu May 14 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.14.1
- Update to new snapshot that renames plugins to fix upgrades
  somewhat (bug 499940)

* Fri May 08 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.08.1
- Add some fixes for shutdown

* Fri May 08 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.4
- Don't slow down progress updating at the end of boot

* Thu May 07 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.3
- Change colors to transition better to gdm

* Wed May 06 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.2
- Make "charge" theme require two-step plugin instead of solar (oops)

* Wed May 06 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.05.06.1
- Update to "plugin-rework" branch from git

* Wed Apr 08 2009 Jesse Keating <jkeating@redhat.com> - 0.7.0-0.2009.03.10.3
- Drop the version on system-logos requires for now, causing hell with
  other -logos providers not having the same version.

* Wed Mar 18 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.10.2
- Destroy terminal on detach (may help with bug 490965)

* Tue Mar 10 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.10.1
- Address one more issue with password handling.  It wasn't working
  well for secondary devices when using the "details" plugin.

* Mon Mar  9 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.09.1
- Attempt to address some problems with password handling in the
  0.7.0 snapshots

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06.2
- Fix set default script

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06.1
- more scriptlet changes to move from solar to spinfinity

* Fri Mar  6 2009 Ray Strode <rstrode@redhat.com> 0.7.0-0.2009.03.06
- Updated to development snapshot
- Guess progress better on second boot of persistent live images
- Drop upstream patches
- swap "solar" and "spinfinity" scriptlet behavior

* Tue Feb 24 2009 Ray Strode <rstrode@redhat.com> 0.6.0-3
- Add fix-heap-corruptor patch from master.  Problem
  spotted by Mr. McCann.

* Wed Dec 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-2
- Add patch from drop-nash branch for jeremy

* Wed Dec  3 2008 Ray Strode <rstrode@redhat.com> 0.6.0-1
- Update to 0.6.0

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> 0.6.0-0.2008.11.17.3.1
- Strip %%name from %%summary

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.3
- don't give error about missing default.so
- rework packaging of boot-duration to prevent .rpmnew droppings
  (bug 469752)

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.2
- Don't tell gdm to transition unless booting into runlevel 3
  (bug 471785)

* Mon Nov 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.17.1
- Crawl progress bar if boot is way off course (Charlie, bug 471089)

* Fri Nov 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.14.2
- Don't loop forever when tty returns NUL byte (bug 471498)

* Fri Nov 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.14.1
- Generate solar background dynamically to reduce ondisk size, and
  look better at various resolutions (Charlie, bug 471227)

* Thu Nov 13 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.4
- Move Obsoletes: plymouth-text-and-details-only to base package
  so people who had it installed don't end up solar on upgrade

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.3
- Redo packaging to work better with minimal installs
  (bug 471314)

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.2
- Fix plymouth-set-default-plugin to allow external $LIB

* Wed Nov 12 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.12.1
- Fix star image (Charlie, bug 471113)

* Tue Nov 11 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.11.2
- Improve solar flares (Charlie)
- redirect tty again on --show-splash
- ignore subsequent --hide-splash calls after the first one
- turn off kernel printks during boot up

* Tue Nov 11 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.11.1
- Disconnect from tty when init=/bin/bash (bug 471007)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.5
- Force the right arch when calling plymouth-set-default-plugin
  (bug 470732)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.4
- Drop comet (bug 468705)
- make boot-duration config(noreplace)

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.3
- Don't abort if no splash when root is mounted
- Actually move patches upstream

* Mon Nov 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.10.1
- Fix feedback loop with plymouth:debug
- Move patches upstream
- Improve comet animation

* Sun Nov  9 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.4
- Fix up more-debug patch to not assert with plymouth:nolog
  (bug 470569)

* Fri Nov  7 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.3
- add some more debug spew to help debug a problem jlaska is having

* Thu Nov  6 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.2
- show details plugin on --hide-splash so people can see why the splash
  got hidden.

* Thu Nov  6 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.06.1
- Don't exit on plymouth --show-splash after sulogin
- Properly retake console after that --show-splash

* Wed Nov  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.11.05.1
- reset colors on quit --retain-splash
- fix off by one in damage calculation for label

* Tue Nov  4 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.5
- Add a sample boot-duration for livecds and first time boots
  (bug 469752)

* Mon Nov  3 2008 Jeremy Katz <katzj@redhat.com> - 0.6.0-0.2008.10.30.4
- Allow pre-setting the default plugin when calling plymouth-populate-initrd

* Fri Oct 31 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.3
- Add pango minimum version to buildrequires

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.2
- Update prompt text colors to be legible on new artwork

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.30.1
- Patch from Charlie to make password screen match animation better
  (bug 468899)

* Thu Oct 30 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.8
- Fix escape at password prompt (bug 467533)

* Tue Oct 28 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.7
- Don't require /bin/plymouth before it's installed (bug 468925)

* Tue Oct 28 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.6
- Force raw mode for keyboard input with solar and fade-in
  (bug 468880)
- make sure windows get closed on exit

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.5
- Make "Solar" lock icon the same as the "Spinfinity" one.

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.4
- Make plymouth-libs own /usr/lib/plymouth (bug 458071)

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.3
- Default to "Solar" instead of "Spinfinity"

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.2
- Don't set plymouth default plugin to text in %%post

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.27.1
- Add Charlie patch to dither in lower color modes (bug 468276)

* Sun Oct 26 2008 Jeremy Katz <katzj@redhat.com> - 0.6.0-0.2008.10.24.2
- More requires changing to avoid loops (#467356)

* Fri Oct 24 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.24.1
- Add updated progress bar for solar plugin from Charlie
- Log plymouth:debug output to boot log
- Ignore sigpipe signals in daemon

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.23.2
- Bump so name of libply to hopefully force plymouth to get installed
  before kernel (or at least make plymouth-libs and plymouth get installed
  on the same side of kernel in the transaction).

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.23.1
- Add patch from Charlie to align progress bar to milestones during boot up
- force tty to be sane on exit (bug 467207)

* Thu Oct 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.3
- add empty files section for text-and-details-only so the subpackage
  shows up.

* Wed Oct 22 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.2
- add text-and-details-only subpackage so davej can uninstall
  spinfinity, pango, cairo etc from his router.

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.21.1
- Minor event loop changes
- drop upstream patches
- Charlie Brej fix for progress bar resetting when escape gets pressed

* Tue Oct 21 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.4
- Don't make plymouth-libs require plymouth (more fun with 467356)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.3
- Add initscripts requires (bug 461322)

* Mon Oct 20 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.2
- Put tty1 back in "cooked" mode when going into runlevel 3
  (bug 467207)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.17.1
- Clear screen in details plugin when it's done
- Make plymouth-update-initrd a small wrapper around mkinitrd instead
  of the broken monstrosity it was before.

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.3
- Move plymouth-set-default-plugin, plymouth-update-initrd, and
  plymouth-populate-initrd to plymouth-scripts subpackage
  (the last fix didn't actually help with bug 467356)

* Fri Oct 17 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.2
- Move plymouth-set-default-plugin to -libs (might help with bug 467356)
- Fix up requires, provides and postun scripts

* Wed Oct 15 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.15.1
- Don't free windows on --hide-splash (fix from Jeremy)

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.14.1
- Solar fixes from Charlie Brej
- Better cpu usage from Charlie

* Fri Oct 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.08.2
- Add Requires(post): nash (bug 466500)

* Wed Oct 08 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.08.1
- Rework how "console=" args done again, to hopefully fix
  bug 460565

* Mon Oct 06 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.10.06.1
- Add "Solar" plugin from Charles Brej
- Move things around so computers with separate /usr boot
  (hopefully this won't break things, but it probably will)
- Make GDM show up on vt1 for all plugins

* Tue Sep 30 2008 Jeremy Katz <katzj@redhat.com> 0.6.0-0.2008.09.25.2
- Remove mkinitrd requires to break the dep loop and ensure things
  get installed in the right order

* Thu Sep 25 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.25.1
- Add new snapshot to fold in Will Woods progress bar, and
  move ajax's splash upstream, putting the old text splash
  in a "pulser" subpackage

* Tue Sep 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.23.1
- Last snapshot was broken

* Mon Sep 22 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.22.1
- Update to latest snapshot to get better transition support

* Fri Sep 19 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.15.2
- Turn on gdm trigger for transition

* Mon Sep 15 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.15.1
- add quit command with --retain-splash option to client

* Wed Sep 10 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.10.1
- Fix text rendering for certain machines

* Mon Sep  8 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.4
- More serial console fixes (bug 460565 again)

* Fri Sep  5 2008 Bill Nottingham <notting@redhat.com> 0.6.0-0.2008.09.05.3
- make the text plugin use the system release info rather than a hardcoded 'Fedora 10'

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.2
- Try to support multiple serial consoles better
  (bug 460565)

* Fri Sep  5 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.09.05.1
- Fix some confusion with password handling in details plugin

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.27.1
- Fix another crasher for users with encrypted disks (this time in
  the text plugin, not the client)

* Wed Aug 27 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.27
- Update to latest snapshot
- Add the ability to show text prompts in graphical plugin
- Fix crasher for users with encrypted disks

* Fri Aug 23 2008 Ray Strode <rstrode@redhat.com> 0.6.0-0.2008.08.22
- Update to latest snapshot

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-20.2008.08.13
- Update previous patch to remove some assertions

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-19.2008.08.13
- add a patch that may help serial console users

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-18.2008.08.13
- add spool directory to file list

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-17.2008.08.13
- Make plymouth-gdm-hooks require plymouth-utils

* Wed Aug 13 2008 Ray Strode <rstrode@redhat.com> 0.5.0-16.2008.08.13
- Add a boot failure viewer to login screen (written by Matthias)

* Tue Aug 12 2008 Adam Jackson <ajax@redhat.com> 0.5.0-15.2008.08.08
- plymouth-0.5.0-textbar-hotness.patch: Change the text plugin to a slightly
  more traditional progress bar, to maintain the illusion of progress better
  than the eternally oscillating cylon. Note: still incomplete.

* Fri Aug  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-14.2008.08.08
- Don't require a modifiable text color map (may fix serial consoles)

* Thu Aug  7 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-13.2008.08.07
- Update to new snapshot which when combined with a new mkinitrd should
  make unlocking encrypted root partitions work again

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-12.2008.08.06
- Update to new snapshot which fixes some assertion failures in the
  client code

* Wed Aug  6 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-11.2008.08.01
- Add Requires(post): plymouth to plugins so they get plymouth-set-default-plugin (bug 458071)

* Tue Aug  5 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-10.2008.08.01
- Add plymouth dirs to file list (bug 457871)

* Fri Aug  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-9.2008.08.01
- new plymout-populate-initrd features don't work with the set -e at the
  top of it.

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.08.01
- Update to another snapshot to actually get new
  plymouth-populate-initrd features

* Thu Jul 31 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-8.2008.07.31
- Update to snapshot to get new plymouth-populate-initrd features
- Make removing rhgb use details plugin instead of exiting

* Thu Jul 31 2008 Peter Jones <pjones@redhat.com> - 0.5.0-7
- Make it a mkinitrd requires instead of a nash requires (that will
  still pull in nash, but we need mkinitrd for newer plymouth-populate-initrd)

* Wed Jul 30 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-6
- Add nash requires

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-5
- Use a new heuristic for finding libdir, since the old
  one falls over on ia64

* Wed Jul  9 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- add ctrl-r to rotate text color palette back to stock values

* Tue Jul  8 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- Fix populate script on ppc (bug 454353)

* Tue Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-2
- Pull in spinfinity by default.  This whole "figure out
  which plugin to use" set of scripts and scriptlets
  needs work.  We need to separate distro default from
  user choice.

* Thu Jul  1 2008 Ray Strode <rstrode@redhat.com> - 0.5.0-1
- Add new client "ask-for-password" command which feeds
  the user input to a program instead of standard output,
  and loops when the program returns non-zero exit status.

* Thu Jun 26 2008 Ray Strode <rstrode@redhat.com> - 0.4.5-1
- Update to version 0.4.5
- Make text plugin blue and less 80s

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-4
- Make "Password: " show up correctly in text plugin

* Wed Jun 25 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-3
- Require elfutils (bug 452797)

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-2
- Make plymouth-set-default-plugin --reset choose the latest
  installed plugin, not the earliest

* Sun Jun 22 2008 Ray Strode <rstrode@redhat.com> - 0.4.0-1
- Update to version 0.4.0
- Only run if rhgb is on kernel command line
- Make text plugin more animated

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-2
- dont go back to text mode on exit

* Mon Jun 16 2008 Ray Strode <rstrode@redhat.com> - 0.3.2-1
- Update to version 0.3.2
- show gradient in spinfinity plugin
- Drop fade out in spinfinity plugin
- fix throbber placement
- rename graphical.so to default.so

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-3
- scriplet should be preun, not postun

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-2
- Fix postun scriptlet

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.1-1
- Update to version 0.3.1
- Don't ship generated initrd scripts in tarball

* Thu Jun 12 2008 Ray Strode <rstrode@redhat.com> - 0.3.0-1
- Update to version 0.3.0
- Better plugin handling
- Better integration with mkinitrd (pending mkinitrd changes)
- random bug fixes

* Mon Jun  9 2008 Ray Strode <rstrode@redhat.com> - 0.2.0-1
- Update to version 0.2.0
- Integrate more tightly with nash (pending nash changes)
- ship libs for out of tree splash plugins
- gradient support
- random bug fixes

* Fri May 30 2008 Ray Strode <rstrode@redhat.com> - 0.1.0-1
- Initial import, version 0.1.0
