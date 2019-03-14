## Superfish Parameter Sweeps

Most of the files in this directory are related to parameter sweeps in
superfish. Each directory contains a "template.temp" and a
"vary_ellfish_property.py". The results of these parameter sweeps are
not included. In order to generate them the corresponding
vary_ellfish_property.py file will have to be run.

__template.temp__
is a

__vary_ellfish_property.py__

## Instructions
- Install the suite of SUPERFISH packages. Ensure that the directory
  which contains the binaries is in the system PATH. For linux SUPERFISH
  seem to work well with WINE.
- Install Python 3 along with matplotlib and numpy. I have not tested these
  scripts with Python 2.
- Open the appropriate vary_ellfish_property.py file in a text editor and
  uncomment **one** of the blocks at the top of the file. For example
  ```
  #file_name = 'template.temp'
  #new_directory = 'right_dome_b'
  #property = "RIGHT_DOME_B"
  #values = np.linspace(8, 25, 10)
  ```
  would become
  ```
  file_name = 'template.temp'
  new_directory = 'right_dome_b'
  property = "RIGHT_DOME_B"
  values = np.linspace(8, 25, 10)
  ```
  these four variables ```file_name```, ```new_directory```, ```property```
  and ```values``` should be declared **only once**. If multiple "blocks"
  are left uncommented then the variables will be overwritten.
- Edit the call to ELLFISH in vary_ellfish_property.py to make this work on
  your system (approx line 52). These scripts were originally run on a mix of
  windows and linux machines, on linux the call to ELLFISH will require a call
  to wine first.

  *Windows*
  ```
  subprocess.run(['ELLFISH', '{:.3f}.ell'.format(i)])
  ```

  *Linux*
  ```
    subprocess.run(['wine', 'ELLFISH', '{:.3f}.ell'.format(i)])
  ```

- Open a terminal and change to the directory containing the
  vary_ellfish_property.py which has been modified.
- The script automatically copies files and folders into a new (tidy) directory
  structure, so ensure that the directory is empty other than the necessary files.
- Run the scripy with  ```python vary_ellfish_property.py```
- When the sweep has finished return to the script, comment out the completed
  block and uncomment the next sweep block and repeat this process.
