# TODO

Continue chat from [specstory](https://specstory.com/) with the following:

```txt

great! but i want you to accomodate for the following logic:

Since i'll upload to streamlit cloud , there could be multiple users who access application . Therefore, i want you to do the following : 

* when a user requests to download audios of a specific range, then first check temp folder to see if some (or all) of the ayah requestss has already been fuliflled or not (e.g., if the user wants to download 1:3 for afasy, whose reciter id is 1, then we check for the presence of that file in temp folder, so that if it's already there, then we don't need to redownload it)

* no audio files older than 1 day are kept in temp or output file, this is to ensure storage on streamlit cloud isn't overfilled

Try to make the logic mentioned above in a code detached from the rest of the py files, e.g., a py file (with a name appropriate of post cleaning) , and the functinons of that file are then imported to our main codebase (maybe, see if you have better code-organization ideas)

```