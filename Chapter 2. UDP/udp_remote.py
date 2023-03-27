import argparse, random, socket, sys
#sys : 파이썬 인터프리터가 제공하는 변수나 함수를 제어할 수 있는 방법을 제공

MAX_BYTES = 65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        
        #서버는 0.5의 확률로 응답하지 않음
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        
        sock.sendto(message.encode('ascii'), address)
        

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))
    
    #Blocking(for 0.1s to wait until new data arrives)
    delay = 0.1 
    text = 'This is another message'
    data = text.encode('ascii')
    
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        
        #예외처리
        try:
            data = sock.recv(MAX_BYTES)
            
        #Expoenetial Backoff -> 점진적으로 증가하므로 네트워크에 트래픽 증가 예방
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request 
            
            #delay가 2.0s 넘기면 런타임에러(maximum delay)
            if delay > 2.0: # - maximum delay.
                raise RuntimeError('I think the server is down') from exc
        else:
            break   # we are done, and can stop looping

    print('The server says {!r}'.format(data.decode('ascii')))
    

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
