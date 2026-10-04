# Hanuri

사무실 두 곳과 집에서 같은 코드, 자료 버전, 작업 기록으로 이어서 일하기 위한 프로젝트입니다.

## 저장 위치

| 내용 | 위치 |
| --- | --- |
| 코드, 문서, 작업 기록 | GitHub `dreamer0691/hanuri` |
| 대용량 원본과 결과물 | Google Drive의 프로젝트 폴더 |
| 개발 도구와 작업 중인 파일 | 클라우드 개발 환경 |
| 내려받은 자료 | `.cache/data/` (Git 제외, 재생성 가능) |

## 작업 시작

기존 `/workspace/hanuri` 체크아웃을 사용합니다. 클라우드 작업은 이미 격리되어 있으므로 별도 worktree를 만들 필요가 없습니다.

1. `git status --short --branch`로 미저장 변경을 확인합니다.
2. `git fetch origin`으로 원격 상태를 확인합니다. 로컬 변경이 없고 현재 브랜치에 upstream이 있으면 `git pull --ff-only`로 갱신합니다. 다른 작업 브랜치에서는 원격 변경을 검토한 후 병합합니다. 충돌 시 파일을 덮어쓰거나 강제 초기화하지 않습니다.
3. `AGENTS.md`와 `docs/current-status.md`를 읽습니다.
4. 아래 검사를 실행하고 필요한 자료만 준비합니다.

```bash
cd /workspace/hanuri
python3 scripts/check_workspace.py
# 매니페스트에 등록된 자료를 캐시에 준비한 후:
python3 scripts/check_workspace.py --verify-cache
```

현재 도구는 Python 3.12 이상과 표준 라이브러리만 사용합니다. 추가 패키지 설치나 서버 시작은 필요하지 않습니다. 앱 기술 스택은 아직 정하지 않았습니다.

## 작업 종료

`docs/current-status.md`에 완료한 일, 진행 중인 일, 다음 명령, 검증 결과, 사용한 자료 버전을 남깁니다. 중요한 선택은 `docs/decisions.md`에 기록합니다.

변경을 검토한 뒤 필요한 파일을 명시적으로 선택하여 커밋하고 작업 브랜치를 원격으로 푸시합니다. 다른 장소에서 이어갈 변경은 원격에 올라가 있어야 합니다. 초기 `main` 게시 후 일반 작업은 `git switch -c task/<작업명>`으로 시작하고 PR을 통해 병합합니다. 같은 브랜치를 여러 장소에서 동시에 수정하지 않습니다.

Google Drive 인증 정보와 대용량 자료는 Git에 넣지 않습니다. 연결 방법과 자료 등록 형식은 [자료 관리](docs/data-management.md), 장소 이동 절차는 [작업 재개](docs/workflow.md)를 참고하세요.
