import glob, os, sys, shutil, subprocess

args = sys.argv
#print("arg list: " + str(args))

# [ script_name, source_files, original_files, output_files ]
# Source files are the files you WANT THE DATES FROM
# original files are the files you want to PASTE THIS DATE ONTO
# Output files are the new modified original files with the source dates

if len(args) != 4:
    print ("Please add the folders of the original files and new files you want to use\n EG: \"auto-date.py source_files original_files output_files\"")
    exit()

# Get currend Dir
cwd = os.getcwd()

# Construct Source, original, and output directories
source_path = cwd + "/" + args[1]
original_path = cwd + "/" + args[2]
output_path = cwd + "/" + args[3]
source_path = os.path.abspath(source_path)
original_path = os.path.abspath(original_path)
output_path = os.path.abspath(output_path)

print("current directory is: " + cwd)
print("The source_path is: " + source_path)
print("The original path is: " + original_path)
print("The output path is: " + output_path)

########### MAKE SOURCE LIST OF FILES AND TIMES ###########
source_file_list = os.listdir(source_path)
sfl = []
source_dict = {} # {filename_w/o_ext: [ext, date_created]}

for item in source_file_list:
    if not item.startswith("."):
        sfl.append(item)
        filename, extension = item.split(".")
        date_created = os.stat(source_path + "/" + item).st_birthtime
        source_dict[filename] = [extension, date_created]

print(source_dict)

###############SOURCE LIST COMPLETE #########################

############### COPY ORIGINAL FILES #########################
original_file_list = os.listdir(original_path)
print("\nCopying Files to Output Directory...\n")
for item in original_file_list:
    if not item.startswith("."):
        shutil.copy2(original_path + "/" + item, output_path + "/")
print("\nDone Copying files, Renaming\n")
############## END COPY FILES ###########################

############## MODIFY OUTPUT FILES #########################

output_file_list = os.listdir(output_path)
for item in output_file_list:
    if not item.startswith("."):
        filename, extension = item.split(".")
        if filename in source_dict:
            ## Use exiftool first
            ## exiftool -overwrite_original -tagsfromfile Unencoded/MVI_2670.MOV EncodedFixed/MVI_2670.mp4
            subprocess.call(["exiftool", "-overwrite_original", "-tagsfromfile", source_path + "/" + filename + "." + source_dict[filename][0], output_path + "/" + item]) 

            ## Then change the OS things
            time = source_dict[filename][1]
            os.utime(output_path + "/" + item, (time, time))

