Name:           guava
Version:        09
Release:        2%{?dist}
Summary:        Google Core Libraries for Java

Group:          Development/Libraries
License:        ASL 2.0 
URL:            http://code.google.com/p/guava-libraries
#svn export http://guava-libraries.googlecode.com/svn/tags/release05/ guava-r05
#tar jcf guava-r05.tar.bz2 guava-r05/
Source0:        %{name}-r%{version}.tar.bz2
#Remove parent definition which doesn't really to be used
Patch0:        %{name}-pom.patch

BuildArch: noarch

BuildRequires:  maven
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  java-devel >= 0:1.7.0
BuildRequires:  jpackage-utils
BuildRequires:  jsr-305 >= 0-0.7.20090319svn
BuildRequires:  ant-nodeps

Requires:       java
Requires:       jpackage-utils

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
%setup -q -n %{name}-r%{version}

rm -r lib/* gwt-*

%patch0 -p1


%build

mvn-rpmbuild install javadoc:aggregate

%install

# jars
install -Dpm 644 target/guava-r%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom


%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "com.google.collections:google-collections"

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/

%pre javadoc
# workaround for rpm bug 646523 (can be removed in F-18)
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%doc COPYING README README.maven
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
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
