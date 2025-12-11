We captured network traffic from a suspicious user's machine. There's evidence they logged into a web application.

Your task is to analyze the packet capture and find the credentials they used.

Intel: The target logged into a web application using HTTP (not HTTPS). Their password is the flag!

Tools: Wireshark, tcpdump, tshark, or any packet analyzer

Flag Format: DECCTF{...}
View Hint

Look for HTTP traffic. In Wireshark, use the filter: http
View Hint

Look for HTTP traffic. In Wireshark, use the filter: http
View Hint

Look for HTTP traffic. In Wireshark, use the filter: http
View Hint

Login forms typically use HTTP POST requests. Filter for: http.request.method == POST
View Hint

Login forms typically use HTTP POST requests. Filter for: http.request.method == POST
View Hint

Login forms typically use HTTP POST requests. Filter for: http.request.method == POST
View Hint

In Wireshark, right-click on a POST packet and select 'Follow > HTTP Stream' to see the full request with form data.
View Hint

In Wireshark, right-click on a POST packet and select 'Follow > HTTP Stream' to see the full request with form data.
View Hint

In Wireshark, right-click on a POST packet and select 'Follow > HTTP Stream' to see the full request with form data.
