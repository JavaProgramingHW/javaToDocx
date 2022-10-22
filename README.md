# 자바프로그래밍을 위한 문서 생성기

### 사용법

* 파일명은 Hw(챕터)_(문제번호) 로 통일한다, 이는 패키지 폴더도 적용된다. ex. Hw1_1
* Scanner로 입력이 필요한 프로그램은 파일 맨 위에 아래 예시와 같은 주석을 달아둔다.
```java
/*
first input data
second input data
*/
```
* 만약 패키지라면 메인 프로그램 명과 패키지 폴더 이름을 동일하게 설정한다. ex. Hw1_1/Hw1_1.java
* java 11 이상이 필요하다.

### 실행법

* 최초 실행시 : 
- Windows - `pip install -r requirements.txt`
- else(Ubuntu, macos, ...) - `pip3 install -r requirements.txt`

* 프로그램 실행
```
python3 main.py
```

### Docx --> hwp

1. 한글 프로그램을 연다
2. 프로그램 돌려서 나온 `result.docx` 파일을 연다
3. `다른 이름으로 저장하기` 를 누른다
4. 파일 확장자명을 hwp로 저장한다

* 한글이 없으면?
-> 돈내고 사. 없으면 어차피 과제 못하잖아

### Opensource

* [UML-Parser](https://github.com/SnehaVM/UML-Parser)
* [Java2UML](https://github.com/tlqaksqhr/Java2UML)
* [carbon-api](https://github.com/StarkBotsIndustries/Carbon)
* [pexpect](https://github.com/pexpect/pexpect)
* [wexpect](https://github.com/raczben/wexpect)
* [natsort](https://github.com/SethMMorton/natsort)
* [python-docx](https://github.com/python-openxml/python-docx)