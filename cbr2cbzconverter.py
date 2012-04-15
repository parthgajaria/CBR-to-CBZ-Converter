import UnRAR2
import os
import sys
import zipfile
import shutil

def create_cbz(no_dir=False):
	rarc = UnRAR2.RarFile(os.path.join(root,file))
	file_list = rarc.infolist()
	zip_file_name = None
	#Looking for the directory in the rar
	if not no_dir:
		for inner_file in file_list:
			if inner_file.isdir:
				zip_file_name = inner_file.filename
				break
	else:
		#We already no there's no directory in the rar
		zip_file_name = file[:-4]
		
	if not zip_file_name == None:
		#Need this for writing cbz with no dir and to remove extracted directory
		folder_name = zip_file_name
		zip_file_name = zip_file_name + '.cbz'
		zip_file_name = os.path.join(root, zip_file_name)
		folder_path = os.path.join(root, folder_name)
		extract_path = None
		if not no_dir:
			extract_path = os.path.abspath(rootdir)
		else:
			extract_path = os.path.join(os.path.abspath(rootdir), file[:-4])
		rarc.extract(path = extract_path)
		zip_file = zipfile.ZipFile(zip_file_name, 'w')
		for image in file_list:
			if not image.isdir:
				if not no_dir:
					file_path = os.path.join(root, image.filename)
				else:
					file_path = os.path.join(root, folder_name, image.filename)
				zip_file.write(file_path)	
		zip_file.close()
		shutil.rmtree(os.path.join(root, folder_name))
	else:
		raise NameError("Error: Invalid File Name")

def check_if_dir():
	dir_count = 0
	# Populates the list with all the file names in a given directory structure
	for files_in_archive in UnRAR2.RarFile(os.path.join(root,file)).infoiter():
		if (files_in_archive.isdir):
			dir_count = dir_count + 1
	if (dir_count == 0):
		no_dir = True
	elif (dir_count > 1):
		raise NameError("Error: Invalid CBR File")
	else:
		no_dir = False
		
	return no_dir

#Should be the directory containing cbr files
rootdir = sys.argv[1]

#Look through directory tree
for root, subFolders, files in os.walk(rootdir):
	for file in files:
		if(file[-4:] == ".cbr"):
			#Check if rar will extract to a directory or not
			no_dir = check_if_dir()
			#extract all the files in CBR
			create_cbz(no_dir)
				
				