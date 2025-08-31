# 변수 세팅
TS=$(date +%Y%m%d-%H%M)
BK=~/px-backup-$TS
mkdir -p "$BK"

# 기본 정보 스냅샷
echo "Python: $(python3 -V)"        >  "$BK/ENVINFO.txt"
echo "OS:"                           >> "$BK/ENVINFO.txt"
cat /etc/os-release                  >> "$BK/ENVINFO.txt"
echo -e "\nKernel: $(uname -a)"      >> "$BK/ENVINFO.txt"

# venv 패키지 목록 (복구 핵심)
source ~/picar-x/px-venv/bin/activate
pip freeze > "$BK/requirements.txt"

# 프로젝트/예제 코드
tar -C ~ -czf "$BK/picar-x-code.tar.gz"  picar-x

# 설정 파일들
mkdir -p "$BK/config"
[ -f ~/.config/picar-x/picarx.conf ] && cp ~/.config/picar-x/picarx.conf "$BK/config/"
sudo bash -c 'tar -czf "'"$BK"'/opt-picar-x.tar.gz" -C / opt/picar-x 2>/dev/null || true'

# 포트오디오 등 시스템 패키지 기록(참고용)
dpkg -l | egrep 'pyaudio|portaudio|lgpio|i2c-tools' > "$BK/DEB_PACKAGES.txt" || true

# 복구 스크립트 생성
cat > "$BK/restore.sh" <<'SH'
#!/usr/bin/env bash
set -e
echo "[1/5] 폴더 준비"
mkdir -p ~/picar-x ~/.config/picar-x

echo "[2/5] 코드 복원"
tar -C ~ -xzf ./picar-x-code.tar.gz

echo "[3/5] 시스템 패키지(권장)"
sudo apt update
sudo apt install -y libportaudio2 portaudio19-dev python3-pyaudio python3-lgpio i2c-tools

echo "[4/5] 파이썬 환경"
cd ~/picar-x
python3 -m venv px-venv
source px-venv/bin/activate
pip install --upgrade pip
# 우선 GitHub 공식 패키지로 맞춤
pip install --no-cache-dir "git+https://github.com/sunfounder/robot-hat.git"
pip install --no-cache-dir "git+https://github.com/sunfounder/picar-x.git"
# 필요 시 추가 의존성
pip install -r ../px-backup-*/requirements.txt || true

echo "[5/5] 설정 복원"
[ -f ./../px-backup-*/config/picarx.conf ] && cp ./../px-backup-*/config/picarx.conf ~/.config/picar-x/picarx.conf
grep -q PICARX_CONFIG ~/.bashrc || echo 'export PICARX_CONFIG="$HOME/.config/picar-x/picarx.conf"' >> ~/.bashrc
source ~/.bashrc

echo "복원 완료. 테스트:"
python3 - <<'PY'
import time, os
from picarx import Picarx
print("CONFIG:", os.getenv("PICARX_CONFIG"))
px=Picarx(); px.forward(30); time.sleep(1); px.stop()
print("Forward OK")
PY
SH
chmod +x "$BK/restore.sh"

# 최종 묶음
tar -C ~ -czf "$HOME/px-backup-$TS.tar.gz" "px-backup-$TS"
echo "==> 백업 파일: $HOME/px-backup-$TS.tar.gz"
