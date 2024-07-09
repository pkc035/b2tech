# 비투텍 백엔드 프로젝트

## 소개
이 프로젝트는 Django와 Django REST Framework(DRF)를 사용하여 구현한 비투텍 백엔드 시스템입니다. 이 시스템은 회원가입 및 로그인, 위치 정보 저장, 접근 제한 구역 알림, 위치 공유 등의 기능을 제공합니다. 이 프로젝트는 Docker Compose를 사용하여 PostgreSQL, Nginx, Django를 배포합니다.

## 주요 기능

### 회원 가입 및 로그인
- 회원가입은 휴대폰 번호로 진행됩니다.
- 로그인 후 인증은 JWT 토큰을 사용합니다.

### 접근 제한 구역 설정
- 관리자는 특정 이름으로 접근 제한 구역을 설정할 수 있으며, 구역은 Boundary의 위치 좌표를 포함합니다.

### 유저 위치 정보 저장
- 로그인된 유저는 자신의 현재 좌표를 서버에 전송하여 저장합니다.

### 접근 제한 구역 안내 메시지 저장
- 유저의 위치 정보가 설정된 구역 안에 있는지 확인 후, 특정 구역 안에 있다면 해당 정보를 알림 메시지로 저장합니다.

### 접근 제한 구역 알림 메시지 확인
- 유저는 자신의 위험 메시지를 확인 및 삭제할 수 있습니다.

### 위치 공유
- 공유 그룹을 만들어 휴대폰 번호로 초대할 수 있습니다.
- 초대받은 회원은 동의 또는 거부할 수 있으며, 동의 후 언제든 공유 그룹에서 나올 수 있습니다.
- 공유 그룹에 참여한 모든 이들이 위치 정보를 서로 확인할 수 있습니다.

## API 엔드포인트

### 사용자 관련 API (/api/users/)
- **회원가입**: `/signup/`
- **로그인**: `/login/`
- **토큰 갱신**: `/token/refresh/`

### 위치 관련 API (/api/locations/)
- **위치 리스트**: `/`
- **위치 생성**: `/create/`
- **그룹 위치 리스트**: `/groups/<int:group_id>/locations/`

### 알림 관련 API (/api/notifications/)
- **구역 리스트 및 생성**: `/boundaries/`
- **구역 상세조회, 수정, 삭제**: `/boundaries/<int:pk>/`
- **알림 리스트**: `/`
- **알림 상세조회 및 삭제**: `/<int:pk>/`

### 그룹 관련 API (/api/groups/)
- **그룹 리스트**: `/`
- **그룹 생성**: `/create/`
- **그룹 상세조회, 수정, 삭제**: `/<int:pk>/`
- **그룹 초대**: `/<int:pk>/invite/`
- **초대 수락**: `/invitations/<int:pk>/accept/`
- **초대 거절**: `/invitations/<int:pk>/reject/`
- **그룹 탈퇴**: `/<int:pk>/leave/`

## 설치 및 실행

### 1. 환경 설정
- Docker 및 Docker Compose가 설치되어 있어야 합니다.

### 3. Docker Compose 실행
```bash
docker-compose up --build
```

### 4. 마이그레이션 및 슈퍼유저 생성
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. 서버 접속
- 웹 애플리케이션: [http://localhost:8888](http://localhost:8888)
- Django 관리자 페이지: [http://localhost:8888/admin](http://localhost:8888/admin)

## 테스트
- 테스트는 Django 테스트 프레임워크를 사용하여 실행할 수 있습니다.
```bash
docker-compose exec web python manage.py test
```

## 관리자 계정
- 관리자 페이지에 접근 가능한 계정 정보는 다음과 같습니다:
  - **Phone Number**: 01000000000
  - **비밀번호**: 01000000000

## 배포
- 이 프로젝트는 Nginx, Gunicorn, PostgreSQL, Python3을 사용하여 Docker Compose로 배포됩니다.

## Swagger 문서
- API 문서는 Swagger를 사용하여 제공합니다.
  - [Swagger UI](http://localhost:8888/swagger/)

  