Name:          guava
Version:       11.0.2
Release:       2%{?dist}
Summary:       Google Core Libraries for Java

Group:         Development/Libraries
License:       ASL 2.0 
URL:           http://code.google.com/p/guava-libraries
# git clone https://code.google.com/p/guava-libraries/
# cd guava-libraries && git archive --format=tar --prefix=guava-11.0.2/ v11.0.2 | xz > guava-11.0.2.tar.xz
Source0:       %{name}-%{version}.tar.xz
Patch0:        guava-11.0.2-remove-animal-sniffer.patch

BuildRequires: java-devel >= 0:1.7.0
BuildRequires: jpackage-utils
BuildRequires: sonatype-oss-parent

BuildRequires: maven
BuildRequires: maven-compiler-plugin
BuildRequires: maven-dependency-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-provider-junit4
#BuildRequires: animal-sniffer
#BuildRequires: mojo-signatures

BuildRequires: jsr-305 >= 0-0.6.20090319svn
BuildRequires: ant-nodeps
BuildRequires: jdiff

Requires:      jsr-305

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
Guava is a suite of core and expanded libraries that include 
utility classes, Google's collections, io classes, and much 
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
find . -name '*.jar' -delete

# guava/lib/jdiff.jar
ln -sf $(build-classpath jdiff) guava/lib/jdiff.jar

%patch0 -p0

sed -i "s|<module>guava-gwt</module>|<!--module>guava-gwt</module-->|" pom.xml
sed -i "s|<module>guava-testlib</module>|<!--module>guava-testlib</module-->|" pom.xml
sed -i "s|<module>guava-tests</module>|<!--module>guava-tests</module-->|" pom.xml

%build

mvn-rpmbuild install javadoc:aggregate

%install

# jars
mkdir -p %{buildroot}%{_javadir}
install -pm 644 %{name}/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -pm 644 %{name}-bootstrap/target/%{name}-bootstrap-%{version}.jar %{buildroot}%{_javadir}/guava-bootstrap.jar

# poms
mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-parent.pom
%add_maven_depmap JPP-%{name}-parent.pom
install -pm 644 %{name}/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "com.google.collections:google-collections"
install -pm 644 %{name}-bootstrap/pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}-bootstrap.pom
%add_maven_depmap JPP-%{name}-bootstrap.pom %{name}-bootstrap.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/

%pre javadoc
# workaround for rpm bug 646523 (can be removed in F-18)
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%doc AUTHORS CONTRIBUTORS COPYING README*
%{_javadir}/%{name}*.jar
%{_mavenpomdir}/JPP-%{name}*.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}
%doc COPYING

%changelog
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
