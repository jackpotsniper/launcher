# Jackpot Sniper Launcher
Due to the Google Web Store (GWS) policies, [Jackpot Sniper](https://github.com/jackpotsniper/extension) can't be published to the GWS and it needs to be downloaded from Github and ran as 'unpacked extension'. That's a bit too geeky and complex. Here comes a simple launcher which removes all that complexity and makes it super easy to run Chrome with Jackpot Sniper.

## What it does
The launcher is quite simple and it olny does two things:
- updates the Jackpot Sniper extension to the latest version if needed
- starts a new Chrome window, in a dedicated user profile, with the Jackpot Sniper extension loaded in it

## Which variant to choose
The launcher is distributed as a binary (executable) file as well as open source for those who prefer such option. There's no difference in functionality, they all do the same.

<a name="open-source"></a>
### Open Source
If you are not a fan of binary files, feel free to download shell script `jackpot-sniper.sh` or Python variant `jackpot-sniper.py` of the launcher. Once you downloaded your preferred variant, you need to make it executable by running this command in the same location where the file is located: `chmod +x jackpot-sniper.sh`. This won't start Chrome yet but it will make possible to run the script. Now you should be able to run it by double click or with a command `./jackpot-sniper.sh`.

### Windows ###
If you are on Windows your best bet is `jackpot-sniper.msi` which can be downloaded from the [latest release](https://github.com/jackpotsniper/launcher/releases). It's a standard installer which installs executable binary and creates a desktop shortcut. It doesn't require any special permissions even though Windows will ask you to approve "*changes to the system*" => well, it just extracts executable from the installer, not really changes to the system. Once installed, Jackpot Sniper can be started with a desktop shortcut.

### Mac OS ###
The binary for Mac OS is comming in near future. For now, your best bet is to download shell script `jackpot-sniper.sh` from the latest release or from `src` folder. Look at the paragraph [Open Source](#open-source).

### Linux ###
As usual, if you are on Linux you've got more options to choose from. One would be the binary `jackpot-sniper.bin` or any [open source](#open-source) variant.