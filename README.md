# Python 유틸 모음

## 가상환경 생성
```
python -m venv venv
```

<br />

## 가상환경 활성화
```
(Windows)
venv/Scripts/activate

(Linux/Mac)
source venv/bin/activate
```

<br />

## 설치된 라이브러리 목록 추출
#### - Git에 올리는 경우
```
pip freeze > requirements.txt
```

<br />

## 라이브러리 한 번에 설치
#### - Git에서 내려받는 경우
```
pip install -r requirements.txt
```

<br />

## Editable 모드로 설치
```
pip install -e .
```