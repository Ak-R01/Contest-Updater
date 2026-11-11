#Maintainer: Ak-R01
pkgname=contest-updater
pkgver=1.0.0
pkggrel=1
pkgdesc='Sync upcoming Codeforces contests to Google Calendar'
arch=('any')
url='https://github.com/Ak-R01/Contest-Updater'
license=('MIT')
depends=('python'
         'python-google-api-python-client'
         'python-google-auth-oauthlib'
         'python-google-auth-httplib2'
         'python-requests')
optdepends=('libnotify: desktop notifications on errors')
source=("#pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('REPLACE_ME')

package() {
  cd "Contest-Updater-$pkgver"
  install -Dm644 calender.py "$pkgdir/usr/share/$pkgname/calender.py"
  install -Dm644 contests_getter.py "$pkgdir/usr/share/$pkgname/contests_getter.py"

  install -Dm644 contest-updater.service "$pkgdir/usr/lib/systemd/user/contest-updater.service"
  install -Dm644 contest-updater.timer "$pkgdir/usr/lib/systemd/user/contest-updater.timer"

  install -Dm755 /dev/stdin "$pkgdir/usr/bin/$pkgname" <<'EOF'
#!/bin/sh
exec python /usr/share/contest-updater/calender.py "$@"
EOF
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}