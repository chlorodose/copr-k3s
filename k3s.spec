%global tag             1.35.1
%global debug_package   %{nil}

Name:           k3s
Release:        %autorelease
Version:        %{tag}
Summary:        Lightweight Kubernetes

License:        Apache-2.0
URL:            https://k3s.io
Source:         https://github.com/k3s-io/k3s/archive/refs/tags/v%{tag}+k3s1.tar.gz
Source1:        https://github.com/k3s-io/k3s/releases/download/v%{tag}+k3s1/k3s
Source2:        https://github.com/k3s-io/k3s/releases/download/v%{tag}+k3s1/k3s-arm64

ExclusiveArch:  x86_64 arm64

BuildRequires:  systemd

%description
The certified Kubernetes distribution built for IoT & Edge computing.

%files
%{_bindir}/k3s
%{_bindir}/kubectl
%{_bindir}/crictl
%{_bindir}/ctr
%{_prefix}/lib/systemd/system/k3s.service
%{_sysconfdir}/rancher/k3s/config.yaml
%{_sysconfdir}/rancher/k3s/config.yaml.d/

%prep
%autosetup -n k3s-%{tag}-k3s1
echo 'write-kubeconfig-mode: "0644"' >config.yaml

%install
install -m 0755 -vd                         %{buildroot}%{_bindir}
%if "%{_buildarch}" == "arm64"
    install -m 0755 -vp %{S:2}              %{buildroot}%{_bindir}/k3s
%else
    install -m 0755 -vp %{S:1}              %{buildroot}%{_bindir}/k3s
%endif
ln -sf k3s                                  %{buildroot}%{_bindir}/kubectl
ln -sf k3s                                  %{buildroot}%{_bindir}/crictl
ln -sf k3s                                  %{buildroot}%{_bindir}/ctr
install -m 0755 -vd                         %{buildroot}%{_prefix}/lib/systemd/system/
install -m 0644 -vp k3s.service             %{buildroot}%{_prefix}/lib/systemd/system/k3s.service
install -m 0755 -vd                         %{buildroot}%{_sysconfdir}/rancher/k3s/
install -m 0644 -vp config.yaml             %{buildroot}%{_sysconfdir}/rancher/k3s/config.yaml
install -m 0755 -vd                         %{buildroot}%{_sysconfdir}/rancher/k3s/config.yaml.d/

%post
%systemd_post k3s.service

%postun
%systemd_postun k3s.service

%changelog
%autochangelog
