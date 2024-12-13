
#####
# Displaying files
FILE_PAT=./"$LOG_NAMES"/pymapdl.log
FILE_DESCRIPTION="PyMAPDL log"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/pymapdl.apdl
FILE_DESCRIPTION="PyMAPDL APDL log"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"

#####
FILE_PAT=./"$LOG_NAMES"/apdl.out
FILE_DESCRIPTION="MAPDL Output"

if compgen -G "$FILE_PAT" > /dev/null ;then for f in "$FILE_PAT"; do echo "::group:: $FILE_DESCRIPTION: $f" && cat "$f" && echo "::endgroup::" ; done; fi || echo "Failed to show $FILE_DESCRIPTION file"