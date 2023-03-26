import argparse, socket
from datetime import datetime
# argparse : 명령행의 인자를 파싱할 때 사용하는 모듈(하나 Script의 동작을 여러 상황에 따라 다르게 동작하도록 쓰일 때)

MAX_BYTES = 65535

def server(port) :
    #socket 생성 / AF_INET : IPv4 / SOCK_DGRAM : UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #socket 포트 지정 (튜플로 (host, port)주소 받음
    sock.bind(('127.0.0.1', port))
    
    #getsockname : 소켓 자신의 주소 반환
    print('Listening at {}'.format(sock.getsockname()))
    
    
    #waiting forever : while True: 
    while True:
        #recvfrom : 소켓에서 데이터 수신 (반환값 : (bytes, address)쌍) *bytes: 수신한 데이터를 나타네는 바이트열 객체
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        
        #{!r} : '!r'는 repr()을 적용 - 문자열 출력
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        
        #socket에 데이터 보냄
        sock.sendto(data, address)
        

def client(port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))
    

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    
    #ArgumentParser : 프로그램 실행 시 커맨드 라인에 인수를 받아 처리를 간단히 할 수 있도록 하는 표준 라이브러리
    #인자값을 받을 수 있는 인스턴스 생성
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    
    #입력받을 인자값 등록 
    #choices: 리스트 형태로 전달하면, 리스트의 원소와 일치하는 것만 취함
    #help : -help 옵션을 받았을 때, 표시될 메세지 목록에서 스위치의 도움말 설정
    parser.add_argument('role', choices=choices, help='which role to play')
    
    
    #metavar: usage 메세지를 출력할 때 표시할 메타변수 이름을 지정해줌
    #type: 파싱하여 저장할 때 타입 변경 가능 -> 여기서는 int형으로
    #default: 뒤에 별도 값이 없는 경우 디폴트로 들어갈 값
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')

    #각 인자의 리스트를 받아 파싱한 결과를 되돌려줌
    args = parser.parse_args()
    
    function = choices[args.role]
    function(args.p)
