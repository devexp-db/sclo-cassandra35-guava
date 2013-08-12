Name:          guava
Version:       13.0
Release:       6%{?dist}
Summary:       Google Core Libraries for Java
License:       ASL 2.0 
URL:           http://code.google.com/p/guava-libraries
# git clone https://code.google.com/p/guava-libraries/
# (cd ./guava-libraries && git archive --format=tar --prefix=guava-%{version}/ v%{version}) | xz >guava-%{version}.tar.xz
Source0:       %{name}-%{version}.tar.xz

BuildRequires: java-devel >= 0:1.7.0
BuildRequires: mvn(org.sonatype.oss:oss-parent)

BuildRequires: maven-local
BuildRequires: maven-dependency-plugin

BuildRequires: mvn(com.google.code.findbugs:jsr305) >= 0-0.6.20090319svn
BuildRequires: ant

BuildArch:     noarch

%description
Guava is a suite of core and expanded libraries that include 
utility classes, Google's collections, io classes, and much 
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
find . -name '*.jar' -delete

%pom_disable_module guava-gwt
%pom_disable_module guava-testlib
%pom_disable_module guava-tests
%pom_remove_plugin :animal-sniffer-maven-plugin guava
%pom_remove_plugin :maven-gpg-plugin

%build

%mvn_file :%{name} %{name}
%mvn_alias :%{name} "com.google.collections:google-collections"
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc AUTHORS CONTRIBUTORS COPYING README*

%files javadoc -f .mfiles-javadoc
%doc COPYING

%changelog
* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 13.0-6
- fix rhbz#992456
- update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Replace BR on ant-nodeps with ant

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 13.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-1
- Update to upstream version 13.0
- Remove RPM bug workaround
- Convert patches to pom macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 gil cattaneo <puntogil@libero.it> 11.0.2-1
- Update to 11.0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 09-1
- Update to 09
- Packaging fixes
- Build with maven

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Hui wang <huwang@redhat.com> - 05-4
- Patch pom

* Fri Jun 18 2010 Hui Wang <huwang@redhat.com> - 05-3
- Fixed jar name in install section
- Removed spaces in description

* Thu Jun 17 2010 Hui Wang <huwang@redhat.com> - 05-2
- Fixed summary
- Fixed description
- Fixed creating symlink insturctions
- add depmap

* Thu Jun 10 2010 Hui Wang <huwang@redhat.com> - 05-1
- Initial version of the package
