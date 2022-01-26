'''
Docs: https://github.com/davidkastner/pyQMMM/blob/main/pyqmmm/README.md
DESCRIPTION
    Reaction path calculations often need to be restarted from a later point.
    For example, when rerunning a scan of the peak to get higher resolution TS.
    Afterwards, the .xyz files of the two scans need to be stitched together.
    Here, users can specify the frames from each file that need to be combined.
    The script will generate a new combined file.

    Author: David Kastner
    Massachusetts Institute of Technology
    kastner (at) mit . edu

'''
################################ DEPENDENCIES ##################################
import glob

################################## FUNCTIONS ###################################

'''
Search the current directory for all xyz files and remove any non-trajectories
Parameters
-------
atoms : list
    list of atoms indices
Get the user's reaction coordinate definition.
Returns
-------
trajectory_list : list
    list string names of all the trajectory xyz files in the directory
'''


def get_xyz_filenames():
    # Get all xyz files and sort them
    file_list = glob.glob('./*.xyz')
    sorted(file_list)
    xyz_filename_list = []

    # Loop through files and check to see if they are trajectories
    for file in file_list:
        with open(file, 'r') as current_file:
            trajectory = False
            first_line = True
            header_count = 0
            # If the atom count appears more than once than it is a trajectory
            for line in current_file:
                if first_line == True:
                    atom_count = line.strip()
                    header_count += 1
                    first_line = False
                if line.strip() == atom_count:
                    header_count += 1
                if header_count > 1:
                    trajectory = True
                    break
        # Combine all the trajectory files into a single list
        if trajectory == True:
            xyz_filename_list.append(file)

        print('We found these .xyz files: {}'.format(xyz_filename_list))

    return xyz_filename_list


'''
Get the request frames for each file from the user.
Parameters
----------
xyz_filename : str
    The filename of the current xyz trajectory of interest

Returns
-------
frames : list
    The frames the user requested to be extracted from the xyz trajectory
'''


def request_frames(xyz_filename):
    # What frames would you like from the first .xyz file?
    request = input('Frames from {}? (e.g., 1,3-5): '.format(xyz_filename))

    if request != '':
        # Check the request and convert it to a list even if it is hyphenated
        temp = [(lambda sub: range(sub[0], sub[-1] + 1))
                (list(map(int, ele.split('-')))) for ele in request.split('-')]
        frames = [b for a in temp for b in a]

    print('For {} you requested frames {}.'.format(xyz_filename, frames))

    return frames


'''
Turns an xyz trajectory file into a list of lists where each element is a frame.
Parameters
----------
xyz_filename : string
    The file name of a trajectory

Returns
-------
trajectory_list : list
    List of lists containing the trajectory with each frame saved as an element
'''


def multiframe_xyz_to_list(xyz_filename):
    # Variables that measure our progress in parsing the optim.xyz file
    xyz_as_list = []  # List of lists containing all frames
    frame_contents = ''
    line_count = 0
    frame_count = 0
    first_line = True  # Marks if we've looked at the atom count yet

    # Loop through optim.xyz and collect distances, energies and frame contents
    with open(xyz_filename, 'r') as trajectory:
        for line in trajectory:
            # We determine the section length using the atom count in first line
            if first_line == True:
                section_length = int(line.strip()) + 2
                first_line = False
            # At the end of the section reset the frame-specific variables
            if line_count == section_length:
                line_count = 0
                frame_contents = ''
                frame_count += 1

            frame_contents += line
            line_count += 1

        xyz_as_list.append(frame_contents)

    print('We found {} frames in {}.'.format(len(xyz_as_list, xyz_filename)))

    return xyz_as_list


def combine_xyz_files():
    # Welcome the user to the file and introduce basic functionality
    print('\n.-------------------.')
    print('| COMBINE XYZ FILES |')
    print('.-------------------.\n')
    print('Searches current directory for xyz trajectory files.')
    print('You can combine as many xyz files as you need.')
    print('Name your xyz file as 1.xyz, 2.xyz, etc.')
    print('Leave the prompt blank when you are done.\n')

    # Search through all xyz's in the current directory and get the trajectories
    xyz_filename_list = get_xyz_filenames()
    # For each xyz file convert to a list a select the requested frames
    combined_xyz_list = []
    for file in xyz_filename_list:
        xyz_list = multiframe_xyz_to_list(file)
        requested_frames = request_frames(file)[1, 2, 3, 8]
        requested_xyz_list = [frame for index, frame in enumerate(
            xyz_list) if index + 1 in requested_frames]
        # Ask the user if they want the frames reversed for a given xyz file
        reverse_bool = input('True to reverse {}, else Return.'.format(file))
        if reverse_bool == True:
            requested_xyz_list = requested_xyz_list.reverse()
        combined_xyz_list += requested_xyz_list

    with open('combined.xyz', 'w') as combined_file:
        for entry in xyz_list:
            combined_file.write(entry)


if __name__ == "__main__":
    combine_xyz_files()
