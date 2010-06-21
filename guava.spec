Name:           guava
Version:        05
Release:        3%{?dist}
Summary:        Google Core Libraries for Java

Group:          Development/Libraries
License:        ASL 2.0 
URL:            http://code.google.com/p/guava-libraries
#svn export http://guava-libraries.googlecode.com/svn/tags/release05/ guava-r05
#tar jcf guava-r05.tar.bz2 guava-r05/
Source0:        %{name}-r%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires:  ant
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  jsr-305
BuildRequires:  ant-nodeps

Requires:       java
Requires:       jpackage-utils

Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

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

sed -i "s/jsr305.jar/jsr-305.jar/" build.xml

%build
rm lib/* -r
build-jar-repository -s -p lib jsr-305

ant -Drelease=%{version} -Djava5home=%{_jvmdir} dist

%install
rm -rf %{buildroot}

# jars
install -Dpm 644 build/dist/guava-r%{version}/%{name}-r%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap com.google.guava %{name} %{version} JPP %{name}
%add_to_maven_depmap com.google.collections google-collections 1.0 JPP %{name}

# poms
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf build/javadoc/*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README README.maven
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
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