# pushcap
After my broadband provider decided to actually enforce its download cap and took my free credit, I decided I needed an automated way to get notifications of my data usage.

I use an unlocked *Huawei B593s-22* 4G/LTE Router to get my Internet access. Selenium and Chromedriver log me into the Router locally and grab my data usage, then send me a push notification. It does this once a day. I use Launchd and [https://pushover.net/](pushover.net) to automate the process. 

![pushcap ios screen](https://www.dropbox.com/s/9ayhsm5r91z88fs/pushcap-ios.png?dl=1)

If you're going to use this yourself, know that I did no security testing. Your username and password could be sniffed over wifi I guess. See below for setup instructions.

**This is for Mac OS X only.**

## setup
I assume you have python, virtualenv, virtualenvwrapper, pip and the Chrome Browser installed.
+ Clone this repo
+ Install Chromedriver via homebrew
  + `brew install chromedriver`
+  Create a new environment using virtualenvwrapper
  + `mkvirtualenv <env>`
+ Install Python Dependencies for your version of Python
  + Python 3
    + `pip install -r requirements.txt`
  + Python 2
    + `pip install requests dotenv`
    + `pip install selenium`
+ Create a new app on [https://pushover.net/](pushover.net) and note your user and app keys
+ Create a *.env* file with **unquoted** Environment Variables for
  + Router Username
  + Router Password
  + Router IP Address
  + Pushover Application Token
  + Pushover User Key
  + Pushover Message Title
+ Test that your program works manually with
  + `python app.py`
+ If you get this far move on to automating below

## automating
You need two things to automate the notifications:

1. A bash shell script that calls your python program
2. A launchd plist file that calls your shell script

### 1. bash shell script
Find the path to the virtualenv environment you created above. You’re looking for the path to your python executable for that environment. Mine is `~/Envs/pcap/bin/python3.6` *pcap* is my environment.

Create a bash script (*script.sh*) like so:
```
#!/bin/bash
$HOME/Envs/pcap/bin/python3.6 $HOME/Sites/python/pushcap/app.py
```

Make your script executable:

`chmod +x script.sh`

Test your script manually:

`./script.sh`

### 2. launchd plist file
You need to create a plist file called something like `com.me.pushcap.plist` and store it in `~/Library/LaunchAgents`

To manage the loading and unloading of plist files you can use *launchctl*:

+ `launchctl load com.me.pushcap.plist`
+ `launchctl unload com.me.pushcap.plist`
+ `launchctl list | grep 'me'`

We will use 6 parameters or keys in our plist file:

1. Label
2. Program
3. RunAtLoad
4. StandardErrorPath
5. StandardOutPath
6. StartCalendarInterval

Copy one of the files in `~/Library/LaunchAgents` - the `com.google.keystone.agent.plist` for example. Remove everything *inside* the `<dict>` tag and save the file as `com.me.pushcap.plist`

Add the following inside the `<dict>` tag block:
```
<key>Label</key>
<string>com.me.pushcap</string>
<key>Program</key>
<string>/Users/me/Sites/python/pushcap/script.sh</string>
<key>RunAtLoad</key>
<true/>
<key>StandardErrorPath</key>
<string>/tmp/pushcap.err</string>
<key>StandardOutPath</key>
<string>/tmp/pushcap.out</string>
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>21</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

Load the plist file with *launchctl* and check that it returns a `0` when you list the process:

+ `launchctl load com.me.pushcap.plist`
+ `launchctl list | grep 'me'`

Verify that you are receiving push notifications from Pushover.
