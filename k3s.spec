%bcond check 0
%bcond bootstrap 0

%global tag             v1.35.1
%global topdir          k3s-1.35.1-k3s1

%global goipath         github.com/k3s-io/k3s
Version:                %{tag}

%gometa -L -f

%global golicenses      LICENSE
%global godocs          docs ADOPTERS.md BUILDING.md CODE_OF_CONDUCT.md\\\
                        CONTRIBUTING.md GOVERNANCE.md README.md ROADMAP.md\\\
                        contrib/ansible/README.md contrib/util/DIAGNOSTICS.md\\\
                        scripts/airgap/image-list.txt updatecli/README.md

Name:           k3s
Release:        %autorelease
Summary:        Lightweight Kubernetes

License:        Apache-2.0
URL:            https://k3s.io
Source:         https://github.com/k3s-io/k3s/archive/refs/tags/%{tag}+k3s1.tar.gz
Source1:        https://github.com/chlorodose/copr-k3s/releases/download/%{tag}/k3s-vendor.tar.zst

BuildRequires:  systemd

%description
The certified Kubernetes distribution built for IoT & Edge computing.

%gopkg

%prep
%goprep -A
tar --zstd -xf %{S:1}

%if %{without bootstrap}
%go_generate_buildrequires
%endif

%if %{without bootstrap}
%build
%gobuild -o %{gobuilddir}/bin/k3s %{goipath}
%endif

%install
%gopkginstall
%if %{without bootstrap}
install -m 0755 -vd                         %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/k3s   %{buildroot}%{_bindir}/k3s
ln -sf k3s                                  %{buildroot}%{_bindir}/kubectl
ln -sf k3s                                  %{buildroot}%{_bindir}/crictl
ln -sf k3s                                  %{buildroot}%{_bindir}/ctr
install -m 0755 -vd                         %{buildroot}%{_libdir}/systemd/system/
install -m 0644 -vp k3s.service             %{buildroot}%{_libdir}/systemd/system/k3s.service
%endif

%if %{without bootstrap}
%if %{with check}
%check
%gocheck2
%endif
%endif

%if %{without bootstrap}
%files
%license LICENSE
%doc docs README.md ADOPTERS.md BUILDING.md CODE_OF_CONDUCT.md CONTRIBUTING.md
%doc GOVERNANCE.md ROADMAP.md contrib/ansible/README.md
%doc contrib/util/DIAGNOSTICS.md scripts/airgap/image-list.txt
%doc updatecli/README.md
%{_bindir}/k3s
%{_bindir}/kubectl
%{_bindir}/crictl
%{_bindir}/ctr
%{_libdir}/systemd/system/k3s.service
%endif

%gopkgfiles

%changelog
%autochangelog
