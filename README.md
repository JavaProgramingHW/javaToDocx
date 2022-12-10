# 자바프로그래밍을 위한 문서 생성기

### Java code guide

* [Eclipse](https://www.eclipse.org/downloads/) 나 [IntelliJ](https://www.jetbrains.com/ko-kr/idea/) 에서 텍스트 포맷을 UTF-8 로 설정해야한다. 그렇지 않으면 결과값에서 한글이 깨진다.
* 파일명은 Hw(챕터)_(문제번호) 로 통일한다, 이는 패키지 폴더도 적용된다. ex. Hw1_1
* (챕터) 와 (문제번호) 는 int값이어야 한다. str값일 경우 문제번호 작성 과정 중 제거된다.
* 만약 패키지라면 메인 java 프로그램 명과 패키지 폴더 이름을 동일하게 설정한다. ex. Hw1_1/Hw1_1.java
* 코드 실행시 매개변수 삽입이 필요한 경우 - 만약 `java Hw1_1.java <파일명1> <파일명2>` 와 같이 실행이 필요한 경우, 메인 java 프로그램 맨 위에 아래 예시와 같은 주석을 달아둔다.
```java
// <파일명1> <파일명2>
```
* Scanner로 입력이 필요한 프로그램은 메인 java 프로그램 맨 위 혹은 매개변수 주석 바로 아래 예시와 같은 주석을 달아둔다.
```java
/*
first input data
second input data
*/
```
* 매개변수 삽입과 Scanner 입력 둘 다 필요한 경우 아래와 같이 작성한다.
```java
// <파일명1> <파일명2>
/*
first input data
second input data
*/
```

### Requirements

* java 11 이상이 필요하다.
* python-docx 모듈과 python3.11 버전은 호환이 불가능하기 때문에 python3.10 이하, python3.6 이상 버전이 필요하다(python3.10 버전 권장)

### 주의
Windows 환경에서는 오류가 **다수** 발생할 수 있음<br>
UNIX 환경(macOS)과 UNIX-like 환경(Linux)을 권장함<br>
결과물에 누락된 **UML Class Diagram 이미지나 실행 결과 이미지**가 존재할 수 있으니 문서화 이후 재확인이 필요하다

### 실행법

- Windows - start.bat 파일을 더블클릭하여 실행한다.

* 최초 실행시 : 
- Linux, macOS, ... - `pip3 install -r requirements.txt`

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