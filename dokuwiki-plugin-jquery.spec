%define		plugin		jquery
Summary:	Provides the jQuery JavaScript Framework for other plugins/templates
Name:		dokuwiki-plugin-%{plugin}
Version:	20090210
Release:	1
License:	GPL v3
Group:		Applications/WWW
Source0:	http://wiki.birth-online.de/_media/software/php/jquery.tar.gz
# Source0-md5:	3fe95631afdd7a300d6696cb3ba699a6
URL:		http://www.dokuwiki.org/plugin:jquery
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	sed >= 4.0
Requires:	dokuwiki >= 20090206
Requires:	jquery
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
Provides the jQuery JavaScript Framework for other plugins/templates.

%prep
%setup -qc
mv %{plugin}/* .

mv {INFO,info}.txt
sed -i -e 's,INFO.txt,info.txt,' *.php

version=$(awk '/date/{print $2}' info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
ln -snf %{_datadir}/jquery/jquery.js $RPM_BUILD_ROOT%{plugindir}/script.js

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/*.js
