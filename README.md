# Description
- 구글 뉴스에서 해외 신문 크롤링을 하기 위해 만든 파이썬 프로그램
    - 해외 기사 수집이 목적이기 때문에 영문 기사만 수집됨
- 기사의 제목, 기사 내용, url이 수집됨
    - 한계: 1년 단위로 크롤링을 하게 되어있지만 구글 뉴스의 한계인지 최대 90~100개 정도의 기사만 수집됨
## Environment
- M1 macOS Ventura 13.2.1(22D68)에서 개발되었으며 셀레니움 등의 크롤링 라이브러리를 사용하고 있음
- requirements.txt 로 필요 패키지 설치 가능
## Prerequisite
- macOS에서 작동할 수 있도록 pystan 버전을 수정하였음 
- selenium과 파이썬 버전은 자신의 운영체제에 맞게 운용 필요
## Files
- .venvCrawler: 파이썬 가상환경
- crawl_result: output excel 저장 폴더 (키워드-날짜 등이 제목으로 저장됨)
- driver: 크롬 드라이버 위치
- .gitignore: 파일 무시
- crawler.py: 실행 파일
- requirements.txt: 설치 파일 목록
## Usage
파이썬을 부르고 파일을 실행해주고, 검색하고 싶은 키워드를 입력해준다. 
### Usage examples
- "검색 키워드"를 추가해 목표하는 키워드를 엑셀로 받을 수 있다. 
    - 실행 진도가 나오며 네트워크 환경에 따라 다르지만 늦으면 20~30분 정도 걸림 <br>
```python3 crawler.py -k "<검색 키워드>" ```<br>
```python3 crawler.py --keyword "<검색 키워드>" ```