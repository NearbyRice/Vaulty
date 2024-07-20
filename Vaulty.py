import os
import json
from datetime import datetime
import sys
from cryptography.fernet import Fernet
import base64
import shutil
import time
import tkinter as tk
from tkinter import filedialog
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def run_as_admin():
    if is_admin():
        print("Already running as administrator.")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def generate_symmetric_key():
    return Fernet.generate_key()

def symmetric_encrypt(file_data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_data)
    return encrypted_data

def symmetric_decrypt(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data

def set_default_app():
    # TODO: Implement setting default app for .ACC extension
    pass

def zip_folders_in_safe():
    safe_folder = os.path.join(os.getcwd(), '.privacySafe', '.safe')

    folders_found = False

    for item in os.listdir(safe_folder):
        item_path = os.path.join(safe_folder, item)
        if os.path.isdir(item_path):
            # Create a unique zip file name based on the current timestamp
            zip_file_name = f"{item}.zip"
            zip_file_path = os.path.join(safe_folder, zip_file_name)

            # Zip the folder
            shutil.make_archive(zip_file_path[:-4], 'zip', item_path)
            
            # Remove the original folder
            shutil.rmtree(item_path)

            folders_found = True

    if not folders_found:
        return

def create_folders():
    privacy_safe_folder = os.path.join(os.getcwd(), '.privacySafe')
    folders = ['.db', '.safe', '.temp']
    for folder in folders:
        folder_path = os.path.join(privacy_safe_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

def create_index_json():
    privacy_safe_folder = os.path.join(os.getcwd(), '.privacySafe')
    if not os.path.exists(privacy_safe_folder):
        os.makedirs(privacy_safe_folder)

    create_folders()

    db_folder = os.path.join(privacy_safe_folder, '.db')
    index_path = os.path.join(db_folder, 'index.json')


    if not os.path.exists(index_path):
        # Create index.json with initial data
        initial_data = {"files": []}
        with open(index_path, 'w') as index_file:
            json.dump(initial_data, index_file)


def get_file_type(file_extension, default_type=9):
    # Define file type based on extension
    code_extensions = ['.abap', '.asc', '.ash', '.ampl', '.mod', '.g4', '.apib', '.apl', '.dyalog', '.asp', '.asax', '.ascx', '.ashx', '.asmx', '.aspx', '.axd', '.dats', '.hats', '.sats', '.as', '.adb', '.ada', '.ads', '.agda', '.als', '.apacheconf', '.vhost', '.cls', '.applescript', '.scpt', '.arc', '.ino', '.asciidoc', '.adoc', '.asc', '.aj', '.asm', '.a51', '.inc', '.nasm', '.aug', '.ahk', '.ahkl', '.au3', '.awk', '.auk', '.gawk', '.mawk', '.nawk', '.bat', '.cmd', '.befunge', '.bison', '.bb', '.bb', '.decls', '.bmx', '.bsv', '.boo', '.b', '.bf', '.brs', '.bro', '.c', '.cats', '.h', '.idc', '.w', '.cs', '.cake', '.cshtml', '.csx', '.cpp', '.c++', '.cc', '.cp', '.cxx', '.h', '.h++', '.hh', '.hpp', '.hxx', '.inc', '.inl', '.ipp', '.tcc', '.tpp', '.c-objdump', '.chs', '.clp', '.cmake', '.cmake.in', '.cob', '.cbl', '.ccp', '.cobol', '.cpy', '.css', '.csv', '.capnp', '.mss', '.ceylon', '.chpl', '.ch', '.ck', '.cirru', '.clw', '.icl', '.dcl', '.click', '.clj', '.boot', '.cl2', '.cljc', '.cljs', '.cljs.hl', '.cljscm', '.cljx', '.hic', '.coffee', '._coffee', '.cake', '.cjsx', '.cson', '.iced', '.cfm', '.cfml', '.cfc', '.lisp', '.asd', '.cl', '.l', '.lsp', '.ny', '.podsl', '.sexp', '.cp', '.cps', '.cl', '.coq', '.v', '.cppobjdump', '.c++-objdump', '.c++objdump', '.cpp-objdump', '.cxx-objdump', '.creole', '.cr', '.feature', '.cu', '.cuh', '.cy', '.pyx', '.pxd', '.pxi', '.d', '.di', '.d-objdump', '.com', '.dm', '.zone', '.arpa', '.d', '.darcspatch', '.dpatch', '.dart', '.diff', '.patch', '.dockerfile', '.djs', '.dylan', '.dyl', '.intr', '.lid', '.E', '.ecl', '.eclxml', '.ecl', '.sch', '.brd', '.epj', '.e', '.ex', '.exs', '.elm', '.el', '.emacs', '.emacs.desktop', '.em', '.emberscript', '.erl', '.es', '.escript', '.hrl', '.xrl', '.yrl', '.fs', '.fsi', '.fsx', '.fx', '.flux', '.f90', '.f', '.f03', '.f08', '.f77', '.f95', '.for', '.fpp', '.factor', '.fy', '.fancypack', '.fan', '.fs', '.for', '.eam.fs', '.fth', '.4th', '.f', '.for', '.forth', '.fr', '.frt', '.fs', '.ftl', '.fr', '.g', '.gco', '.gcode', '.gms', '.g', '.gap', '.gd', '.gi', '.tst', '.s', '.ms', '.gd', '.glsl', '.fp', '.frag', '.frg', '.fs', '.fsh', '.fshader', '.geo', '.geom', '.glslv', '.gshader', '.shader', '.vert', '.vrx', '.vsh', '.vshader', '.gml', '.kid', '.ebuild', '.eclass', '.po', '.pot', '.glf', '.gp', '.gnu', '.gnuplot', '.plot', '.plt', '.go', '.golo', '.gs', '.gst', '.gsx', '.vark', '.grace', '.gradle', '.gf', '.gml', '.graphql', '.dot', '.gv', '.man', '.1', '.1in', '.1m', '.1x', '.2', '.3', '.3in', '.3m', '.3qt', '.3x', '.4', '.5', '.6', '.7', '.8', '.9', '.l', '.me', '.ms', '.n', '.rno', '.roff', '.groovy', '.grt', '.gtpl', '.gvy', '.gsp', '.hcl', '.tf', '.hlsl', '.fx', '.fxh', '.hlsli', '.html', '.htm', '.html.hl', '.inc', '.st', '.xht', '.xhtml', '.mustache', '.jinja', '.eex', '.erb', '.erb.deface', '.phtml', '.http', '.hh', '.php', '.haml', '.haml.deface', '.handlebars', '.hbs', '.hb', '.hs', '.hsc', '.hx', '.hxsl', '.hy', '.bf', '.pro', '.dlm', '.ipf', '.ini', '.cfg', '.prefs', '.pro', '.properties', '.irclog', '.weechatlog', '.idr', '.lidr', '.ni', '.i7x', '.iss', '.io', '.ik', '.thy', '.ijs', '.flex', '.jflex', '.json', '.geojson', '.lock', '.topojson', '.json5', '.jsonld', '.jq', '.jsx', '.jade', '.j', '.java', '.jsp', '.js', '._js', '.bones', '.es', '.es6', '.frag', '.gs', '.jake', '.jsb', '.jscad', '.jsfl', '.jsm', '.jss', '.njs', '.pac', '.sjs', '.ssjs', '.sublime-build', '.sublime-commands', '.sublime-completions', '.sublime-keymap', '.sublime-macro', '.sublime-menu', '.sublime-mousemap', '.sublime-project', '.sublime-settings', '.sublime-theme', '.sublime-workspace', '.sublime_metrics', '.sublime_session', '.xsjs', '.xsjslib', '.jl', '.ipynb', '.krl', '.sch', '.brd', '.kicad_pcb', '.kit', '.kt', '.ktm', '.kts', '.lfe', '.ll', '.lol', '.lsl', '.lslp', '.lvproj', '.lasso', '.las', '.lasso8', '.lasso9', '.ldml', '.latte', '.lean', '.hlean', '.less', '.l', '.lex', '.ly', '.ily', '.b', '.m', '.ld', '.lds', '.mod', '.liquid', '.lagda', '.litcoffee', '.lhs', '.ls', '._ls', '.xm', '.x', '.xi', '.lgt', '.logtalk', '.lookml', '.ls', '.lua', '.fcgi', '.nse', '.pd_lua', '.rbxs', '.wlua', '.mumps', '.m', '.m4', '.m4', '.ms', '.mcr', '.mtml', '.muf', '.m', '.mak', '.d', '.mk', '.mkfile', '.mako', '.mao', '.md', '.markdown', '.mkd', '.mkdn', '.mkdown', '.ron', '.mask', '.mathematica', '.cdf', '.m', '.ma', '.mt', '.nb', '.nbp', '.wl', '.wlt', '.matlab', '.m', '.maxpat', '.maxhelp', '.maxproj', '.mxt', '.pat', '.mediawiki', '.wiki', '.m', '.moo', '.metal', '.minid', '.druby', '.duby', '.mir', '.mirah', '.mo', '.mod', '.mms', '.mmk', '.monkey', '.moo', '.moon', '.myt', '.ncl', '.nl', '.nsi', '.nsh', '.n', '.axs', '.axi', '.axs.erb', '.axi.erb', '.nlogo', '.nl', '.lisp', '.lsp', '.nginxconf', '.vhost', '.nim', '.nimrod', '.ninja', '.nit', '.nix', '.nu', '.numpy', '.numpyw', '.numsc', '.ml', '.eliom', '.eliomi', '.ml4', '.mli', '.mll', '.mly', '.objdump', '.m', '.h', '.mm', '.j', '.sj', '.omgrofl', '.opa', '.opal', '.cl', '.opencl', '.p', '.cls', '.scad', '.org', '.ox', '.oxh', '.oxo', '.oxygene', '.oz', '.pwn', '.inc', '.php', '.aw', '.ctp', '.fcgi', '.inc', '.php3', '.php4', '.php5', '.phps', '.phpt', '.pls', '.pck', '.pkb', '.pks', '.plb', '.plsql', '.sql', '.sql', '.pov', '.inc', '.pan', '.psc', '.parrot', '.pasm', '.pir', '.pas', '.dfm', '.dpr', '.inc', '.lpr', '.pp', '.pl', '.al', '.cgi', '.fcgi', '.perl', '.ph', '.plx', '.pm', '.pod', '.psgi', '.t', '.6pl', '.6pm', '.nqp', '.p6', '.p6l', '.p6m', '.pl', '.pl6', '.pm', '.pm6', '.t', '.pkl', '.l', '.pig', '.pike', '.pmod', '.pod', '.pogo', '.pony', '.ps', '.eps', '.ps1', '.psd1', '.psm1', '.pde', '.pl', '.pro', '.prolog', '.yap', '.spin', '.proto', '.asc', '.pub', '.pp', '.pd', '.pb', '.pbi', '.purs', '.py', '.bzl', '.cgi', '.fcgi', '.gyp', '.lmi', '.pyde', '.pyp', '.pyt', '.pyw', '.rpy', '.tac', '.wsgi', '.xpy', '.pytb', '.qml', '.qbs', '.pro', '.pri', '.r', '.rd', '.rsx', '.raml', '.rdoc', '.rbbas', '.rbfrm', '.rbmnu', '.rbres', '.rbtbar', '.rbuistate', '.rhtml', '.rmd', '.rkt', '.rktd', '.rktl', '.scrbl', '.rl', '.raw', '.reb', '.r', '.r2', '.r3', '.rebol', '.red', '.reds', '.cw', '.rpy', '.rs', '.rsh', '.robot', '.rg', '.rb', '.builder', '.fcgi', '.gemspec', '.god', '.irbrc', '.jbuilder', '.mspec', '.pluginspec', '.podspec', '.rabl', '.rake', '.rbuild', '.rbw', '.rbx', '.ru', '.ruby', '.thor', '.watchr', '.rs', '.rs.in', '.sas', '.scss', '.smt2', '.smt', '.sparql', '.rq', '.sqf', '.hqf', '.sql', '.cql', '.ddl', '.inc', '.prc', '.tab', '.udf', '.viw', '.sql', '.db2', '.ston', '.svg', '.sage', '.sagews', '.sls', '.sass', '.scala', '.sbt', '.sc', '.scaml', '.scm', '.sld', '.sls', '.sps', '.ss', '.sci', '.sce', '.tst', '.self', '.sh', '.bash', '.bats', '.cgi', '.command', '.fcgi', '.ksh', '.sh.in', '.tmux', '.tool', '.zsh', '.sh-session', '.shen', '.sl', '.slim', '.smali', '.st', '.cs', '.tpl', '.sp', '.inc', '.sma', '.nut', '.stan', '.ML', '.fun', '.sig', '.sml', '.do', '.ado', '.doh', '.ihlp', '.mata', '.matah', '.sthlp', '.styl', '.sc', '.scd', '.swift', '.sv', '.svh', '.vh', '.toml', '.txl', '.tcl', '.adp', '.tm', '.tcsh', '.csh', '.tex', '.aux', '.bbx', '.bib', '.cbx', '.cls', '.dtx', '.ins', '.lbx', '.ltx', '.mkii', '.mkiv', '.mkvi', '.sty', '.toc', '.tea', '.t', '.txt', '.fr', '.nb', '.ncl', '.no', '.textile', '.thrift', '.t', '.tu', '.ttl', '.twig', '.ts', '.tsx', '.upc', '.anim', '.asset', '.mat', '.meta', '.prefab', '.unity', '.uno', '.uc', '.ur', '.urs', '.vcl', '.vhdl', '.vhd', '.vhf', '.vhi', '.vho', '.vhs', '.vht', '.vhw', '.vala', '.vapi', '.v', '.veo', '.vim', '.vb', '.bas', '.cls', '.frm', '.frx', '.vba', '.vbhtml', '.vbs', '.volt', '.vue', '.owl', '.webidl', '.x10', '.xc', '.xml', '.ant', '.axml', '.ccxml', '.clixml', '.cproject', '.csl', '.csproj', '.ct', '.dita', '.ditamap', '.ditaval', '.dll.config', '.dotsettings', '.filters', '.fsproj', '.fxml', '.glade', '.gml', '.grxml', '.iml', '.ivy', '.jelly', '.jsproj', '.kml', '.launch', '.mdpolicy', '.mm', '.mod', '.mxml', '.nproj', '.nuspec', '.odd', '.osm', '.plist', '.pluginspec', '.props', '.ps1xml', '.psc1', '.pt', '.rdf', '.rss', '.scxml', '.srdf', '.storyboard', '.stTheme', '.sublime-snippet', '.targets', '.tmCommand', '.tml', '.tmLanguage', '.tmPreferences', '.tmSnippet', '.tmTheme', '.ts', '.tsx', '.ui', '.urdf', '.ux', '.vbproj', '.vcxproj', '.vssettings', '.vxml', '.wsdl', '.wsf', '.wxi', '.wxl', '.wxs', '.x3d', '.xacro', '.xaml', '.xib', '.xlf', '.xliff', '.xmi', '.xml.dist', '.xproj', '.xsd', '.xul', '.zcml', '.xsp-config', '.xsp.metadata', '.xpl', '.xproc', '.xquery', '.xq', '.xql', '.xqm', '.xqy', '.xs', '.xslt', '.xsl', '.xojo_code', '.xojo_menu', '.xojo_report', '.xojo_script', '.xojo_toolbar', '.xojo_window', '.xtend', '.yml', '.reek', '.rviz', '.sublime-syntax', '.syntax', '.yaml', '.yaml-tmlanguage', '.yang', '.y', '.yacc', '.yy', '.zep', '.zimpl', '.zmpl', '.zpl', '.desktop', '.desktop.in', '.ec', '.eh', '.edn', '.fish', '.mu', '.nc', '.ooc', '.rst', '.rest', '.rest.txt', '.rst.txt', '.wisp', '.prg', '.ch', '.prw']
    image_extensions = ['.png', '.jpeg', '.tiff', '.rif', '.jp2', '.webp', '.IIQ', '.DCR', '.K25', '.KDC', '.CRW', '.CR2', '.ERF', '.MEF', '.mos', '.nef', '.nrw', '.orf', '.pef', '.rw2', '.arw', '.srf', '.sr2', '.hdr', '.heif', '.avif', '.jxl', '.bmp', '.ppm', '.pgm', '.pbm', '.pnm', '.afphoto', '.cd5', '.clip', '.cpt', '.kra', '.mdp', '.pdn', '.psd', '.psp', '.sai', '.xcf', '.bpg', '.IFF-DEEP', '.drw', '.ecw', '.fits', '.flif', '.ico']
    video_extensions = ['.webm', '.mkv', '.flv', '.vob', '.ogv', '.drc', '.gif', '.gifv', '.mng', '.avi', '.mts', '.m2ts', '.ts', '.mov', '.qt', '.wmv', '.yuh', '.rm', '.rmvb', '.viv', '.asf', '.amv', '.mp4', '.m4p', '.m4v', '.mpg', '.mp3', '.mpeg', '.mpe', '.mpv', '.m2v', '.svi', '.3gp', '.3g2', '.mxf', '.roq', '.nsv', '.f4v', '.f4p', '.f4a', '.f4b']
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac']
    document_extensions = ['.doc', '.docx', '.html', '.htm', '.odt', '.pdf', '.xls', '.xlsx', '.ods', '.ppt', '.pptx', '.txt', '.text']
    archive_extensions = ['.zip', '.tar', '.gz', '.rar']
    installer_extensions = ['.msi', '.deb', '.rpm']
    executable_extensions = ['.exe', '.bin', '.sh', '.bat', '.cmd']

    if file_extension in code_extensions:
        return 4  # Code
    elif file_extension in image_extensions:
        return 3  # Image
    elif file_extension in video_extensions:
        return 2  # Video
    elif file_extension in audio_extensions:
        return 7  # Audio
    elif file_extension in document_extensions:
        return 1  # Document
    elif file_extension in archive_extensions:
        return 6  # Archive
    elif file_extension in installer_extensions:
        return 8  # Installer
    elif file_extension in executable_extensions:
        return 5  # Executable
    else:
        return default_type  # Files without extension

def update_index(file_path):
    # Create necessary folders in .privacySafe
    create_folders()

    db_folder = os.path.join(os.getcwd(), '.privacySafe', '.db')
    index_path = os.path.join(db_folder, 'index.json')

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)
        print("Loading index")

    # Get file information
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    file_type = get_file_type(file_extension)
    print(f"File Name: {str(file_name)}, File Extention: {str(file_extension)}, and File Type: {str(file_type)}")

    # Check if the file is stored in .safe
    safe_folder = os.path.join(os.getcwd(), '.privacySafe', '.safe')
    safe_file_path = os.path.join(safe_folder, file_name)

    if not os.path.exists(safe_file_path):
        # Log error
        error_log_path = os.path.join(db_folder, 'error_log.txt')
        error_message = f"Error: {file_name} is not stored in .safe folder."
        with open(error_log_path, 'a') as error_log:
            error_log.write(error_message + '\n')
        return

    # Check if the encrypted file already exists
    print(f"Checking if file {str(file_name)} is already in data base...")
    encrypted_file_path = os.path.join(safe_folder, os.path.splitext(file_name)[0] + '.ACC')
    if not os.path.exists(encrypted_file_path):
        # Read file data
        with open(safe_file_path, 'rb') as file:
            file_data = file.read()

        # Generate symmetric key
        print("Generating key...")
        key = generate_symmetric_key()

        # Encrypt file data
        print("Encrypting file...")
        encrypted_data = symmetric_encrypt(file_data, key)

        # Save encrypted data back to .safe with .ACC extension
        print("Saving file...")
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print("Adding entry...")
        # Add new entry to index
        entry = {
            "ID": file_type,
            "DATE": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "EID": 1,  # Symmetric encryption
            "KEY": key.decode('utf-8'),  # Store key as a string
            "OFN": file_name,
            "DL": encrypted_file_path,  # Store encrypted file location
        }

        index_data["files"].append(entry)

        # Update index file
        print("Updating index...")
        with open(index_path, 'w') as index_file:
            json.dump(index_data, index_file)

        # Remove the original file in .safe
        print("Removing original file...")
        os.remove(safe_file_path)

def check_memory_usage():
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return free_memory  # Assuming free memory is a suitable measure, you may adjust this based on your needs

def check_for_new_files():
    safe_folder = os.path.join(os.getcwd(), '.privacySafe', '.safe')
    index_path = os.path.join(os.getcwd(), '.privacySafe', '.db', 'index.json')

    with open(index_path, 'r') as index_file:
        index_data = json.load(index_file)

    existing_files = {entry['DL'] for entry in index_data['files']}
    new_files = []

    for file_name in os.listdir(safe_folder):
        file_path = os.path.join(safe_folder, file_name)
        if file_path not in existing_files:
            new_files.append(file_path)

    return new_files


def decrypt_file(file_path, key, encryption_type, original_file_name):
    # Create a temporary folder if it doesn't exist
    temp_folder = os.path.join(os.getcwd(), '.privacySafe', '.temp')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Copy the file to the temporary folder
    temp_file_path = os.path.join(temp_folder, original_file_name)
    shutil.copy(file_path, temp_file_path)

    # Decrypt the file
    with open(temp_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    if encryption_type == 1:  # Symmetric encryption
        decrypted_data = symmetric_decrypt(encrypted_data, key)
    else:
        tk.messagebox.showinfo("Information", "Unsupported encryption type")
        return

    # Save the decrypted data back to the file
    with open(temp_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    # Open the folder in file explorer
    os.system(f'explorer /select,{temp_file_path}')

    # Close the script
    sys.exit()


def argument():
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'decrypt':
        print("Decrypting...")
        # Open a file selector window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(title="Select the file to decrypt", filetypes=[("All Files", "*.*")])

        # Check if a file was selected
        if not file_path:   
            tk.messagebox.showinfo("NoFileSelected", "No file selected for decryption.")
            return
        
        create_folders()

        db_folder = os.path.join(os.getcwd(), '.privacySafe', '.db')
        index_path = os.path.join(db_folder, 'index.json')

        try:
            with open(index_path, 'r') as index_file:
                index_data = json.load(index_file)
                found = False    
            for entry in index_data["files"]:
                # Replace double backslashes and forward slashes with single backslashes
                normalized_data_location = entry["DL"].replace('\\\\', '\\').replace('/', '\\')
                normalized_file_path = file_path.replace('\\\\', '\\').replace('/', '\\')
                
                if normalized_data_location == normalized_file_path:
                    found = True
                    decrypt_file(file_path, entry["KEY"].encode('utf-8'), entry["EID"], entry["OFN"])

            if not found:
                tk.messagebox.showinfo("EntryNotFound", f"File not found in the index: {file_path}")
        except FileNotFoundError:
            tk.messagebox.showinfo("FileNotFound", index_path+" not found try place the program in your user folder")
    elif len(sys.argv) == 2 and sys.argv[1].lower() == 'encrypt':
        main()
    else:
        print("Usage: encrypt or decrypt \nExample: vaulty.py/exe decrypt/encrypt")

def show_info_box():
    info_text = "It's recommended that you place this file at your user root directory."

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a simple info box
    tk.messagebox.showinfo("Information", info_text)

def main():
    show_info_box()
    print("Running enryption...")
    # Create index.json if it doesn't exist
    create_index_json()
 
    while True:
        # Check for new files in .safe every 5 seconds
        zip_folders_in_safe()
        new_files = check_for_new_files()
        print("Checking for new files...")

        if new_files:
            for file_path in new_files:
                print(f"File found {str(file_path)}")
                update_index(file_path)

        time.sleep(5)

def encrypt_index(index_data):
    json_encryption_key = "b'kIxAQ_7ylm9nwtjiXdeMD-8nZnldbPbB27DzgNS8Qdo='"
    create_index_json()
    script_dir = os.path.dirname(__file__)
    db_folder = os.path.join(script_dir, '.privacySafe', '.db')
    index_path = os.path.join(db_folder, 'index.json')
    encrypt_index = symmetric_encrypt(index_data, json_encryption_key)
    with open(index_path, 'w') as index_file:
        encrypted_content = encrypt_index
        index_data = json.dump(encrypted_content, index_file)

    

def decrypt_index():
    # index.json encryption key
    json_encryption_key = "b'kIxAQ_7ylm9nwtjiXdeMD-8nZnldbPbB27DzgNS8Qdo='"
    create_index_json()
    script_dir = os.path.dirname(__file__)
    db_folder = os.path.join(script_dir, '.privacySafe', '.db')
    index_path = os.path.join(db_folder, 'index.json')

    with open(index_path, 'r') as encrypted_index_file:
        encrypted_content = encrypted_index_file.read()
        index_content = symmetric_decrypt(encrypted_content, json_encryption_key)

        index_data = json.loads(index_content)
    
    return index_data

if is_admin() == False:
    tk.messagebox.showinfo("Information", "This program requires elevated privileges to operate properly!")
    exit()
argument()