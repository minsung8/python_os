
1. Process
    - 운영체제(OS)로 부터 할당 받는 자원 단위(실행 중인 프로그램)
    - CPU 동작 시간, 주소 공간 독립적
    - Code, Data, Stack, Heap 독릭접
    - 최소 1개의 메인 스레드 보유
    - 파이프, 파일, 소켓 등을 사용해서 프로세스 간 통신 (but cost 높음) => Context Switching

---------------------------------------------------------

2. Thread
    - 프로세스 내에 실행 흐름 단위
    - 프로세스 자원 사용
    - Stack만 별도 할당 나머지(Code, Data, Heap) 영역은 공유
    - 메모리 공유(변수 공유)
    - 한 스레드의 결과가 다른 스레드에 영향을 끼침
    - 동기화 문제 주의 (디버깅 어려움)

---------------------------------------------------------

3. Multi Thread
    - 한 개의 단일 어플리케이션 -> 여러 스레드로 구성 후 작업 처리
    - 시스템 자원 소모 감소(효율성) => 처리량 증가(cost 감소)
    - 통신 부담 감소, 디버깅 어려움, 단일 프로세스에는 효과 미약
    - 자원 공유 문제(교착 상태), 프로세스에 영향을 끼침

---------------------------------------------------------

4. Multi Process
    - 한 개의 단일 어플리케이션 => 여러 프로세스로 구성 후 작업 처리
    - 한 개의 프로세스 문제 발생은 확산 없음
    - 캐시 체인지, cost 비용 높음(오버헤드)

---------------------------------------------------------

5. GIL(Global Interpreter Lock)
    - CPython -> python(bytecode) 실행 시 여러 Thread 사용할 경우 단일 Thread 만이 Python object에 접근하게 제한 하는 mutex
    - CPython 메모리 관리 이슈 때문에(Thread-safe)
    - 단일 스레드로 충분히 빠름
    - 프로세스 사용 가능(Numpy/Spicy)등 gil 외부 영역에서 효율적인 코딩 가능 
    - 병렬 처리는 MultiProcess, asyncio 등 선택지 다양
    - Thread 동시성 완벽 처리를 위해 -> Jpython, IronPython, Stackless python 등이 존재

---------------------------------------------------------

6. DaemonThread
    - 백그라운드에 실행
    - 메인 스레드 종료 시 즉시 종료
    - 주로 백그라운드 무한 대기 이벤트 발생 실행하는 부분 담당 => JVM(Gabage Collection), 자동 저장
    - 일반 스레드는 작업 종료시 까지 실행

---------------------------------------------------------

7. Group Thread
    - .concurrent.futures
    - .with 문으로 생성 소멸 라이프사이클 관리 용이
    - 디버깅하기 난해
    - 대기중인 작업 -> Quere -> 완료 상태 조사 -> 결과 또는 예외 -> 단일화(캡슐화)

---------------------------------------------------------

8. Lock Case
    - Semaphore : 프로세스간 고융된 자원에 접근 시 문제 발생 가능성 => 한 개의 프로세스만 접근 처리 고안 (경쟁 상태 예방)
    - Mutex : 공유된 자원의 데이터를 여러 스레드가 접근하는 것을 막는 것 => 경쟁 상태 예방
    - Deadlock : 프로세스가 자원을 획득하지 못해 다음 처리를 못하는 무한 대기 상황(교착 상태)
    - Thread Synchronization(스레드 동기화)를 통해 안정적으로 동작하게 처리
    - Semaphore vs Mutex : 
        1. 모두 병렬 프로그래밍 환경에서 상호배제를 위해 사용
        2. Mutex는 단일 스레드가 리소스 또는 중요 세션 소비 허용
        3. Semaphore는 리소스에 대한 제한된 수의 프로세스 동시 엑세스 허용 

---------------------------------------------------------

9. Producer-Consumer Pattern
    - MultiThread 디자인 패턴의 정석
    - 서버측 프로그래밍의 핵심
    - 주로 허리 역할

---------------------------------------------------------
