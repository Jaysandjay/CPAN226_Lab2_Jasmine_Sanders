# This program was modified by Jasmine Sanders / N01747318
import socket
import argparse
import struct

def run_server(port, output_file):
    # 1. Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 2. Bind the socket to the port (0.0.0.0 means all interfaces)
    server_address = ('', port)
    print(f"[*] Server listening on port {port}")
    print(f"[*] Server will save each received file as 'received_<ip>_<port>.jpg' based on sender.")
    sock.bind(server_address)

    # 3. Keep listening for new transfers
    try:
        expected_seq = 0
        buffer = {}
        while True:
            f = None
            sender_filename = None
            reception_started = False
            while True:
                data, addr = sock.recvfrom(4096 + 4)
                # Protocol: If we receive an empty packet, it means "End of File"
                if not data:
                    print(f"[*] End of file signal received from {addr}. Closing.")
                    #Send ACK for EOF
                    sock.sendto(b'EOF', addr)
                    break
                if f is None:
                    print("==== Start of reception ====")
                    ip, sender_port = addr
                    sender_filename = f"received_{ip.replace('.', '_')}_{sender_port}.jpg"
                    f = open(sender_filename, 'wb')
                    print(f"[*] First packet received from {addr}. File opened for writing as '{sender_filename}'.")
                
                # Unpack packet -> unpack returns a tuple
                seq_num = struct.unpack('!I', data[:4])[0] #Slice packet to get first 4 bytes (seq num)
                data = data[4:] #Slice to get remaining bytes (the data)

                #Create and send ACK packet
                ack_packet = struct.pack('!I', seq_num)
                sock.sendto(ack_packet, addr)

                #If seqenced number is the expected sequence, write to the file and increase the expected sequence number
                if expected_seq == seq_num:
                    f.write(data)
                    expected_seq += 1
                    # Check if the next expected sequence is in the buffer and write it to the file
                    while expected_seq in buffer:
                        buffered_data = buffer.pop(expected_seq)
                        f.write(buffered_data)
                        expected_seq += 1
                #If seq num is higher than expected, put data in buffer
                elif seq_num > expected_seq:
                    buffer[seq_num] = data
                else:
                    #Packet is duplicate
                    pass
                
            if f:
                f.close()
                f = None
                expected_seq = 0
                buffer = {}

            print("==== End of reception ====")
    except KeyboardInterrupt:
        print("\n[!] Server stopped manually.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        sock.close()
        print("[*] Server socket closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naive UDP File Receiver")
    parser.add_argument("--port", type=int, default=12001, help="Port to listen on")
    parser.add_argument("--output", type=str, default="received_file.jpg", help="File path to save data")
    args = parser.parse_args()

    try:
        run_server(args.port, args.output)
    except KeyboardInterrupt:
        print("\n[!] Server stopped manually.")
    except Exception as e:
        print(f"[!] Error: {e}")