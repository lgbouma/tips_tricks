IF WIPED BLANK:
(which was necessary, b/c non-LTS to LTS is apparently such a BFD)

key software you want:

----------
CHROME 

not so bad -- just direct-install via debian package. NB the "Ubuntu
Software" package is straight garbage. Do not use it.

Instead:
```
sudo apt-get install -f
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install software-center
sudo apt-get install ~/Downloads/thepackage.deb
```

As one might recall, chrome's automatic version booster got us in this whole
mess to begin wtih.

----------
DROPBOX

a MASSIVE pain in the ass. You can download the debian package off their
website. But to set up all of its indexing, the daemon apparently needs to
first download LITERALLY EVERYTHING IN YOUR FUCKING DROPBOX.

This is because you apparently cannot selective-sync away particular
directories before having first downloaded them. IMO, this is an obvious bug
that someone should fix.

See for instance discussion
https://www.dropbox.com/help/syncing-uploads/selective-sync-overview#troubleshooting
which says "Wait until the folder has uploaded completely (it displays the
green checkmark) before unselecting it in your selective sync settings."

There is also:
"""
If you're running the Dropbox desktop application for the first time, you may
have to wait until Dropbox has finished indexing the files in your Dropbox
folder before you can access selective sync settings. If you see a message that
says "Performing initial sync with server. Please wait...," it means the
Dropbox desktop application is in the process of indexing the files in your
Dropbox folder or you have paused syncing from the Dropbox menu. You can choose
to wait until indexing is complete to access your selective sync settings.
Otherwise, select Cancel to dismiss the message and return to your preferences
window. If you have paused syncing, you can resume syncing via the Dropbox
menu.

Dropbox will continue indexing (as indicated by the icon with rotating arrows
over your Dropbox icon) and you'll still be able to browse and change other
preferences while Dropbox finishes.
"""

If you try to select-sync away anything before doing this (e.g., through
`preferences->selective sync`, whether from the daemon GUI or from cmd-line via

```
/path/to/dropbox.py exclude add ~/Dropbox/path/to/folder/
```

using their "Dropbox command line instructions script", the observed behavior I
get is that your syncing immediately breaks.

Looking at the files in the ~/Dropbox folder, all "green check marks" or
"spinning blue wheels" immediately disappear (e.g., upon the command line
instruction issuance), and the daemon freezes. If you try to turn it off,
and reboot it, the dialogue says "Starting..." indefinitely.

OK, great.

So assuming that downloading everything in my dropbox is a necessary
prerequisite to actually having a functional installation (tricky, b/c the ~Tb
of info I have on dropbox exceeds my harddrive capacity), I moved my dropbox
folder to my 3Tb external HDD. Fortunately, I can move the dropbox folder after
purging all dropbox files, unlinking from the website, and reinstalling.

It might work then???


----------
GET VIM, CONFIGURE IT

https://github.com/lgbouma/dot_files

```
sudo add-apt-repository ppa:jonathonf/vim
sudo apt update
sudo apt install vim
```

vim 8.0 o yes.

But then, also need VUNDLE:
https://github.com/VundleVim/Vundle.vim

And to install all your plugins.

(NB seems like YouCompleteMe fails out of the get-go, but there are certainly
atlernatives)


----------
UBUNTU THINGS

* 16.04 wonky graphics driver stuff that breaks when screen goes dark.

Quickfix:
```
compiz --replace
```


* Hide time, but display date
```
dconf write /com/canonical/indicator/datetime/time-format "'custom'"
dconf write /com/canonical/indicator/datetime/custom-time-format "'%a %d %h'"
```
format as in http://manpages.ubuntu.com/manpages/zesty/en/man3/strftime.3.html.

To reset:
```
dconf reset /com/canonical/indicator/datetime/time-format 
dconf reset /com/canonical/indicator/datetime/custom-time-format 
```

----------
need to install public/private ssh key so that you can be seen on @astro.princeton.


----------
TEX THINGS
`texlive-full` :
	```
	sudo add-apt-repository ppa:jonathonf/texlive-2017
	sudo apt-get update
	sudo apt-get install texlive-full
	```

texstudio

----------
ZOTERO

from `https://github.com/smathot/zotero_installer`,

sudo add-apt-repository ppa:smathot/cogscinl
sudo apt-get update
sudo apt-get install zotero-standalone

----------
DS9

follow description here:

http://spacepioneers.in/installing-sao-ds9-on-ubunutu-16-04-lts/

----------
SSH KEYS

1. run ssh-keygen to get a private and public rsa key
2. add public keys from things u want to tunnel in thru (e.g., laptop to
   workstation) to the `~/.ssh/authorized_keys` file.
3. make sure the latter has permissions s.t. only u can change


----------
GIMP

sudo add-apt-repository ppa:otto-kesselgulasch/gimp-edge
sudo apt update && sudo apt install gimp gimp-gmic
sudo apt install ppa-purge && sudo ppa-purge ppa:otto-kesselgulasch/gimp-edge

the latter reverts to the stable GIMP 2.8.16

----------
inkscape studio

----------
your python distribution, anaconda build etc should be accessible via
Dropbox/miniconda3

(though this breaks and TBH is kind of a bad idea)

----------
your symlink setup is thru Dropbox/dot_files, and the dotfile setup is
preserved in crispy_symlinks.png

symlinks within Dropbox might break. proj_symlinks.png gives the important
ones.

if starting from scratch, you'll have broken any special fancy local shit
you've installed.

E.g.:
AstroImageJ
cdsclient
alglib
boost
boost_serialization
eigen
share/fftw-3.3.3

and probably a bunch of reinstallables from /usr/lib

Notably, reinstalling POET will be a pain.
So might Gaia tools.


==================

>> lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:  Ubuntu 15.04
Release:  15.04
Codename: vivid

We're doing an EOL upgrade from 15.040>16.04

following  https://help.ubuntu.com/community/EOLUpgrades/

and relatedly
https://askubuntu.com/questions/91815/how-to-install-software-or-upgrade-from-an-old-unsupported-release



