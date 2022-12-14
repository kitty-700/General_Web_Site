# Commit 가이드 라인 (v.0.1)

라이브러리 (pip freeze > requirements.txt
```
asgiref==3.5.2
certifi @ file:///C:/b/abs_ac29jvt43w/croot/certifi_1665076682579/work/certifi
Django==4.1.2
django-ckeditor==6.5.1
django-ckeditor-5==0.2.0
django-js-asset==2.0.0
install==1.3.5
Pillow==9.2.0
sqlparse==0.4.3
tzdata==2022.4
wincertstore==0.2
```
Commit Tag 가이드
```
[필수] {Type} : {Subject}
[선택] {Body}
```
* {Type} (예상되는 빈도 순으로 정렬)
  - style    : 로직 수정이 없는 변경의 경우 (코드 포맷팅(정렬), 오타, 주석 변경 등)
  - uiux    : 로직 수정 없이 ui/ux 개선 (style과 달리 화면 상의 변화가 있음)
  - rfctr    : 로직 수정이 있는 변경의 경우 (공통 함수 사용, I/O 변경,  예외 처리, 시스템 동작 개선 등)
  - fix    : rfctr 중 특별히 버그, 오류로 인한 변경의 경우
  - meta    : 서비스의 원형이 되는 메타 수정 (KXX99_99X 등) - 이 경우 메타 적용되는 다른 서비스들도 변경해야 할지 결정 필요
  - feat    : 새로운 기능 추가
  - doc    : 관련 문서 수정
  - test    : 테스트 코드 추가
  - sys     : 시스템 설정 
  - (특별히 중요한 내용일 경우 앞에 ☆ ★ 등으로 표시 (★이 더 중요))

* {Subject}
  - 어떻게(How)보다 무엇을, 왜(What, Why)에 맞춰 작성
  - 마침표 미사용
  - 맨 끝 단어는 명사 (음슴체 X)
  - 여러 의미가 적용된 사항들을 한 Commit 에 모두 담는게 좋은건 아니지만, 꼭 한 Commit 에 해야겠다면 '/' 슬래시로 Subject 구분 (귀찮을 땐 걍 이러고 싶어짐)
  - (선택) 특정 리소스를 강조하고 싶을 경우 맨 앞에 해당 [{Service}] ex) [KAA99_99X] 예외 처리 추가
