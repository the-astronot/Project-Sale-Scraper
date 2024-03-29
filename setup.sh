#!/bin/bash
################################################################################
# setup
##
# Purpose: Prepares env for program
## 
################################################################################
#	Copyright (C) 2022  Max Marshall   
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see https://www.gnu.org/licenses/.
#________________
#|_File_History_|_______________________________________________________________
#|_Programmer______|_Date_______|_Comments______________________________________
#| Max Marshall    | 2022-11-24 | Created File
#|
#|
#|


if [[ ! -d ".venv" ]]; then
	python3 -m venv .venv
	echo "created .venv"
else
	echo ".venv already exists"
fi

source .venv/bin/activate

pip3 install -r requirements.txt
