[![fuzzler-logo](https://github.com/suffs811/writeups/blob/main/fuzzler-imgs/fuzzler-small.jpg)
# Fuzzler
Fuzzler is a penetration testing tool that generates tailored password lists from webpages using Artificial Intelligence/Natural Language Processing. 

>Video walkthrough can be found [here](https://www.youtube.com/watch?v=f6hT4JqDRZY)

Fuzzler executes the following three steps to create wordlists:
1.	Fuzzler crawls the given webpage using CeWL to identify words relevant to that business or organization.
2.	Fuzzler utilizes Natural Language Processing to find synonyms of the words collected in step 1 and then adds them to the wordlist.
3.	Fuzzler uses hashcat to fuzz the wordlist by transforming the words (lowercase, uppercase, capitalized, all capitalized except the first letter, reversed, digits 0-99 prepended/appended, and translated to 1337 speak).

These operations allow Fuzzler to generate incredibly sophisticated wordlists that better represent the passwords used by employees and services of the business/organization than traditional wordlists. 

Feel free to break Fuzzler and let me know how I can make it better!

## usage
download Fuzzler:

`git clone https://www.github.com/suffs811/fuzzler.git`

use fuzzler to generate wordlist:

`python3 fuzzler.py -t 10.10.10.10 -p 8080` 

**the final password list will be in 'fuzzes.txt'**


## other Fuzzler tools
the Fuzzler Limited - Chrome Extension can be found [here](https://github.com/suffs811/fuzzler-ext)

## credit and license
Copyright (c) 2023 suffs811

https://github.com/suffs811

This project is licensed under the MIT License - see the LICENSE file for details.

*Fuzzler has been tested on kali linux 2023.2*

*NOTE: Fuzzler is only intended to be used for personal, legal activities. DO NOT use Fuzzler for illegal hacking activities. I am not liable for any damages caused by the unlawful use of this tool by another person.*

-+- Leave a comment in the Discussion if you have any questions! -+-
