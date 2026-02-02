# This program was modified by Jasmine Sanders / N01747318
import socket
import argparse
import time
import os
import struct

def run_client(target_ip, target_port, input_file):
    # 1. Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (target_ip, target_port)
    #Set timeout
    sock.settimeout(.5)

    print(f"[*] Sending file '{input_file}' to {target_ip}:{target_port}")

    if not os.path.exists(input_file):
        print(f"[!] Error: File '{input_file}' not found.")
        return

    try:
        seq_num = 0
        with open(input_file, 'rb') as f:
            while True:
                # Read a chunk of the file
                chunk = f.read(1024)
                
                if not chunk:
                    # End of file reached
                    break

                #Create packet with sequence number
                packet_header = struct.pack('!I', seq_num) #Format: unsigned int big-endian order (4 bytes)
                packet = packet_header + chunk             #Add chunk to create packet

           

                # Stop and Wait
                while True:
                    # Send the packet
                    sock.sendto(packet, server_address)
                    try:
                        ack_data, _ = sock.recvfrom(4) # Wait for 4 byte ACK
                        ## Unpack packet -> unpack returns a tuple 
                        ack_num = struct.unpack('!I', ack_data)[0]
                        if ack_data == b'EOF':
                            break
                        #If sequence number is acknowledged, increase seq
                        if ack_num == seq_num:
                            seq_num += 1
                            break
                    except socket.timeout:
                        #If timeout, send again
                        print(f"Timeout, resending seq {seq_num}")
                
                # Optional: Small sleep to prevent overwhelming the OS buffer locally
                # (In a perfect world, we wouldn't need this, but raw UDP is fast!)
                time.sleep(0.001)

        # Send empty packet to signal "End of File"
        sock.sendto(b'', server_address)
        print("[*] File transmission complete.")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naive UDP File Sender")
    parser.add_argument("--target_ip", type=str, default="127.0.0.1", help="Destination IP (Relay or Server)")
    parser.add_argument("--target_port", type=int, default=12000, help="Destination Port")
    parser.add_argument("--file", type=str, required=True, help="Path to file to send")
    args = parser.parse_args()

    run_client(args.target_ip, args.target_port, args.file)