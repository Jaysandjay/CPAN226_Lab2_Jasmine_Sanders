# Lab 1 Report

## Screenshot 1
The two jpg files (old_lady.jpg and the received version) from the direct client to server transfer (without the relay).

<img width="975" height="549" alt="image" src="https://github.com/user-attachments/assets/e46adb5d-554d-4a4a-81b9-1afdca482e88" />

## Screenshot 2
The corrupted received_relay.jpg (from Test B).

<img width="837" height="472" alt="image" src="https://github.com/user-attachments/assets/f5c80c94-28f3-4578-a990-14a764b94db6" />

## Screenshot 3
The clean received.jpg after your code fix, successfully transferred through the relay.

<img width="975" height="548" alt="image" src="https://github.com/user-attachments/assets/07987e62-3521-4d2b-8d7d-2f0d004accbf" />


## Screenshot 4 
The result of the Final check. 

<img width="1915" height="1074" alt="image" src="https://github.com/user-attachments/assets/5e22ace0-29c0-433f-b6f2-52592390b979" />

## Buffer logic
The server checks whether the received packet’s sequence number matches the expected sequence. If it does, the server writes the data to the 
file and increments the expected_seq variable. It then loops through a while loop to see if the next expected sequence is already in the buffer, 
writing any buffered data in order and removing it from the buffer. If the received sequence number is higher than expected, the packet is stored 
in the buffer dictionary for later. If the sequence number is lower than expected, the packet is a duplicate and is ignored.

```python
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
```




