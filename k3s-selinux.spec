%global tag     1.6.latest.1

Name:           k3s-selinux
Version:        v%{tag}
Release:        %autorelease
Summary:        SELinux Policy for k3s
License:        Apache-2.0
URL:            https://k3s.io
Source:         https://github.com/k3s-io/k3s-selinux/archive/refs/tags/v%{tag}.tar.gz

BuildArch:      noarch
BuildRequires: container-selinux
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base, policycoreutils
Requires(post): container-selinux
Requires(postun): policycoreutils

Provides:       k3s-selinux

%description
This package installs and sets up the SELinux policy security module for k3s.

%prep
%autosetup -n k3s-selinux-%{tag}

%build
make -C policy/coreos -f /usr/share/selinux/devel/Makefile k3s.pp

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 policy/coreos/k3s.pp %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 policy/coreos/k3s.if %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}/etc/selinux/targeted/contexts/users/

%pre
%selinux_relabel_pre

%posttrans
%selinux_relabel_post


%post
%selinux_modules_install %{_datadir}/selinux/packages/k3s.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    mkdir -p /var/lib/cni
    mkdir -p /var/lib/kubelet/pods
    mkdir -p /var/lib/rancher/k3s/agent/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots
    mkdir -p /var/lib/rancher/k3s/data
    mkdir -p /var/run/flannel
    mkdir -p /var/run/k3s
    restorecon -FR -T 0 -i /etc/systemd/system/k3s.service
    restorecon -FR -T 0 -i /usr/lib/systemd/system/k3s.service
    restorecon -FR -T 0 /var/lib/cni
    restorecon -FR -T 0 /var/lib/kubelet
    restorecon -FR -T 0 /var/lib/rancher
    restorecon -FR -T 0 /var/run/k3s
    restorecon -FR -T 0 /var/run/flannel
fi;

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall k3s
fi;

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/k3s.pp
%{_datadir}/selinux/devel/include/contrib/k3s.if

%changelog
* Thu Feb 19 2026 Chlorodose <chlorodose@chlorodose.me> 1.6.1
- Initial version
