# EmotiBit ML Tools
 GUI-assisted scripts for facilitating data collection for machine learning tasks with EmotiBit data, for makers, artists and experimentation at the Concordia University Sensor Lab during the Winter 2024 Semester.

# Getting started
## Installing
First, make sure you have at least Python 3.8 installed. Then, create and open in your terminal your desired destination directory (should be empty) and run the commands below:
```
git clone https://github.com/CyWP/EmotiBit_ML.git
pip install -r requirements.txt
```
## Running
To run, open in your terminal the directory in which the program was saved and enter:
```
python __init__.py
```
## Data
Some functionalities require the user to input which data they would like to use. The table below specifies which subset of EmotiBit data a given label entails.
For more info on the nature of the data, refer to the official [EmotiBit Documentation](https://github.com/EmotiBit/EmotiBit_Docs/blob/master/Working_with_emotibit_data.md#emotibit-data-types)

| Name |Datatypes|
|----------|----------|
| ALL   | EA, EL, PI, PR, PG, T1, HR, AX, AY, AZ, GX, GY, GZ, MX, MY, MZ |
| IMU  | AX, AY, AZ, GX, GY, GZ, MX, MY, MZ |
| BIO   | EA, EL, PI, PR, PG, T1, HR |
| AG  | AX, AY, AZ, GX, GY, GZ |


# Vectorizer
## Function
The vectorizer is a tool enabling the formatting of data recorded on the EmotiBit's SD card into labelled, vectorized table with time stamps. Files are named as -label-.-name-.csv
## Inputs
**Files to be parsed** \
Path of the raw recording on the EmotiBit's SD card to be parsed \
**Target directory** \
Directory in which parsed files should be saved. \
**Use notes as labels** \
Enables any note logged with the EmotiBit Oscilloscope to be considered as the start of a new label for subsequent recorded data. Differently labelled data will appear in separate files, following the format -label-.-name-.csv. Every sample before the first label is omitted. \
**Test split** \
Enables splitting the parsed data into training and testing sets, with the displayed value indicating the desired proportion of the testing set. If the value is greater than zero, will create two subdirectories (/train and /test) in the target directory.
Since the concerned data is often used as a time series and the window isn't known, the data is not shuffled and simply split into two contiguous blocks of data. \
**Label** \
Manually label data, moot if ''Use notes as labels"" is checked. \
**Name** \
manually add a name for the recording. Does not interfere with the label. If left empty, will simply use a timestamp. \
**Clip First/Last** \
Clips the first/last x samples of every labelled block in a single recording.
## Actions
**Vectorize** \
Runs the vectorizing/parsing script using specified input.

# Dispatcher
## Function
The dispatcher does live vectorization and OSC dispatching of EmotiBit data received through OSC.
## Inputs
**In Port** \
Port to listen, which is the one EmotiBit data is sent to, 12345 by default. \
**Max Frequency** \
Puts a cap on the frequency at which messages are sent. \
**Relayed IP** \
Entry for the IP address to dispatch to \
**Port** \
Entry for the port to use at the destination IP address \
**Use Data** \
Specify which type of data to send (ALL, BIO, IMU, AG) \
## Actions
**Dispatch** \
Start dispatching data to specified addresses in list \
**Add Relay** \
Add input-based address to list

# Writer
## Function
Record data in controlled bursts by vectorizing and writing data in real time. Useful for gestural recordings or anything that should be more strictly segmented. Files are recorded under the format -label-.-timestamp-.csv.
## Inputs
**Label** \
Specify which label to assign to the specific recording. \
**Use Data** \
Specify which type of data to record (ALL, BIO, IMU, AG) \
**In Port** \
Port to listen, which is the one EmotiBit data is sent to, 12345 by default. \
**Max Frequency** \
Puts a cap on the frequency at which data is recorded. \
**Target Directory** \
Directory in which recordings are saved.
## Actions
**Add label** \
Adds the name specified in the entry above as a label in the list. \
**Write to Class/Stop** \
Starts/stops listening to the input port and writing the input data to csv.

# To Do
A list of welcome eventual additions and improvements. \
**Writer: Delay and Duration** \
Add options to set the duration of a recording and an optional before starting to record.