# Scrambler


  ░████╗░██╗░████╗░░█╗░██╗░░██╗████╗░█╗░░░█████╗████╗░
  ██╔══╝█══█╗█╔══█╗█═█╗███╗███║█╔═██╗█║░░░█╔═══╝█╔══█╗
  ╚███╗░█░░═╝████╔╝███║█╔███╔█║████╦╝█║░░░███╗░░████╔╝
  ░╚═██╗█░░█╗█╔══█╗█═█║█║╚█╔╝█║█╔═██╗█║░░░█╔═╝░░█╔══█╗
  ████╔╝╚██╔╝█║░░█║█░█║█║░╚╝░█║████╦╝████╗█████╗█║░░█║
  ╚═══╝░╚══╝░╚═╝░╚═╝╚╝░░░░╚═╝╚════╝░╚════╝╚════╝╚╝░░╚╝

This is a program that is used to scramble/encrypt files on your computer.
Do not use this program to do malicious things with.
I am not responsible for any damage that you do with this software.

**To Run the Program Use the following commands:** <br />
 <br />
***Linux:*** <br />
python -m virtualenv env <br />
source env/bin/activate <br />
pip install -r requirements.txt <br />
python file_encryption.py --help<br />

***Windows:*** <br />
python -m virtualenv env <br />
.\env\Scripts\activate <br />
pip install -r requirements.txt <br />
python file_encryption.py --help<br />

***Deactivating Virtual Environment Linux/Windows:*** <br />
deactivate <br />


In order to run the tests run this command from the root directory of the project.

'''python -m unittest -v tests/test_file_encryption.py'''
