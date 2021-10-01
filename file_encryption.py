import sys
import pickle
import click
import pdb  
import os
import hashlib
from Cryptodome.Cipher import AES
from tkinter import filedialog as fd

# ---------------------------- MAIN WITH ALL OF THE GROUP COMMANDS -------------------
@click.group()
def main():
    """ ░██████╗░█████╗░██████╗░░█████╗░███╗░░░███╗██████╗░██╗░░░░░███████╗██████╗░
        ██╔════╝██╔══██╗██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░░░██╔════╝██╔══██╗
        ╚█████╗░██║░░╚═╝██████╔╝███████║██╔████╔██║██████╦╝██║░░░░░█████╗░░██████╔╝
        ░╚═══██╗██║░░██╗██╔══██╗██╔══██║██║╚██╔╝██║██╔══██╗██║░░░░░██╔══╝░░██╔══██╗
        ██████╔╝╚█████╔╝██║░░██║██║░░██║██║░╚═╝░██║██████╦╝███████╗███████╗██║░░██║
        ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚══════╝╚═╝░░╚═╝

                 ___The program is designed to scramble(encrypt) files___ 
        """
# ----------------------- FUNCTIONS TO ASSIST WITH THE PROCESS ---------------------------------


# ----------------------- Reading and Writing the Keys ---------------------------------
# returns a hash of the file that it is given
def hash_file(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4k
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        hashed_file = sha256_hash.hexdigest()
    return hashed_file

# performes a secure delete
def secure_delete(file_path, passes=4):
    try:
        with open(file_path, "ba+") as delfile:
            length = delfile.tell()
        with open(file_path, "br+") as delfile:
            for i in range(passes):
                delfile.seek(0)
                delfile.write(os.urandom(length))
        os.remove(file_path)
    except: os.remove(file_path)

# Recieves a directory and a key_size and creates a key and initialization vector for the aes encryption and saves it to a pickle file
def write_key(directory, key_size, unencrypted_file_path=''):
    # Extracting the necessary components from the cipher to decrypt with
    pickled_key = {"iv":os.urandom(16), "key":os.urandom(int(key_size)//8)}
    with open(os.path.join(directory, f'{os.path.split(unencrypted_file_path)[1]}{key_size}_bit_key.key'), "wb") as pickle_file:
        pickle.dump(pickled_key, pickle_file)

# Returns the key in bytes from file selection
def load_key(file_name):
    """
    Loads the key from the current directory named 'key.key'
    """
    with open(file_name, "rb") as pickle_file:
        return pickle.load(pickle_file)

# -------------------------------------- encryption and decryption --------------------------------------

# FOR THE ENCRYPTION AND THE DECRYPTION I AM GOING TO HAVE TO USE THIS LIBRARY BELOW
# https://pycryptodome.readthedocs.io/en/latest/src/examples.html

# This function recieves a key and a file path and decrypts that file and outputs a copy called the original files name + _decrypted on the end
def decrypt_data(key, file_path, mode):
    if mode == "AES":
        try:
            # decrypting data
            # if the file_path is not absolute make it absolute
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # decrypt data
            with open(file_path, "rb") as encrypted_file:

                cipher = AES.new(key["key"], iv=key["iv"], mode=AES.MODE_CFB)
                decrypted_data = cipher.decrypt(encrypted_file.read())

                # Write the file with the correct unique filename
                temp_path = os.path.join(os.path.split(file_path)[0], os.path.split(file_path)[1].replace("_encrypted", "", 1))
                with open(temp_path, "wb") as decrypted_file:
                    decrypted_file.write(decrypted_data)
            click.echo(f'Decrypted {file_path}') 

            # delete the data
            secure_delete(file_path)
        except FileNotFoundError:
            click.echo(f'File Not Found Error: {file_path}')
    else:
        click.echo("Only AES is supported at the moment...")

# This function recieves a key and a file path and encrypts that file and outputs a copy called the original files name + _encrypted on the end
def encrypt_data(key, file_path, mode):
    try:
        # Recommended encryption from https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
        if mode == "AES":
            cipher = AES.new(key["key"], iv=key["iv"], mode=AES.MODE_CFB)
            # encrypting data and writing data to the encrypted file
            with open(file_path, "rb") as unencrypted_file:
                encrypted_data = cipher.encrypt(unencrypted_file.read())
                with open(os.path.join(os.path.split(file_path)[0], os.path.split(file_path)[1] + "_encrypted"), "wb") as encrypted_file:
                    encrypted_file.write(encrypted_data)
            click.echo(f'Encrypted {file_path}') 
            # Delete the original file
            secure_delete(file_path)
            return True
        else:
            click.echo("AES is only supported at the moment...")
    except OSError:
        click.echo(f'Skipping OSError: {file_path}') 
        return False
    except FileNotFoundError:
        click.echo(f'Skipping FileNotFoundError: {file_path}') 
        return False

def directory_encrypt(directory, key_size, mode, pickle_key={}):
    for x in os.listdir(directory):
        if ("scrambler" not in directory.lower()) and ("scrambler" not in x.lower()):
            if os.path.isdir(os.path.join(directory, x)):
                # Check to see if python is contained in the folder path. if it is do not attempt to encrypt any of the below folders or files
                directory_encrypt(os.path.join(directory, x), key_size, mode, pickle_key)
            # to make sure that the file is a file and that its name is not the encryption program name 
            elif os.path.isfile(os.path.join(directory, x)):
                # making an exclude keyword list to make sure that none of the keywords lowered in the list are in the directorypath at all 
                # create a key and encrypt the file
                key = {"iv":os.urandom(16), "key":os.urandom(int(key_size)//8)}
                if "keychain" not in x.lower():
                    test = encrypt_data(key, os.path.join(directory,x), mode)
                else:
                    test = False

                # if the file encrypted correctly without errors then hash it and save the key
                if test:
                    # Hashing the encryptedfile 
                    file_path = os.path.join(directory, x)
                    hashed_file = hash_file(file_path + "_encrypted")

                    # assigning the hash of the encrypted file to the key to decrypt it with
                    pickle_key[hashed_file] = key
    return pickle_key

def directory_decrypt(directory, key, mode):
    for x in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, x)):
            directory_decrypt(os.path.join(directory, x), key, mode)
        elif os.path.isfile(os.path.join(directory, x)):
            # find the hash of the file
            hashed_file = hash_file(os.path.join(directory, x))

            # extract the key dictionary
            with open(key, 'rb') as pickled_key:
                keychain = pickle.load(pickled_key)

            # if the key exists in the dictionary
            if hashed_file in keychain.keys():
                decrypt_data(keychain[hashed_file], os.path.join(directory, x), mode)

# -------------------------------------- COMMANDS --------------------------------------

# -------------------------------------- Generate Key Command --------------------------------------

@main.command()
@click.option("--location", default=os.getcwd(),
        help="Specify a location for where the key will be located. Default is the current directory that this file is run in.")
@click.option("--key-size", default="256", type=click.Choice(["128", "256"]),
        help="This is an option to select if you want to specify the key size to generate. By default it is 128 bits.")
def generate_key(location, key_size):
    """
    'python <file> generate_key --help'\n
    Generates a key and save it into a file in the current directory by default
    """
    write_key(location, key_size)

# -------------------------------------- encrypt command --------------------------------------

@main.command()
@click.option('--directory', '-d', default=None, required=False,
        help="Very versitile feature that allows for you to encrypt a directory and all sub directories. All of the keys are saved to a dictionary that which each key corresponds with the hash of the encrypted file it belongs to. I call this the key ring. This can later be used to decrypt any file that matches its corresponding key.")

@click.option("--key-path","-k", default=None, 
        help="If this option if used then it is expecting for the user to enter the full file path for where the key is located. If none is specified then filedialogue will appear for you to pick the file for where the key is located.")
@click.option("--mode", default="AES", type=click.Choice(["AES"]),
        help="If this option is checked you can choose from a list of different options for encryption. The default value is set to AES encryption.")
@click.option("--key-size", default="256", type=click.Choice(["128", "256"]),
        help="If this option is checked you can choose from a list of different options for your choice of keysize for the key that you will use to encrypt the file.")
@click.option("--file-path", "-f", default=None,
        help="This option allows the user to enter the direct file path that they want to encrypt. If none is specified a tkinter file dialog will pop up and ask for the filepath to the file that they want to encrypt.")
def encrypt(directory, key_path, mode, key_size, file_path):
    """
    'python file_encryption.py encrypt --help'\n
    This is a command that you can use to encrypt a single file or every file in a directory if specified with the --directory command. This fucniton works by using one key for each file to do all of the encrypting and then spits eacho of the keys out for all of the files encrypted in the directory into a single KeyChain file that you can use to decrypt once the program is finished encrypting. You can supply your own key if you want with the --key command.
    \n--------------------------------------------------------------\n
    WARNING: DO NOT STOP THE PROGRAM ONCE RUN WITH DIRECTORY MODE!
    IF YOU TRY TO STOP THE PROGRAM WHILE IT IS ENCRYPTING THE KEY WILL NOT BE GENERATED FOR THE FILES THAT IT HAS ALREADY ENCRYPTED. THE FEATURE TO HAVE IT GENERATE A KEY ON FAILURE TO COMPLETE THE PROGRAM IS PLANNED TO BE ADDED IN A FUTURE RELEASE
    """
    # To make sure the user did not choose a value for directory and filepath
    if (directory != None) and (file_path != None):
        click.echo("You cannot select an option for both --directory and --file_path")
    elif directory == None:
        # Key Stuff
        if file_path == None:
            file_path = fd.askopenfilename(title="Select the file to encrypt")
        # if no key path one is created and 
        if key_path == None:
            # Ask for key to be returned in binary format for sending to decryption funciton
            write_key(directory=os.path.split(file_path)[0], key_size=key_size, unencrypted_file_path=file_path)
            key = load_key(fd.askopenfilename(title="Select the newly generated key", initialdir=os.path.split(file_path)[0]))
        else:
            # Ask for key to be returned in binary format for sending to decryption funciton with the keypath provided from the command line tool the 
            key = load_key(key_path)

        # encrpyting now
        print("Encrypting your file...")
        encrypt_data(key, file_path, mode)
        print("File Encrypted")
    else:        
        # Directory encrypt then writing the key with the correct name so it doesnt overwrite any other previously generated keys
        x = directory_encrypt(directory, key_size, mode)
        i = 1
        name = "KeyChain" 
        if os.path.exists(os.path.join(directory, name)):
            while os.path.exists(os.path.join(directory, f'KeyChain{i}')):
                i += 1
            name = f'KeyChain{i}'
        with open(os.path.join(directory, name), "wb") as pickled_key:
            pickle.dump(x, pickled_key)
        click.echo("Done!")

# -------------------------------------- decrypt command --------------------------------------

@main.command()
@click.option('--directory', '-d',  default=None,
        help="Selecting this lets you decrypt with a corresponding keychain. You can select a keychain dictionary pickle file that corresponds to a previously encrypted directory and use that to select any directory of your choice. Once you select anotther directory this program will then scan that directory recursively trying to match each of the files hash to see if it exists inside of the keychain. If it does not exist inside of the python dictionary keychain then the file is simply skipped and not attempted to be decrypted. If a match is found it will be decrypted with its corresponding key found in the un-pickled dictionary keychain.")

@click.option("--key-path","-k", default=None, 
        help="If this option if used then it is expecting for the user to enter the full file path for where the key is located. If none is specified then filedialogue will appear for you to pick the file for where the key is located.")
@click.option("--mode", default="AES", type=click.Choice(["AES"]),
        help="If this option is checked you can choose from a list of different options for decryption. The default value is set to AES decryption.")
@click.option("--file-path","-f", default=None,
        help="This is the option to enter the direct filepath to the file you would like to decrypt. If this is none and you did not select directory then you will be promted to select the file in a tkinter file dialogue")
# this is the command function 
def decrypt(directory, key_path, mode, file_path):
    """
    'python file_encryption.py decrypt --help'\n
    This is a command that you can use to decrypt a single file or every file in a directory if specified with the --directory command. This fucniton works by using one key for each file to do all of the encrypting and then spits eacho of the keys out for all of the files encrypted in the directory into a single KeyChain file that you can use to decrypt once the program is finished encrypting. You can supply your own key if you want with the --key command.\n
    Note: A key feature for this program is that if you have previously done a directory decrypt you can also use that key to decrypt any of the files in that directory by itself with the single file decrypt option
    """
    # To make sure the user did not choose a value for directory and filepath
    if (directory != None) and (file_path != None):
        click.echo("You cannot select an option for both --directory and --file_path")
    # for file encryption
    elif directory == None:
        # the default option
        if file_path == None:
            file_path = fd.askopenfilename(title="select the encrypted file")

        # if user did not enter ask 
        if key_path == None:
            key_path = fd.askopenfilename(title="Select the key", initialdir=os.path.split(file_path)[0])
            # load the key and decrypt
            key = load_key(key_path)
            decrypt_data(key, file_path, mode)
            click.echo("Done!")
        else:
            # find the hash of the file
            # Read and update hash string value in blocks of 4k
            hashed_file = hash_file(file_path)
            decrypt_data(load_key(key_path)[hashed_file], file_path, mode)
            click.echo("Done!")

    elif file_path == None:
        # if user did not enter ask for key
        if key_path == None:
            key_path = fd.askopenfilename(title="Select the key", initialdir=directory)
        # for directory encryption
        directory_decrypt(directory, key_path, mode)
        click.echo("Done!")

# -------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    main.add_command(decrypt)
    main.add_command(encrypt)
    main.add_command(generate_key)
    main()
